🔐 Secure EC2 Backup Automation Portal with Flask & S3
This is a Flask-based web dashboard hosted on an AWS EC2 instance that automates secure file backups to Amazon S3. It follows AWS best practices by using IAM roles, KMS encryption, CloudWatch monitoring, and SNS notifications for real-time backup visibility and alerting.

📦 Tech Stack
Backend: Python, Flask, Boto3
Cloud Services: AWS EC2, S3, IAM, KMS, SNS, CloudWatch
Automation: Cron Jobs (for scheduled backups)
Monitoring: AWS CloudWatch Logs, Alarms, SNS
✅ Features
Web-based interface to trigger and manage file backups
S3 bucket integration with server-side encryption (SSE-KMS)
IAM roles used for secure, credential-free access to S3
Real-time monitoring via CloudWatch (Logs + Alarms)
Email/SMS notifications using Amazon SNS for backup success/failure
Secure architecture with role-based access and logging
🛠️ How to Run Locally
Clone the repo:
git clone https://github.com/strangepranav/secure-app-backup.git
cd secure-ec2-backup-app

# Install dependencies:
pip install -r requirements.txt

# Run the Flask app:
python app.py


📊 Architecture Overview
EC2 instance runs Flask app
IAM role provides S3 access
Files uploaded from EC2 to encrypted S3 bucket
CloudWatch monitors app logs
SNS triggers notifications for backup events

🧠 What I Learned
Implementing IAM roles for fine-grained access control
Managing S3 encryption using AWS KMS
Building secure web apps with Flask + AWS SDK (Boto3)
Integrating CloudWatch and SNS for monitoring and alerting
Applying AWS Well-Architected security principles


✍️ Author
Pranav Patil
LinkedIn: linkedin.com/in/pranav-patil-152003p
GitHub: github.com/strangepranav
