# Script de PowerShell para sincronizar el repositorio con GitHub
$ErrorActionPreference = "Continue"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Inicializador de Git y Cargador a GitHub" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Verificar si git está instalado
try {
    $gitVersion = git --version
    Write-Host "Se encontró: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Git no está instalado o no se encuentra en el PATH." -ForegroundColor Red
    Write-Host "Por favor, instale Git desde https://git-scm.com/ e intente nuevamente." -ForegroundColor Yellow
    exit 1
}

# 2. Inicializar Git
if (-not (Test-Path ".git")) {
    Write-Host "Inicializando repositorio Git local..." -ForegroundColor Yellow
    git init
    git branch -M main
    Write-Host "Repositorio local inicializado en la rama main." -ForegroundColor Green
} else {
    Write-Host "El repositorio Git ya está inicializado." -ForegroundColor Green
}

# 3. Agregar origen remoto
$existingRemotes = git remote
$hasOrigin = $false
if ($existingRemotes) {
    foreach ($r in $existingRemotes) {
        if ($r -eq "origin") {
            $hasOrigin = $true
        }
    }
}

if ($hasOrigin) {
    Write-Host "El origen remoto (origin) ya existe." -ForegroundColor Green
    $originUrl = git remote get-url origin
    Write-Host "El origen actual apunta a: $originUrl" -ForegroundColor Gray
    
    if ($originUrl -notmatch "MktLeadGen") {
        Write-Host "Actualizando el origen remoto a https://github.com/westland/MktLeadGen.git..." -ForegroundColor Yellow
        git remote set-url origin https://github.com/westland/MktLeadGen.git
    }
} else {
    Write-Host "Agregando origen remoto que apunta a: https://github.com/westland/MktLeadGen.git" -ForegroundColor Yellow
    git remote add origin https://github.com/westland/MktLeadGen.git
    Write-Host "Origen remoto agregado con éxito." -ForegroundColor Green
}

# 4. Preparar archivos (Stage)
Write-Host "Preparando archivos..." -ForegroundColor Yellow
git add .
Write-Host "Archivos preparados." -ForegroundColor Green

# 5. Crear Commit
Write-Host "Creando commit..." -ForegroundColor Yellow
git commit -m "Commit inicial de Generador de Prospectos de Marketing (MktLeadGen)"
Write-Host "Cambios comprometidos." -ForegroundColor Green

# 6. Cargar en GitHub (Push)
Write-Host "Subiendo a GitHub..." -ForegroundColor Yellow
Write-Host "¡Asegúrese de haber creado el repositorio vacío MktLeadGen en GitHub antes de este paso!" -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "¡Carga exitosa! El proyecto está en vivo en GitHub." -ForegroundColor Green
} else {
    Write-Host "La carga de Git falló. Verifique la existencia del repositorio o la autenticación de Git." -ForegroundColor Red
}
Write-Host "==========================================================" -ForegroundColor Cyan
