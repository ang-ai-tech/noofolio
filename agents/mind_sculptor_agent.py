"""
Mind Sculptor Agent - Random Question Generator

Generates contextual random questions to deepen the user's profile
and improve NooMe's reliability.
"""

import anthropic
import openai
from pathlib import Path
import json
import random
import os


class MindSculptorAgent:
    """Generates random contextual questions for profile deepening"""

    def __init__(self, provider="anthropic"):
        self.provider = provider

    def generate_question(self, portfolio_data, previous_answers=None):
        """
        Generate a random but contextual question based on the user's profile

        Args:
            portfolio_data: User's portfolio JSON data
            previous_answers: List of previously answered questions (to avoid repeats)

        Returns:
            dict: {"text": "question text", "hint": "optional hint", "category": "category"}
        """

        # Extract context from portfolio
        context = self._extract_context(portfolio_data)
        previous_questions = [qa['question'] for qa in (previous_answers or [])]

        prompt = f"""Sei il Mind Sculptor di Noofolio, un sistema che genera domande profonde e casuali per mappare la mente umana.

CONTESTO UTENTE:
{context}

DOMANDE GIÀ FATTE:
{chr(10).join(['- ' + q for q in previous_questions]) if previous_questions else 'Nessuna'}

ISTRUZIONI:
1. Genera UNA domanda random ma contestuale al profilo dell'utente
2. La domanda deve essere:
   - Inaspettata e stimolante
   - Collegata al contesto professionale/personale dell'utente
   - Utile per capire come pensa, decide, reagisce
   - Non ripetitiva rispetto alle precedenti
3. Varia tra questi tipi:
   - Decisioni passate e biforcazioni critiche
   - Fallimenti e lezioni apprese
   - Opinioni controverse nel suo campo
   - Valori e linee rosse
   - Curiosità intellettuali
   - Abitudini di pensiero e bias
   - Scenari ipotetici ("E se...")
   - Pattern comportamentali

FORMATO RISPOSTA (JSON):
{{
  "text": "La domanda completa",
  "hint": "Un suggerimento opzionale per aiutare la risposta (max 1 frase)",
  "category": "decision|failure|opinion|values|curiosity|habits|hypothetical|patterns"
}}

Genera la domanda:"""

        if self.provider == "anthropic":
            return self._generate_anthropic(prompt)
        elif self.provider == "openai":
            return self._generate_openai(prompt)
        elif self.provider == "google":
            return self._generate_google(prompt)
        else:
            raise ValueError(f"Provider not supported: {self.provider}")

    def _extract_context(self, portfolio_data):
        """Extract relevant context from portfolio data"""
        identity = portfolio_data.get('identity', {})
        meta = portfolio_data.get('meta', {})
        analysis = portfolio_data.get('analysis', {})

        context_parts = []

        # Basic info
        if identity.get('name'):
            context_parts.append(f"Nome: {identity['name']}")

        # Archetype
        archetype = meta.get('archetype', {})
        if archetype.get('archetype_name'):
            context_parts.append(f"Archetipo: {archetype['archetype_name']}")

        # Patterns
        patterns = analysis.get('patterns', {})
        if patterns:
            context_parts.append(f"Pattern identificati: {json.dumps(patterns, ensure_ascii=False)[:200]}...")

        # Raw input highlights
        raw_input = portfolio_data.get('_raw_input', {})
        if raw_input.get('superpotere'):
            context_parts.append(f"Superpotere: {raw_input['superpotere']}")
        if raw_input.get('against_data'):
            context_parts.append(f"Ha una storia di decisioni contro corrente")
        if raw_input.get('biggest_failure'):
            context_parts.append(f"Ha condiviso fallimenti passati")

        return "\n".join(context_parts) if context_parts else "Profilo in costruzione"

    def _generate_anthropic(self, prompt):
        """Generate using Claude"""
        import os
        client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))

        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text
        # Extract JSON from response
        try:
            # Try to find JSON in response
            start = content.find('{')
            end = content.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = content[start:end]
                return json.loads(json_str)
            else:
                # Fallback
                return {
                    "text": content.strip(),
                    "hint": "",
                    "category": "general"
                }
        except:
            return {
                "text": content.strip(),
                "hint": "",
                "category": "general"
            }

    def _generate_openai(self, prompt):
        """Generate using OpenAI"""
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=400
        )

        content = response.choices[0].message.content

        try:
            start = content.find('{')
            end = content.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = content[start:end]
                return json.loads(json_str)
            else:
                return {
                    "text": content.strip(),
                    "hint": "",
                    "category": "general"
                }
        except:
            return {
                "text": content.strip(),
                "hint": "",
                "category": "general"
            }

    def _generate_google(self, prompt):
        """Generate using Google Gemini"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)

            content = response.text

            try:
                start = content.find('{')
                end = content.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = content[start:end]
                    return json.loads(json_str)
                else:
                    return {
                        "text": content.strip(),
                        "hint": "",
                        "category": "general"
                    }
            except:
                return {
                    "text": content.strip(),
                    "hint": "",
                    "category": "general"
                }
        except ImportError:
            return {
                "text": "Errore: Google Generative AI SDK non installato. Esegui: pip install google-generativeai",
                "hint": "",
                "category": "error"
            }
