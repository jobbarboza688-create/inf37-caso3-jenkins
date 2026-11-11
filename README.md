# Caso N.º 3 | INF-37 | UIA

Estudiante: ____________________  
Docente: Federico Sánchez Díaz  
Fecha del enunciado: 4/11/2026. Preparación: 11/11/2026. Valor del caso: 5%.

## Alcance y estado

Implementación de laboratorio para XYZ SOLUTIONS S.A. Aplicación Python sin dependencias
de ejecución: API HTTP `/health`, respuesta JSON y función de suma validada. Jenkins
obtiene GitHub, crea venv, instala herramientas, prueba, analiza, empaqueta wheel/sdist
y publica automáticamente en un servidor de pruebas independiente.

**No se ha ejecutado Jenkins, GitHub remoto ni el despliegue Docker.** El motor Docker
no estaba disponible en la preparación. Los registros `reports/local-*.log` documentan
únicamente ejecuciones locales reales; `validation.json` contiene códigos de salida y fecha
UTC. No usar estos registros como capturas de Jenkins. Las evidencias externas siguen
pendientes aunque el código esté preparado. Véase `EVIDENCIAS.md`.

## 1. Requisitos

Docker Engine y Compose v2 en Linux, o Docker Desktop con contenedores Linux en Windows;
Git, navegador, acceso a Docker Hub, repositorio público GitHub y PyPI. Reservar como
referencia 4 GB de RAM y espacio para imágenes. Puertos locales 8080 y 8000 libres.
En Windows, `setup.ps1` evita depender de Bash; `setup.sh` es para Bash/Linux/WSL.
No subir contraseñas, tokens, entornos virtuales ni `evidence/` con secretos al repositorio.

## 2. Publicar el código en GitHub

Crear un repositorio vacío en GitHub (sin README remoto). Desde esta carpeta ejecutar,
sustituyendo únicamente USUARIO y REPOSITORIO por los datos reales:

```sh
git init -b main
git add .
git commit -m "Implementar CI/CD Caso 3"
git remote add origin https://github.com/USUARIO/REPOSITORIO.git
git push -u origin main
```

Git requiere una identidad configurada por el usuario. Autenticarse con Git Credential
Manager o SSH; nunca incluir un token en la URL o en Jenkinsfile. Para repositorio público,
Jenkins clona sin credenciales. Para privado, registrar en Jenkins una credencial de lectura
de GitHub y seleccionarla en SCM; no añadirla al código. No se ha creado un repositorio
real desde este entorno.

## 3. Instalar Jenkins en Docker (Parte 1, 50%)

```sh
bash scripts/setup.sh
```

En PowerShell, desde esta carpeta:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
```

Ambos scripts verifican Docker, validan Compose, construyen la imagen y arrancan servicios.
Detienen la instalación ante un error. Los comandos equivalentes son:

```sh
docker version
docker compose config
docker compose build
docker compose up -d
docker compose ps
docker compose logs --tail=100 jenkins
docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Abrir http://localhost:8080, desbloquear con la clave, crear un administrador propio,
y completar el asistente usando los plugins ya instalados. No registrar la clave ni
credenciales en las capturas de entrega. Jenkins conserva sus datos en `jenkins_home`.
`init` finaliza con éxito al preparar propietario UID/GID 1000 de `releases`; es normal
que no quede en ejecución.

La imagen instala Python, venv, Git y curl; `jenkins-plugin-cli` instala:

| Plugin | Uso |
|---|---|
| workflow-aggregator | Pipeline y sintaxis declarativa |
| git | checkout del repositorio |
| github | integración opcional con GitHub |
| junit | publicación nativa del XML de pytest |
| timestamper | marcas de tiempo de consola |

**flake8, pytest y bandit son paquetes Python ejecutados por Jenkins; Python es el
intérprete. No se presentan como tres plugins Jenkins independientes.** Se instalan en
el venv de cada ejecución con `requirements-dev.txt`. Los reportes de flake8 y bandit
se archivan; pytest se integra con `junit`. No hace falta Docker Pipeline porque los
pasos usan Python y el volumen compartido, sin invocar Docker desde Jenkins.

## 4. Crear Pipeline (Parte 2, 50%)

1. Jenkins > New Item > nombre `caso3-xyz` > Pipeline > OK.
2. Pipeline > Definition > Pipeline script from SCM > SCM Git.
3. Repository URL: URL real del paso 2. Credentials: ninguna para público.
4. Branch Specifier `*/main`. Script Path `Jenkinsfile`. Guardar.
5. Build Now. En la primera ejecución se registra el SCM para la consulta periódica.
6. Consultar Console Output y Stage View (si está instalado) o la vista de etapas
   disponible. Abrir Test Result y Archived Artifacts.

El Jenkinsfile consulta cambios cada cinco minutos aproximadamente (`H/5`); así funciona
sin exponer Jenkins a Internet. Un webhook es opcional y requiere una URL HTTPS real
accesible por GitHub: configurar `/github-webhook/` y el disparador GitHub correspondiente.
La configuración entregada usa polling; no exige webhook ni túnel.

Este laboratorio usa el ejecutor del controlador (Manage Jenkins > Nodes > Built-In Node,
al menos un ejecutor). No ejecute código de terceros sin confianza en este Jenkins. Para
uso empresarial, separar agentes y permisos de despliegue. El volumen compartido tiene
sentido para este servidor de pruebas local, no sustituye un servidor remoto de producción.

## 5. Flujo y comandos ejecutados en Jenkins

El archivo `Jenkinsfile` es la fuente exacta. Resumen ejecutable en un shell Linux:

```sh
git rev-parse HEAD
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pip install --no-build-isolation -e .
mkdir -p reports
.venv/bin/python -m pip freeze > reports/dependencies.txt
.venv/bin/python -m flake8 src tests scripts --output-file=reports/flake8.txt
.venv/bin/python -m pytest -v --junitxml=reports/pytest.xml
.venv/bin/python -m bandit -r src scripts -f json -o reports/bandit.json
.venv/bin/python -m build --no-isolation
sha256sum dist/* > reports/SHA256SUMS
.venv/bin/python scripts/deploy.py dist/*.whl
```

Los tres controles se ejecutan aun cuando uno falle; después cualquier código distinto
de cero bloquea empaquetado/despliegue. No se usa `--exit-zero` ni se ocultan errores con
`|| true`. En `post/always` se publican XML y artefactos disponibles. `allowEmptyResults`
solo permite documentar fallos anteriores a pytest; no convierte un fallo en éxito.

## 6. Destino de pruebas y reversión

`testserver` es un contenedor separado basado en la misma imagen que Jenkins para que
el intérprete de los venv sea compatible. Jenkins escribe en el volumen `/srv`; el servidor
lo monta en lectura. No se monta el socket de Docker ni se requiere SSH o privilegio
Docker dentro de Jenkins. En http://localhost:8000/health se verá la API tras el despliegue.

`deploy.py` crea `/srv/releases/BUILD_NUMBER-COMMIT`, instala el wheel con `--no-index
--no-deps`, registra SHA-256/commit y cambia atómicamente `/srv/current`. `watch.py` detecta
el cambio, detiene el proceso anterior e inicia el nuevo. La salud exige `status=ok` y
el identificador de la nueva release, evitando aceptar accidentalmente la versión vieja.
Si falla, se restaura el enlace previo y el pipeline termina con error. El primer fallo
retira el enlace; puede haber una interrupción breve y la recuperación debe verificarse.
No es un despliegue sin caída. `disableConcurrentBuilds()` evita despliegues concurrentes
del mismo job; dedicar este volumen a un único job. Las releases no se borran automáticamente.

```sh
curl -f http://localhost:8000/health
docker compose logs --tail=100 testserver
docker compose exec jenkins cat /srv/current/release.json
docker compose exec jenkins readlink /srv/current
```

Prueba de control: introducir temporalmente un test que falle, hacer commit/push y
construir. Debe fallar Calidad y pruebas, omitir despliegue y conservar el enlace de la
versión anterior. Revertir el commit y repetir. Para probar rollback, en una rama de
laboratorio provocar que la API no arranque pero mantener los tests aprobados, construir
y comprobar restauración de `current` y salud previa. Estas pruebas externas están pendientes.

## 7. Validación local independiente de Jenkins

Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
```

Windows:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
.venv/Scripts/python scripts/validate.py
```

La validación genera los logs reales, XML y JSON, wheel/sdist y configuración Compose
resuelta. La comprobación de Docker queda registrada; su indisponibilidad se informa
separadamente del estado de las comprobaciones Python. Para ejecutar la aplicación:

```sh
.venv/bin/python -m xyzapp
```

En Windows usar `.venv/Scripts/python -m xyzapp`. Los tests incluyen suma, entradas no
numéricas y solicitudes HTTP reales de salud y 404 en un puerto local efímero.

## 8. Reproducibilidad y límites

Versiones directas fijadas en requirements y backend de construcción. La etiqueta
`lts-jdk21`, paquetes apt y resolución transitiva de plugins son móviles: reproducción
funcional prevista, no imagen binaria idéntica. Tras la primera instalación satisfactoria,
guardar digest de la base, listado completo de plugins y dependencias de ese Linux;
fijar digest y versiones resueltas si se exige reproducción exacta. No se atribuye éxito
a una imagen o combinación de plugins que no se ha construido en este entorno.

```sh
docker image inspect xyz-jenkins:caso3 > evidence/image-inspect.json
docker compose exec jenkins python3 --version
docker compose exec jenkins sh -c 'find /var/jenkins_home/plugins -name "*.jpi"'
```

En Jenkins, Manage Jenkins > Script Console (solo administrador), ejecutar:

```groovy
Jenkins.instance.pluginManager.plugins.sort { it.shortName }.each {
  println("${it.shortName}:${it.version}")
}
```

Guardar el resultado sin datos secretos y las versiones de `reports/dependencies.txt`.
La única supresión Bandit del servidor HTTP B104 se justifica por el enlace interno del
contenedor con puerto publicado en loopback. B603 documenta comandos de subprocesos
controlados sin shell; B310 se restringe a la URL HTTP interna fija. Bandit es análisis
estático, no certifica ausencia total de vulnerabilidades. No se usa este servidor HTTP
didáctico como servidor de producción.

## 9. Operación y problemas frecuentes

Motor no disponible: iniciar Docker Desktop y esperar su motor Linux; repetir `docker
version`. Puerto ocupado: liberar 8080/8000 o modificar solo el puerto del host en Compose.
Fallo de plugins/PyPI: revisar conectividad y proxy y reconstruir, sin quitar controles.
Permission denied en /srv: comprobar que init terminó correctamente y UID 1000 coincide.
No aparece app: comprobar Console Output, `deploy.json` y logs del servidor. Si se mueve
la carpeta, volver a crear el servicio para actualizar el bind de `watch.py`.

```sh
docker compose down
docker compose up -d
```

`down` conserva datos. No usar `down -v` salvo que se desee eliminar expresamente todos
los datos del laboratorio, incluidas configuración y releases. Se excluyen secretos de
Git; nunca incorporar la clave inicial al PDF.

## Referencias oficiales

- https://www.jenkins.io/doc/book/installing/docker/
- https://www.jenkins.io/doc/book/managing/plugins/
- https://www.jenkins.io/doc/book/pipeline/syntax/
- https://bandit.readthedocs.io/en/latest/man/bandit.html
- https://docs.pytest.org/en/stable/how-to/output.html
- https://flake8.pycqa.org/en/latest/user/invocation.html
- https://packaging.python.org/en/latest/tutorials/packaging-projects/
