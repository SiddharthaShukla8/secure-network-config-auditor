Secure Network Configuration Auditor

A Python–Flask based tool that automatically scans router/switch configuration files to identify security vulnerabilities such as Telnet access, SSHv1 usage, weak passwords, insecure ACLs, and SNMP public communities. The tool provides severity-based alerts and recommended fixes through a simple and responsive web interface.

📌 Features

Upload or paste router/switch configuration files

Automatic parsing of Cisco-style network configs

Vulnerability detection:

Telnet enabled

SSH version 1

Plaintext/weak passwords

SNMP community “public”

permit ip any any ACL detection

Clean UI with light-blue theme

JSON-based detailed report

Easy to extend with additional checks

🧠 Why This Project?

Misconfigured network devices are one of the largest sources of security breaches.
This tool automates the process of reviewing configuration files, making it faster and more reliable than manual audits.

🛠️ Tech Stack

Python 3

Flask (Web Framework)

HTML/CSS (Frontend)

Regex for parsing

GNS3 / Packet Tracer (optional – for generating configs)

📁 Project Structure
config_auditor/
│
├── app.py                 # Flask server
├── parser_mod.py          # Config parser
├── checks.py              # Vulnerability checks
│
├── templates/
│     ├── index.html       # Upload UI
│     └── report.html      # Results page
│
└── static/
      └── style.css        # UI styling
