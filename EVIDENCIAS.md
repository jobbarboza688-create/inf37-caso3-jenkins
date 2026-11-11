# Evidencias auténticas de ejecución

Fecha: 11/11/2026. Zona: America/Costa_Rica (UTC-6). La consola Jenkins usa UTC;
la vista gráfica del navegador muestra hora local. No se recrearon pantallas.
Repositorio: https://github.com/jobbarboza688-create/inf37-caso3-jenkins

## Ejecuciones reales

| Build | Resultado | Análisis |
|---|---|---|
| 1 | FAILURE | 10 tests aprobados, tres observaciones Bandit B404 de severidad baja. No se empaquetó ni desplegó. |
| 2 | FAILURE | Calidad y paquetes correctos; faltaba exportar GIT_COMMIT al despliegue. Corregido. |
| 3 | SUCCESS | Primer flujo completo. Se mejoró después el formato del reporte deploy.json. |
| 4 | SUCCESS | flake8=0, pytest=0, bandit=0; 10 tests; paquetes y JSON válidos; release 4-1e60a8ef91b1. |
| 5 | FAILURE esperado | Rama evidence-rollback, commit 9314bcca9e7a: fallo de arranque, salud rechazada y enlace restaurado al build 4. API recuperada. |

El estado final posterior se registra en build-N.json, health.json y release.json.
El código normal permanece en main. La rama de fallo se conserva solo para reproducir
la prueba, sin integrarla a main. No se afirma una prueba de fallo unitario intencional.

## Capturas originales dentro del ZIP

Ubicación: evidence/screenshots/. Cada archivo conserva la captura sin editar.

| Archivo | Evidencia |
|---|---|
| 01-jenkins-instalado.jpg | Pantalla de desbloqueo real, sin contraseña visible. |
| 02-asistente-jenkins.jpg | Asistente inicial. |
| 03-docker-contenedores.png | Motor activo; Jenkins y testserver ejecutándose; init finalizado. |
| 04-github-repositorio.jpg | Repositorio público y archivos publicados. |
| 05-jenkins-listo.jpg | Finalización de la instalación. |
| 06-crear-pipeline.jpg | Creación del job Pipeline. |
| 07-configuracion-scm.jpg | GitHub, rama main y Jenkinsfile. |
| 08-build1-bloqueo-seguridad.jpg | Calidad rechazada y etapas posteriores omitidas. |
| 09-plugins-git.jpg | Plugins Git y GitHub instalados. |
| 10-plugin-junit.jpg | JUnit instalado para XML de pytest. |
| 11-build4-artefactos.jpg | Artefactos y reportes archivados. |
| 12-build4-etapas-correctas.jpg | Todas las etapas aprobadas. |
| 13-build4-pruebas.jpg | Diez pruebas aprobadas en Jenkins. |
| 14-build4-servidor-salud.jpg | API con release del build 4. |
| 15-build5-rollback-consola.jpg | Consola del rechazo y restauración. |
| 16-build5-salud-restaurada.jpg | API recuperada con release del build 4. |

## Registros originales

build-N-console.log contiene la consola real, build-N.json los metadatos Jenkins y
build-N-archive/ los artefactos originales. inventory.json registra Python y plugins;
job-config.xml conserva SCM sin token; health.json, release.json y server.log documentan
el servidor. Los flujos *.stdout.log y *.stderr.log registran el instalador Windows.

El instalador PowerShell se corrigió para capturar stdout/stderr por separado y evaluar
ExitCode: el progreso normal de Docker en stderr no equivale a fallo. Se volvió a
ejecutar completo con salida satisfactoria. Se mantuvo la autenticación de Jenkins.

No se incluyen contraseñas, tokens, claves privadas ni logs de arranque que muestren
la clave inicial. Las evidencias no constituyen una certificación de producción.
