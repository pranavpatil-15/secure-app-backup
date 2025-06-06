from flask import Flask, jsonify, render_template, send_file, request
import boto3
import os
from cryptography.fernet import Fernet
import datetime
import subprocess

app = Flask(__name__, template_folder="templates")

# Configuration
BUCKET_NAME = "cloud-ec2-backups"
BACKUP_DIR = "/home/ubuntu/workspace/ec2-cloud-backup/files_to_backup"
TEMP_DIR = "/tmp"
KEY_FILE_PATH = os.environ.get('ENCRYPTION_KEY_FILE', '/home/ubuntu/workspace/ec2-cloud-backup/secret.key')
s3 = boto3.client("s3")

def get_cipher():
    with open(KEY_FILE_PATH, 'rb') as key_file:
        key = key_file.read()
    return Fernet(key)

def delete_old_backups(days=30):
    """Delete backups older than X days from S3."""
    threshold_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    if "Contents" in response:
        for obj in response["Contents"]:
            if obj["LastModified"] < threshold_date:
                s3.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])
                print(f"Deleted old backup: {obj['Key']}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/list_backups")
def list_backups():
    """List all backups stored in S3."""
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        backups = [obj["Key"] for obj in response.get("Contents", [])]
        return jsonify(backups)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/create_backup", methods=["POST"])
def create_backup():
    """Create a backup, encrypt, and upload to S3."""
    try:
        backup_filename = f"backup_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.tar.gz"
        local_backup_path = os.path.join(TEMP_DIR, backup_filename)
        encrypted_backup_path = local_backup_path + ".enc"

        # Create tar.gz archive of the directory
        subprocess.run(['tar', '-czf', local_backup_path, '-C', BACKUP_DIR, '.'], check=True)

        # Encrypt the backup
        cipher = get_cipher()
        with open(local_backup_path, 'rb') as f:
            encrypted_data = cipher.encrypt(f.read())
        with open(encrypted_backup_path, 'wb') as f:
            f.write(encrypted_data)

        # Upload encrypted file to S3
        s3.upload_file(encrypted_backup_path, BUCKET_NAME, os.path.basename(encrypted_backup_path))

        # Clean up local files
        os.remove(local_backup_path)
        os.remove(encrypted_backup_path)

        return jsonify({"message": f"{os.path.basename(encrypted_backup_path)} uploaded to {BUCKET_NAME} successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/restore/<backup_name>", methods=["POST"])
def restore_backup(backup_name):
    """Download, decrypt, and extract a backup from S3."""
    try:
        encrypted_path = os.path.join(TEMP_DIR, backup_name)
        decrypted_path = encrypted_path.replace('.enc', '')

        # Download from S3
        s3.download_file(BUCKET_NAME, backup_name, encrypted_path)

        # Decrypt
        cipher = get_cipher()
        with open(encrypted_path, 'rb') as enc_file:
            decrypted_data = cipher.decrypt(enc_file.read())
        with open(decrypted_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)

        # Extract
        subprocess.run(['tar', '-xzf', decrypted_path, '-C', BACKUP_DIR], check=True)

        # Clean up
        os.remove(encrypted_path)
        os.remove(decrypted_path)

        return jsonify({"message": f"{backup_name} restored successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_backup(filename):
    """Download and decrypt a backup from S3."""
    try:
        encrypted_path = os.path.join(TEMP_DIR, filename)
        decrypted_path = encrypted_path.replace('.enc', '')

        s3.download_file(BUCKET_NAME, filename, encrypted_path)

        cipher = get_cipher()
        with open(encrypted_path, 'rb') as enc_file:
            decrypted_data = cipher.decrypt(enc_file.read())
        with open(decrypted_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)

        response = send_file(decrypted_path, as_attachment=True, download_name=os.path.basename(decrypted_path))

        # Clean up after sending
        @response.call_on_close
        def cleanup():
            os.remove(encrypted_path)
            os.remove(decrypted_path)

        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/cleanup_old_backups", methods=["POST"])
def cleanup_old_backups():
    """Delete old backups from S3."""
    try:
        days = int(request.args.get('days', 30))
        delete_old_backups(days=days)
        return jsonify({"message": f"Backups older than {days} days deleted."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

