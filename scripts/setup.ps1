$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
New-Item -ItemType Directory -Force evidence | Out-Null
# Windows PowerShell 5 interpreta stderr nativo como errores PowerShell.
# Docker envia progreso normal a stderr: capturar ambos flujos y evaluar ExitCode.
function Invoke-DockerStep {
    param([string[]]$DockerArgs, [string]$Name)
    $stdout = Join-Path (Get-Location) "evidence/$Name.stdout.log"
    $stderr = Join-Path (Get-Location) "evidence/$Name.stderr.log"
    $process = Start-Process -FilePath 'docker' -ArgumentList $DockerArgs `
        -WindowStyle Hidden -Wait -PassThru `
        -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    Get-Content -LiteralPath $stdout -Tail 10
    Get-Content -LiteralPath $stderr -Tail 10
    if ($process.ExitCode -ne 0) {
        throw "Docker fallo en $Name (codigo $($process.ExitCode)); revisar evidence/."
    }
}
Invoke-DockerStep -DockerArgs @('version') -Name 'docker-version'
Invoke-DockerStep -DockerArgs @('compose', 'config') -Name 'compose-config'
Invoke-DockerStep -DockerArgs @('compose', 'build') -Name 'build'
Invoke-DockerStep -DockerArgs @('compose', 'up', '-d') -Name 'start'
Invoke-DockerStep -DockerArgs @('compose', 'ps') -Name 'containers'
Write-Host 'Abra http://localhost:8080 tras iniciar Jenkins.'
Write-Host 'Clave: docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword'
