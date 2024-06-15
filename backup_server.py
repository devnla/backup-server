import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from tabulate import tabulate
import shlex

load_dotenv()

server = os.getenv('SERVER')
port = int(os.getenv('PORT'))
ssh_type = os.getenv('SSH_TYPE')
username = os.getenv('SSH_USER')
password = os.getenv('SSH_PASS')
ssh_key = os.getenv('SSH_KEY_PATH')
remote_dir = os.getenv('REMOTE_DIR')
local_dir = os.getenv('LOCAL_DIR')
log_file = os.getenv('LOG_FILE')

def create_log_file():
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write("Timestamp - Details\n")


def log_backup(details):
    create_log_file()
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now()} - {details}\n")

def display_log():
    with open(log_file, 'r') as f:
        logs = [
            line.strip().split(' - ') for line in f.readlines()
        ]
        headers = ["Timestamp", "Details"]
        print(tabulate(logs, headers, tablefmt="grid"))

if ssh_type == 'pass':
    ssh_command = f"sshpass -p {shlex.quote(password)} ssh -p {port}"
elif ssh_type == 'key':
    ssh_command = f"ssh -p {port} -i {shlex.quote(ssh_key)}"
else:
    raise ValueError("Invalid SSH_TYPE in .env file. Use 'pass' or 'key'.")

rsync_command = f"rsync -avz -e \"{ssh_command}\" {username}@{server}:{remote_dir} {local_dir}"

try:
    # Execute the rsync command
    result = subprocess.run(rsync_command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        log_backup(f"Backup successful: {result.stdout.strip()}")
    else:
        log_backup(f"Backup failed: {result.stderr.strip()}")
except Exception as e:
    log_backup(f"Backup error: {str(e)}")

# Display the log table in CLI
display_log()