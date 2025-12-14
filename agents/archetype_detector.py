"""
Archetype Detector Agent
Analizza le risposte dell'utente e determina il suo archetipo a 3 assi:
- Ruolo (Builder, Designer, Strategist, Communicator, Operator, Guide)
- Personalità (Chaos, Order, Minimal, Rebel, Warm, Data)
- AI Style (Cyborg, Hybrid, Artisan)
"""

import os
import json
from typing import Dict, Any

class ArchetypeDetector:
    """
    Agente che profila l'utente basandosi sulle sue risposte
    e assegna un archetipo a 3 dimensioni.
    """
    
    # Mapping nomi creativi per combinazioni
    ARCHETYPE_NAMES = {
        # Builder combinations
        ("builder", "chaos", "cyborg"): "The Alchemist",
        ("builder", "chaos", "hybrid"): "The Inventor",
        ("builder", "chaos", "artisan"): "The Tinkerer",
        ("builder", "order", "cyborg"): "The Engineer",
        ("builder", "order", "hybrid"): "The Architect",
        ("builder", "order", "artisan"): "The Craftsman",
        ("builder", "minimal", "cyborg"): "The Minimalist Builder",
        ("builder", "minimal", "hybrid"): "The Essentialist",
        ("builder", "minimal", "artisan"): "The Purist",
        ("builder", "rebel", "cyborg"): "The Disruptor",
        ("builder", "rebel", "hybrid"): "The Maverick",
        ("builder", "rebel", "artisan"): "The Renegade",
        ("builder", "warm", "cyborg"): "The Enabler",
        ("builder", "warm", "hybrid"): "The Facilitator",
        ("builder", "warm", "artisan"): "The Maker",
        ("builder", "data", "cyborg"): "The Optimizer",
        ("builder", "data", "hybrid"): "The Analyst Builder",
        ("builder", "data", "artisan"): "The Precision Maker",
        
        # Designer combinations
        ("designer", "chaos", "cyborg"): "The Dreamer",
        ("designer", "chaos", "hybrid"): "The Visionary",
        ("designer", "chaos", "artisan"): "The Artist",
        ("designer", "order", "cyborg"): "The Systematizer",
        ("designer", "order", "hybrid"): "The Design Engineer",
        ("designer", "order", "artisan"): "The Formalist",
        ("designer", "minimal", "cyborg"): "The Reducer",
        ("designer", "minimal", "hybrid"): "The Sculptor",
        ("designer", "minimal", "artisan"): "The Zen Master",
        ("designer", "rebel", "cyborg"): "The Provocateur",
        ("designer", "rebel", "hybrid"): "The Iconoclast",
        ("designer", "rebel", "artisan"): "The Punk",
        ("designer", "warm", "cyborg"): "The Empath Designer",
        ("designer", "warm", "hybrid"): "The Human-Centered",
        ("designer", "warm", "artisan"): "The Soulful Designer",
        ("designer", "data", "cyborg"): "The UX Scientist",
        ("designer", "data", "hybrid"): "The Evidence-Based",
        ("designer", "data", "artisan"): "The Measurer",
        
        # Strategist combinations
        ("strategist", "chaos", "cyborg"): "The Chaos Navigator",
        ("strategist", "chaos", "hybrid"): "The Opportunist",
        ("strategist", "chaos", "artisan"): "The Intuitive",
        ("strategist", "order", "cyborg"): "The Systems Thinker",
        ("strategist", "order", "hybrid"): "The Navigator",
        ("strategist", "order", "artisan"): "The Planner",
        ("strategist", "minimal", "cyborg"): "The Focused Strategist",
        ("strategist", "minimal", "hybrid"): "The Clarity Seeker",
        ("strategist", "minimal", "artisan"): "The Essentialist Thinker",
        ("strategist", "rebel", "cyborg"): "The Contrarian",
        ("strategist", "rebel", "hybrid"): "The Challenger",
        ("strategist", "rebel", "artisan"): "The Revolutionary",
        ("strategist", "warm", "cyborg"): "The People Strategist",
        ("strategist", "warm", "hybrid"): "The Diplomat",
        ("strategist", "warm", "artisan"): "The Counselor",
        ("strategist", "data", "cyborg"): "The Quant",
        ("strategist", "data", "hybrid"): "The Analyst",
        ("strategist", "data", "artisan"): "The Detective",
        
        # Communicator combinations
        ("communicator", "chaos", "cyborg"): "The Amplifier",
        ("communicator", "chaos", "hybrid"): "The Connector",
        ("communicator", "chaos", "artisan"): "The Free Spirit",
        ("communicator", "order", "cyborg"): "The Structured Voice",
        ("communicator", "order", "hybrid"): "The Clear Channel",
        ("communicator", "order", "artisan"): "The Methodical Writer",
        ("communicator", "minimal", "cyborg"): "The Signal Cutter",
        ("communicator", "minimal", "hybrid"): "The Distiller",
        ("communicator", "minimal", "artisan"): "The Poet",
        ("communicator", "rebel", "cyborg"): "The Provocative Voice",
        ("communicator", "rebel", "hybrid"): "The Truth Teller",
        ("communicator", "rebel", "artisan"): "The Manifesto Writer",
        ("communicator", "warm", "cyborg"): "The Empathic Voice",
        ("communicator", "warm", "hybrid"): "The Storyteller",
        ("communicator", "warm", "artisan"): "The Bard",
        ("communicator", "data", "cyborg"): "The Data Narrator",
        ("communicator", "data", "hybrid"): "The Evidence Writer",
        ("communicator", "data", "artisan"): "The Reporter",
        
        # Operator combinations
        ("operator", "chaos", "cyborg"): "The Chaos Tamer",
        ("operator", "chaos", "hybrid"): "The Firefighter",
        ("operator", "chaos", "artisan"): "The Crisis Handler",
        ("operator", "order", "cyborg"): "The Automator",
        ("operator", "order", "hybrid"): "The Process Master",
        ("operator", "order", "artisan"): "The Operator",
        ("operator", "minimal", "cyborg"): "The Lean Operator",
        ("operator", "minimal", "hybrid"): "The Streamliner",
        ("operator", "minimal", "artisan"): "The Simplifier",
        ("operator", "rebel", "cyborg"): "The Hacker",
        ("operator", "rebel", "hybrid"): "The Rule Bender",
        ("operator", "rebel", "artisan"): "The Workaround Master",
        ("operator", "warm", "cyborg"): "The Support Pillar",
        ("operator", "warm", "hybrid"): "The Helper",
        ("operator", "warm", "artisan"): "The Caretaker",
        ("operator", "data", "cyborg"): "The Sentinel",
        ("operator", "data", "hybrid"): "The Monitor",
        ("operator", "data", "artisan"): "The Watchkeeper",
        
        # Guide combinations
        ("guide", "chaos", "cyborg"): "The Exploration Guide",
        ("guide", "chaos", "hybrid"): "The Adventure Leader",
        ("guide", "chaos", "artisan"): "The Pathfinder",
        ("guide", "order", "cyborg"): "The Systematic Mentor",
        ("guide", "order", "hybrid"): "The Structured Guide",
        ("guide", "order", "artisan"): "The Teacher",
        ("guide", "minimal", "cyborg"): "The Zen Guide",
        ("guide", "minimal", "hybrid"): "The Focused Mentor",
        ("guide", "minimal", "artisan"): "The Wise Minimalist",
        ("guide", "rebel", "cyborg"): "The Unconventional Mentor",
        ("guide", "rebel", "hybrid"): "The Challenger Coach",
        ("guide", "rebel", "artisan"): "The Socratic",
        ("guide", "warm", "cyborg"): "The Tech-Enabled Coach",
        ("guide", "warm", "hybrid"): "The Mentor",
        ("guide", "warm", "artisan"): "The Sage",
        ("guide", "data", "cyborg"): "The Performance Coach",
        ("guide", "data", "hybrid"): "The Evidence-Based Mentor",
        ("guide", "data", "artisan"): "The Measured Guide",
    }
    
    @classmethod
    def get_archetype_name(cls, role: str, personality: str, ai_style: str) -> str:
        """Restituisce il nome creativo per la combinazione"""
        key = (role.lower(), personality.lower(), ai_style.lower())
        return cls.ARCHETYPE_NAMES.get(key, f"The {personality.capitalize()} {role.capitalize()}")
    
    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        self.llm = self._init_llm()
    
    def _init_llm(self):
        if self.provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model="claude-sonnet-4-5-20250929",
                temperature=0.4,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        elif self.provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0.4,
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        else:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.4,
                api_key=os.getenv("OPENAI_API_KEY")
            )
    
    def run(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analizza i dati utente e restituisce l'archetipo.
        """
        
        system_prompt = """SEI UN "PSYCHOLOGICAL PROFILER" PER PROFESSIONISTI.
Il tuo compito è analizzare la psiche professionale dell'utente e assegnargli un archetipo a 3 dimensioni.

ASSE 1 - RUOLO (Cosa fa):
- builder: Crea da zero (Dev, Founder, Maker)
- designer: Dà forma alle cose (UI, Product, Visual)
- strategist: Pensa e pianifica (Consultant, PM)
- communicator: Traduce e racconta (Writer, Marketing)
- operator: Fa funzionare (Ops, Data, DevOps)
- guide: Insegna e guida (Coach, Lead, Mentor)

ASSE 2 - PERSONALITÀ (Come lo fa):
- chaos: Esplora, sperimenta, rompe. Layout: grafo disordinato
- order: Sistema, struttura, scala. Layout: griglia rigida
- minimal: Essenziale, silenzio, focus. Layout: quasi vuoto
- rebel: Sfida, provoca, polarizza. Layout: punk, glitch
- warm: Umano, empatico, accogliente. Layout: morbido
- data: Numeri, prove, risultati. Layout: dashboard

ASSE 3 - AI STYLE:
- cyborg: AI ovunque, trasparenza sui prompt usati
- hybrid: AI come assistente, umano al centro
- artisan: "Human Made", minimo uso AI

ANALIZZA:
1. Il CV e background per dedurre il RUOLO
2. Come descrive il suo processo e decisioni per dedurre PERSONALITÀ
3. Le risposte su AI per dedurre AI STYLE

RISPONDI SOLO CON JSON VALIDO:
{
    "role": "uno tra: builder, designer, strategist, communicator, operator, guide",
    "personality": "uno tra: chaos, order, minimal, rebel, warm, data",
    "ai_style": "uno tra: cyborg, hybrid, artisan",
    "combo": "Role × Personality × AI_Style (es: Builder × Chaos × Cyborg)",
    "reasoning": "Una frase che spiega perché hai scelto questa combinazione",
    "tagline": "Una tagline di 5-7 parole che cattura l'essenza della persona"
}"""

        # Prepara il contenuto da analizzare
        analysis_content = f"""
NOME: {user_data.get('nome', '')} {user_data.get('cognome', '')}

CV/BACKGROUND:
{user_data.get('cv_content', 'Non fornito')}

SUPERPOTERE:
{user_data.get('superpotere', 'Non specificato')}

PRESENTAZIONE:
{user_data.get('presentazione', 'Non fornita')}

DECISIONE CONTRO CORRENTE:
{user_data.get('against_data', 'Non specificata')}

PROGETTI:
{json.dumps(user_data.get('projects', []), ensure_ascii=False)}

PEGGIOR DECISIONE:
{user_data.get('worst_decision', 'Non specificata')}

ERESIA PROFESSIONALE:
{user_data.get('heresy', 'Non specificata')}

ANTI-SKILLS:
{user_data.get('anti_skills', 'Non specificate')}

RED FLAGS:
{user_data.get('red_flags', 'Non specificati')}

FALLIMENTO PIÙ GRANDE:
{user_data.get('biggest_failure', 'Non specificato')}

PATTERN DI FALLIMENTO:
{user_data.get('pattern_failure', 'Non specificato')}

AI - COSA USA:
{user_data.get('ai_guilty', 'Non specificato')}

AI - COSA NON USA MAI:
{user_data.get('ai_never', 'Non specificato')}

AI - MEGLIO DI ME:
{user_data.get('ai_better', 'Non specificato')}

UMANO - MEGLIO DELL'AI:
{user_data.get('human_better', 'Non specificato')}

DELTA STORY:
{user_data.get('delta_story', 'Non specificata')}

COMUNICAZIONE:
{user_data.get('communication', 'Non specificata')}

CRASH TRIGGERS:
{user_data.get('crash_triggers', 'Non specificati')}

BIAS NOTI:
{user_data.get('known_biases', 'Non specificati')}

RABBIT HOLE ATTUALE:
{user_data.get('rabbit_hole', 'Non specificato')}

COSA VUOLE IMPARARE:
{user_data.get('learning_next', 'Non specificato')}

PROGETTO DEI SOGNI:
{user_data.get('dream_project', 'Non specificato')}
"""

        try:
            from langchain_core.prompts import ChatPromptTemplate
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{content}")
            ])
            
            chain = prompt | self.llm
            response = chain.invoke({"content": analysis_content})
            
            # Parse JSON response
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Clean up response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            result = json.loads(response_text.strip())
            
            # Aggiungi nome creativo
            archetype_name = self.get_archetype_name(
                result.get('role', 'builder'),
                result.get('personality', 'order'),
                result.get('ai_style', 'hybrid')
            )
            result['archetype_name'] = archetype_name
            result['combo_display'] = f"{archetype_name} = {result.get('combo', '')}"
            
            return result
            
        except Exception as e:
            print(f"Archetype detection error: {e}")
            # Fallback intelligente basato su keyword
            return self._fallback_detection(user_data)
    
    def _fallback_detection(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback detection basato su keyword analysis"""
        
        all_text = " ".join([
            str(v) for v in user_data.values() if isinstance(v, str)
        ]).lower()
        
        # Detect role
        role = "builder"
        if any(w in all_text for w in ["design", "ux", "ui", "visual", "figma"]):
            role = "designer"
        elif any(w in all_text for w in ["strategy", "consult", "plan", "project manager", "pm"]):
            role = "strategist"
        elif any(w in all_text for w in ["write", "content", "copy", "marketing", "comunic"]):
            role = "communicator"
        elif any(w in all_text for w in ["data", "ops", "devops", "infrastructure", "analytics"]):
            role = "operator"
        elif any(w in all_text for w in ["teach", "mentor", "coach", "lead", "team"]):
            role = "guide"
        
        # Detect personality
        personality = "order"
        if any(w in all_text for w in ["caos", "experiment", "break", "curiosity", "esplor"]):
            personality = "chaos"
        elif any(w in all_text for w in ["minimal", "essential", "simple", "focus", "silenz"]):
            personality = "minimal"
        elif any(w in all_text for w in ["rebel", "contro", "sfida", "status quo", "odio"]):
            personality = "rebel"
        elif any(w in all_text for w in ["empath", "person", "team", "umano", "relazion"]):
            personality = "warm"
        elif any(w in all_text for w in ["data", "metric", "kpi", "numero", "risultat"]):
            personality = "data"
        
        # Detect AI style
        ai_style = "hybrid"
        ai_text = f"{user_data.get('ai_guilty', '')} {user_data.get('ai_never', '')}".lower()
        if any(w in ai_text for w in ["sempre", "tutto", "90%", "ovunque"]):
            ai_style = "cyborg"
        elif any(w in ai_text for w in ["mai", "rifiuto", "human", "mano"]):
            ai_style = "artisan"
        
        combo = f"{role.capitalize()} × {personality.capitalize()} × {ai_style.capitalize()}"
        archetype_name = self.get_archetype_name(role, personality, ai_style)
        
        return {
            "role": role,
            "personality": personality,
            "ai_style": ai_style,
            "combo": combo,
            "archetype_name": archetype_name,
            "combo_display": f"{archetype_name} = {combo}",
            "reasoning": "Archetipo determinato da analisi keyword (fallback)",
            "tagline": f"The {personality.capitalize()} {role.capitalize()}"
        }
