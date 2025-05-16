import os
import zipfile
import boto3
from datetime import datetime
from cryptography.fernet import Fernet

# === CONFIGURATION ===
FILES_DIR = '/home/ubuntu/ec2_backup_project/files_to_backup'
BACKUP_DIR = '/home/ubuntu/backups'
BUCKET_NAME = 'cloud-ec2-backups'
KEY_FILE_PATH = '/home/ubuntu/ec2_backup_project/secret.key'

DB_USER = 'backup'
DB_PASSWORD = '1542003'
DB_NAME = 'backupdb'
DB_BACKUP_FILE = f"/tmp/db_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql.gz"

SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:123456789012:BackupAlerts'  # Replace with actual ARN

# === AWS CLIENTS ===
s3 = boto3.client('s3')
sns = boto3.client('sns')

# === ENCRYPTION ===
def load_or_create_key():
    if os.path.exists(KEY_FILE_PATH):
        with open(KEY_FILE_PATH, 'rb') as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE_PATH, 'wb') as key_file:
            key_file.write(key)
        return key

ENCRYPTION_KEY = load_or_create_key()
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_file(file_path):
    with open(file_path, "rb") as file:
        encrypted_data = cipher.encrypt(file.read())
    enc_file_path = file_path + ".enc"
    with open(enc_file_path, "wb") as file:
        file.write(encrypted_data)
    os.remove(file_path)  # Clean up the unencrypted file
    return enc_file_path

def create_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    zip_filename = f'backup_{timestamp}.zip'
    zip_path = os.path.join(BACKUP_DIR, zip_filename)

    # Step 1: Zip files
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
        for foldername, subfolders, filenames in os.walk(FILES_DIR):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, FILES_DIR)
                backup_zip.write(file_path, arcname)
    print(f"[✔] Created ZIP: {zip_filename}")

    # Step 2: MySQL dump
    dump_cmd = f"mysqldump -u {DB_USER} -p'{DB_PASSWORD}' {DB_NAME} | gzip > {DB_BACKUP_FILE}"
    dump_status = os.system(dump_cmd)
    if dump_status != 0:
        print("[✘] MySQL backup failed")
        return
    print("[✔] MySQL dump completed")

    # Step 3: Encrypt
    encrypted_zip_path = encrypt_file(zip_path)
    encrypted_db_path = encrypt_file(DB_BACKUP_FILE)
    print("[✔] Files encrypted")

    # Step 4: Upload to S3
    try:
        s3.upload_file(encrypted_zip_path, BUCKET_NAME, os.path.basename(encrypted_zip_path))
        s3.upload_file(encrypted_db_path, BUCKET_NAME, os.path.basename(encrypted_db_path))
        print("[✔] Uploaded to S3")
    except Exception as e:
        print(f"[✘] S3 Upload Failed: {e}")
        return

    # Step 5: Notify via SNS
    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"Backup Successful at {timestamp}",
            Subject="EC2 Backup Status"
        )
        print("[✔] SNS notification sent")
    except Exception as e:
        print(f"[✘] SNS Notification Failed: {e}")

if __name__ == '__main__':
    create_backup()

