"""
Signature Detector Agent
Identifica la "firma cognitiva" unica dell'utente - il modo distintivo in cui pensa e lavora.
"""

import os
import json
from typing import Dict, Any


class SignatureDetector:
    """
    Identifica la Work Signature - la firma inconscia che rende
    riconoscibile il lavoro di questa persona.
    """
    
    def __init__(self, provider: str = "anthropic"):
        self.provider = provider
        self.llm = self._init_llm()
    
    def _init_llm(self):
        if self.provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model="claude-sonnet-4-5-20250929",
                temperature=0.6,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        elif self.provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0.6,
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        else:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.6,
                api_key=os.getenv("OPENAI_API_KEY")
            )
    
    def run(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Rileva la firma cognitiva unica dell'utente.
        """
        
        system_prompt = """Sei un esperto nel rilevare la "firma cognitiva" dei professionisti.

La WORK SIGNATURE è il pattern inconscio che rende riconoscibile il lavoro di una persona.
È come una firma: unica, coerente, presente in tutto ciò che fa.

ANALIZZA le risposte e identifica:

1. SIGNATURE MOVES: Azioni/approcci che questa persona fa SEMPRE
   (es: "semplifica brutalmente", "cerca il dato nascosto", "connette domini distanti")

2. THINKING STYLE: Come processa le informazioni
   (es: visuale vs verbale, bottom-up vs top-down, divergente vs convergente)

3. UNIQUE LENS: La prospettiva unica attraverso cui vede i problemi
   (es: "vede tutto come sistema", "cerca sempre l'incentivo nascosto")

4. ANTI-SIGNATURE: Cosa NON fa mai, anche se altri lo farebbero
   (es: "mai segue la prima idea", "mai decide senza dormirci sopra")

5. FINGERPRINT PHRASE: Una frase che potrebbe essere attribuita SOLO a questa persona

RISPONDI SOLO CON JSON:
{
    "signature_moves": [
        {"move": "descrizione", "evidence": "esempio dalle risposte", "frequency": "sempre/spesso/quando conta"}
    ],
    "thinking_style": {
        "processing": "visuale/verbale/cinestetico",
        "approach": "bottom-up/top-down/oscillante",
        "mode": "divergente/convergente/iterativo",
        "pace": "veloce/riflessivo/burst"
    },
    "unique_lens": "Descrizione della prospettiva unica",
    "anti_signature": ["cosa non fa 1", "cosa non fa 2"],
    "fingerprint_phrase": "Una frase che solo questa persona direbbe",
    "overall_signature": "Una sintesi in 10-15 parole della firma cognitiva"
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
            return self._fallback()
    
    def _prepare_content(self, user_data: Dict) -> str:
        """Prepara tutto il contenuto disponibile"""
        sections = []
        for key, value in user_data.items():
            if value and isinstance(value, str) and len(value) > 10:
                sections.append(f"[{key.upper()}]\n{value}")
            elif value and isinstance(value, list):
                sections.append(f"[{key.upper()}]\n{json.dumps(value, ensure_ascii=False)}")
        return "\n\n".join(sections)
    
    def _fallback(self) -> Dict:
        return {
            "signature_moves": [],
            "thinking_style": {
                "processing": "mix",
                "approach": "oscillante",
                "mode": "iterativo",
                "pace": "riflessivo"
            },
            "unique_lens": "In analisi",
            "anti_signature": [],
            "fingerprint_phrase": "",
            "overall_signature": "Professionista con firma in definizione"
        }
