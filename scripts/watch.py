"""Servidor independiente: reinicia el proceso al cambiar el enlace current."""
import os
import signal
# Arranque controlado del interprete de la release; nunca se usa shell=True.
import subprocess  # nosec B404
import time
from pathlib import Path

process = None
current = None
running = True


def stop(signum, frame):
    global running
    running = False


signal.signal(signal.SIGTERM, stop)
while running:
    target = Path("/srv/current")
    release = target.resolve() if target.exists() else None
    if release != current or (process and process.poll() is not None):
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        current = release
        if release:
            command = [str(release / "venv/bin/python"), "-m", "xyzapp"]
            environment = dict(os.environ, RELEASE_ID=release.name)
            process = subprocess.Popen(command, env=environment)  # nosec B603
    time.sleep(1)
if process and process.poll() is None:
    process.terminate()
    process.wait(timeout=5)
