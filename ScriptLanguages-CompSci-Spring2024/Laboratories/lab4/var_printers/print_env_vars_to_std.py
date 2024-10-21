import os
import sys

# Retrieve all environment variables
env_vars = os.environ

# If there are command line arguments, filter the environment variables
if len(sys.argv) > 1:
    filtered_env_vars = {key: value for key, value in env_vars.items() if any(arg.lower() in key.lower() for arg in sys.argv[1:])}
else:
    filtered_env_vars = env_vars

# Sort and print the environment variables
for key in sorted(filtered_env_vars):
    print(f"{key}: {filtered_env_vars[key]}")

sys.argv = ["script_name", "path", "user"]
