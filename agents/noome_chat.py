"""
NooMe Chat Agent - My MindMirror
Clone conversazionale che risponde come l'utente basandosi sui suoi dati.
"""

import os
import json
from typing import Dict, Any, List
from pathlib import Path


class NooMeChat:
    """
    Il clone conversazionale dell'utente.
    Risponde alle domande basandosi sul contesto del Noofolio.
    """
    
    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        self.llm = self._init_llm()
        self.corrections: List[Dict] = []
    
    def _init_llm(self):
        if self.provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model="claude-sonnet-4-5-20250929",
                temperature=0.7,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        elif self.provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0.7,
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        else:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )
    
    def load_corrections(self, profile_id: str):
        """Carica le correzioni precedenti per questo profilo"""
        corrections_path = Path(__file__).parent.parent / f"data/corrections/{profile_id}.json"
        if corrections_path.exists():
            with open(corrections_path, 'r', encoding='utf-8') as f:
                self.corrections = json.load(f)
    
    def save_correction(self, profile_id: str, question: str, wrong_answer: str, correct_answer: str):
        """Salva una correzione per migliorare risposte future"""
        correction = {
            "question": question,
            "wrong_answer": wrong_answer,
            "correct_answer": correct_answer
        }
        self.corrections.append(correction)
        
        corrections_path = Path(__file__).parent.parent / f"data/corrections/{profile_id}.json"
        corrections_path.parent.mkdir(parents=True, exist_ok=True)
        with open(corrections_path, 'w', encoding='utf-8') as f:
            json.dump(self.corrections, f, ensure_ascii=False, indent=2)
    
    def respond(self, question: str, portfolio_data: Dict[str, Any], profile_id: str = None) -> str:
        """
        Risponde a una domanda come se fosse l'utente.
        """
        
        # Carica correzioni se disponibili
        if profile_id:
            self.load_corrections(profile_id)
        
        # Prepara contesto dalle correzioni
        corrections_context = ""
        if self.corrections:
            corrections_context = "\n\nCORREZIONI PRECEDENTI (usa queste come ground truth):\n"
            for c in self.corrections[-10:]:  # Ultime 10 correzioni
                corrections_context += f"- Domanda: {c['question']}\n  Risposta corretta: {c['correct_answer']}\n"
        
        # Estrai info chiave dal portfolio
        identity = portfolio_data.get('identity', {})
        name = identity.get('name', 'Professionista')
        
        # Converti portfolio in stringa JSON (senza variabili template)
        portfolio_str = json.dumps(portfolio_data, ensure_ascii=False, indent=2)
        
        system_prompt = f"""Sei il clone digitale di {name}. Rispondi come se fossi {name} in prima persona.

REGOLE:
1. Rispondi SEMPRE in prima persona ("Io...", "Nel mio caso...", "La mia esperienza...")
2. Basa le risposte SOLO sui dati forniti. Non inventare.
3. Se non hai informazioni sufficienti, dì "Non ho condiviso dettagli su questo nel mio Noofolio"
4. Mantieni il tono e la personalità che emergono dai dati
5. Sii conciso ma autentico
6. Cita la sezione del Noofolio da cui trai l'informazione quando rilevante

CONTESTO DEL NOOFOLIO:
{portfolio_str}
{corrections_context}

Rispondi alla domanda del recruiter/visitatore come farebbe {name}."""

        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=question)
            ]
            
            response = self.llm.invoke(messages)
            
            response_text = response.content if hasattr(response, 'content') else str(response)
            return response_text
            
        except Exception as e:
            return f"Mi dispiace, al momento non riesco a elaborare la domanda. Errore: {str(e)}"
    
    def suggest_questions(self, portfolio_data: Dict[str, Any]) -> List[str]:
        """Suggerisce domande interessanti basate sul portfolio"""
        
        suggestions = []
        
        # Basate sulle sezioni popolate
        if portfolio_data.get('decision_log', {}).get('projects'):
            suggestions.append("Come hai gestito la decisione più difficile nel tuo ultimo progetto?")
        
        if portfolio_data.get('failure_museum', {}).get('biggest'):
            suggestions.append("Cosa hai imparato dal tuo fallimento più grande?")
        
        if portfolio_data.get('human_delta', {}).get('delta_story'):
            suggestions.append("Puoi farmi un esempio di quando hai fatto meglio dell'AI?")
        
        if portfolio_data.get('human_api', {}).get('crash_triggers'):
            suggestions.append("Come preferisci ricevere feedback?")
        
        if portfolio_data.get('curiosity_stack', {}).get('rabbit_hole'):
            suggestions.append("Cosa stai esplorando in questo momento?")
        
        if portfolio_data.get('whats_next', {}).get('dream_project'):
            suggestions.append("Qual è il tuo progetto dei sogni?")
        
        # Default suggestions
        if len(suggestions) < 3:
            suggestions.extend([
                "Come affronteresti un progetto con budget e tempo limitati?",
                "Qual è il tuo processo quando inizi un nuovo progetto?",
                "Come gestisci i conflitti nel team?"
            ])
        
        return suggestions[:5]
