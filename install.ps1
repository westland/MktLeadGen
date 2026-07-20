# Instalador de PowerShell para Windows 11 - Generador de Prospectos de Marketing
$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "🚀 Instalador de Generador de Prospectos de Marketing" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Verificar instalación de Python
Write-Host "🔍 Verificando instalación de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ Se encontró: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no está instalado o no se ha agregado a la variable de entorno PATH." -ForegroundColor Red
    Write-Host "Por favor, instale Python 3.10+ y seleccione 'Agregar python.exe al PATH' durante la instalación." -ForegroundColor Yellow
    exit 1
}

# 2. Configurar entorno virtual
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Creando entorno virtual en el directorio .venv..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ Entorno virtual creado con éxito." -ForegroundColor Green
} else {
    Write-Host "✅ La carpeta del entorno virtual (.venv) ya existe." -ForegroundColor Green
}

# 3. Actualizar pip e instalar dependencias
Write-Host "⚡ Instalando dependencias del proyecto (esto puede tardar un par de minutos)..." -ForegroundColor Yellow
& .venv\Scripts\python.exe -m pip install --upgrade pip

# Instalar dependencias
& .venv\Scripts\pip.exe install crewai crewai-tools praw discord.py streamlit pandas schedule python-dotenv langchain-google-genai nest-asyncio pyyaml requests beautifulsoup4

Write-Host "✅ Dependencias instaladas con éxito." -ForegroundColor Green

# 4. Manejar archivo de configuración .env
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Host "📝 Creando archivo .env a partir de la plantilla .env.example..." -ForegroundColor Yellow
        Copy-Item .env.example .env
        Write-Host "⚠️ Recuerde revisar el archivo .env y completar sus claves de API." -ForegroundColor DarkYellow
    } else {
        Write-Host "❌ Falta la plantilla .env.example. No se pudo crear el .env por defecto." -ForegroundColor Red
    }
} else {
    Write-Host "✅ El archivo de configuración .env ya existe." -ForegroundColor Green
}

# 5. Crear accesos directos de inicio rápido batch
Write-Host "💾 Generando accesos directos por lotes para Windows..." -ForegroundColor Yellow

# Acceso directo al Panel de Control
$dashboardBat = "@echo off`r`ncd /d %~dp0`r`ncall .venv\Scripts\activate.bat`r`nstreamlit run dashboard.py`r`npause"
$dashboardBat | Out-File -FilePath "start_dashboard.bat" -Encoding ascii -NoNewline

# Acceso directo al Escaneo
$scraperBat = "@echo off`r`ncd /d %~dp0`r`ncall .venv\Scripts\activate.bat`r`npython -m src.marketing_leads_generator.main`r`npause"
$scraperBat | Out-File -FilePath "run_scraper.bat" -Encoding ascii -NoNewline

# Acceso directo al Programador
$schedulerBat = "@echo off`r`ncd /d %~dp0`r`ncall .venv\Scripts\activate.bat`r`npython scheduler.py`r`npause"
$schedulerBat | Out-File -FilePath "start_scheduler.bat" -Encoding ascii -NoNewline

Write-Host "✅ Creado: start_dashboard.bat" -ForegroundColor Green
Write-Host "✅ Creado: run_scraper.bat" -ForegroundColor Green
Write-Host "✅ Creado: start_scheduler.bat" -ForegroundColor Green

# 6. Crear acceso directo en el Escritorio
Write-Host "🖥️ Creando acceso directo en el Escritorio..." -ForegroundColor Yellow
try {
    $WshShell = New-Object -ComObject WScript.Shell
    $DesktopPath = [System.Environment]::GetFolderPath('Desktop')
    $Shortcut = $WshShell.CreateShortcut("$DesktopPath\Generador de Prospectos de Marketing.lnk")
    
    $ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { $PWD.ProviderPath }
    $Shortcut.TargetPath = "$ScriptDir\start_dashboard.bat"
    $Shortcut.WorkingDirectory = "$ScriptDir"
    $Shortcut.Description = "Panel de Control del Generador de Prospectos de Marketing"
    $Shortcut.IconLocation = "%SystemRoot%\System32\imageres.dll, 262"
    $Shortcut.Save()
    Write-Host "✅ Acceso directo creado en el Escritorio: Generador de Prospectos de Marketing.lnk" -ForegroundColor Green
} catch {
    Write-Host "⚠️ No se pudo crear el acceso directo en el Escritorio: $_" -ForegroundColor Yellow
}

Write-Host "----------------------------------------------------------" -ForegroundColor Cyan
Write-Host "🎉 ¡Instalación completada con éxito!" -ForegroundColor Green
Write-Host "Ahora puede ejecutar 'start_dashboard.bat' o usar el acceso directo en el Escritorio para abrir la interfaz." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
