"""Inventario verificable sin contrasenas ni configuracion sensible."""
import json
import platform
import zipfile
from pathlib import Path

plugins = {}
for path in Path('/var/jenkins_home/plugins').glob('*.jpi'):
    with zipfile.ZipFile(path) as archive:
        manifest = archive.read('META-INF/MANIFEST.MF').decode()
    values = dict(line.split(': ', 1) for line in manifest.splitlines()
                  if ': ' in line)
    plugins[values.get('Short-Name', path.stem)] = values.get('Plugin-Version')
print(json.dumps({'python': platform.python_version(), 'plugins': plugins}, indent=2))
