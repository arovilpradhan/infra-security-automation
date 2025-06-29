# This Script logins to the firewall IP and gets the copy of running config and saves it inside "backups" folder.
import paramiko
import datetime
import os
import time

FIREWALL_IP = '192.1xx.x.x'
USERNAME = 'fw_username'
PASSWORD = 'fw_password'
BACKUP_DIR = 'backups' # Directory where the config file will be backedup into (Folder Will be created if not existing).

os.makedirs(BACKUP_DIR, exist_ok=True)
def connect_ssh(ip, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
        print("[+] SSH connection established.")
        return client
    except Exception as e:
        print(f"[-] SSH connection failed: {e}")
        return None

def backup_config(client):
    try:
        shell = client.invoke_shell()
        time.sleep(1)
        shell.recv(1000)  # Clear welcome message

        shell.send('set cli pager off\n')
        time.sleep(0.5)
        shell.recv(1000)

        shell.send('show config running\n')
        time.sleep(6)  # Adjust if config is large

        output = ""
        while shell.recv_ready():
            output += shell.recv(10000).decode()

        # === STEP 1: WRITE RAW OUTPUT FIRST ===
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"palo_config_backup_{timestamp}.xml"
        filepath = os.path.join(BACKUP_DIR, filename)

        with open(filepath, 'w') as raw_file:
            raw_file.write(output)

        print(f"[+] Raw config saved to: {filepath}")

        # === STEP 2: REMOVE TOP 6 AND BOTTOM 4 LINES ===
        with open(filepath, 'r') as file:
            lines = file.readlines()

        if len(lines) > 10:
            trimmed_lines = lines[6:-4]
        else:
            trimmed_lines = lines

        with open(filepath, 'w') as file:
            file.writelines(trimmed_lines)

        print(f"[+] Trimmed config saved to: {filepath}")

        # === STEP 3: REMOVE EXTRA BLANK LINES (double spacing fix) ===
        with open(filepath, 'r') as file:
            lines = file.readlines()

        cleaned_lines = [line for line in lines if line.strip() != '']  # Remove truly blank lines

        with open(filepath, 'w') as file:
            file.writelines(cleaned_lines)

        print(f"[+] Final cleaned config saved to: {filepath}")
    except Exception as e:
        print(f"[-] Failed during config backup: {e}")


def main():
    ssh_client = connect_ssh(FIREWALL_IP, USERNAME, PASSWORD)
    if ssh_client:
        backup_config(ssh_client)
        ssh_client.close()

if __name__ == "__main__":
    main()
