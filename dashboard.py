import os
import sys
import streamlit as st
import pandas as pd
from datetime import datetime

# Ensure project root is in path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from src.marketing_leads_generator.tools.lead_utils import load_existing_leads, save_leads
except ImportError:
    try:
        from tools.lead_utils import load_existing_leads, save_leads
    except ImportError:
        from src.marketing_leads_generator.tools.lead_utils import load_existing_leads, save_leads

def load_outreach_config() -> dict:
    config_path = os.path.join(PROJECT_ROOT, "outreach_config.json")
    default_config = {
        "objectives": "Encontrar usuarios con puntos de dolor específicos que coincidan con las palabras clave de búsqueda, identificar sus problemas y generar borradores de correos electrónicos de contacto personalizados y útiles que ofrezcan una solución gratuita orientada al valor.",
        "sales_pitch": "Nuestro producto/servicio de software está diseñado para resolver estas frustraciones exactas. Brindamos automatización altamente robusta, APIs REST estándar, integraciones multiplataforma y soporte técnico las 24 horas, los 7 días de la semana.",
        "guardrails": "Mantenga el mensaje natural y amigable. No parezca spam. Limite la longitud a 150 palabras. No use plantillas genéricas: haga referencia a su comentario exacto. Cumpla con CAN-SPAM.",
        "samples": [
            "Asunto: Solución para sus problemas con [Punto de Dolor]\n\nHola [Nombre],\n\nVi su publicación mencionando sus dificultades con [Punto de Dolor] en los foros.\n\nNuestro producto cuenta con una función integrada para automatizar esto exactamente, eliminando la necesidad de manejarlo manualmente. ¿Estaría abierto a una demostración rápida y gratuita de 15 minutos para ver cómo puede ahorrarle tiempo?\n\nSaludos cordiales,\nEquipo de Contacto"
        ]
    }
    if os.path.exists(config_path):
        try:
            import json
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default_config
    return default_config

def save_outreach_config(config: dict):
    config_path = os.path.join(PROJECT_ROOT, "outreach_config.json")
    import json
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def generate_email_with_llm(lead: dict) -> str:
    try:
        from src.marketing_leads_generator.crew import get_llm, HAS_CREW_LLM
        llm = get_llm()
    except Exception:
        llm = None
        HAS_CREW_LLM = False
        
    config = load_outreach_config()
    
    fallback_text = (
        f"Asunto: Solución para sus problemas con {lead.get('pain_points', 'sus sistemas')}\n\n"
        f"Hola {lead.get('username')},\n\n"
        f"Vi que está teniendo dificultades con {lead.get('pain_points', 'su sistema')}.\n\n"
        f"Ofrecemos una solución que resuelve esto exactamente. "
        f"¿Estaría abierto a una consulta rápida de 15 minutos para revisar cómo podemos ayudarle?\n\n"
        f"Saludos cordiales,\nEquipo de Outreach"
    )
    
    if not llm:
        return fallback_text
        
    prompt = (
        f"Eres un asistente profesional de contacto y marketing por correo electrónico.\n"
        f"Escribe un correo electrónico frío, personalizado y sumamente atractivo a un cliente potencial, redactado por completo en español.\n"
        f"Detalles sobre el prospecto:\n"
        f"- Nombre de usuario: {lead.get('username')}\n"
        f"- Resultado Objetivo / Meta: {lead.get('desired_rating', 'N/A')}\n"
        f"- Categoría / Tema: {lead.get('class', 'N/A')}\n"
        f"- Puntos de Dolor: {lead.get('pain_points', 'N/A')}\n\n"
        f"Debes adherirte estrictamente a las siguientes pautas y parámetros en español:\n"
        f"1. Objetivos del Correo:\n{config.get('objectives')}\n\n"
        f"2. Características/Funciones del Producto/Servicio (Sales Pitch):\n{config.get('sales_pitch')}\n\n"
        f"3. Restricciones y Reglas de Escritura (Guardrails):\n{config.get('guardrails')}\n\n"
        f"4. Estructura el correo siguiendo exactamente este formato (no incluyas explicaciones ni texto introductorio, empieza directamente con 'Asunto:'):\n"
        f"Asunto: <Línea de Asunto>\n\n"
        f"<Cuerpo del Correo - Línea 1>\n"
        f"<Cuerpo del Correo - Línea 2>\n..."
    )
    
    try:
        if HAS_CREW_LLM:
            if hasattr(llm, "call"):
                response = llm.call([{"role": "user", "content": prompt}])
                return response
            elif hasattr(llm, "invoke"):
                response = llm.invoke(prompt)
                if hasattr(response, "content"):
                    return response.content
                return str(response)
        else:
            response = llm.invoke(prompt)
            if hasattr(response, "content"):
                return response.content
            return str(response)
    except Exception as e:
        print(f"Error during LLM generate: {e}")
        return fallback_text

def load_env_keys() -> dict:
    env_path = os.path.join(PROJECT_ROOT, ".env")
    keys = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    parts = line.split("=", 1)
                    k = parts[0].strip()
                    v = parts[1].strip()
                    if v.startswith(('"', "'")) and v.endswith(('"', "'")):
                        v = v[1:-1]
                    keys[k] = v
    return keys

def save_env_keys(updated_keys: dict):
    env_path = os.path.join(PROJECT_ROOT, ".env")
    existing_lines = []
    
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            existing_lines = f.readlines()
            
    processed_keys = set()
    new_lines = []
    
    for line in existing_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in line:
            parts = line.split("=", 1)
            k = parts[0].strip()
            if k in updated_keys:
                new_lines.append(f"{k}={updated_keys[k]}\n")
                processed_keys.add(k)
                continue
        new_lines.append(line)
        
    for k, v in updated_keys.items():
        if k not in processed_keys:
            if new_lines and not new_lines[-1].endswith("\n"):
                new_lines[-1] = new_lines[-1] + "\n"
            new_lines.append(f"{k}={v}\n")
            
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

# Page configuration for a premium dashboard layout
st.set_page_config(
    page_title="Generador de Prospectos de Marketing",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom styling for a premium dark mode with neon accents
st.markdown("""
<style>
    /* Styling headers and custom premium look */
    .main-title {
        font-family: 'Outfit', 'Inter', sans-serif;
        background: linear-gradient(135deg, #a855f7 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    .lead-card {
        border-radius: 12px;
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .badge {
        display: inline-block;
        padding: 0.25em 0.6em;
        font-size: 75%;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.375rem;
        margin-right: 0.5rem;
    }
    .badge-reddit {
        background-color: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .badge-discord {
        background-color: rgba(99, 102, 241, 0.2);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    .badge-other {
        background-color: rgba(107, 114, 128, 0.2);
        color: #9ca3af;
        border: 1px solid rgba(107, 114, 128, 0.3);
    }
    .badge-score {
        background-color: rgba(234, 179, 8, 0.2);
        color: #facc15;
        border: 1px solid rgba(234, 179, 8, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for view mode
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "leads"

# Navigation at the top of the page
col_title, col_nav = st.columns([2, 1])
with col_title:
    st.markdown('<div class="main-title">🚀 Generador de Prospectos</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Búsqueda agresiva de prospectos en Reddit, Discord, Hacker News, Amazon y GitHub</div>', unsafe_allow_html=True)
with col_nav:
    st.write("") # Espaciador
    st.write("") # Espaciador
    if st.session_state.view_mode == "leads":
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("⚙️ Ajustes de API", use_container_width=True):
                st.session_state.view_mode = "settings"
                st.rerun()
        with col_btn2:
            if st.button("⚙️ Prompts de Contacto", use_container_width=True):
                st.session_state.view_mode = "prompts"
                st.rerun()
    else:
        if st.button("📋 Volver al Registro", use_container_width=True):
            st.session_state.view_mode = "leads"
            st.rerun()

# If view_mode is settings, render the settings page and stop
if st.session_state.view_mode == "settings":
    st.subheader("⚙️ Configurar Claves API y Variables de Entorno")
    st.markdown("Use este formulario para actualizar de forma segura las variables de entorno en su archivo `.env`. Los valores existentes están ocultos por seguridad.")
    
    current_env = load_env_keys()
    
    with st.form("env_config_form"):
        col_env1, col_env2 = st.columns(2)
        
        updated_env = {}
        has_updates = False
        
        with col_env1:
            st.markdown("#### 🤖 APIs de LLM y Escaneo")
            
            # Gemini Key
            has_gemini = "GEMINI_API_KEY" in current_env and current_env["GEMINI_API_KEY"]
            gemini_placeholder = "Configurado (Oculto) - Ingrese una nueva clave para anular" if has_gemini else "Ingrese la Clave API de Gemini"
            gemini_val = st.text_input("Clave API de Google Gemini", type="password", placeholder=gemini_placeholder)
            if gemini_val:
                updated_env["GEMINI_API_KEY"] = gemini_val
                has_updates = True
                
            # Reddit Client ID
            has_reddit_id = "REDDIT_CLIENT_ID" in current_env and current_env["REDDIT_CLIENT_ID"]
            reddit_id_placeholder = "Configurado (Oculto) - Ingrese un nuevo ID para anular" if has_reddit_id else "Ingrese el ID de Cliente de Reddit"
            reddit_id_val = st.text_input("ID de Cliente de Reddit", type="password", placeholder=reddit_id_placeholder)
            if reddit_id_val:
                updated_env["REDDIT_CLIENT_ID"] = reddit_id_val
                has_updates = True
                
            # Reddit Client Secret
            has_reddit_secret = "REDDIT_CLIENT_SECRET" in current_env and current_env["REDDIT_CLIENT_SECRET"]
            reddit_secret_placeholder = "Configurado (Oculto) - Ingrese un nuevo Secreto para anular" if has_reddit_secret else "Ingrese el Secreto de Cliente de Reddit"
            reddit_secret_val = st.text_input("Secreto de Cliente de Reddit", type="password", placeholder=reddit_secret_placeholder)
            if reddit_secret_val:
                updated_env["REDDIT_CLIENT_SECRET"] = reddit_secret_val
                has_updates = True
                
            # Reddit User Agent
            has_reddit_ua = "REDDIT_USER_AGENT" in current_env and current_env["REDDIT_USER_AGENT"]
            reddit_ua_placeholder = current_env.get("REDDIT_USER_AGENT", "MktLeadGen/1.0 (by /u/YourRedditUsername)")
            reddit_ua_val = st.text_input("Agente de Usuario de Reddit", value=reddit_ua_placeholder if not has_reddit_ua else "", placeholder="Ingrese el Agente de Usuario (o deje en blanco para mantener el configurado)")
            if reddit_ua_val:
                updated_env["REDDIT_USER_AGENT"] = reddit_ua_val
                has_updates = True
                
            # Discord Bot Token
            has_discord = "DISCORD_BOT_TOKEN" in current_env and current_env["DISCORD_BOT_TOKEN"]
            discord_placeholder = "Configurado (Oculto) - Ingrese un nuevo token para anular" if has_discord else "Ingrese el Token del Bot de Discord"
            discord_val = st.text_input("Token del Bot de Discord", type="password", placeholder=discord_placeholder)
            if discord_val:
                updated_env["DISCORD_BOT_TOKEN"] = discord_val
                has_updates = True
                
            # Amazon Scraper Key
            has_amazon = "AMAZON_SCRAPER_API_KEY" in current_env and current_env["AMAZON_SCRAPER_API_KEY"]
            amazon_placeholder = "Configurado (Oculto) - Ingrese una nueva clave para anular" if has_amazon else "Ingrese la Clave API de Amazon Scraper (Opcional)"
            amazon_val = st.text_input("Clave API de Amazon Scraper", type="password", placeholder=amazon_placeholder)
            if amazon_val:
                updated_env["AMAZON_SCRAPER_API_KEY"] = amazon_val
                has_updates = True
                
            # GitHub Token
            has_github = "GITHUB_TOKEN" in current_env and current_env["GITHUB_TOKEN"]
            github_placeholder = "Configurado (Oculto) - Ingrese un nuevo token para anular" if has_github else "Ingrese el Token de Acceso Personal de GitHub (Opcional)"
            github_val = st.text_input("Token de GitHub (Opcional)", type="password", placeholder=github_placeholder)
            if github_val:
                updated_env["GITHUB_TOKEN"] = github_val
                has_updates = True
                
        with col_env2:
            st.markdown("#### 📧 Configuración de Correo SMTP para Outreach")
            
            # SMTP Email
            has_smtp_email = "SMTP_EMAIL" in current_env and current_env["SMTP_EMAIL"]
            smtp_email_placeholder = current_env.get("SMTP_EMAIL", "your_smtp_email@gmail.com")
            smtp_email_val = st.text_input("Dirección de correo SMTP", value=smtp_email_placeholder if not has_smtp_email else "", placeholder="Ingrese el correo del remitente (o deje en blanco para mantener el configurado)")
            if smtp_email_val:
                updated_env["SMTP_EMAIL"] = smtp_email_val
                has_updates = True
                
            # SMTP Password
            has_smtp_pass = "SMTP_PASSWORD" in current_env and current_env["SMTP_PASSWORD"]
            smtp_pass_placeholder = "Configurado (Oculto) - Ingrese una nueva contraseña para anular" if has_smtp_pass else "Ingrese la Contraseña SMTP"
            smtp_pass_val = st.text_input("Contraseña SMTP / Contraseña de aplicación", type="password", placeholder=smtp_pass_placeholder)
            if smtp_pass_val:
                updated_env["SMTP_PASSWORD"] = smtp_pass_val
                has_updates = True
                
            # SMTP Server
            has_smtp_server = "SMTP_SERVER" in current_env and current_env["SMTP_SERVER"]
            smtp_server_placeholder = current_env.get("SMTP_SERVER", "smtp.gmail.com")
            smtp_server_val = st.text_input("Servidor SMTP", value=smtp_server_placeholder if not has_smtp_server else "", placeholder="Ingrese el servidor SMTP (o deje en blanco para mantener el configurado)")
            if smtp_server_val:
                updated_env["SMTP_SERVER"] = smtp_server_val
                has_updates = True
                
            # SMTP Port
            has_smtp_port = "SMTP_PORT" in current_env and current_env["SMTP_PORT"]
            smtp_port_placeholder = current_env.get("SMTP_PORT", "587")
            smtp_port_val = st.text_input("Puerto SMTP", value=smtp_port_placeholder if not has_smtp_port else "", placeholder="Ingrese el puerto SMTP (o deje en blanco para mantener el configurado)")
            if smtp_port_val:
                updated_env["SMTP_PORT"] = smtp_port_val
                has_updates = True

        submitted_env = st.form_submit_button("💾 Guardar Configuraciones de Entorno")
        if submitted_env:
            if has_updates:
                save_env_keys(updated_env)
                st.success("¡Configuraciones actualizadas con éxito en el archivo `.env`!")
                st.rerun()
            else:
                st.info("No se realizaron modificaciones para guardar.")
    
    st.stop()

# If view_mode is prompts, render the prompts page and stop
if st.session_state.view_mode == "prompts":
    st.subheader("⚙️ Configurar Objetivos de Outreach, Discurso de Ventas y Reglas")
    st.markdown("Personalice cómo genera el LLM los correos electrónicos fríos. Los objetivos dictan la meta, el discurso de ventas describe el producto y las reglas imponen restricciones.")
    
    config = load_outreach_config()
    
    with st.form("prompts_config_form"):
        objectives = st.text_area("1. Objetivos de la Campaña", value=config.get("objectives", ""), height=100, help="¿Cuál es la meta del envío de correos?")
        sales_pitch = st.text_area("2. Discurso de Ventas del Producto/Servicio (Características)", value=config.get("sales_pitch", ""), height=150, help="¿Qué características o servicios estamos ofreciendo?")
        guardrails = st.text_area("3. Reglas y Restricciones de Escritura", value=config.get("guardrails", ""), height=100, help="Pautas de estilo, restricciones o límites de longitud.")
        
        st.markdown("#### 📧 Correo Electrónico de Muestra de Referencia")
        sample_email = st.text_area("Salida de Correo de Muestra", value=config.get("samples", [""])[0] if config.get("samples") else "", height=200, help="Ejemplo de la estructura de correo deseada.")
        
        submitted_prompts = st.form_submit_button("💾 Guardar Configuración de Contacto")
        if submitted_prompts:
            new_config = {
                "objectives": objectives,
                "sales_pitch": sales_pitch,
                "guardrails": guardrails,
                "samples": [sample_email] if sample_email else []
            }
            save_outreach_config(new_config)
            st.success("¡Configuración de prompts de contacto actualizada con éxito!")
            st.session_state.view_mode = "leads"
            st.rerun()
            
    st.stop()

leads = load_existing_leads()

# ----------------- SIDEBAR FILTERS & STATS -----------------
st.sidebar.header("📊 Controles y Ajustes")

if leads:
    df_temp = pd.DataFrame(leads)
    total_leads = len(df_temp)
    contacted_count = df_temp.get("contacted", pd.Series([False]*total_leads)).sum()
    pending_count = total_leads - contacted_count
else:
    total_leads, contacted_count, pending_count = 0, 0, 0

st.sidebar.markdown(f"""
- **Total de prospectos recopilados**: `{total_leads}`
- **Outreach pendiente**: `{pending_count}`
- **Clientes contactados**: `{contacted_count}`
""")

st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Acciones de Agentes")

if st.sidebar.button("🔍 Ejecutar Escaneo de Agentes", help="Instruir a los agentes de CrewAI para buscar en Reddit, Discord, Hacker News, Amazon y GitHub"):
    with st.spinner("Los agentes de Gemini están buscando prospectos en las plataformas... esto puede tardar de 1 a 2 minutos."):
        try:
            # Import dynamically to avoid loading latency on startup
            from src.marketing_leads_generator.main import run as run_crew
            run_crew()
            st.sidebar.success("Scan complete! Leads list updated.")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Scan failed: {e}")

if st.sidebar.button("📧 Correo a Prospectos Top (Top 5%)", help="Enviar correos personalizados por el LLM al top 5% de prospectos por puntuación"):
    if not leads:
        st.sidebar.info("¡No hay prospectos disponibles para enviar correos. ¡Ejecute el escaneo primero!")
    else:
        with st.spinner("Generando y enviando correos electrónicos a los prospectos principales..."):
            try:
                from send_email import send_personalized_email
                
                # Sort leads by score descending
                sorted_leads = sorted(leads, key=lambda x: x.get("lead_score", 0), reverse=True)
                top_count = max(1, int(len(sorted_leads) * 0.05))
                top_leads = sorted_leads[:top_count]
                
                sent_count = 0
                skipped_leads = []
                
                for lead in top_leads:
                    to_email = lead.get("email")
                    if not to_email:
                        skipped_leads.append(lead.get("username"))
                        continue
                    
                    email_text = generate_email_with_llm(lead)
                    
                    subject = "Propuesta de Contacto"
                    body = email_text
                    if "Subject:" in email_text or "Asunto:" in email_text:
                        parts = email_text.split("\n\n", 1)
                        sub_line = parts[0]
                        subject = sub_line.replace("Subject:", "").replace("Asunto:", "").strip()
                        if len(parts) > 1:
                            body = parts[1]
                    
                    success = send_personalized_email(to_email, subject, body)
                    if success:
                        # Update lead in local leads list to contacted
                        target_user = lead.get("username")
                        target_url = lead.get("url") or lead.get("jump_url")
                        for main_lead in leads:
                            lead_url = main_lead.get("url") or main_lead.get("jump_url")
                            if main_lead.get("username") == target_user and lead_url == target_url:
                                main_lead["contacted"] = True
                                break
                        sent_count += 1
                
                save_leads(leads)
                
                if sent_count > 0:
                    st.sidebar.success(f"¡Se enviaron {sent_count} correo(s) con éxito!")
                if skipped_leads:
                    st.sidebar.warning(f"No se configuraron correos para los prospectos principales: {', '.join(skipped_leads)}")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Error en el proceso de correo electrónico: {e}")

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtros")

min_score = st.sidebar.slider("Puntuación Mínima", min_value=1, max_value=10, value=6)

platforms = ["Todos"]
if total_leads > 0 and "platform" in df_temp.columns:
    platforms += sorted(df_temp["platform"].dropna().unique().tolist())
selected_platform = st.sidebar.selectbox("Filtrar por Plataforma", platforms)

contact_status = st.sidebar.radio(
    "Estado de Contacto",
    ["Solo Pendientes", "Solo Contactados", "Todos los Prospectos"]
)

st.sidebar.markdown("---")

# ----------------- ADD MANUAL LEAD FORM -----------------
with st.sidebar.expander("➕ Agregar Prospecto Manual", expanded=False):
    with st.form("manual_lead_form", clear_on_submit=True):
        username = st.text_input("Usuario / Autor *")
        platform = st.selectbox("Plataforma", ["Reddit", "Discord", "HackerNews", "Amazon", "GitHub", "Other"])
        url = st.text_input("URL del Mensaje / Publicación")
        email = st.text_input("Dirección de Correo (opcional)")
        current_rating = st.text_input("Contexto Actual (ej. v1.0 o calificación baja)")
        desired_rating = st.text_input("Resultado Objetivo / Meta")
        class_spec = st.text_input("Categoría / Tema (ej. Ret Paladin o SaaS)")
        pain_points = st.text_area("Puntos de Dolor")
        personalized_message = st.text_area("Borrador de Contacto (opcional)")
        score = st.slider("Puntuación de Calidad", 1, 10, 7)
        
        submitted = st.form_submit_button("Agregar Prospecto")
        if submitted:
            if not username:
                st.error("¡El nombre de usuario es obligatorio!")
            else:
                new_lead = {
                    "timestamp": datetime.now().isoformat(),
                    "username": username,
                    "platform": platform,
                    "url": url,
                    "email": email,
                    "current_rating": current_rating,
                    "desired_rating": desired_rating,
                    "class": class_spec,
                    "pain_points": pain_points,
                    "lead_score": score,
                    "contacted": False
                }
                leads.append(new_lead)
                save_leads(leads)
                st.success("¡Prospecto agregado con éxito!")
                st.rerun()

# ----------------- MAIN DISPLAY AREA -----------------
if not leads:
    st.info("No se encontraron prospectos en `marketing_leads.json`. ¡Ejecute el escaneo de los agentes para recopilarlos, o agregue uno manualmente en la barra lateral!")
else:
    df = pd.DataFrame(leads)
    
    # Ensure contacted column exists
    if "contacted" not in df.columns:
        df["contacted"] = False
        
    # Apply filters
    filtered_df = df[df["lead_score"] >= min_score]
    
    if selected_platform != "Todos":
        filtered_df = filtered_df[filtered_df["platform"] == selected_platform]
        
    if contact_status == "Solo Pendientes":
        filtered_df = filtered_df[filtered_df["contacted"] == False]
    elif contact_status == "Solo Contactados":
        filtered_df = filtered_df[filtered_df["contacted"] == True]

    if filtered_df.empty:
        st.warning("Ningún prospecto coincide con los criterios de filtrado seleccionados.")
    else:
        # Display Overview Table
        st.subheader("📋 Resumen del Registro de Prospectos")
        display_df = filtered_df.copy()
        
        # Clean columns for display table
        cols_to_show = ["timestamp", "username", "platform", "lead_score", "current_rating", "desired_rating", "class", "contacted"]
        cols_available = [c for c in cols_to_show if c in display_df.columns]
        
        st.dataframe(
            display_df[cols_available].sort_values(by="lead_score", ascending=False),
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("🔍 Revisión Detallada de Contacto")

        for idx, row in filtered_df.iterrows():
            platform_str = str(row.get('platform', 'Other'))
            badge_class = f"badge-{platform_str.lower()}"
            
            # Create a card view for each lead
            with st.container():
                st.markdown(f"""
                <div class="lead-card">
                    <h4>
                        <span class="badge {badge_class}">{platform_str}</span>
                        <span class="badge badge-score">Puntaje: {row.get('lead_score', 'N/A')}/10</span>
                        Usuario: {row.get('username')}
                    </h4>
                    <p style="font-size:0.9rem; color:#64748b;">Recopilado: {row.get('timestamp', 'Desconocido')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_left, col_right = st.columns([1, 2])
                
                with col_left:
                    st.write(f"**Contexto Actual:** `{row.get('current_rating') or 'N/A'}`")
                    st.write(f"**Resultado / Meta:** `{row.get('desired_rating') or 'N/A'}`")
                    st.write(f"**Categoría / Tema:** `{row.get('class') or 'N/A'}`")
                    st.write(f"**URL de Destino:** [Abrir Enlace]({row.get('url') or row.get('jump_url') or '#'})")
                    st.write(f"**Puntos de Dolor:** {row.get('pain_points') or 'Ninguno mencionado'}")
                    
                    # Email editing field
                    email_val = st.text_input("📧 Correo del Cliente", value=row.get("email", ""), key=f"email_{idx}")
                    if email_val != row.get("email", ""):
                        target_user = row.get("username")
                        target_url = row.get("url") or row.get("jump_url")
                        for lead in leads:
                            lead_url = lead.get("url") or lead.get("jump_url")
                            if lead.get("username") == target_user and lead_url == target_url:
                                lead["email"] = email_val
                                break
                        save_leads(leads)
                        st.success(f"¡Correo actualizado para {target_user}!")
                        st.rerun()
                    
                    # Persist contacted state back to database
                    is_contacted = bool(row.get("contacted", False))
                    button_label = "Marcar como Pendiente" if is_contacted else "Marcar como Contactado"
                    
                    if st.button(button_label, key=f"btn_contact_{idx}"):
                        # Locate lead in main list and flip contacted state
                        target_user = row.get("username")
                        target_url = row.get("url") or row.get("jump_url")
                        
                        for lead in leads:
                            lead_url = lead.get("url") or lead.get("jump_url")
                            if lead.get("username") == target_user and lead_url == target_url:
                                lead["contacted"] = not is_contacted
                                break
                        save_leads(leads)
                        st.success(f"¡Estado de contacto actualizado para {target_user}!")
                        st.rerun()

                with col_right:
                    message_draft = row.get('personalized_message') or ""
                    st.text_area("✍️ Borrador de Mensaje Personalizado", value=message_draft, height=140, key=f"txt_{idx}")
                    st.caption("Revise, edite y copie el borrador de arriba para contactar al prospecto a través de su plataforma nativa.")
                st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'/>", unsafe_allow_html=True)
