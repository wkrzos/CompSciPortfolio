# backup_utils.py

import os
import json
from datetime import datetime

def get_backup_dir():
    """
    Returns the dir to the .backups folder, takin in account the BACKUPS_DIR environmental variable.
    """
    default_backup_dir = os.path.join(os.path.expanduser("~"), '.backups')
    return os.getenv('BACKUPS_DIR', default_backup_dir)

def log_backup(backup_dir, source_dir, backup_file_name):
    """
    Saves the data of a backup to the history.json in backup_dir folder.
    """
    history_path = os.path.join(backup_dir, 'history.json')
    record = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source_directory': source_dir,
        'backup_file_name': backup_file_name
    }
    
    if os.path.exists(history_path):
        with open(history_path, 'r+', encoding='utf-8') as file:
            history = json.load(file)
            history.append(record)
            file.seek(0)
            json.dump(history, file, indent=4)
    else:
        with open(history_path, 'w', encoding='utf-8') as file:
            json.dump([record], file, indent=4)
