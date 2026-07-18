---
title: Marketing Leads Generator
emoji: 🚀
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# Marketing Leads Generator (MktLeadGen)

This application is a generalized, agentic market research and lead generation tool. It scours platforms (Reddit, Discord, Hacker News, Amazon reviews, and GitHub discussions) for prospective customers experiencing specific pain points, qualifies them based on user-defined criteria, and compiles them into a Streamlit control center. It dynamically drafts cold email outreach copy matching your objectives, sales pitch features, and custom writing guardrails.

## Tech Stack
- **Framework**: CrewAI (agentic research and outreach copy generation)
- **UI**: Streamlit
- **Scraper Engines**: Reddit API (PRAW), Discord API (discord.py), Hacker News API (Algolia Search), GitHub Search API, Amazon product reviews parser.
- **LLM**: Gemini (default priority), Grok (xAI), or OpenAI.

---

## ⚙️ Step-by-Step Local Installation (Windows 11)

1. **Extract Project Folder**:
   Extract the files to your preferred local drive path (e.g. `C:\Users\westl\MktLeadGen`).

2. **Run Installer**:
   Open PowerShell inside the folder and run:
   ```powershell
   .\install.ps1
   ```
   *This automatically builds your local Python virtual environment (`.venv`), installs all requirements, creates configuration templates, writes Windows batch shortcuts, and generates a double-clickable **Marketing Leads Generator** shortcut on your Desktop with an appropriate rocket icon.*

3. **Configure Environment Secrets**:
   Configure these by opening the generated `.env` file directly, or by launching the dashboard and clicking the **`⚙️ API Settings`** button:
   - `GEMINI_API_KEY`: Paste your Gemini API key (already pre-loaded for your default workspace).
   - `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET`: Put your Reddit Developer script credentials.
   - `DISCORD_BOT_TOKEN`: Put your Discord Bot token.
   - `AMAZON_SCRAPER_API_KEY`: Enter an optional proxy scraping key (e.g., ScraperAPI) to bypass Amazon CAPTCHA blocks.
   - `GITHUB_TOKEN`: Enter an optional GitHub PAT to query issues/discussions.
   - `SMTP_EMAIL` / `SMTP_PASSWORD`: Configure your sender email and App Password to enable automated email outreach.

---

## 🖥️ Running & Accessing the Dashboard

1. Double-click the **`start_dashboard.bat`** file in the root folder.
2. It will activate the virtual environment and start Streamlit.
3. Your default browser will open automatically to the control panel at:
   👉 **`http://localhost:8501`**

---

## 🤖 Directing Agents to Generate Marketing Leads

Once on the dashboard:
1. **Configure Campaign Prompts**: Click **`⚙️ Outreach Prompts`** in the header. Set your **Objectives**, define the core features of your product/service in the **Sales Pitch**, specify writing restrictions under **Guardrails**, and provide a reference **Sample Email**.
2. **Trigger Scan**: Click **`🔍 Run Agents Scan`** in the sidebar. The agents will search across Reddit, Discord, Hacker News, Amazon reviews, and GitHub for discussions matching your target keyword queries.
3. **Review Scoring**: Filter leads using the **Min Lead Score** slider to review qualified, high-intent prospective clients.
4. **Outreach**: View the custom outreach draft created by the LLM (personalized with their specific pain points and target outcome), copy it, and DM them.
5. **Automated Email Outreach**: Enter a prospective client's email under **Client Email** in their detailed view (or fill it in during manual lead creation). Click **`📧 Email Top Leads (Top 5%)`** in the sidebar. The copywriter agent will compile a custom email pitch using your sales pitch features and send it automatically using your configured SMTP settings.
