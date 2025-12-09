# import re
# from collections import defaultdict

# def parse_config(text):
#     lines = [l.rstrip() for l in text.splitlines()]
#     cfg_parsed = {
#         "interfaces": [l for l in lines if l.startswith("interface") or l.strip().startswith("ip address")],
#         "lines": [l for l in lines if l.startswith("line") or l.startswith("username")],
#         "snmp": [l for l in lines if l.startswith("snmp-server")],
#         "acls": [l for l in lines if re.match(r'^(access-list|ip access-list)', l)],
#         "services": [l for l in lines if any(s in l for s in ("telnet", "ssh", "enable secret", "enable password"))],
#         "raw": lines
#     }
#     return cfg_parsed
import re


def normalize_line(line: str) -> str:
    """Strip trailing spaces and ignore comment-like lines."""
    line = line.rstrip("\n\r")
    # Ignore full-line comments (Cisco style '!' or '#')
    if line.strip().startswith("!") or line.strip().startswith("#"):
        return ""
    return line


def parse_config(text: str):
    """
    Very simple Cisco-style parser.
    Returns a dict with keys used by checks.py
    """
    lines_raw = text.splitlines()
    lines = [normalize_line(l) for l in lines_raw]
    lines = [l for l in lines if l]  # drop empty

    interfaces = []
    current_if = None

    for l in lines:
        if l.lower().startswith("interface "):
            current_if = l
            interfaces.append(l)
        elif current_if and l.startswith(" "):
            interfaces.append(l)
        else:
            current_if = None

    cfg_parsed = {
        "interfaces": interfaces,
        "lines": [l for l in lines if l.lower().startswith("line ")
                  or l.lower().startswith("username ")],
        "snmp": [l for l in lines if l.lower().startswith("snmp-server")],
        "acls": [l for l in lines if re.match(r'^(access-list|ip access-list)', l, re.I)],
        "services": [
            l for l in lines
            if any(s in l.lower() for s in ("telnet", "ssh", "enable secret", "enable password"))
        ],
        "raw": lines,
    }
    return cfg_parsed
