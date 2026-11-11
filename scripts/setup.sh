#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p evidence
docker version > evidence/docker-version.txt 2>&1
docker compose config > evidence/compose-resolved.yaml
docker compose build 2>&1 | tee evidence/build.log
docker compose up -d 2>&1 | tee evidence/start.log
docker compose ps | tee evidence/containers.txt
echo 'Espere el inicio de Jenkins. Abra http://localhost:8080'
echo 'Clave: docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword'
