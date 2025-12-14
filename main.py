from fastapi import FastAPI, Request, Form, HTTPException, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, FileResponse
from pathlib import Path
import json
import yaml
from typing import Optional, List
from dotenv import load_dotenv
import asyncio
from datetime import datetime

load_dotenv()

# Import file processor
import sys
sys.path.append('utils')
from file_processor import FileProcessor

# Load config
CONFIG_PATH = Path("config.yaml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

LLM_PROVIDER = CONFIG["llm"]["provider"]

# FastAPI setup
app = FastAPI(title="Noofolio - Your Work, Not Your Role")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Import agents
from agents.archetype_detector import ArchetypeDetector
from agents.pattern_extractor import PatternExtractor
from agents.decision_archaeologist import DecisionArchaeologist
from agents.signature_detector import SignatureDetector
from agents.narrative_composer import NarrativeComposer
from agents.portfolio_generator import PortfolioGenerator
from agents.noome_chat import NooMeChat

# Simple in-memory session storage (use Redis in production)
sessions = {}

def get_all_profiles():
    """Get all profiles from data/profiles"""
    profiles_dir = Path("data/profiles")
    profiles = []
    if profiles_dir.exists():
        for json_file in profiles_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                profiles.append({
                    'id': json_file.stem,
                    'name': data.get('identity', {}).get('name', json_file.stem),
                    'archetype': data.get('meta', {}).get('archetype', {}),
                    'has_html': json_file.with_suffix('.html').exists()
                })
            except:
                pass
    return profiles

def save_portfolio(user_data, html, json_data):
    """Save portfolio to files"""
    profiles_dir = Path("data/profiles")
    profiles_dir.mkdir(parents=True, exist_ok=True)
    
    name = f"{user_data.get('nome', 'user')}_{user_data.get('cognome', 'x')}"
    pid = name.lower().replace(' ', '_')
    
    with open(profiles_dir / f"{pid}.json", 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    with open(profiles_dir / f"{pid}.html", 'w', encoding='utf-8') as f:
        f.write(html)
    
    return pid

# ============================================
# ROUTES
# ============================================

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    """Landing page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/onboarding", response_class=HTMLResponse)
async def onboarding(request: Request):
    """Onboarding page - choose Express or Deep mode"""
    return templates.TemplateResponse("onboarding.html", {"request": request})

@app.get("/create", response_class=HTMLResponse)
async def create_start(request: Request):
    """Start portfolio creation (Deep mode)"""
    # Initialize session
    session_id = request.cookies.get("session_id", "default")
    sessions[session_id] = {"step": 1, "data": {}}
    
    return templates.TemplateResponse("create.html", {
        "request": request,
        "step": 1,
        "total_steps": 10,  # Updated to 10 steps
        "data": {}
    })

@app.get("/create/express", response_class=HTMLResponse)
async def create_express(request: Request):
    """Express mode - 5 questions only"""
    return templates.TemplateResponse("express.html", {"request": request})

@app.post("/create/step/{step}")
async def create_step(request: Request, step: int):
    """Handle form step submission"""
    form_data = await request.form()
    session_id = request.cookies.get("session_id", "default")
    
    # Get or create session
    if session_id not in sessions:
        sessions[session_id] = {"step": step, "data": {}}
    
    # Process form data
    for key, value in form_data.items():
        if key not in ['cv_file', 'images[]']:  # Skip file fields
            sessions[session_id]["data"][key] = value
    
    # Handle CV file upload (Step 1)
    if step == 1:
        cv_type = form_data.get('cv_type', 'text')
        
        if cv_type == 'upload' and 'cv_file' in form_data:
            cv_file = form_data['cv_file']
            if cv_file and hasattr(cv_file, 'file'):
                try:
                    file_content = await cv_file.read()
                    cv_text = FileProcessor.process_cv_file(file_content, cv_file.filename)
                    sessions[session_id]["data"]['cv_content'] = cv_text
                    sessions[session_id]["data"]['cv_source'] = 'upload'
                except Exception as e:
                    return templates.TemplateResponse("create.html", {
                        "request": request,
                        "step": step,
                        "total_steps": 10,
                        "data": sessions[session_id]["data"],
                        "error": f"Errore nel processare il CV: {str(e)}"
                    })
        
        elif cv_type == 'link':
            cv_link = form_data.get('cv_link', '')
            sessions[session_id]["data"]['cv_content'] = f"Link CV: {cv_link}\n\n(Nota: scaricare e processare il CV dal link)"
            sessions[session_id]["data"]['cv_source'] = 'link'
        
        # Process multiple links
        link_urls = form_data.getlist('link_url[]')
        link_types = form_data.getlist('link_type[]')
        
        links = []
        for url, ltype in zip(link_urls, link_types):
            if url and url.strip():
                links.append({"url": url, "type": ltype})
        
        sessions[session_id]["data"]["links"] = links
    
    # Handle images upload (Step 9)
    if step == 9:
        images_files = form_data.getlist('images[]')
        
        if images_files and images_files[0].filename:  # Check if files were uploaded
            try:
                files_data = []
                for img_file in images_files[:10]:  # Max 10
                    if img_file and hasattr(img_file, 'file'):
                        file_content = await img_file.read()
                        files_data.append({
                            'content': file_content,
                            'filename': img_file.filename
                        })
                
                processed_images = FileProcessor.process_multiple_images(files_data)
                sessions[session_id]["data"]["images"] = processed_images
            except Exception as e:
                print(f"Error processing images: {e}")
                sessions[session_id]["data"]["images"] = []
    
    # Move to next step
    next_step = step + 1
    sessions[session_id]["step"] = next_step
    
    if next_step <= 10:
        # Return next step form
        return templates.TemplateResponse("create.html", {
            "request": request,
            "step": next_step,
            "total_steps": 10,
            "data": sessions[session_id]["data"]
        })
    else:
        # Final step - trigger generation
        return templates.TemplateResponse("create.html", {
            "request": request,
            "step": 10,
            "total_steps": 10,
            "data": sessions[session_id]["data"],
            "ready_to_generate": True
        })

@app.get("/api/generate-stream")
async def generate_portfolio_stream(request: Request):
    """Generate portfolio with live progress updates using SSE"""
    
    async def event_generator():
        session_id = request.cookies.get("session_id", "default")
        user_data = sessions.get(session_id, {}).get("data", {})
        
        if not user_data:
            yield f"data: {json.dumps({'error': 'No data in session'})}\n\n"
            return
        
        try:
            # Step 1: Archetype
            yield f"data: {json.dumps({'step': 1, 'status': 'running', 'text': '🔍 Rilevamento archetipo...'})}\n\n"
            await asyncio.sleep(0.5)
            
            archetype = ArchetypeDetector(provider=LLM_PROVIDER).run(user_data)
            archetype_name = archetype.get("archetype_name", "")
            yield f"data: {json.dumps({'step': 1, 'status': 'done', 'text': f'✅ Archetipo: {archetype_name} ', 'data': archetype})}\n\n"
            await asyncio.sleep(0.5)
            
            # Step 2: Patterns
            yield f"data: {json.dumps({'step': 2, 'status': 'running', 'text': '🧩 Estrazione pattern...'})}\n\n"
            await asyncio.sleep(0.5)
            
            patterns = PatternExtractor(provider=LLM_PROVIDER).run(user_data)
            yield f"data: {json.dumps({'step': 2, 'status': 'done', 'text': '✅ Pattern estratti'})}\n\n"
            await asyncio.sleep(0.5)
            
            # Step 3: Decisions
            yield f"data: {json.dumps({'step': 3, 'status': 'running', 'text': '🌳 Analisi decisioni...'})}\n\n"
            await asyncio.sleep(0.5)
            
            decisions = DecisionArchaeologist(provider=LLM_PROVIDER).run(user_data)
            yield f"data: {json.dumps({'step': 3, 'status': 'done', 'text': '✅ Decisioni analizzate'})}\n\n"
            await asyncio.sleep(0.5)
            
            # Step 4: Signature
            yield f"data: {json.dumps({'step': 4, 'status': 'running', 'text': '✏️ Rilevamento firma...'})}\n\n"
            await asyncio.sleep(0.5)
            
            signature = SignatureDetector(provider=LLM_PROVIDER).run(user_data)
            yield f"data: {json.dumps({'step': 4, 'status': 'done', 'text': '✅ Firma rilevata'})}\n\n"
            await asyncio.sleep(0.5)
            
            # Step 5: Narrative
            yield f"data: {json.dumps({'step': 5, 'status': 'running', 'text': '📖 Composizione narrativa...'})}\n\n"
            await asyncio.sleep(0.5)
            
            narrative = NarrativeComposer(provider=LLM_PROVIDER).run(user_data, archetype, patterns, decisions, signature)
            yield f"data: {json.dumps({'step': 5, 'status': 'done', 'text': '✅ Narrativa composta'})}\n\n"
            await asyncio.sleep(0.5)
            
            # Step 6: Portfolio
            yield f"data: {json.dumps({'step': 6, 'status': 'running', 'text': '🎨 Generazione portfolio...'})}\n\n"
            await asyncio.sleep(0.5)
            
            generator = PortfolioGenerator()
            enriched = user_data.copy()
            enriched.update({
                '_patterns': patterns,
                '_decisions': decisions,
                '_signature': signature,
                '_narrative': narrative
            })
            html, json_data = generator.run(enriched, archetype)
            
            json_data['analysis'] = {
                'patterns': patterns,
                'decisions': decisions,
                'signature': signature,
                'narrative': narrative
            }
            json_data['_raw_input'] = user_data
            
            # Save
            profile_id = save_portfolio(user_data, html, json_data)
            
            yield f"data: {json.dumps({'step': 6, 'status': 'done', 'text': '✅ Portfolio generato!', 'profile_id': profile_id, 'archetype': archetype})}\n\n"
            
            # Final event
            yield f"data: {json.dumps({'complete': True, 'profile_id': profile_id})}\n\n"
            
        except Exception as e:
            import traceback
            yield f"data: {json.dumps({'error': str(e), 'traceback': traceback.format_exc()})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
async def generate_portfolio(request: Request):
    """Generate portfolio using AI agents"""
    try:
        session_id = request.cookies.get("session_id", "default")
        user_data = sessions.get(session_id, {}).get("data", {})
        
        if not user_data:
            raise HTTPException(status_code=400, detail="No data in session")
        
        # Validation
        if not user_data.get('nome') or not user_data.get('cognome') or not user_data.get('cv_content'):
            raise HTTPException(status_code=400, detail="Nome, cognome e CV sono obbligatori")
        
        # Run agents pipeline
        progress_data = []
        
        # Step 1: Archetype Detection
        progress_data.append({"step": 1, "status": "running", "text": "🔍 Archetipo..."})
        archetype = ArchetypeDetector(provider=LLM_PROVIDER).run(user_data)
        progress_data.append({"step": 1, "status": "done", "data": archetype})
        
        # Step 2: Pattern Extraction
        progress_data.append({"step": 2, "status": "running", "text": "🧩 Pattern..."})
        patterns = PatternExtractor(provider=LLM_PROVIDER).run(user_data)
        progress_data.append({"step": 2, "status": "done"})
        
        # Step 3: Decision Archaeology
        progress_data.append({"step": 3, "status": "running", "text": "🌳 Decisioni..."})
        decisions = DecisionArchaeologist(provider=LLM_PROVIDER).run(user_data)
        progress_data.append({"step": 3, "status": "done"})
        
        # Step 4: Signature Detection
        progress_data.append({"step": 4, "status": "running", "text": "✏️ Firma..."})
        signature = SignatureDetector(provider=LLM_PROVIDER).run(user_data)
        progress_data.append({"step": 4, "status": "done"})
        
        # Step 5: Narrative Composition
        progress_data.append({"step": 5, "status": "running", "text": "📖 Narrativa..."})
        narrative = NarrativeComposer(provider=LLM_PROVIDER).run(user_data, archetype, patterns, decisions, signature)
        progress_data.append({"step": 5, "status": "done"})
        
        # Step 6: Portfolio Generation
        progress_data.append({"step": 6, "status": "running", "text": "🎨 Portfolio..."})
        generator = PortfolioGenerator()
        enriched = user_data.copy()
        enriched.update({'_patterns': patterns, '_decisions': decisions, '_signature': signature, '_narrative': narrative})
        html, json_data = generator.run(enriched, archetype)
        
        # Add analysis to JSON
        json_data['analysis'] = {
            'patterns': patterns,
            'decisions': decisions,
            'signature': signature,
            'narrative': narrative
        }
        json_data['_raw_input'] = user_data
        
        # Save portfolio
        profile_id = save_portfolio(user_data, html, json_data)
        
        progress_data.append({"step": 6, "status": "done", "profile_id": profile_id})
        
        return JSONResponse({
            "success": True,
            "profile_id": profile_id,
            "archetype": archetype,
            "progress": progress_data
        })
        
    except Exception as e:
        import traceback
        return JSONResponse({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }, status_code=500)

@app.post("/api/generate-express")
async def generate_express(request: Request):
    """Generate portfolio from Express mode (5 questions)"""
    try:
        form_data = await request.form()
        
        # Build simplified user_data
        user_data = {
            'nome': form_data.get('nome'),
            'cognome': form_data.get('cognome'),
            'cv_content': form_data.get('cv_content'),
            'superpotere': form_data.get('superpotere'),
            'against_data': form_data.get('key_decision'),  # Map to decision log
            'human_better': form_data.get('human_delta'),  # Map to human delta
            'main_link': form_data.get('main_link', ''),
            # Set defaults for missing fields
            'presentazione': '',
            'projects': [],
            'worst_decision': '',
            'heresy': '',
            'anti_skills': '',
            'red_flags': '',
            'biggest_failure': '',
            'pattern_failure': '',
            'belief_murdered': '',
            'ai_guilty': '',
            'ai_never': '',
            'ai_better': '',
            'delta_story': '',
            'masterclass': '',
            'books': '',
            'people': '',
            'rabbit_hole': '',
            'communication': '',
            'crash_triggers': '',
            'known_biases': '',
            'ideal_conditions': '',
            'learning_next': '',
            'two_years': '',
            'dream_project': ''
        }
        
        # Run simplified pipeline
        archetype = ArchetypeDetector(provider=LLM_PROVIDER).run(user_data)
        generator = PortfolioGenerator()
        html, json_data = generator.run(user_data, archetype)
        
        json_data['_raw_input'] = user_data
        json_data['mode'] = 'express'
        
        profile_id = save_portfolio(user_data, html, json_data)
        
        return JSONResponse({
            "success": True,
            "profile_id": profile_id,
            "archetype": archetype,
            "redirect": f"/result/{profile_id}"
        })
        
    except Exception as e:
        import traceback
        return JSONResponse({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }, status_code=500)

@app.get("/result/{profile_id}", response_class=HTMLResponse)
async def result_page(request: Request, profile_id: str):
    """Show generation result with preview and downloads"""
    profiles_dir = Path("data/profiles")
    json_path = profiles_dir / f"{profile_id}.json"
    html_path = profiles_dir / f"{profile_id}.html"
    
    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        portfolio_data = json.load(f)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        portfolio_html = f.read()
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "profile_id": profile_id,
        "archetype": portfolio_data.get('meta', {}).get('archetype', {}),
        "portfolio_html": portfolio_html,
        "portfolio_json": json.dumps(portfolio_data, indent=2, ensure_ascii=False)
    })

@app.get("/explore", response_class=HTMLResponse)
async def explore(request: Request):
    """Explore existing portfolios"""
    profiles = get_all_profiles()
    return templates.TemplateResponse("explore.html", {
        "request": request,
        "profiles": profiles
    })

@app.get("/view/{profile_id}", response_class=HTMLResponse)
async def view_portfolio(request: Request, profile_id: str):
    """View a specific portfolio with NooMe chat"""
    profiles_dir = Path("data/profiles")
    html_path = profiles_dir / f"{profile_id}.html"
    json_path = profiles_dir / f"{profile_id}.json"
    
    if not html_path.exists() or not json_path.exists():
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        portfolio_html = f.read()
    
    with open(json_path, 'r', encoding='utf-8') as f:
        portfolio_data = json.load(f)
    
    profile_name = portfolio_data.get('identity', {}).get('name', profile_id)
    
    return templates.TemplateResponse("view.html", {
        "request": request,
        "profile_id": profile_id,
        "profile_name": profile_name,
        "portfolio_html": portfolio_html,
        "portfolio_data": portfolio_data
    })

@app.post("/api/chat/{profile_id}")
async def chat_with_noome(request: Request, profile_id: str):
    """Chat with NooMe for a specific profile"""
    try:
        data = await request.json()
        message = data.get("message", "")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Load profile data
        profiles_dir = Path("data/profiles")
        json_path = profiles_dir / f"{profile_id}.json"
        
        if not json_path.exists():
            raise HTTPException(status_code=404, detail="Profile not found")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            portfolio_data = json.load(f)
        
        # Get NooMe response
        chat = NooMeChat(provider=LLM_PROVIDER)
        response = chat.respond(message, portfolio_data, profile_id)
        
        # Save conversation
        conversations_path = Path(f"data/conversations/{profile_id}.json")
        conversations_path.parent.mkdir(parents=True, exist_ok=True)
        
        conversations = []
        if conversations_path.exists():
            with open(conversations_path, 'r', encoding='utf-8') as f:
                conversations = json.load(f)
        
        # Find or create current conversation
        session_id = request.cookies.get("visitor_session", str(datetime.now().timestamp()))
        current_conv = None
        for conv in conversations:
            if conv.get('session_id') == session_id:
                current_conv = conv
                break
        
        if not current_conv:
            current_conv = {
                'id': str(len(conversations)),
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'messages': []
            }
            conversations.append(current_conv)
        
        # Add messages
        current_conv['messages'].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        current_conv['messages'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat(),
            'corrected': False
        })
        
        # Save
        with open(conversations_path, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, ensure_ascii=False, indent=2)
        
        return JSONResponse({
            "success": True,
            "response": response
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.get("/select-profile", response_class=HTMLResponse)
async def select_profile(request: Request):
    """Select profile to access"""
    profiles = get_all_profiles()
    return templates.TemplateResponse("select_profile.html", {
        "request": request,
        "profiles": profiles
    })

@app.get("/dashboard/{profile_id}", response_class=HTMLResponse)
async def dashboard(request: Request, profile_id: str):
    """Personal dashboard for profile owner"""
    profiles_dir = Path("data/profiles")
    json_path = profiles_dir / f"{profile_id}.json"
    html_path = profiles_dir / f"{profile_id}.html"
    
    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Profile not found")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        portfolio_data = json.load(f)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        portfolio_html = f.read()
    
    name = portfolio_data.get('identity', {}).get('name', profile_id)
    archetype = portfolio_data.get('meta', {}).get('archetype', {})
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "profile_id": profile_id,
        "name": name,
        "archetype": archetype,
        "portfolio_html": portfolio_html
    })

@app.get("/select-profile", response_class=HTMLResponse)

@app.get("/corrections/{profile_id}", response_class=HTMLResponse)
async def corrections_page(request: Request, profile_id: str):
    """Corrections page for NooMe training"""
    # Load conversations from file
    conversations_path = Path(f"data/conversations/{profile_id}.json")
    corrections_path = Path(f"data/corrections/{profile_id}.json")
    
    conversations = []
    if conversations_path.exists():
        with open(conversations_path, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
    
    # Calculate reliability score
    corrections_made = 0
    if corrections_path.exists():
        with open(corrections_path, 'r', encoding='utf-8') as f:
            corrections_made = len(json.load(f))
    
    # Load profile to get questions_answered
    profiles_dir = Path("data/profiles")
    json_path = profiles_dir / f"{profile_id}.json"
    
    questions_answered = 10  # Default for full Deep mode
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data.get('mode') == 'express':
                questions_answered = 5
    
    # Calculate score (0-5)
    # Base: questions answered (max 2 stars)
    # Corrections: +0.5 star per 5 corrections (max 3 stars)
    score = min(2, questions_answered / 5)
    score += min(3, corrections_made / 5 * 0.5)
    reliability_score = round(score, 1)
    
    return templates.TemplateResponse("corrections.html", {
        "request": request,
        "profile_id": profile_id,
        "conversations": conversations,
        "reliability_score": reliability_score,
        "questions_answered": questions_answered,
        "corrections_made": corrections_made,
        "total_conversations": len(conversations)
    })

@app.post("/api/save-correction/{profile_id}")
async def save_correction(request: Request, profile_id: str):
    """Save a correction for NooMe training"""
    try:
        data = await request.json()

        # Load existing corrections
        corrections_path = Path(f"data/corrections/{profile_id}.json")
        corrections_path.parent.mkdir(parents=True, exist_ok=True)

        corrections = []
        if corrections_path.exists():
            with open(corrections_path, 'r', encoding='utf-8') as f:
                corrections = json.load(f)

        # Add new correction
        correction = {
            "conv_id": data.get("conv_id"),
            "msg_index": data.get("msg_index"),
            "original_response": "",  # Could fetch from conversations
            "corrected_response": data.get("corrected_response"),
            "timestamp": datetime.now().isoformat()
        }
        corrections.append(correction)

        # Save
        with open(corrections_path, 'w', encoding='utf-8') as f:
            json.dump(corrections, f, ensure_ascii=False, indent=2)

        return JSONResponse({"success": True})

    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.get("/mind-sculptor/{profile_id}", response_class=HTMLResponse)
async def mind_sculptor_page(request: Request, profile_id: str, from_creation: bool = False):
    """Mind Sculptor page - Random question generator"""
    return templates.TemplateResponse("mind_sculptor.html", {
        "request": request,
        "profile_id": profile_id,
        "from_creation": from_creation
    })

@app.get("/api/mind-sculptor/question/{profile_id}")
async def generate_random_question(profile_id: str):
    """Generate a random contextual question"""
    try:
        from agents.mind_sculptor_agent import MindSculptorAgent

        # Load profile data
        profiles_dir = Path("data/profiles")
        json_path = profiles_dir / f"{profile_id}.json"

        if not json_path.exists():
            raise HTTPException(status_code=404, detail="Profile not found")

        with open(json_path, 'r', encoding='utf-8') as f:
            portfolio_data = json.load(f)

        # Load previous answers
        answers_path = Path(f"data/mind_sculptor/{profile_id}_answers.json")
        previous_answers = []
        if answers_path.exists():
            with open(answers_path, 'r', encoding='utf-8') as f:
                previous_answers = json.load(f)

        # Generate question
        agent = MindSculptorAgent(provider=LLM_PROVIDER)
        question = agent.generate_question(portfolio_data, previous_answers)

        return JSONResponse({
            "success": True,
            "question": question
        })

    except Exception as e:
        import traceback
        return JSONResponse({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }, status_code=500)

@app.post("/api/mind-sculptor/answer/{profile_id}")
async def save_random_answer(request: Request, profile_id: str):
    """Save answer to a random question"""
    try:
        data = await request.json()

        # Load existing answers
        answers_path = Path(f"data/mind_sculptor/{profile_id}_answers.json")
        answers_path.parent.mkdir(parents=True, exist_ok=True)

        answers = []
        if answers_path.exists():
            with open(answers_path, 'r', encoding='utf-8') as f:
                answers = json.load(f)

        # Add new answer
        from datetime import datetime
        answer = {
            "question": data.get("question"),
            "answer": data.get("answer"),
            "timestamp": datetime.now().isoformat()
        }
        answers.append(answer)

        # Save
        with open(answers_path, 'w', encoding='utf-8') as f:
            json.dump(answers, f, ensure_ascii=False, indent=2)

        return JSONResponse({"success": True})

    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.post("/api/mind-sculptor/feedback/{profile_id}")
async def save_question_feedback(request: Request, profile_id: str):
    """Save feedback on a generated question"""
    try:
        data = await request.json()

        # Load existing feedback
        feedback_path = Path(f"data/mind_sculptor/{profile_id}_feedback.json")
        feedback_path.parent.mkdir(parents=True, exist_ok=True)

        feedbacks = []
        if feedback_path.exists():
            with open(feedback_path, 'r', encoding='utf-8') as f:
                feedbacks = json.load(f)

        # Add new feedback
        from datetime import datetime
        feedback = {
            "question": data.get("question"),
            "feedback": data.get("feedback"),
            "timestamp": datetime.now().isoformat()
        }
        feedbacks.append(feedback)

        # Save
        with open(feedback_path, 'w', encoding='utf-8') as f:
            json.dump(feedbacks, f, ensure_ascii=False, indent=2)

        return JSONResponse({"success": True})

    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

# Run: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)