from flask import Flask, jsonify, render_template, send_file
import boto3
import os
from cryptography.fernet import Fernet
import datetime

app = Flask(__name__)
BUCKET_NAME = "cloud-ec2-backups"
s3 = boto3.client("s3")

KEY_FILE_PATH = '/home/ubuntu/ec2_backup_project/secret.key'

def get_cipher():
    with open(KEY_FILE_PATH, 'rb') as key_file:
        key = key_file.read()
    return Fernet(key)

# ✅ Delete old backups older than 30 days
def delete_old_backups(days=30):
    try:
        threshold_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        if "Contents" in response:
            for obj in response["Contents"]:
                if obj["LastModified"] < threshold_date:
                    s3.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])
                    print(f"Deleted old backup: {obj['Key']}")
    except Exception as e:
        print(f"Error deleting old backups: {str(e)}")

@app.route("/")
def home():
    delete_old_backups()  # ✅ Clean old backups on dashboard load
    return render_template("index.html")

@app.route("/list_backups")
def list_backups():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        if "Contents" in response:
            backups = [obj["Key"] for obj in response["Contents"]]
        else:
            backups = []
        return jsonify(backups)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/restore/<backup_name>")
def restore_backup(backup_name):
    try:
        s3.download_file(BUCKET_NAME, backup_name, f"/tmp/{backup_name}")
        os.system(f"unzip /tmp/{backup_name} -d /home/ubuntu/ec2_backup_project/files_to_backup")
        return jsonify({"message": f"{backup_name} restored successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/download/<filename>")
def download_backup(filename):
    try:
        s3.download_file(BUCKET_NAME, filename, f'/tmp/{filename}')

        if filename.endswith('.enc'):
            cipher = get_cipher()
            encrypted_path = f'/tmp/{filename}'
            decrypted_path = encrypted_path.replace('.enc', '')

            with open(encrypted_path, 'rb') as enc_file:
                decrypted_data = cipher.decrypt(enc_file.read())
            with open(decrypted_path, 'wb') as dec_file:
                dec_file.write(decrypted_data)

            return send_file(decrypted_path, as_attachment=True, download_name=os.path.basename(decrypted_path))

        return send_file(f'/tmp/{filename}', as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

