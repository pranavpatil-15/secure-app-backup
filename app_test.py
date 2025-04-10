from flask import Flask, jsonify, render_template, send_file
import boto3
import os
from datetime import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")

BUCKET_NAME = "cloud-ec2-backups"
BACKUP_DIR = "/home/ubuntu/ec2_backup_project/files_to_backup"
TEMP_DIR = "/tmp"

s3 = boto3.client("s3")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create_backup", methods=["POST"])
def create_backup():
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file = f"backup_{timestamp}.tar.gz"
        local_path = os.path.join(TEMP_DIR, backup_file)
        os.system(f"tar -czf {local_path} -C {BACKUP_DIR} .")
        s3.upload_file(local_path, BUCKET_NAME, backup_file)
        return f"✅ {backup_file} uploaded to S3!"
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

@app.route("/show_backups")
def show_backups():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        objects = response.get("Contents", [])
        files = [obj["Key"] for obj in objects]
        return jsonify({"backups": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_file(filename):
    try:
        download_path = f"/tmp/{filename}"
        s3.download_file(BUCKET_NAME, filename, download_path)
        return send_file(download_path, as_attachment=True)
    except Exception as e:
        return f"Error downloading file: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)

