"""
Pattern Extractor Agent
Analizza le risposte dell'utente per estrarre pattern ricorrenti nel modo di pensare/lavorare.
"""

import os
import json
from typing import Dict, Any, List


class PatternExtractor:
    """
    Estrae pattern ricorrenti dalle risposte dell'utente:
    - Pattern decisionali
    - Pattern di errore
    - Pattern di successo
    - Temi ricorrenti
    """
    
    def __init__(self, provider: str = "anthropic"):
        self.provider = provider
        self.llm = self._init_llm()
    
    def _init_llm(self):
        if self.provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model="claude-sonnet-4-5-20250929",
                temperature=0.5,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        elif self.provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0.5,
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        else:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.5,
                api_key=os.getenv("OPENAI_API_KEY")
            )
    
    def run(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analizza i dati utente ed estrae pattern.
        """
        
        system_prompt = """Sei un analista di pattern comportamentali professionali.
Analizza le risposte dell'utente e identifica PATTERN RICORRENTI.

CERCA:
1. PATTERN DECISIONALI: Come prende decisioni? (dati vs intuito, veloce vs riflessivo, solo vs team)
2. PATTERN DI ERRORE: Errori che tende a ripetere (overconfidence, procrastinazione, scope creep...)
3. PATTERN DI SUCCESSO: Cosa funziona per questa persona quando ha successo
4. TEMI RICORRENTI: Parole, concetti, valori che ritornano spesso
5. CONTRADDIZIONI: Cose che dice di fare vs cose che sembra fare davvero

RISPONDI SOLO CON JSON:
{
    "decision_patterns": [
        {"pattern": "descrizione", "evidence": "citazione/esempio", "frequency": "alto/medio/basso"}
    ],
    "error_patterns": [
        {"pattern": "descrizione", "evidence": "citazione", "lesson_learned": "se presente"}
    ],
    "success_patterns": [
        {"pattern": "descrizione", "evidence": "citazione", "replicable": true/false}
    ],
    "recurring_themes": ["tema1", "tema2", ...],
    "contradictions": [
        {"says": "cosa dice", "seems": "cosa sembra", "interpretation": "possibile spiegazione"}
    ],
    "work_signature": "Una frase che cattura la 'firma' lavorativa unica di questa persona"
}"""

        content = self._prepare_content(user_data)
        
        try:
            from langchain_core.prompts import ChatPromptTemplate
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{content}")
            ])
            
            chain = prompt | self.llm
            response = chain.invoke({"content": content})
            
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            return json.loads(response_text.strip())
            
        except Exception as e:
            return self._fallback_patterns(user_data)
    
    def _prepare_content(self, user_data: Dict) -> str:
        """Prepara il contenuto per l'analisi"""
        sections = []
        
        for key, value in user_data.items():
            if value and isinstance(value, str) and len(value) > 10:
                sections.append(f"[{key.upper()}]\n{value}")
            elif value and isinstance(value, list):
                sections.append(f"[{key.upper()}]\n{json.dumps(value, ensure_ascii=False)}")
        
        return "\n\n".join(sections)
    
    def _fallback_patterns(self, user_data: Dict) -> Dict:
        """Pattern di fallback se l'LLM fallisce"""
        return {
            "decision_patterns": [],
            "error_patterns": [],
            "success_patterns": [],
            "recurring_themes": [],
            "contradictions": [],
            "work_signature": "Professionista in analisi"
        }
