"""Validacion local con registros autenticos y codigos de salida."""
import datetime
import json
import os
# Herramientas de validacion fijas, invocadas como listas sin shell.
import subprocess  # nosec B404
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
reports = root / "reports"
reports.mkdir(exist_ok=True)
(reports / "flake8.txt").unlink(missing_ok=True)
(reports / "flake8.txt").touch()
temporary = root / ".tmp"
temporary.mkdir(exist_ok=True)
environment = dict(os.environ, TMP=str(temporary), TEMP=str(temporary))
commands = [
    [sys.executable, "--version"],
    [sys.executable, "-m", "pip", "install", "--no-build-isolation",
     "--no-deps", "-e", "."],
    [sys.executable, "-m", "pytest", "-v", "--junitxml=reports/pytest.xml"],
    [sys.executable, "-m", "flake8", "src", "tests", "scripts",
     "--output-file=reports/flake8.txt"],
    [sys.executable, "-m", "bandit", "-r", "src", "scripts", "-f", "json",
     "-o", "reports/bandit.json"],
    [sys.executable, "-m", "build", "--no-isolation"],
    ["docker", "compose", "config"],
    ["docker", "version"],
]
results = []
for index, command in enumerate(commands):
    result = subprocess.run(  # nosec B603
        command, cwd=root, env=environment, capture_output=True, text=True)
    log = "$ " + " ".join(command) + "\n" + result.stdout + result.stderr
    log += "\nEXIT_CODE=" + str(result.returncode) + "\n"
    (reports / f"local-{index:02}.log").write_text(log, encoding="utf-8")
    results.append({"command": command, "exit": result.returncode,
                    "log": f"local-{index:02}.log"})
    print(index, result.returncode, " ".join(command[1:]))
(reports / "validation.json").write_text(json.dumps({
    "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "platform": sys.platform, "results": results}, indent=2), encoding="utf-8")
sys.exit(any(row["exit"] for row in results[:-1]))
