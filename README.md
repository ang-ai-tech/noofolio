# 🧠 Noofolio - FastAPI Version

**Your work, not your role.** Portfolio AI-native con upload CV, progress bar live, export PDF.

## ✨ Features

### Core Features
- ✅ **Onboarding intelligente** - Scegli Express (5 min) o Deep Mode (30 min)
- ✅ **Upload CV** - Supporta PDF, Word, link condivisi o testo diretto
- ✅ **Multi-link dinamici** - Aggiungi LinkedIn, GitHub, Behance, ecc.
- ✅ **Progress bar live** - Vedi in real-time la generazione del portfolio con SSE
- ✅ **Export multi-formato** - Download HTML, JSON o PDF
- ✅ **NooMe Chat Widget** - Clone AI floating come Intercom
- ✅ **Sistema correzioni** - Migliora l'affidabilità del tuo NooMe
- ✅ **Punteggio affidabilità** - Sistema a stelle (0-5⭐)
- ✅ **Upload immagini** - Arricchisci il portfolio con foto personali

### Futuri Sviluppi (Coming Soon)
- 📧 Email notifications quando qualcuno chatta con NooMe
- 📊 Analytics dashboard (visite, domande, sezioni più lette)
- 🔗 Social sharing integrato
- 🎯 Job Match AI automatico
- 🌐 Multi-lingua (EN, ES, FR)
- 🎨 Theme customizer

## 🚀 Quick Start

### 1. Installazione

```bash
# Clone repo
git clone <your-repo>
cd noofolio

# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Note: WeasyPrint richiede librerie di sistema
# Ubuntu/Debian:
sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0

# macOS (con Homebrew):
brew install pango gdk-pixbuf libffi

# Windows: scarica GTK+ da https://gtk.org
```

### 2. Configurazione

```bash
# Copia .env.example
cp .env.example .env

# Aggiungi le tue API keys
# .env file:
GOOGLE_API_KEY=your-gemini-key
ANTHROPIC_API_KEY=your-anthropic-key  # opzionale
OPENAI_API_KEY=your-openai-key        # opzionale
```

### 3. Run

```bash
# Development mode (auto-reload)
uvicorn main:app --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

Apri: **http://localhost:8000**

---

## 📁 Struttura Progetto

```
noofolio/
├── main.py                    # FastAPI app
├── requirements.txt
├── .env
├── config.yaml
├── agents/                    # LangChain agents (invariati)
│   ├── __init__.py
│   ├── archetype_detector.py
│   ├── pattern_extractor.py
│   ├── decision_archaeologist.py
│   ├── signature_detector.py
│   ├── narrative_composer.py
│   ├── portfolio_generator.py
│   └── noome_chat.py
├── utils/                     # NEW - Utilities
│   ├── __init__.py
│   └── file_processor.py      # PDF/Word/Image processing
├── templates/                 # Jinja2 templates
│   ├── base.html
│   ├── index.html            # Landing page
│   ├── onboarding.html       # NEW - Onboarding
│   ├── express.html          # NEW - Express mode
│   ├── create.html           # Form multi-step (10 steps)
│   ├── explore.html          # Browse portfolios
│   ├── view.html             # View + NooMe chat widget
│   ├── result.html           # Generation result
│   ├── corrections.html      # NEW - NooMe corrections
│   ├── dashboard.html        # Owner dashboard
│   └── select_profile.html
├── static/
│   ├── css/
│   │   └── style.css         # Main stylesheet
│   └── js/
│       └── htmx.min.js       # HTMX (CDN fallback)
└── data/
    ├── profiles/              # Generated portfolios
    ├── uploads/               # NEW - Uploaded files (CV, images)
    ├── conversations/         # NEW - Chat history
    └── corrections/           # NEW - NooMe corrections
```

---

## 🔧 Nuove Features Tecniche

### 1. File Upload Processing

Supporta CV in **PDF**, **Word** (.doc, .docx) e **link condivisi**:

```python
from utils.file_processor import FileProcessor

# Extract text from PDF
text = FileProcessor.process_cv_file(file_content, "cv.pdf")

# Process images
images = FileProcessor.process_multiple_images(files, max_images=10)
```

### 2. Progress Bar Live (SSE)

Generazione portfolio con aggiornamenti real-time:

```javascript
const eventSource = new EventSource('/api/generate-stream');
eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    // Update progress bar
    progressBar.style.width = data.percent + '%';
};
```

### 3. Export PDF

Converti portfolio HTML in PDF con WeasyPrint:

```python
# Route: /export/pdf/{profile_id}
from weasyprint import HTML
pdf_bytes = HTML(string=html_content).write_pdf()
```

### 4. NooMe Affidabilità Score

Formula: `(domande_risposte / 5 * 2) + (correzioni / 5 * 0.5)`
- Express Mode: max ⭐⭐ (5 domande)
- Deep Mode: max ⭐⭐⭐⭐⭐ (10 domande + correzioni)

---

## 🔄 Differenze da Streamlit

| Feature | Streamlit | FastAPI |
|---------|-----------|---------|
| **Routing** | Session state | URL routes |
| **Templates** | Python strings | Jinja2 files |
| **CSS** | Inline Python | Separate .css |
| **Forms** | st.form() | HTMX + forms |
| **Interactivity** | Reruns | HTMX swaps |
| **Performance** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Customization** | Limited | Full control |

---

## 🛠 Development

### Modificare lo stile

Edita `static/css/style.css` - no Python needed.

### Aggiungere una route

```python
# main.py
@app.get("/new-page")
async def new_page(request: Request):
    return templates.TemplateResponse("new_page.html", {"request": request})
```

### Modificare un template

Edita file in `templates/` - Jinja2 syntax.

### Debug

```bash
# Logs in console
uvicorn main:app --reload --log-level debug
```

---

## 📦 Deploy

### Railway (Recommended)

```bash
# Install CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

Config automatica - rileva FastAPI.

### Render

1. Push to GitHub
2. New Web Service su Render
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Launch
fly launch

# Deploy
fly deploy
```

---

## 🎯 API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page |
| `/onboarding` | GET | Onboarding - scelta Express/Deep |
| `/create` | GET | Portfolio creation (Deep mode) |
| `/create/express` | GET | Express mode (5 questions) |
| `/create/step/{step}` | POST | Submit form step (with file upload) |
| `/api/generate` | POST | Generate portfolio (legacy) |
| `/api/generate-stream` | GET | Generate with live progress (SSE) |
| `/api/generate-express` | POST | Generate from Express mode |
| `/result/{profile_id}` | GET | Show result with preview |
| `/explore` | GET | Browse portfolios |
| `/view/{profile_id}` | GET | View with NooMe chat widget |
| `/api/chat/{profile_id}` | POST | Chat with NooMe |
| `/corrections/{profile_id}` | GET | NooMe corrections page |
| `/api/save-correction/{profile_id}` | POST | Save correction |
| `/export/pdf/{profile_id}` | GET | Export portfolio as PDF |
| `/download/html/{profile_id}` | GET | Download HTML |
| `/download/json/{profile_id}` | GET | Download JSON |

---

## ⚙️ Configuration

Edit `config.yaml`:

```yaml
llm:
  provider: "gemini"  # gemini, anthropic, openai
  temperature: 0.7

api:
  daily_limit: 100
```

---

## 🐛 Troubleshooting

### Port already in use
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Templates not found
```bash
# Check structure
ls templates/  # Should show .html files
```

### Static files 404
```bash
# Check structure
ls static/css/style.css  # Should exist
```

---

## 📝 License

MIT License

---

## 🙏 Credits

Creato per **AI Works Challenge** (Cosmico, Dec 2025).

Convertito da Streamlit a FastAPI + Jinja2 + HTMX.