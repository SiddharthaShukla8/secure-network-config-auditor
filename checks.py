import re

def check_telnet(cfg):
    findings=[]
    if any("telnet" in l.lower() for l in cfg["raw"]):
        findings.append({"issue":"Telnet enabled", "severity":"HIGH",
                         "fix":"Disable telnet and enable ssh: 'transport input ssh'"})
    return findings

def check_ssh_version(cfg):
    findings=[]
    if any("ip ssh version 1" in l.lower() for l in cfg["raw"]):
        findings.append({"issue":"SSH v1 enabled", "severity":"HIGH",
                         "fix":"Use 'ip ssh version 2'"})
    return findings

def check_weak_passwords(cfg):
    findings=[]
    for l in cfg["lines"]+cfg["services"]:
        if "password " in l.lower() and "enable secret" not in l.lower():
            findings.append({"issue":"Plaintext password found", "severity":"HIGH",
                             "fix":"Use 'enable secret' with strong hash"})
    return findings

def check_snmp(cfg):
    findings=[]
    if any("snmp-server community public" in r.lower() for r in cfg["raw"]):
        findings.append({"issue":"Default SNMP 'public' community", "severity":"HIGH",
                         "fix":"Use SNMPv3 with authentication"})
    return findings

def check_open_ports(cfg):
    findings=[]
    for l in cfg["acls"]:
        if re.search(r'permit\s+ip\s+any\s+any', l, re.I):
            findings.append({"issue":"ACL permits any-any", "severity":"HIGH",
                             "fix":"Use least privilege ACLs"})
    return findings

def run_checks(cfg):
    results=[]
    results += check_telnet(cfg)
    results += check_ssh_version(cfg)
    results += check_weak_passwords(cfg)
    results += check_snmp(cfg)
    results += check_open_ports(cfg)
    unique = {r['issue']: r for r in results}
    return list(unique.values())
