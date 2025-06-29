# SolarWinds IP Status Changer

A Python script to automate the process of updating the status of an IP address in the SolarWinds IPAM (IP Address Manager) system using its API.

This tool helps network or infrastructure teams mark IPs as "Available", "Reserved", or "Used" in the SolarWinds web portal.

---

## ⚙️ Features

- 🔐 Uses HTTP Basic Authentication (Domain\Username)
- 🌐 Sends secure API request to SolarWinds IPAM endpoint
- 📝 Updates the IP status (e.g., from "Used" to "Available")
- 🚫 SSL warning suppression for environments using self-signed certs

---

## 🧾 Input

The following values are **hardcoded in the script** (customize before running):

- `IPAddress`: IP you want to update (e.g., `10.100.50.25`)
- `Status`: New status value (e.g., `Available`, `Used`, `Reserved`)
- `username`, `password`: SolarWinds domain credentials
- `solarwinds_url`: API endpoint (usually ends with `ChangeIpStatus`)

---

## 📤 Output

- ✅ On success:  
  ```bash
  Successfully updated IP status to Available
  
❌ On failure:
Failed to update IP status. Status Code: 401, Error: Unauthorized

