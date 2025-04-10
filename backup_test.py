import boto3
import os
from datetime import datetime

# Constants
BUCKET_NAME = "cloud-ec2-backups"
BACKUP_DIR = "/home/ubuntu/ec2_backup_project/files_to_backup"
TEMP_DIR = "/tmp"

# Create unique backup filename
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
backup_filename = f"backup_{timestamp}.tar.gz"
local_backup_path = os.path.join(TEMP_DIR, backup_filename)

try:
    # Create tar.gz archive
    os.system(f"tar -czf {local_backup_path} -C {BACKUP_DIR} .")

    # Upload to S3
    s3 = boto3.client("s3")
    s3.upload_file(local_backup_path, BUCKET_NAME, backup_filename)

    print(f"✅ Backup successful: {backup_filename} uploaded to S3 bucket {BUCKET_NAME}")
except Exception as e:
    print(f"❌ Backup failed: {e}")

