# Palo Alto Firewall – Running Config Backup Script

A Python automation script to SSH into a Palo Alto firewall, execute the `show config running` command, and store the output as a timestamped configuration backup.

This tool is useful for operations, backup scheduling, change tracking, and incident response teams.

---

## ⚙️ Features

- 🔐 Connects to firewall over SSH using `paramiko`
- 🧾 Runs `show config running` and saves output
- 🕒 Timestamps backup files (e.g., `palo_config_backup_20250629_153045.xml`)
- ✂️ Automatically trims:
  - The first 6 and last 4 lines of raw config (removes banners/prompts)
  - Empty lines (double spacing cleanup)
- 🗂️ Stores output inside a `backups/` folder (auto-created)

---

## 🔐 Authentication

Edit the following hardcoded variables in the script before running:
```python
FIREWALL_IP = '192.1xx.x.x'
USERNAME = 'fw_username'
PASSWORD = 'fw_password'

--------------------------------
Output:-

backups/palo_config_backup_YYYYMMDD_HHMMSS.xml
