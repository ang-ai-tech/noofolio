"""
Narrative Composer Agent
Compone la narrativa finale del portfolio, creando un racconto coerente
che connette tutti gli elementi estratti dagli altri agenti.
"""

import os
import json
from typing import Dict, Any


class NarrativeComposer:
    """
    Compone la narrativa del Noofolio combinando:
    - Archetype
    - Pattern estratti
    - Decisioni scavate
    - Work signature
    """
    
    def __init__(self, provider: str = "anthropic"):
        self.provider = provider
        self.llm = self._init_llm()
    
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
    
    def run(
        self,
        user_data: Dict[str, Any],
        archetype: Dict[str, Any],
        patterns: Dict[str, Any] = None,
        decisions: Dict[str, Any] = None,
        signature: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Compone la narrativa finale integrando tutti gli insight.
        """
        
        personality = archetype.get('personality', 'order')
        
        # Tone mapping per personalità
        tone_map = {
            'chaos': 'energico, sperimentale, con salti logici inaspettati',
            'order': 'strutturato, chiaro, professionale ma non freddo',
            'minimal': 'essenziale, poetico, ogni parola pesa',
            'rebel': 'diretto, provocatorio, senza compromessi',
            'warm': 'personale, empatico, racconta storie',
            'data': 'preciso, basato su evidenze, numeri quando rilevanti'
        }
        
        tone = tone_map.get(personality, 'professionale')
        
        system_prompt = f"""Sei un narrative designer specializzato in personal branding autentico.

TONO DA USARE: {tone}

Devi comporre una NARRATIVA COERENTE per il Noofolio di questa persona.
Non stai scrivendo un CV. Stai raccontando CHI È questa persona quando lavora.

ELEMENTI DA INTEGRARE:
- Archetipo: {archetype.get('combo_display', archetype.get('combo', 'N/A'))}
- Pattern: {json.dumps(patterns, ensure_ascii=False) if patterns else 'Non disponibili'}
- Signature: {json.dumps(signature, ensure_ascii=False) if signature else 'Non disponibile'}

OUTPUT RICHIESTO (JSON):
{{
    "headline": "Una frase potente di apertura (max 10 parole)",
    "opening_story": "Paragrafo di apertura che cattura l'essenza (50-80 parole)",
    "core_narrative": "Il cuore della narrativa (100-150 parole)",
    "section_intros": {{
        "decision_log": "Intro per sezione decisioni (1-2 frasi)",
        "anti_skills": "Intro per sezione anti-skills (1-2 frasi)",
        "failure_museum": "Intro per sezione fallimenti (1-2 frasi)",
        "human_delta": "Intro per sezione AI vs Human (1-2 frasi)",
        "curiosity_stack": "Intro per sezione input intellettuali (1-2 frasi)",
        "human_api": "Intro per sezione come lavorare insieme (1-2 frasi)"
    }},
    "closing_statement": "Frase di chiusura memorabile",
    "meta_narrative": "Qual è il filo rosso che tiene insieme tutto?"
}}"""

        content = f"""
DATI UTENTE:
Nome: {user_data.get('nome', '')} {user_data.get('cognome', '')}
Superpotere: {user_data.get('superpotere', '')}
Presentazione: {user_data.get('presentazione', '')}
Eresia: {user_data.get('heresy', '')}
Fallimento: {user_data.get('biggest_failure', '')}
Human Delta: {user_data.get('delta_story', '')}
"""
        
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
            return self._fallback(user_data, archetype)
    
    def _fallback(self, user_data: Dict, archetype: Dict) -> Dict:
        name = f"{user_data.get('nome', '')} {user_data.get('cognome', '')}".strip() or "Professionista"
        return {
            "headline": f"{name}: {archetype.get('tagline', 'In costruzione')}",
            "opening_story": user_data.get('presentazione', '')[:200] or "Portfolio in costruzione.",
            "core_narrative": "",
            "section_intros": {
                "decision_log": "Le decisioni che mi hanno formato.",
                "anti_skills": "Cosa scelgo di non fare.",
                "failure_museum": "Dove ho sbagliato e cosa ho imparato.",
                "human_delta": "Cosa faccio meglio dell'AI.",
                "curiosity_stack": "Da dove vengono le mie idee.",
                "human_api": "Come lavorare con me."
            },
            "closing_statement": "",
            "meta_narrative": ""
        }
