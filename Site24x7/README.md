# Site24x7 Monitor Deletion Automation

A Python-based automation tool to authenticate with the Site24x7 API, fetch monitor details by name, and delete monitors in a secure, token-driven way.

This script helps infrastructure or monitoring teams quickly decommission outdated monitors without manual portal access.

---

## 🔐 Authentication Setup

The script uses **Zoho OAuth 2.0 tokens** to authenticate.

- Credentials and tokens are stored securely in:
  - `Site24x7OauthTokenDetails.json`

- The script will automatically:
  - Generate a new token if none exists
  - Refresh expired tokens
  - Store updated tokens in the `.json` file

---

## 📥 Input

- Monitor Name (entered by user at runtime)

Example:
```bash
Enter the monitor name: test-server-02

---------------------------------------

Output:-
Your hostname 'test-server-02' with ID '123456' has been successfully deleted.
