# Generador de Prospectos de Marketing - Guía del Usuario

Esta guía detalla las instrucciones de instalación, configuración, ejecución y sincronización del repositorio Git de la aplicación Generador de Prospectos de Marketing (`MktLeadGen`) en Windows 11.

---

## 🛠️ Requisitos Previos

1. **Python 3.10+**: Asegúrese de que Python esté instalado y agregado a su PATH de Windows.
2. **Git**: Instalado y autenticado con su cuenta de GitHub.

---

## 🚀 Instalación en Windows 11

Proporcionamos un script de instalación automatizado `install.ps1` que configura un entorno virtual de Python, instala las dependencias, verifica los archivos y crea archivos por lotes (batch) de inicio rápido.

### Pasos:
1. Abra **PowerShell** (o Terminal) y navegue al directorio del proyecto:
   ```powershell
   cd C:\Users\westl\MktLeadGen
   ```
2. Habilite la ejecución de scripts para este proceso (si aparece el aviso):
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```
3. Ejecute el instalador:
   ```powershell
   .\install.ps1
   ```
   *Esto configurará el entorno, instalará los requisitos, escribirá los accesos directos de inicio rápido y colocará un acceso directo personalizado de **Generador de Prospectos de Marketing** con un icono de cohete directamente en su Escritorio.*

Esto generará tres scripts de inicio en el directorio raíz:
- `start_dashboard.bat` — Inicia la interfaz de Streamlit.
- `run_scraper.bat` — Inicia un escaneo único por consola.
- `start_scheduler.bat` — Ejecuta un programador en segundo plano que realiza comprobaciones diarias a las 09:00.

---

## ⚙️ Configuración (`.env`)

Configure sus claves en el archivo `.env` en la carpeta raíz o a través de la interfaz del panel de control:

### 1. Clave API de LLM (Cerebros de la Tripulación)
Su clave API de Gemini activa ya está configurada:
```env
GEMINI_API_KEY=su_clave_api_aquí
```

### 2. Configuración de la API de Reddit
Para escanear Reddit:
1. Vaya a [Preferencias de Aplicaciones de Reddit](https://www.reddit.com/prefs/apps).
2. Haga clic en **Create another app...** (seleccione el tipo **script**).
3. Establezca el Nombre como `MktLeadGen` y el URI de redireccionamiento a `http://localhost:8080`.
4. Copie el ID del cliente (debajo del nombre de la aplicación) y el Secreto.
5. Ingrese en el `.env`:
   ```env
   REDDIT_CLIENT_ID=su_id
   REDDIT_CLIENT_SECRET=su_secreto
   ```

### 3. Configuración del Bot de Discord
Para escanear el historial de mensajes de Discord:
1. Vaya al [Portal de Desarrolladores de Discord](https://discord.com/developers/applications) y cree una aplicación.
2. En la pestaña **Bot**, genere un token y habilite el **Message Content Intent**.
3. Invite al bot a sus servidores objetivo.
4. Ingrese en el `.env`:
   ```env
   DISCORD_BOT_TOKEN=su_token
   ```

### 4. Scraper de Reseñas de Amazon (Opcional)
Para consultar las reseñas de productos de Amazon sin bloqueos:
```env
AMAZON_SCRAPER_API_KEY=su_clave_de_proxy
```

### 5. Token de Búsqueda de GitHub (Opcional)
Para consultar problemas/discusiones de GitHub:
```env
GITHUB_TOKEN=su_token_de_acceso_personal
```

---

## 💻 Ejecución del Sistema

- **Panel de Control de Streamlit**: Haga doble clic en `start_dashboard.bat` (o ejecute `streamlit run dashboard.py`).
  - Visualice la lista de prospectos recopilados.
  - Filtre por Puntuación, Plataforma y Estado de Contacto.
  - Review y copie los borradores de contacto personalizados.
  - Establezca los objetivos de contacto, el discurso de ventas del producto, las reglas de escritura y las plantillas en la pantalla **`⚙️ Prompts de Contacto`**.
  - Envíe **correos electrónicos de contacto frío personalizados por Gemini** al top 5% de prospectos con mayor puntaje haciendo clic en **`📧 Correo a Prospectos Top (Top 5%)`** en la barra lateral.
  - Marque los prospectos como Contactados (se guarda directamente en `marketing_leads.json`).
  
- **Escaneo de Agentes**: Haga doble clic en `run_scraper.bat` (o ejecute `python -m src.marketing_leads_generator.main`).
  - Ejecuta los agentes de CrewAI para buscar en la web, calificar prospectos y generar borradores personalizados.

- **Programador en Segundo Plano**: Haga doble clic en `start_scheduler.bat` (o ejecute `python scheduler.py`).
  - Mantiene un programador ligero abierto en la terminal, ejecutando el escaneo automáticamente todas las mañanas a las 09:00.

---

## 📂 Subir a GitHub (Repositorio `MktLeadGen`)

### Para inicializar y subir:
1. Asegúrese de haber creado el repositorio vacío `MktLeadGen` en su cuenta de GitHub (`github.com/westland`).
2. Haga correr el script `setup_git.ps1` en PowerShell o ejecute los siguientes comandos:
   ```powershell
   git init
   git branch -M main
   git remote add origin https://github.com/westland/MktLeadGen.git
   git add .
   git commit -m "Initial commit of Marketing Leads Generator"
   git push -u origin main
   ```
