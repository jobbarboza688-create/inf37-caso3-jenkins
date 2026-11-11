"""Despliegue de laboratorio mediante volumen compartido; rollback por salud."""
import hashlib
import json
import os
# Comandos internos en listas, sin shell; no se aceptan comandos del usuario.
import subprocess  # nosec B404
import sys
import time
import urllib.request
import venv
from pathlib import Path


def run(command):
    subprocess.run(command, check=True)  # nosec B603


def switch(target):
    temporary = Path("/srv/.next")
    temporary.unlink(missing_ok=True)
    temporary.symlink_to(target, target_is_directory=True)
    os.replace(temporary, "/srv/current")


wheel = Path(sys.argv[1]).resolve()
release_id = os.environ["BUILD_NUMBER"] + "-" + os.environ["GIT_COMMIT"][:12]
release = Path("/srv/releases") / release_id
release.mkdir(parents=True, exist_ok=False)
venv.create(release / "venv", with_pip=True)
python = str(release / "venv/bin/python")
run([python, "-m", "pip", "install", "--no-index", "--no-deps", str(wheel)])
metadata = {"release": release_id, "commit": os.environ["GIT_COMMIT"],
            "sha256": hashlib.sha256(wheel.read_bytes()).hexdigest()}
(release / "release.json").write_text(json.dumps(metadata))
previous = Path("/srv/current").resolve() if Path("/srv/current").exists() else None
switch(release)
# Dar tiempo al supervisor para detectar el cambio antes de probar salud.
time.sleep(3)
for attempt in range(30):
    try:
        endpoint = "http://testserver:8000/health"
        with urllib.request.urlopen(endpoint, timeout=2) as r:  # nosec B310
            health = json.load(r)
            if health.get("status") == "ok" and health.get("release") == release_id:
                print(json.dumps(metadata))
                break
    except (OSError, ValueError):
        pass
    time.sleep(1)
else:
    if previous:
        switch(previous)
    else:
        Path("/srv/current").unlink(missing_ok=True)
    raise SystemExit("Fallo de salud: se restauro el enlace anterior; revisar servidor")
