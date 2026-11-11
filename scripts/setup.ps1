$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
New-Item -ItemType Directory -Force evidence | Out-Null
docker version 2>&1 | Tee-Object evidence/docker-version.txt
if ($LASTEXITCODE -ne 0) { throw 'Inicie el motor de Docker Desktop (Linux containers).' }
docker compose config | Out-File evidence/compose-resolved.yaml -Encoding utf8
if ($LASTEXITCODE -ne 0) { throw 'Compose no valido' }
docker compose build 2>&1 | Tee-Object evidence/build.log
if ($LASTEXITCODE -ne 0) { throw 'Fallo de construccion' }
docker compose up -d 2>&1 | Tee-Object evidence/start.log
if ($LASTEXITCODE -ne 0) { throw 'Fallo de inicio' }
docker compose ps | Tee-Object evidence/containers.txt
Write-Host 'Abra http://localhost:8080 tras iniciar Jenkins.'
Write-Host 'Clave: docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword'
