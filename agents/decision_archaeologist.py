"""
Decision Archaeologist Agent
Scava nelle decisioni passate dell'utente per costruire un "Decision Tree" delle scelte chiave.
"""

import os
import json
from typing import Dict, Any, List


class DecisionArchaeologist:
    """
    Analizza le decisioni passate e costruisce:
    - Albero decisionale con biforcazioni
    - "Roads Not Taken" - strade scartate
    - Criteri decisionali impliciti
    """
    
    def __init__(self, provider: str = "anthropic"):
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
        Analizza decisioni e costruisce l'albero decisionale.
        """
        
        system_prompt = """Sei un archeologo delle decisioni professionali.
Analizza le risposte dell'utente e ricostruisci le DECISIONI CHIAVE della sua carriera.

Per ogni decisione importante, identifica:
1. IL BIVIO: Quale era la scelta da fare?
2. LE OPZIONI: Quali erano le alternative?
3. LA SCELTA: Cosa ha scelto?
4. IL CRITERIO: Perché ha scelto così? (valori, dati, intuito, pressioni?)
5. LA STRADA SCARTATA: Cosa sarebbe successo con l'altra scelta?
6. IL RISULTATO: Come è andata?

RISPONDI SOLO CON JSON:
{
    "key_decisions": [
        {
            "title": "Nome breve della decisione",
            "context": "Situazione che ha richiesto la scelta",
            "options": [
                {"option": "Opzione A", "pros": ["pro1"], "cons": ["con1"]},
                {"option": "Opzione B", "pros": ["pro1"], "cons": ["con1"]}
            ],
            "chosen": "Quale opzione ha scelto",
            "criteria": "Perché ha scelto così",
            "road_not_taken": "Cosa sarebbe successo altrimenti",
            "outcome": "Come è andata",
            "lesson": "Cosa ha imparato"
        }
    ],
    "decision_style": {
        "speed": "veloce/riflessivo/dipende",
        "input_preference": "dati/intuito/mix",
        "risk_tolerance": "alto/medio/basso",
        "social_preference": "solo/consulta/consenso"
    },
    "implicit_values": ["valore1", "valore2"],
    "decision_traps": ["trappola ricorrente 1", "trappola 2"]
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
            return self._fallback(user_data)
    
    def _prepare_content(self, user_data: Dict) -> str:
        """Prepara contenuto rilevante per analisi decisioni"""
        relevant_keys = [
            'against_data', 'projects', 'worst_decision',
            'biggest_failure', 'pattern_failure', 'belief_murdered',
            'heresy', 'anti_skills', 'delta_story'
        ]
        
        sections = []
        for key in relevant_keys:
            value = user_data.get(key)
            if value:
                if isinstance(value, str) and len(value) > 10:
                    sections.append(f"[{key.upper()}]\n{value}")
                elif isinstance(value, list):
                    sections.append(f"[{key.upper()}]\n{json.dumps(value, ensure_ascii=False)}")
        
        return "\n\n".join(sections)
    
    def _fallback(self, user_data: Dict) -> Dict:
        """Fallback se LLM fallisce"""
        return {
            "key_decisions": [],
            "decision_style": {
                "speed": "dipende",
                "input_preference": "mix",
                "risk_tolerance": "medio",
                "social_preference": "consulta"
            },
            "implicit_values": [],
            "decision_traps": []
        }
