print("🚀 Setting up Python environment on EC2 via Paramiko")

import paramiko
from datetime import datetime
import os
import stat
from pathlib import Path
import io
import yaml

# --- Load Secrets ---
def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

secrets = load_yaml("config/secrets.yaml")
config = load_yaml("config/config.yaml")

aws = secrets["aws"]
hostname = aws["hostname"]
username = aws["username"]
key_path = Path(aws["key_path"]).expanduser().resolve()

print(f"🔑 Key path: {key_path}")

# Display permissions BEFORE chmod
mode_before = os.stat(key_path).st_mode
print(f"🔍 Permissions BEFORE: Octal: {oct(mode_before)}, Symbolic: {stat.filemode(mode_before)}")

# chmod 400 for Linux/macOS
if os.name != "nt":
    os.chmod(key_path, stat.S_IRUSR)
    mode_after = os.stat(key_path).st_mode
    print(f"🔐 Permissions AFTER : Octal: {oct(mode_after)}, Symbolic: {stat.filemode(mode_after)}")
else:
    print("⚠️ Skipping chmod: running on Windows")

# Load RSA Key
try:
    with open(key_path, 'r') as f:
        key_data = f.read()
    key = paramiko.RSAKey.from_private_key(io.StringIO(key_data))
    print("🔐 Fingerprint:", key.get_fingerprint().hex())
except Exception as e:
    print(f"❌ Failed to load RSA key: {e}")
    exit(1)

# SSH client setup
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print(f"🔌 Connecting to {hostname} as {username}...")

try:
    client.connect(
        hostname=hostname,
        username=username,
        pkey=key,
        look_for_keys=False,
        allow_agent=False
    )
    print("✅ Connected successfully!")
except paramiko.AuthenticationException:
    print("❌ Authentication failed.")
    exit(1)
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)

# Commands to prepare EC2
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"test.test.{current_date}"
folder_name = "merlin"

commands = [
    "uname -a",
    "sudo yum update -y",
    "sudo yum install python3 -y",
    "sudo yum install python3-pip -y",  # ← додано
    "python3 --version",
    "pip3 --version",
    f"mkdir -p {folder_name}",
    f"touch {folder_name}/{filename}"
]

for cmd in commands:
    print(f"➡️ Running: {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd)
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if output:
        print(f"✅ Output:\n{output}")
    if error:
        print(f"⚠️ Error:\n{error}")

client.close()
print("🏁 Done. EC2 is ready for Python-based ETL.")