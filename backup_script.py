from flask import Flask, jsonify, render_template
import boto3
import os
from datetime import datetime

app = Flask(__name__, template_folder="templates")

# Configuration
BUCKET_NAME = "cloud-ec2-backups"
BACKUP_DIR = "/home/ubuntu/ec2_backup_project/files_to_backup"
TEMP_DIR = "/tmp"  # Temporary directory for downloads
s3 = boto3.client("s3")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/list_backups")
def list_backups():
    """List all backups stored in S3."""
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        objects = response.get("Contents", [])
        backups = [obj["Key"] for obj in objects]
        return jsonify(backups)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/backup")
def create_backup():
    try:
        backup_filename = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.tar.gz"
        local_backup_path = os.path.join(TEMP_DIR, backup_filename)

        # Create tar.gz archive of the directory
        os.system(f"tar -czf {local_backup_path} -C {BACKUP_DIR} .")

        # Upload to S3
        s3.upload_file(local_backup_path, BUCKET_NAME, backup_filename)

        return jsonify({"message": f"{backup_filename} uploaded to {BUCKET_NAME} successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/restore/<backup_name>")

def restore_backup(backup_name):
    try:
        local_backup_path = os.path.join(TEMP_DIR, backup_name)

        # Ensure file exists in S3 before downloading
        s3.head_object(Bucket=BUCKET_NAME, Key=backup_name)
        s3.download_file(BUCKET_NAME, backup_name, local_backup_path)

        # Extract the tar.gz archive
        os.system(f"tar -xzf {local_backup_path} -C {BACKUP_DIR}")
        return jsonify({"message": f"{backup_name} restored successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":  # Line 66 (Correct indentation)
    try:  # Line 67 (Correct indentation)
        app.run(host="10.0.0.60", port=5005, debug=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print("Port 5000 is already in use. Try a different port.")

