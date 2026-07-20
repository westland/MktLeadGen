---
title: Marketing Leads Generator
emoji: 🚀
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# Generador de Prospectos de Marketing (MktLeadGen)

Esta aplicación es una herramienta generalizada y basada en agentes para la investigación de mercado y la generación de prospectos. Escanea plataformas (Reddit, Discord, Hacker News, reseñas de Amazon y discusiones de GitHub) para encontrar clientes potenciales que experimenten puntos de dolor específicos, los califica según los criterios definidos por el usuario y los recopila en un centro de control Streamlit. Redacta de forma dinámica borradores de mensajes de contacto por correo electrónico que coincidan con sus objetivos de campaña, discurso de ventas y reglas de escritura personalizadas.

## Pila Tecnológica
- **Framework**: CrewAI (generación de borradores y búsqueda con agentes)
- **UI**: Streamlit
- **Motores de Escaneo**: API de Reddit (PRAW), API de Discord (discord.py), API de Hacker News (Búsqueda Algolia), API de Búsqueda de GitHub, extractor de reseñas de productos de Amazon.
- **LLM**: Gemini (prioridad por defecto), Grok (xAI) o OpenAI.

---

## ⚙️ Instalación Local Paso a Paso (Windows 11)

1. **Extraer la Carpeta del Proyecto**:
   Extraiga los archivos en la ruta de su unidad local preferida (ej. `C:\Users\westl\MktLeadGen`).

2. **Ejecutar el Instalador**:
   Abra **PowerShell** dentro de la carpeta y ejecute:
   ```powershell
   .\install.ps1
   ```
   *Esto compila automáticamente su entorno virtual de Python local (`.venv`), instala todos los requisitos, crea plantillas de configuración, genera scripts batch de inicio para Windows y crea un acceso directo de **Generador de Prospectos de Marketing** directamente en su Escritorio con un icono de cohete.*

3. **Configurar Secretos de Entorno**:
   Configure estos abriendo el archivo `.env` generado directamente, o iniciando el panel de control y haciendo clic en el botón **`⚙️ Ajustes de API`**:
   - `GEMINI_API_KEY`: Pegue su clave API de Gemini (ya precargada para su espacio de trabajo predeterminado).
   - `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET`: Coloque sus credenciales de script de desarrollador de Reddit.
   - `DISCORD_BOT_TOKEN`: Coloque su token del Bot de Discord.
   - `AMAZON_SCRAPER_API_KEY`: Ingrese una clave API de proxy opcional (ej. ScraperAPI) para omitir bloqueos de CAPTCHA de Amazon.
   - `GITHUB_TOKEN`: Ingrese un token de acceso personal (PAT) de GitHub opcional para buscar en discusiones/problemas.
   - `SMTP_EMAIL` / `SMTP_PASSWORD`: Configure su correo electrónico de remitente y contraseña de aplicación para habilitar el envío automático de correos de contacto.

---

## 🖥️ Ejecución y Acceso al Panel de Control

1. Haga doble clic en el archivo **`start_dashboard.bat`** en la carpeta raíz.
2. Activará el entorno virtual e iniciará Streamlit.
3. Su navegador predeterminado se abrirá automáticamente en el panel de control en:
   👉 **`http://localhost:8501`**

---

## 🤖 Dirigir Agentes para Generar Prospectos de Marketing

Una vez en el panel de control:
1. **Configurar Prompts de Campaña**: Haga clic en **`⚙️ Prompts de Contacto`** en el encabezado. Defina los **Objetivos de la Campaña**, describa las características clave de su producto/servicio en el **Discurso de Ventas**, establezca restricciones de redacción bajo **Reglas de Escritura** y proporcione una **Muestra de Correo** de referencia.
2. **Ejecutar Escaneo**: Haga clic en **`🔍 Ejecutar Escaneo de Agentes`** en la barra lateral. Los agentes buscarán en Reddit, Discord, Hacker News, Amazon y GitHub conversaciones que coincidan con sus consultas de palabras clave.
3. **Revisar Puntuación**: Utilice el deslizador **Puntuación Mínima** en la barra lateral para revisar prospectos calificados de alta relevancia.
4. **Outreach**: Vea el borrador personalizado redactado por el LLM (adaptado a sus problemas específicos y metas), cópielo y envíelo por mensaje directo en su plataforma nativa.
5. **Envío Automático de Correos**: Ingrese el correo de un prospecto bajo **Correo del Cliente** en su tarjeta detallada (o agréguelo al crear un prospecto manual). Haga clic en **`📧 Correo a Prospectos Top (Top 5%)`** en la barra lateral. El agente redactor compilará un correo personalizado utilizando su discurso de ventas y lo enlazará de manera automática usando sus configuraciones de SMTP.
