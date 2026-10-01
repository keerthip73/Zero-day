$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$BackendDir = Join-Path $ProjectRoot "backend"
$BundledMaven = "C:\Program Files\JetBrains\IntelliJ IDEA Community Edition 2023.2.5\plugins\maven\lib\maven3\bin\mvn.cmd"

if (Get-Command mvn -ErrorAction SilentlyContinue) {
    $Maven = "mvn"
} elseif (Test-Path $BundledMaven) {
    $Maven = $BundledMaven
} else {
    throw "Maven was not found. Install Maven or use IntelliJ IDEA Community Edition bundled Maven."
}

Set-Location $BackendDir
$env:ML_SERVICE_URL = "http://127.0.0.1:8000"
& $Maven spring-boot:run "-Dspring-boot.run.profiles=local"
