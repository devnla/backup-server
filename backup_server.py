import os
import subprocess
import shlex
import argparse
from datetime import datetime
from dotenv import load_dotenv
from tabulate import tabulate

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


def log_backup(details):
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now()} - {details}\n")
        f.write("=" * 50 + "\n")
        print(f"{datetime.now()} - {details}\n")

def display_log(num_records):
    with open(log_file, 'r') as f:
        logs = [line.strip().split(' - ') for line in f.readlines()]
    if num_records > 0:
        logs = logs[-num_records:]
    headers = ["Timestamp", "Details"]
    print(tabulate(logs, headers))

def backup():
    if ssh_type == 'pass':
        ssh_command = f"sshpass -p {shlex.quote(password)} ssh -p {port}"
    elif ssh_type == 'key':
        ssh_command = f"ssh -p {port} -i {shlex.quote(ssh_key)}"
    else:
        raise ValueError("Invalid SSH_TYPE in .env file. Use 'pass' or 'key'.")

    rsync_command = f"rsync -avz -e \"{ssh_command}\" {username}@{server}:{remote_dir} {local_dir}"

    try:
        print(f"{datetime.now()} - Making backup from {server} of {remote_dir} to {local_dir}.")
        result = subprocess.run(rsync_command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            log_backup(f"Backup successful: {result.stdout.strip()} \n")
        else:
            log_backup(f"Backup failed: {result.stderr.strip()} \n")
    except Exception as e:
        log_backup(f"Backup error: {str(e)}")

    print(f"{datetime.now()} - Backup complete.")


parser = argparse.ArgumentParser(description="Backup Server with Rsync")
subparsers = parser.add_subparsers(dest="command", required=True)

# Backup command
backup_parser = subparsers.add_parser("backup", help="Make a backup")

# Log command
log_parser = subparsers.add_parser("log", help="Display backup logs")
log_parser.add_argument("num_records", type=int, help="Number of log records to display")

# Parse the arguments
args = parser.parse_args()
if args.command == "backup":
    backup()
elif args.command == "log":
    display_log(args.num_records)