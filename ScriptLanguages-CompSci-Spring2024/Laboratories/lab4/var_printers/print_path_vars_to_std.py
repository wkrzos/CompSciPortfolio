import os

# This function lists all directories in the PATH environment variable
def list_path_dirs():
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    for dir in path_dirs:
        print(dir)

# This function lists each directory in the PATH environment variable along with executable files in them
def list_executables_in_path_dirs():
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    for dir in path_dirs:
        try:
            # Listing only files which are executable
            executables = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and os.access(os.path.join(dir, f), os.X_OK)]
            print(f"Directory: {dir}")
            for executable in executables:
                print(f"  - {executable}")
        except Exception as e:
            # Handling directories that cannot be accessed
            print(f"Directory: {dir} - Error: {e}")


# Functionality a:
# list_path_dirs()

# Functionality b:
list_executables_in_path_dirs()
