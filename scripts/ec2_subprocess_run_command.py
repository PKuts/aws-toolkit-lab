import subprocess
import yaml
from pathlib import Path

print("🚀 EC2 SSH via system subprocess")

# Load secrets
with open("config/secrets.yaml", 'r') as f:
    secrets = yaml.safe_load(f)

aws = secrets["aws"]
key_path = Path(aws["key_path"]).expanduser()
host = f"{aws['username']}@{aws['hostname']}"
command_to_run = "echo Hello from EC2"

ssh_command = [
    "ssh",
    "-i", str(key_path),
    "-o", "StrictHostKeyChecking=no",
    "-o", "ConnectTimeout=10",
    host,
    command_to_run
]

print(f"🔧 Running command: {' '.join(ssh_command)}")

try:
    result = subprocess.run(ssh_command, capture_output=True, text=True, timeout=15)

    if result.returncode == 0:
        print("✅ SSH Command Success:")
        print(result.stdout.strip())
    else:
        print("❌ SSH Command Failed:")
        print(result.stderr.strip())

except subprocess.TimeoutExpired:
    print("⏱️ Timeout: SSH command took too long.")
except FileNotFoundError:
    print("❌ Error: SSH not found.")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
