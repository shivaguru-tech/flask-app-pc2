"""
release_report.py — XYZ Company release health checker.

Unlike a plain pytest-style test file, this script scans the project
directory, checks that the site files exist and are well-formed, then
prints a small release report. Designed to run as a Jenkins pipeline
stage before deployment.

Usage:
    python3 release_report.py
"""

import os
import sys
from datetime import datetime


REQUIRED_FILES = ["index.html", "main.css"]


def file_check(filename):
    path = os.path.join(os.getcwd(), filename)
    exists = os.path.isfile(path)
    size = os.path.getsize(path) if exists else 0
    return {"file": filename, "exists": exists, "size_bytes": size}


def html_references_css(html_file, css_file):
    if not os.path.isfile(html_file):
        return False
    with open(html_file) as f:
        contents = f.read()
    return css_file in contents


def build_report():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    checks = [file_check(f) for f in REQUIRED_FILES]
    css_linked = html_references_css("index.html", "main.css")

    all_present = all(c["exists"] for c in checks)
    healthy = all_present and css_linked

    print("=" * 42)
    print(" XYZ COMPANY — RELEASE HEALTH REPORT")
    print("=" * 42)
    print(f" Generated : {timestamp}")
    for c in checks:
        status = "OK" if c["exists"] else "MISSING"
        print(f" {c['file']:<12} : {status} ({c['size_bytes']} bytes)")
    print(f" CSS linked  : {'YES' if css_linked else 'NO'}")
    print(f" Overall     : {'HEALTHY' if healthy else 'UNHEALTHY'}")
    print("=" * 42)

    return healthy


if __name__ == "__main__":
    is_healthy = build_report()
    sys.exit(0 if is_healthy else 1)
