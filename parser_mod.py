import re
from collections import defaultdict

def parse_config(text):
    lines = [l.rstrip() for l in text.splitlines()]
    cfg_parsed = {
        "interfaces": [l for l in lines if l.startswith("interface") or l.strip().startswith("ip address")],
        "lines": [l for l in lines if l.startswith("line") or l.startswith("username")],
        "snmp": [l for l in lines if l.startswith("snmp-server")],
        "acls": [l for l in lines if re.match(r'^(access-list|ip access-list)', l)],
        "services": [l for l in lines if any(s in l for s in ("telnet", "ssh", "enable secret", "enable password"))],
        "raw": lines
    }
    return cfg_parsed
