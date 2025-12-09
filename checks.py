# import re

# def check_telnet(cfg):
#     findings=[]
#     if any("telnet" in l.lower() for l in cfg["raw"]):
#         findings.append({"issue":"Telnet enabled", "severity":"HIGH",
#                          "fix":"Disable telnet and enable ssh: 'transport input ssh'"})
#     return findings

# def check_ssh_version(cfg):
#     findings=[]
#     if any("ip ssh version 1" in l.lower() for l in cfg["raw"]):
#         findings.append({"issue":"SSH v1 enabled", "severity":"HIGH",
#                          "fix":"Use 'ip ssh version 2'"})
#     return findings

# def check_weak_passwords(cfg):
#     findings=[]
#     for l in cfg["lines"]+cfg["services"]:
#         if "password " in l.lower() and "enable secret" not in l.lower():
#             findings.append({"issue":"Plaintext password found", "severity":"HIGH",
#                              "fix":"Use 'enable secret' with strong hash"})
#     return findings

# def check_snmp(cfg):
#     findings=[]
#     if any("snmp-server community public" in r.lower() for r in cfg["raw"]):
#         findings.append({"issue":"Default SNMP 'public' community", "severity":"HIGH",
#                          "fix":"Use SNMPv3 with authentication"})
#     return findings

# def check_open_ports(cfg):
#     findings=[]
#     for l in cfg["acls"]:
#         if re.search(r'permit\s+ip\s+any\s+any', l, re.I):
#             findings.append({"issue":"ACL permits any-any", "severity":"HIGH",
#                              "fix":"Use least privilege ACLs"})
#     return findings

# def run_checks(cfg):
#     results=[]
#     results += check_telnet(cfg)
#     results += check_ssh_version(cfg)
#     results += check_weak_passwords(cfg)
#     results += check_snmp(cfg)
#     results += check_open_ports(cfg)
#     unique = {r['issue']: r for r in results}
#     return list(unique.values())
import re


def check_telnet(cfg):
    findings = []
    raw = cfg.get("raw", [])
    if any("telnet" in l.lower() for l in raw):
        findings.append({
            "issue": "Telnet enabled",
            "severity": "HIGH",
            "fix": "Disable Telnet and allow only SSH: 'transport input ssh'"
        })
    return findings


def check_ssh_version(cfg):
    findings = []
    raw = cfg.get("raw", [])
    if any("ip ssh version 1" in l.lower() for l in raw):
        findings.append({
            "issue": "SSH v1 enabled",
            "severity": "HIGH",
            "fix": "Configure 'ip ssh version 2' for secure SSH."
        })
    return findings


def check_weak_passwords(cfg):
    findings = []
    lines = cfg.get("lines", [])
    services = cfg.get("services", [])

    for l in lines + services:
        low = l.lower()
        if "password " in low and "enable secret" not in low:
            findings.append({
                "issue": "Plaintext password found",
                "severity": "HIGH",
                "fix": "Use 'enable secret' or 'username <user> secret <pwd>' with strong password."
            })

    # simple weak patterns
    weak_keywords = ["cisco", "admin", "password", "1234", "12345", "123456"]
    for l in lines + services:
        if "password" in l.lower():
            if any(w in l.lower() for w in weak_keywords):
                findings.append({
                    "issue": "Weak password pattern detected",
                    "severity": "MEDIUM",
                    "fix": "Use a long, random password with letters, numbers and symbols."
                })

    return findings


def check_snmp(cfg):
    findings = []
    raw = cfg.get("raw", [])

    for l in raw:
        low = l.lower()
        if "snmp-server community" in low:
            if "public" in low or "private" in low:
                findings.append({
                    "issue": "Insecure SNMP community (public/private)",
                    "severity": "HIGH",
                    "fix": "Use SNMPv3 with auth+priv or strong custom community name."
                })
    return findings


def check_acls(cfg):
    findings = []
    acls = cfg.get("acls", [])

    for l in acls:
        if re.search(r'permit\s+ip\s+any\s+any', l, re.I):
            findings.append({
                "issue": "ACL permits ip any any",
                "severity": "HIGH",
                "fix": "Avoid 'permit ip any any'. Restrict traffic using least-privilege rules."
            })
    return findings


def check_best_practices(cfg):
    findings = []
    raw = cfg.get("raw", [])

    # service password-encryption missing
    has_password = any("password " in l.lower() for l in raw)
    has_encryption = any("service password-encryption" in l.lower() for l in raw)
    if has_password and not has_encryption:
        findings.append({
            "issue": "Password encryption not enabled",
            "severity": "MEDIUM",
            "fix": "Add 'service password-encryption' to hide plain passwords in config."
        })

    # banner recommendation
    if not any(l.lower().startswith("banner ") for l in raw):
        findings.append({
            "issue": "Login banner not configured",
            "severity": "LOW",
            "fix": "Configure legal warning banner to discourage unauthorized access."
        })

    return findings


def run_checks(cfg):
    results = []
    results += check_telnet(cfg)
    results += check_ssh_version(cfg)
    results += check_weak_passwords(cfg)
    results += check_snmp(cfg)
    results += check_acls(cfg)
    results += check_best_practices(cfg)

    # de-duplicate by (issue, severity)
    unique = {}
    for r in results:
        key = (r["issue"], r["severity"])
        unique[key] = r
    return list(unique.values())
