import json
import os
import sys

deploy_version = os.environ.get("DEPLOY_VERSION", "")

if not deploy_version:
    print("ERROR: DEPLOY_VERSION is empty")
    sys.exit(1)

print(f"==========================================")
print(f"Deploying vertotal version: {deploy_version}")
print(f"==========================================")

with open("versions.json", "r") as f:
    data = json.load(f)

ver1_version = data["ver1"]
ver2_version = data["ver2"]

print(f"ver1 version to deploy: {ver1_version}")
print(f"ver2 version to deploy: {ver2_version}")

with open("DEPLOY_VER1_VERSION.txt", "w") as f:
    f.write(ver1_version)

with open("DEPLOY_VER2_VERSION.txt", "w") as f:
    f.write(ver2_version)

print(f"Ready to deploy ver1 v{ver1_version} and ver2 v{ver2_version}")
