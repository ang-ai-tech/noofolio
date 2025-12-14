# 🧠 Noofolio - The AI-Native Anti-Portfolio

> **Your work, not your role.**
> L'anti-portfolio che mappa il tuo pensiero, non le tue competenze.

**Noofolio** = **No-Portfolio** (contro il vecchio formato) + **Noosfera** (sfera del pensiero)

Mentre l'AI colonizza la produzione, Noofolio cattura ciò che ti rende insostituibile: il tuo modo di pensare, decidere, fallire e imparare.

---

## 🎯 Cos'è Noofolio?

Noofolio non è un curriculum migliorato. È un **sistema di cattura dell'impronta cognitiva professionale** — il modo in cui pensi, decidi, fallisce, impari e ti differenzi.

### L'Anti-Curriculum

Un CV ti chiede: *"Cosa hai fatto?"*
Noofolio ti chiede: *"Quando hai deciso **contro** i dati?"*

Questa inversione rivela:
- **Decision Log**: Le biforcazioni dove hai scelto A invece di B, e perché
- **Failure Museum**: I fallimenti veri, non "punti deboli camuffati da punti di forza"
- **Human Delta**: Cosa fai tu che l'AI non può replicare
- **Anti-Skills**: Cosa rifiuti di fare (e perché è un punto di forza)
- **Human API**: Il manuale per lavorare con te

---

## ✨ Features

### Core Features Implementate
- ✅ **Onboarding intelligente** - Scegli Express (5 min) o Deep Mode (30 min)
- ✅ **Upload CV** - Supporta PDF, Word, link condivisi o testo diretto
- ✅ **Multi-link dinamici** - Aggiungi LinkedIn, GitHub, Behance, ecc.
- ✅ **Progress bar live** - Vedi in real-time la generazione del portfolio con SSE
- ✅ **7 Agenti AI specializzati** - Pipeline multi-agente per analisi profonda
- ✅ **72 Archetipi** - Sistema 3D: Ruolo × Personalità × AI-Relation
- ✅ **NooMe Chat Widget** - Clone conversazionale AI 24/7 (come Intercom)
- ✅ **Mind Sculptor** - Genera domande random per approfondire il profilo
- ✅ **MindMirror** - Sistema di correzione per migliorare l'affidabilità di NooMe
- ✅ **Punteggio affidabilità** - Sistema a stelle (0-5⭐) basato su completezza
- ✅ **Export multi-formato** - Download HTML, JSON o PDF
- ✅ **Stili adattivi** - Il design cambia in base all'archetipo rilevato
- ✅ **Demo preconfigurata** - API key incluse, pronta all'uso per i giudici

### Futuri Sviluppi (Coming Soon)
- 📧 **Email notifications** - Avviso quando qualcuno chatta con il tuo NooMe
- 📊 **Analytics dashboard** - Visite, domande frequenti, sezioni più lette
- 🔗 **Social sharing** - Condividi su LinkedIn, genera QR code
- 🎯 **Job Match AI** - Upload JD e ottieni fit score automatico
- 🌐 **Multi-lingua** - EN, ES, FR con NooMe poliglotta
- 🎨 **Theme customizer** - Personalizza colori, font, layout

---

## 🏗️ Architettura Multi-Agente

Noofolio usa **7 agenti AI specializzati** che lavorano in pipeline:

### 1. Generazione Iniziale (5 Agenti)

```
Input Utente → CV + Risposte Form
         ↓
┌─────────────────────────────────────┐
│ 1. Archetype Detector               │
│    Identifica pattern comportamentali│
│    → 72 archetipi possibili         │
│    (Ruolo × Modalità × AI-Relation) │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ 2. Pattern Extractor                │
│    Estrae ricorrenze decisionali    │
│    e metodologie personali          │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ 3. Decision Archaeologist           │
│    Analizza momenti di biforcazione │
│    e scelte contro corrente         │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ 4. Signature Detector               │
│    Identifica la "firma" unica      │
│    nel modo di lavorare             │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ 5. Narrative Composer               │
│    Compone tutto in una storia      │
│    coerente e unica                 │
└─────────────────────────────────────┘
         ↓
  Portfolio HTML + JSON + NooMe Ready
```

### 2. Evoluzione Continua (2 Agenti)

```
┌──────────────────────┐      ┌────────────────────────┐
│ 6. NooMe             │      │ 7. Mind Sculptor       │
│ (Clone Conv.)        │      │ (Question Generator)   │
└──────────────────────┘      └────────────────────────┘
         ↓                             ↓
  Risponde a Visitatori      Genera domande random
  basandosi su Portfolio     per approfondire profilo
         ↓                             ↓
  Feedback Visitatore        Utente risponde/skippa
         ↓                             ↓
  Correzione in              Risposta arricchisce
  MindMirror (owner)         Portfolio e NooMe
         ↓                             ↓
  Aggiornamento NooMe        Loop continuo
  (Affidabilità ↑)           (Evoluzione profilo)
```

**Perché multi-agente?**
- **Specializzazione**: Ogni agente è esperto nel suo dominio
- **Qualità**: Prompt ottimizzati per task specifici
- **Modularità**: Debug e miglioramento incrementale
- **Scalabilità**: Parallelizzazione potenziale

---

## 🚀 Installazione e Avvio

### Prerequisiti

- Python 3.9+
- pip
- Git

### 1. Clone del Repository

```bash
git clone https://github.com/your-username/noofolio.git
cd noofolio
```

### 2. Creazione Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installazione Dipendenze

```bash
pip install -r requirements.txt
```

#### Nota: WeasyPrint (per PDF Export)

WeasyPrint richiede librerie di sistema:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
```

**macOS (con Homebrew):**
```bash
brew install pango gdk-pixbuf libffi
```

**Windows:**
Scarica GTK+ da https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases

### 4. Configurazione API Keys

Il progetto è **già configurato con API key funzionanti** per la demo (budget €5 offerto da Angelo).

Se vuoi usare le tue chiavi o il credito si esaurisce:

1. **Copia il file .env:**
```bash
cp .env.example .env
```

2. **Modifica .env con le tue chiavi:**
```env
# LLM API Keys
GOOGLE_API_KEY=your-google-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
OPENAI_API_KEY=your-openai-api-key  # opzionale

# Server Configuration
PORT=8000
```

#### Dove Ottenere le API Keys

- **Anthropic Claude** (Raccomandato): https://console.anthropic.com/ (5$ credito gratuito)
- **Google Gemini** (Gratuito): https://makersuite.google.com/app/apikey
- **OpenAI GPT-4**: https://platform.openai.com/api-keys

#### Configurazione Frontend vs Backend

**Le API key vanno SOLO nel backend** (file `.env`):
- ✅ Backend (.env): Sicuro, chiavi nascoste
- ❌ Frontend (JavaScript): PERICOLOSO, chiavi esposte pubblicamente

Il frontend usa **sessionStorage** solo per override temporaneo in demo mode, ma le chiavi sono inviate al backend e non salvate in produzione.

### 5. Configurazione Modello LLM

Modifica `config.yaml` per scegliere il provider:

```yaml
llm:
  provider: "anthropic"  # anthropic, google, openai
  models:
    gemini: "gemini-2.0-flash"
    anthropic: "claude-sonnet-4-5-20250929"  # Usato di default
    openai: "gpt-4-turbo-preview"
  temperature: 0.7
```

Il modello **claude-sonnet-4-5-20250929** è configurato di default (più recente e performante).

### 6. Avvio dell'Applicazione

#### Modo Automatico (Auto-open browser)

```bash
python main.py
```

Il browser si aprirà automaticamente su `http://localhost:8000`

#### Modo Manuale (Uvicorn)

**Development mode (auto-reload):**
```bash
uvicorn main:app --reload
```

**Production mode:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Apri manualmente: **http://localhost:8000**

### 7. Configurazione Porta Personalizzata

Modifica `.env`:
```env
PORT=3000  # o qualsiasi altra porta
```

Poi avvia con:
```bash
python main.py
```

---

## 📁 Struttura del Progetto

```
noofolio/
├── main.py                      # FastAPI app principale
├── requirements.txt             # Dipendenze Python
├── .env                         # API keys (NON committare!)
├── config.yaml                  # Configurazione LLM e archetipi
│
├── agents/                      # 🤖 7 Agenti AI Specializzati
│   ├── __init__.py
│   ├── archetype_detector.py   # 1. Rileva archetipo (72 possibili)
│   ├── pattern_extractor.py    # 2. Estrae pattern decisionali
│   ├── decision_archaeologist.py # 3. Analizza decision log
│   ├── signature_detector.py   # 4. Identifica firma unica
│   ├── narrative_composer.py   # 5. Compone narrativa
│   ├── portfolio_generator.py  # 6. Genera HTML adattivo
│   └── noome_chat.py           # 7. Clone conversazionale
│
├── utils/                       # Utilità
│   ├── __init__.py
│   └── file_processor.py       # PDF/Word/Image processing
│
├── templates/                   # 🎨 Template Jinja2
│   ├── base.html               # Layout base
│   ├── index.html              # Landing page
│   ├── onboarding.html         # Onboarding Express/Deep
│   ├── create.html             # Form Deep Mode (10 steps)
│   ├── express.html            # Form Express (5 domande)
│   ├── explore.html            # Browse portfolios
│   ├── view.html               # Portfolio view + NooMe widget
│   ├── result.html             # Generazione completata
│   ├── corrections.html        # MindMirror (correzioni NooMe)
│   ├── dashboard.html          # Dashboard proprietario
│   ├── demo_settings.html      # Impostazioni demo
│   └── select_profile.html     # Switch utente
│
├── static/                      # 🎨 Assets statici
│   ├── css/
│   │   └── style.css           # Stylesheet principale
│   ├── js/
│   │   └── htmx.min.js         # HTMX (CDN fallback)
│   └── assets/
│       ├── logo_white.png      # Logo hero
│       └── nav_logo_white.png  # Logo navbar
│
├── data/                        # 💾 Dati generati
│   ├── profiles/               # Portfolio JSON
│   ├── uploads/                # CV e immagini uploadate
│   ├── conversations/          # Cronologia chat NooMe
│   └── corrections/            # Correzioni MindMirror
│
└── docs/                        # 📚 Documentazione
    └── FRAMEWORK.md            # Architettura e filosofia
```

---

## 🎯 API Endpoints

### Pagine Principali

| Route | Method | Descrizione |
|-------|--------|-------------|
| `/` | GET | Landing page con Hero e Value Proposition |
| `/onboarding` | GET | Scelta Express (5 min) o Deep Mode (30 min) |
| `/explore` | GET | Browse portfolios pubblici |
| `/demo-settings` | GET | Configurazione API keys (demo) |

### Creazione Portfolio

| Route | Method | Descrizione |
|-------|--------|-------------|
| `/create` | GET | Form Deep Mode (10 step con sidebar) |
| `/create/express` | GET | Form Express (5 domande rapide) |
| `/create/step/{step}` | POST | Submit step form (con upload CV/immagini) |
| `/api/generate` | POST | Genera portfolio (legacy, sync) |
| `/api/generate-stream` | GET | Genera portfolio con live progress (SSE) |
| `/api/generate-express` | POST | Genera da Express mode |

### Visualizzazione e Export

| Route | Method | Descrizione |
|-------|--------|-------------|
| `/result/{profile_id}` | GET | Risultato generazione con preview |
| `/view/{profile_id}` | GET | Portfolio pubblico + NooMe chat widget |
| `/dashboard/{profile_id}` | GET | Dashboard proprietario |
| `/export/pdf/{profile_id}` | GET | Export PDF (WeasyPrint) |
| `/download/html/{profile_id}` | GET | Download HTML standalone |
| `/download/json/{profile_id}` | GET | Download dati JSON |

### NooMe & Mind Sculptor

| Route | Method | Descrizione |
|-------|--------|-------------|
| `/api/chat/{profile_id}` | POST | Chat con NooMe (clone AI) |
| `/mind-sculptor/{profile_id}` | GET | Domande random per approfondire |
| `/api/save-sculptor-response/{profile_id}` | POST | Salva risposta Mind Sculptor |
| `/corrections/{profile_id}` | GET | MindMirror: correggi NooMe |
| `/api/save-correction/{profile_id}` | POST | Salva correzione NooMe |

### Gestione Profili

| Route | Method | Descrizione |
|-------|--------|-------------|
| `/select-profile` | GET | Switch tra utenti demo |
| `/api/set-profile` | POST | Imposta utente corrente (sessionStorage) |

---

## 🔧 Caratteristiche Tecniche

### 1. Upload e Processing Files

**CV supportati:**
- PDF (`.pdf`)
- Microsoft Word (`.doc`, `.docx`)
- Link condivisi (Google Drive, Dropbox)
- Testo incollato direttamente

**Esempio uso:**
```python
from utils.file_processor import FileProcessor

# Extract text from CV
cv_text = FileProcessor.process_cv_file(file_content, "cv.pdf")

# Process images
images = FileProcessor.process_multiple_images(files, max_images=10)
```

**Backend (main.py):**
```python
@app.post("/create/step/1")
async def submit_step_1(
    cv_file: Optional[UploadFile] = File(None),
    cv_link: Optional[str] = Form(None)
):
    if cv_file:
        content = await cv_file.read()
        cv_text = FileProcessor.process_cv_file(content, cv_file.filename)
    elif cv_link:
        cv_text = FileProcessor.process_cv_link(cv_link)
```

### 2. Progress Bar Live con SSE (Server-Sent Events)

**Backend (main.py):**
```python
@app.get("/api/generate-stream")
async def generate_stream(request: Request):
    async def event_generator():
        yield f"data: {json.dumps({'status': 'Rilevamento archetipo...', 'percent': 10})}\n\n"
        # ... 7 agenti
        yield f"data: {json.dumps({'status': 'Completato!', 'percent': 100})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

**Frontend (JavaScript):**
```javascript
const eventSource = new EventSource('/api/generate-stream');
eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    progressBar.style.width = data.percent + '%';
    statusText.textContent = data.status;
};
```

### 3. Export PDF con WeasyPrint

**Backend (main.py):**
```python
from weasyprint import HTML

@app.get("/export/pdf/{profile_id}")
async def export_pdf(profile_id: str):
    html_content = load_portfolio_html(profile_id)
    pdf_bytes = HTML(string=html_content).write_pdf()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={profile_id}.pdf"}
    )
```

### 4. Sistema Affidabilità NooMe

**Formula:**
```python
def calculate_reliability(profile_data):
    questions_answered = len(profile_data.get('mind_sculptor_responses', []))
    corrections_made = len(profile_data.get('corrections', []))

    # Express mode: max 2⭐ (5 domande)
    # Deep mode: max 5⭐ (10 domande + correzioni)
    score = (questions_answered / 5 * 2) + (corrections_made / 5 * 0.5)
    return min(5, round(score, 1))
```

**Display:**
```python
stars = "⭐" * int(score) + "☆" * (5 - int(score))
```

### 5. NooMe Chat Widget (Floating)

**Stile Intercom-like:**
```css
.chat-widget {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 400px;
    height: 600px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    z-index: 9999;
}
```

**Backend API:**
```python
@app.post("/api/chat/{profile_id}")
async def chat_with_noome(profile_id: str, message: str = Form(...)):
    profile = load_profile(profile_id)
    noome = NooMeChat(profile)
    response = noome.chat(message)

    # Save conversation
    save_conversation(profile_id, message, response)

    return {"response": response}
```

### 6. Archetipi Dinamici (72 Combinazioni)

**Sistema 3D:**
```yaml
# config.yaml
archetypes:
  roles: [builder, designer, strategist, communicator, operator, guide]  # 6
  personalities: [chaos, order, minimal, rebel, warm, data]              # 6
  ai_styles: [cyborg, hybrid, artisan]                                    # 3

# Total: 6 × 6 × 3 = 216 combinazioni teoriche
# Usate: 72 (subset meaningful)
```

**Detection:**
```python
# agents/archetype_detector.py
archetype = {
    "role": "builder",           # Dai pattern di lavoro
    "personality": "chaos",      # Dallo stile comunicativo
    "ai_style": "pragmatist",    # Dal rapporto con AI
    "combo": "Builder × Chaos × Pragmatist",
    "archetype_name": "The Hacker"
}
```

**Adaptive Styling:**
```python
# agents/portfolio_generator.py
PERSONALITY_CONFIGS = {
    "chaos": {
        "bg_gradient": "linear-gradient(135deg, #1a1a2e, #0f3460)",
        "accent": "#ff6b6b",
        "font_main": "'JetBrains Mono', monospace",
        "card_style": "transform: rotate(-0.5deg);",
        "card_hover": "transform: rotate(0deg) translateY(-4px);",
        "badge_style": "animation: pulse 2s infinite;"
    },
    # ... 5 other personalities
}
```

---

## 🎨 Personalizzazione

### Modificare Stili CSS

Edita `static/css/style.css` - nessun Python necessario.

**Esempio: Cambiare colori primari**
```css
:root {
    --primary: #6366f1;      /* Indigo */
    --primary-light: #818cf8;
    --accent-green: #22c55e;
    --accent-red: #ef4444;
}
```

### Aggiungere una Nuova Route

```python
# main.py
@app.get("/nuova-pagina")
async def nuova_pagina(request: Request):
    return templates.TemplateResponse("nuova_pagina.html", {
        "request": request,
        "title": "Nuova Pagina"
    })
```

### Modificare Template Jinja2

Edita file in `templates/`:

```html
<!-- templates/nuova_pagina.html -->
{% extends "base.html" %}

{% block content %}
<div class="section">
    <h1>{{ title }}</h1>
    <p>Contenuto qui...</p>
</div>
{% endblock %}
```

### Aggiungere un Nuovo Agente

1. **Crea file in `agents/`:**
```python
# agents/nuovo_agente.py
class NuovoAgente:
    def run(self, data):
        # Logica agente
        return result
```

2. **Importa in `main.py`:**
```python
from agents.nuovo_agente import NuovoAgente

# Usa nella pipeline
nuovo = NuovoAgente()
result = nuovo.run(user_data)
```

---

## 🐛 Troubleshooting

### Porta già in uso

**Linux/macOS:**
```bash
# Trova processo
lsof -ti:8000

# Killa processo
lsof -ti:8000 | xargs kill -9
```

**Windows:**
```cmd
# Trova processo
netstat -ano | findstr :8000

# Killa processo (usa PID dalla colonna finale)
taskkill /PID <PID> /F
```

### Templates non trovati

```bash
# Verifica struttura
ls templates/
# Deve mostrare: base.html, index.html, create.html, ecc.

# Controlla percorso in main.py
templates = Jinja2Templates(directory="templates")  # Corretto
```

### File statici 404

```bash
# Verifica CSS esiste
ls static/css/style.css

# Controlla mount in main.py
app.mount("/static", StaticFiles(directory="static"), name="static")
```

### WeasyPrint non funziona

**Error: "Cairo library not found"**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install libcairo2 libpango-1.0-0 libpangocairo-1.0-0
```

**macOS:**
```bash
brew install cairo pango gdk-pixbuf libffi
```

**Windows:**
Scarica e installa GTK+ Runtime:
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases

### API Key non funziona

1. **Verifica .env esiste:**
```bash
ls -la .env
```

2. **Verifica formato:**
```env
# ✅ Corretto
ANTHROPIC_API_KEY=sk-ant-api03-xxx

# ❌ Sbagliato (spazi, quote)
ANTHROPIC_API_KEY = "sk-ant-api03-xxx"
```

3. **Riavvia server** dopo modifiche a `.env`

### Errore "Module not found"

```bash
# Verifica virtual environment attivo
which python  # Deve mostrare path dentro venv/

# Reinstalla dipendenze
pip install -r requirements.txt

# Se persiste, ricrea venv
rm -rf venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📦 Deploy in Produzione

### Railway (Raccomandato)

1. **Installa CLI:**
```bash
npm i -g @railway/cli
```

2. **Login:**
```bash
railway login
```

3. **Deploy:**
```bash
railway up
```

Railway rileva automaticamente FastAPI e configura tutto.

**Aggiungi variabili d'ambiente:**
```bash
railway variables set ANTHROPIC_API_KEY=sk-ant-...
railway variables set GOOGLE_API_KEY=AIza...
```

### Render

1. Push repo su GitHub
2. Vai su https://render.com
3. New → Web Service
4. Connetti repo GitHub
5. Configura:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Aggiungi Environment Variables (API keys)
7. Deploy!

### Fly.io

1. **Installa flyctl:**
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Login:**
```bash
fly auth login
```

3. **Launch:**
```bash
fly launch
```

4. **Deploy:**
```bash
fly deploy
```

**Aggiungi secrets:**
```bash
fly secrets set ANTHROPIC_API_KEY=sk-ant-...
fly secrets set GOOGLE_API_KEY=AIza...
```

### Docker (Opzionale)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build e run:**
```bash
docker build -t noofolio .
docker run -p 8000:8000 --env-file .env noofolio
```

---

## ⚙️ Configurazione Avanzata

### config.yaml Completo

```yaml
# LLM Settings
llm:
  provider: "anthropic"  # anthropic, google, openai
  models:
    gemini: "gemini-2.0-flash"
    anthropic: "claude-sonnet-4-5-20250929"
    openai: "gpt-4-turbo-preview"
  temperature: 0.7

# API Limits
api:
  daily_limit: 100
  calls_today: 0
  last_reset: null

# User Settings
user:
  refresh_days: 0  # 0 = sempre chiedi aggiornamenti

# Archetipi (72 combinazioni)
archetypes:
  roles:
    - id: builder
      name: "Builder"
    - id: designer
      name: "Designer"
    # ... altri 4

  personalities:
    - id: chaos
      name: "Chaos"
      palette: ["#ff6b6b", "#4ecdc4"]
    # ... altri 5

  ai_styles:
    - id: cyborg
      name: "Cyborg"
    # ... altri 2

# Demo Profiles
demo_profiles:
  - id: "marco_rossi"
    name: "Marco Rossi"
    archetype: "Builder × Chaos × Pragmatist"
  # ... altri profili
```

### Environment Variables (.env)

```env
# LLM API Keys (BACKEND ONLY - mai committare!)
GOOGLE_API_KEY=your-google-gemini-key
ANTHROPIC_API_KEY=your-anthropic-claude-key
OPENAI_API_KEY=your-openai-gpt4-key

# Server
PORT=8000
HOST=0.0.0.0

# Debug
DEBUG=false
LOG_LEVEL=info

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=pdf,doc,docx,jpg,png

# Session
SESSION_SECRET=your-secret-key-here
```

---

## 📊 Metriche e Monitoraggio

### Logging

```python
# main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.get("/")
async def home():
    logger.info("Home page accessed")
    return templates.TemplateResponse("index.html", {"request": request})
```

### Analytics (Futuro)

Dashboard `/analytics/{profile_id}` mostrerà:
- 👥 Visite totali
- 💬 Domande NooMe più frequenti
- 📊 Sezioni più lette
- 🌍 Geografia visitatori
- ⏱️ Tempo medio sul profilo

---

## 🧪 Testing

### Test Manuali

1. **Generazione Express:**
   - Vai su `/onboarding`
   - Scegli "Express Mode"
   - Compila 5 domande
   - Verifica generazione con progress bar
   - Controlla portfolio generato

2. **Generazione Deep:**
   - Scegli "Deep Mode"
   - Compila tutti 10 step
   - Upload CV e immagini
   - Verifica sidebar step
   - Controlla portfolio completo

3. **NooMe Chat:**
   - Apri portfolio (`/view/{id}`)
   - Clicca widget chat
   - Fai domande varie
   - Verifica risposte coerenti

4. **Mind Sculptor:**
   - Vai su `/mind-sculptor/{id}`
   - Rispondi a domande random
   - Verifica salvataggio
   - Controlla affidabilità aumentata

5. **Export:**
   - Scarica HTML
   - Scarica JSON
   - Genera PDF (verifica formattazione)

### Test Automatici (Futuro)

```python
# tests/test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Noofolio" in response.text

def test_api_chat():
    response = client.post("/api/chat/marco_rossi",
        data={"message": "Ciao"})
    assert response.status_code == 200
    assert "response" in response.json()
```

---

## 📚 Risorse e Documentazione

### Documenti Interni

- **FRAMEWORK.md** - Architettura completa e filosofia del progetto
- **config.yaml** - Configurazione archetipi e LLM
- **requirements.txt** - Dipendenze Python

### Link Utili

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **HTMX Docs**: https://htmx.org/docs/
- **Jinja2 Docs**: https://jinja.palletsprojects.com/
- **Anthropic Claude**: https://docs.anthropic.com/claude/docs
- **Google Gemini**: https://ai.google.dev/docs
- **WeasyPrint**: https://doc.courtbouillon.org/weasyprint/

### AI Works Challenge

Progetto creato per **AI Works Challenge** (Cosmico, Dicembre 2024).

**Requisiti soddisfatti:**
- ✅ Multi-agent AI system
- ✅ Novel interaction paradigm (anti-portfolio)
- ✅ AI-native approach
- ✅ Unique value proposition
- ✅ Working demo
- ✅ Complete documentation

---

## 🙏 Credits

**Creato da:** Angelo & Team
**Challenge:** AI Works (Cosmico)
**Data:** Dicembre 2024
**Stack:** FastAPI + Jinja2 + HTMX + Claude/Gemini

**Riconoscimenti speciali:**
- Budget demo (€5 Anthropic) offerto da Angelo
- Ispirazione: "Noosfera" di Teilhard de Chardin
- Filosofia: Anti-portfolio, focus su pensiero non output

---

## 📝 License

MIT License

Copyright (c) 2024 Noofolio Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🚀 Quick Start Recap

```bash
# 1. Clone
git clone https://github.com/your-username/noofolio.git
cd noofolio

# 2. Virtual env
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Run (auto-open browser)
python main.py

# 5. Apri browser
http://localhost:8000
```

**Demo già configurata!** Le API key sono incluse, puoi iniziare subito a testare.

---

**Happy Noofolioing! 🧠✨**
