import json
import os
import sys

deploy_version = os.environ.get("DEPLOY_VERSION", "").strip()

print(f"==========================================")
print(f"Deploy version requested: '{deploy_version}'")
print(f"==========================================")

if not deploy_version:
    print("ERROR: DEPLOY_VERSION is empty")
    sys.exit(1)

with open("versions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"versions.json content: {data}")

ver1_version = data.get("ver1", "").strip()
ver2_version = data.get("ver2", "").strip()

if not ver1_version:
    print("ERROR: ver1 version not found in versions.json")
    sys.exit(1)

if not ver2_version:
    print("ERROR: ver2 version not found in versions.json")
    sys.exit(1)

print(f"ver1 version to deploy: {ver1_version}")
print(f"ver2 version to deploy: {ver2_version}")

with open("DEPLOY_VER1_VERSION.txt", "w", encoding="utf-8", newline='') as f:
    f.write(ver1_version)

with open("DEPLOY_VER2_VERSION.txt", "w", encoding="utf-8", newline='') as f:
    f.write(ver2_version)

print(f"==========================================")
print(f"Ready to deploy:")
print(f"  ver1 -> v{ver1_version}")
print(f"  ver2 -> v{ver2_version}")
print(f"==========================================")
