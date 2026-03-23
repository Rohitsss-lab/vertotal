import json
import os

def bump(version, bump_type):
    parts = version.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    if bump_type == "major":
        major += 1; minor = 0; patch = 0
    elif bump_type == "minor":
        minor += 1; patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"

repo_name    = os.environ.get("REPO_NAME", "ver")
repo_version = os.environ.get("REPO_VERSION", "1.0.0")
bump_type    = os.environ.get("BUMP_TYPE", "patch")

with open("versions.json", "r") as f:
    data = json.load(f)

data[repo_name] = repo_version

old_umbrella = data["umbrella"]
new_umbrella = bump(old_umbrella, bump_type)
data["umbrella"] = new_umbrella

with open("versions.json", "w") as f:
    json.dump(data, f, indent=2)

with open("NEW_UMBRELLA_VERSION.txt", "w") as f:
    f.write(new_umbrella)

with open("NEW_TAG.txt", "w") as f:
    f.write(f"v{new_umbrella}")

with open("REPO1_VERSION.txt", "w") as f:
    f.write(data["repo1"])

with open("REPO2_VERSION.txt", "w") as f:
    f.write(data["repo2"])

print(f"Umbrella: {old_umbrella} -> {new_umbrella}")
print(f"Updated {repo_name} to {repo_version}")
