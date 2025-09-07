import os
from pathlib import Path

ENV_FILE = ".env"
OUTPUT_FILE = "docker-compose.yml"

env = {}
with open(ENV_FILE) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            v = v.split("#", 1)[0].strip()
            env[k.strip()] = v

backup_paths = [p.strip() for p in env.get("BACKUP_PATHS", "").split(",") if p.strip()]

volumes = []
for path in backup_paths:
    host_path = Path(path).resolve()
    if host_path.exists():
        container_path = f"/data/{host_path.name}"
        volumes.append((str(host_path), container_path))
    else:
        print(f"Warning: path does not exist: {path}")

lines = [
    "version: '3.9'",
    "services:",
    "  backuper:",
    "    build: .",
    "    container_name: tg_backuper",
    "    env_file:",
    "      - .env",
    "    restart: unless-stopped",
    "    volumes:"
]

for host, container in volumes:
    lines.append(f"      - {host}:{container}:ro")

with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(lines))

print(f"Generated {OUTPUT_FILE} with {len(volumes)} volumes.")
