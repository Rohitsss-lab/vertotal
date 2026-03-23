import json
import os
import sys

def bump(version, bump_type):
    parts = version.strip().split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    if bump_type == "major":
        major += 1; minor = 0; patch = 0
    elif bump_type == "minor":
        minor += 1; patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"

# Read from PARAMS.txt file instead of environment variables
params = {}
with open("PARAMS.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if '=' in line:
            key, value = line.split('=', 1)
            params[key.strip()] = value.strip()

repo_name    = params.get("REPO_NAME", "").strip()
repo_version = params.get("REPO_VERSION", "").strip()
bump_type    = params.get("BUMP_TYPE", "patch").strip()

print(f"==========================================")
print(f"REPO_NAME    = '{repo_name}'")
print(f"REPO_VERSION = '{repo_version}'")
print(f"BUMP_TYPE    = '{bump_type}'")
print(f"==========================================")

if not repo_name or repo_name == 'EMPTY':
    print("ERROR: REPO_NAME is empty")
    sys.exit(1)

if not repo_version or repo_version == 'EMPTY':
    print("ERROR: REPO_VERSION is empty")
    sys.exit(1)

with open("versions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"versions.json BEFORE: {data}")

data[repo_name] = repo_version

old_umbrella = data["umbrella"].strip()
new_umbrella = bump(old_umbrella, bump_type)
data["umbrella"] = new_umbrella

print(f"versions.json AFTER: {data}")

with open("versions.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

with open("NEW_UMBRELLA_VERSION.txt", "w", encoding="utf-8", newline='') as f:
    f.write(new_umbrella)

with open("NEW_TAG.txt", "w", encoding="utf-8", newline='') as f:
    f.write(f"v{new_umbrella}")

with open("VER1_VERSION.txt", "w", encoding="utf-8", newline='') as f:
    f.write(data["ver1"])

with open("VER2_VERSION.txt", "w", encoding="utf-8", newline='') as f:
    f.write(data["ver2"])

print(f"Umbrella: {old_umbrella} -> {new_umbrella}")
print(f"Updated {repo_name} to {repo_version}")
