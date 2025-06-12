# 🛠️ AWS Toolkit Lab

This repository contains a collection of Python scripts for interacting with AWS EC2 instances. It is designed as a personal learning toolkit built under WSL (Windows Subsystem for Linux) and focuses on automation, secure remote access, and reproducible environment setup.

## ⚙️ Requirements

- Python 3.8+
- [WSL2](https://learn.microsoft.com/en-us/windows/wsl/)
- `paramiko`, `pyyaml`
- EC2 instance with SSH access
- `~/.ssh/key.pem` (or other valid private key)

## 📁 Project Structure
aws-toolkit-lab/
├── config/
│ ├── config.yaml # General non-sensitive configuration
│ └── secrets.yaml # Sensitive data (ignored by Git)
├── scripts/
│ ├── ec2_paramiko_setup_python_env.py # Full Python setup on EC2 using Paramiko
│ └── ec2_subprocess_run_command.py # Simple command execution using system SSH
├── key/ # SSH private key folder (ignored)
├── data/ # Optional: backup or exportable data (ignored)
├── .gitignore
└── README.md

## 📜 Description of Key Scripts

### `ec2_paramiko_setup_python_env.py`
A robust script that connects to an EC2 instance using `paramiko`, applies security permissions to the SSH key, and automates environment preparation including:
- OS details check
- Python installation
- Version verification
- Directory creation

### `ec2_subprocess_run_command.py`
A lightweight alternative using `subprocess` to run SSH commands via the system shell. Ideal for simple connectivity and validation tests.

## 🔐 Secrets & Config

Sensitive values like hostname, username, and key path are stored in:

```yaml
# config/secrets.yaml (not committed to Git)
aws:
  hostname: "..."
  username: "EC_Your_Name"
  key_path: "Path to pem"

 Non-sensitive configuration in: 
 # config/config.yaml
project: aws-toolkit-lab
region: eu-central-1

🚫 Git Ignore Best Practices
key/
config/secrets.yaml
data/
*.pem

📄 License
This project is licensed under the MIT License. See LICENSE for details. While it's not mandatory, you may mention this in the README — which we've done here for completeness and clarity.

🤖 Note
This project is built and tested under WSL2 on Windows. If running on native Linux or macOS, behavior is expected to be similar but path resolution and permissions may vary.