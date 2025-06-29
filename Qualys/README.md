# Qualys Report Formatter (Version 2)

A Python automation script to process, clean, and format raw KPI-1 and KPI-2 summary reports downloaded from the Qualys VMDR dashboard.

This tool is designed to help vulnerability management, Linux, and Windows teams by preparing a clear, categorized Excel report that segments vulnerabilities by platform, severity, and age.

---

## 📥 Input Files

You’ll need two `.csv` files exported from Qualys:
- **KPI-1 Detailed Report** (Linux/Unix focused vulnerabilities)
- **KPI-2 Detailed Report** (Windows-focused vulnerabilities)

Make sure both files are in the same folder as the script before running.

---

## 🧠 Features

- Combines **KPI-1 & KPI-2** into one Excel workbook with 3 sheets:
  - `Raw`: Complete raw data (cleaned)
  - `KPI-1`: Prioritized Linux/Unix vulns, split into LATE & NON-LATE
  - `KPI-2`: Prioritized Windows vulns, split into LATE & NON-LATE
- Dynamically calculates **Detection Age** from raw data
- Segregates by **SEVERITY levels** and applies **custom Hostname logic**
- Sorts and highlights based on **DETECTION COUNT**
- Formats output Excel with styling (borders, alignment, spacing)

---

## 📊 Output

The final output is a neatly styled `.xlsx` file containing:

- ✅ Late vs Non-Late categorized vulnerabilities
- ✅ Auto-assigned Hostnames (based on OS & pattern logic)
- ✅ Prioritized rows by detection count
- ✅ Additional empty columns for manual tracking (e.g., Action Taken, Comments)

---

## 🛠️ Technologies Used

- `pandas`  
- `openpyxl`  
- `collections.Counter`  
- Standard Python 3 file handling and input prompts

---

## 🛑 Warning

> ⚠️ Make sure to **remove or mask real asset data** or Qualys customer info before sharing reports or scripts.

---

## 📦 EXE Version

If you don't have Python installed, a standalone `.exe` version of this script is available under the [Releases section](https://github.com/arovilpradhan/infra-security-automation/releases).

---

## ✍️ Author & Credits

Script logic and formatting assisted by [Arovil Pradhan](https://github.com/arovilpradhan) during real-world SOC/VM projects with automation use cases.

---
