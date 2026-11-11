# Registro de evidencias externas PENDIENTES

No son capturas ni resultados ejecutados. Completar después de usar infraestructura real.
Mantener una copia final del PDF con estas evidencias anexadas antes de presentarlo como
ejecución integral del caso.

| ID | Evidencia a insertar | Datos que deben ser visibles |
|---|---|---|
| E01 | Instalación Docker/Jenkins | comando, fecha, salida build y compose ps |
| E02 | Herramientas/plugins | versiones Python, plugins y pip freeze del build |
| E03 | Creación del job | SCM GitHub, main y ruta Jenkinsfile; ocultar tokens |
| E04 | Ejecución | número de build, commit, etapas y resultado real |
| E05 | Reportes | Test Result, flake8, JSON bandit y códigos de salida |
| E06 | Artefactos | wheel/sdist, SHA256SUMS y huellas de Jenkins |
| E07 | Despliegue | /health con release, release.json y logs testserver |
| E08 | Control negativo | build fallido y evidencia de no despliegue |
| E09 | Reversión | fallo de salud, current restaurado y salud anterior |

Recopilar con los comandos del README. Para cada evidencia anotar: fecha y zona horaria,
entorno, comando o acción, resultado, nombre del archivo y número de build/commit.
No sustituir estas evidencias por salidas inventadas ni imágenes de terminal recreadas.

## Plantilla por evidencia

ID: ______ Fecha/hora/zona: ______ Build/commit: ______

Acción y comando: ______

Resultado real y código de salida: ______

Archivo o captura adjunta: ______

Análisis: ______
