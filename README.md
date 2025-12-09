Secure Network Configuration Auditor

A Python-Flask based auditing tool that scans router/switch configuration files and detects critical security vulnerabilities such as Telnet access, SSHv1, weak passwords, insecure ACLs, and SNMP public communities.
The system provides severity-based alerts, recommended fixes, and a clean UI for uploading and analyzing configurations.

🚀 Features

✔ Upload or paste router/switch configuration files
✔ Cisco-style config parsing
✔ Real-time vulnerability scanning
✔ Severity levels (HIGH / MEDIUM / LOW)
✔ Recommended fixes for every issue
✔ Clean light-blue UI design
✔ JSON and tabular results
✔ Performance metrics (scan time, line count)
✔ Error handling for invalid configs

🔐 Vulnerabilities Detected

Our system detects:

1. Telnet Enabled

Identifies insecure remote access.

2. SSH Version 1

Deprecated & unsafe protocol.

3. Weak or Plaintext Passwords

Flags passwords like admin, 1234, cisco, etc.

4. SNMP Public/Private Communities

Old insecure monitoring configurations.

5. Insecure ACL Rules

Example: permit ip any any.

6. Missing Best Practices

No password encryption

No login banner

Weak authentication commands

🧠 How It Works

User uploads/pastes configuration

Config parser extracts relevant sections

Security engine runs multiple rule-based checks

Issues are ranked by severity

Results displayed in UI + JSON format

🏗️ Project Architecture
User Input (File/Text)
        ↓
Config Parser  →  Normalized Structure
        ↓
Security Check Engine (Multiple Modules)
        ↓
Issue Aggregator → Severity Ranking
        ↓
Flask Frontend UI → JSON + Table Output

🖥️ Tech Stack

Python 3

Flask (Backend + UI engine)

HTML/CSS (Frontend)

Regex-based parsing

GNS3 / Packet Tracer (for optional config generation)

📁 Project Structure
config_auditor/
│
├── app.py
├── parser_mod.py
├── checks.py
│
├── templates/
│     ├── index.html
│     └── report.html
│
├── static/
│     └── style.css
│
└── README.md

📊 Performance Metrics (Example)
Metric	           Value
Total lines scanned	120
Scan time	         0.004 sec
Issues found	       5
🌱 Future Scope

Auto-fetch configs over SSH

Multi-vendor support (Juniper, MikroTik, HP)

Visualization dashboard

ML-based risk scoring

Export complete PDF report

API support for enterprise integration

📄 License

This project is created for academic and research purposes under the Computer Networks course.
