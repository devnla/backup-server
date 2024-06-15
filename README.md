# Server Backup with rsync

This program is used to backup your server's data like uploaded images by using [rsync](https://en.wikipedia.org/wiki/Rsync).

## Installation

Install the project with python

```bash
    git clone https://github.com/devnla/server-backup.git
    cd server-backup
    cp .env.example .env
    pip install -r requirements.txt
```

## Usage

Run the project

```bash
    python server-backup.py
```

Run the project in cron job daily

```bash
    0 0 * * * /usr/bin/python3 /path/to/server-backup.py
```
    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SERVER` - IP or Host of the server
`PORT` - Port of the server
`SSH_TYPE` - password or private key
`SSH_USER` - username of the server
`SSH_PASS` - password of the server
`SSH_KEY_PATH` - path of the private key
`REMOTE_DIR` - directory on the remote server
`LOCAL_DIR` - directory on the local machine
`LOG_FILE` - path of the log file