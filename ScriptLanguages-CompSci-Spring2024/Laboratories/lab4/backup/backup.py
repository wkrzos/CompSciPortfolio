# backup.py

import os
import sys
import zipfile
from datetime import datetime
from backup_utils import get_backup_dir, log_backup

def create_backup(source_dir):
    """
    Creates a .zip archive including all files from the source_dir folder.
    """
    if not os.path.isdir(source_dir):
        print(f"The directory doesn't exist: {source_dir}")
        sys.exit(1)
    
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    dirname = os.path.basename(os.path.normpath(source_dir))
    backup_dir = get_backup_dir()
    os.makedirs(backup_dir, exist_ok=True)
    
    backup_file_name = f"{timestamp}-{dirname}.zip"
    backup_path = os.path.join(backup_dir, backup_file_name)
    
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                zipf.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                                           os.path.join(source_dir, '..')))
    
    print(f"Backup of {dirname} has been created: {backup_path}")
    return backup_path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python backup.py <directory>")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    backup_path = create_backup(source_dir)
    backup_dir, backup_file_name = os.path.split(backup_path)
    log_backup(backup_dir, source_dir, backup_file_name)
