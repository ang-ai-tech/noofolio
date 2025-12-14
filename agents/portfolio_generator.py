"""
Portfolio Generator Agent
Genera HTML e JSON del Noofolio basandosi sull'archetipo rilevato.
"""

import json
from typing import Dict, Any, Tuple
from datetime import datetime


class PortfolioGenerator:
    """
    Genera il portfolio HTML e JSON basandosi sull'archetipo
    e i dati dell'utente.
    """
    
    # Configurazioni per personalità con stili più accattivanti
    PERSONALITY_CONFIGS = {
        "chaos": {
            "bg_gradient": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
            "accent": "#ff6b6b",
            "accent2": "#4ecdc4",
            "accent3": "#ffd93d",
            "font_main": "'JetBrains Mono', monospace",
            "font_heading": "'Space Grotesk', sans-serif",
            "card_style": "transform: rotate(-0.5deg); transition: all 0.3s ease;",
            "card_hover": "transform: rotate(0deg) translateY(-4px); box-shadow: 0 12px 24px rgba(255, 107, 107, 0.3);",
            "layout": "chaotic",
            "badge_style": "background: linear-gradient(135deg, #ff6b6b, #4ecdc4); animation: pulse 2s ease-in-out infinite;",
            "section_decoration": "border-left: 3px solid #ff6b6b; padding-left: 1.5rem;"
        },
        "order": {
            "bg_gradient": "linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%)",
            "accent": "#3b82f6",
            "accent2": "#1e40af",
            "accent3": "#60a5fa",
            "font_main": "'Inter', sans-serif",
            "font_heading": "'Inter', sans-serif",
            "card_style": "box-shadow: 0 1px 3px rgba(0,0,0,0.1); transition: all 0.3s ease;",
            "card_hover": "box-shadow: 0 8px 16px rgba(59, 130, 246, 0.2); transform: translateY(-2px);",
            "layout": "grid",
            "badge_style": "background: linear-gradient(135deg, #3b82f6, #1e40af); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);",
            "section_decoration": "border-bottom: 2px solid #3b82f6; padding-bottom: 0.5rem;"
        },
        "minimal": {
            "bg_gradient": "#ffffff",
            "accent": "#000000",
            "accent2": "#666666",
            "accent3": "#999999",
            "font_main": "'Libre Baskerville', serif",
            "font_heading": "'Libre Baskerville', serif",
            "card_style": "border: none; border-bottom: 1px solid #e5e7eb; transition: all 0.3s ease;",
            "card_hover": "border-bottom: 1px solid #000000; padding-left: 1rem;",
            "layout": "minimal",
            "badge_style": "background: #000000; border: 2px solid #000000;",
            "section_decoration": "border-bottom: 1px solid #000000; padding-bottom: 0.25rem; margin-bottom: 2rem;"
        },
        "rebel": {
            "bg_gradient": "#000000",
            "accent": "#ff0000",
            "accent2": "#ffffff",
            "accent3": "#ff6b6b",
            "font_main": "'Space Mono', monospace",
            "font_heading": "'Space Mono', monospace",
            "card_style": "border: 2px solid #ff0000; transition: all 0.3s ease; position: relative;",
            "card_hover": "border-color: #fff; box-shadow: 0 0 20px rgba(255, 0, 0, 0.5); transform: scale(1.02);",
            "layout": "rebel",
            "badge_style": "background: #ff0000; border: 2px solid #ff0000; text-transform: uppercase; letter-spacing: 0.15em; animation: glitch 3s infinite;",
            "section_decoration": "border-left: 4px solid #ff0000; padding-left: 2rem; position: relative;"
        },
        "warm": {
            "bg_gradient": "linear-gradient(135deg, #fff5e6 0%, #ffecd2 100%)",
            "accent": "#e74c3c",
            "accent2": "#f39c12",
            "accent3": "#e67e22",
            "font_main": "'Merriweather', serif",
            "font_heading": "'Playfair Display', serif",
            "card_style": "border-radius: 20px; box-shadow: 0 4px 12px rgba(231, 76, 60, 0.1); transition: all 0.3s ease;",
            "card_hover": "box-shadow: 0 8px 24px rgba(231, 76, 60, 0.2); transform: translateY(-4px);",
            "layout": "warm",
            "badge_style": "background: linear-gradient(135deg, #e74c3c, #f39c12); border-radius: 30px; box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);",
            "section_decoration": "border-radius: 12px 0 0 0; border-top: 3px solid #e74c3c; border-left: 3px solid #f39c12; padding: 0.5rem 0 0 1rem;"
        },
        "data": {
            "bg_gradient": "#0f172a",
            "accent": "#22c55e",
            "accent2": "#3b82f6",
            "accent3": "#8b5cf6",
            "font_main": "'Roboto Mono', monospace",
            "font_heading": "'Roboto', sans-serif",
            "card_style": "background: linear-gradient(135deg, rgba(34, 197, 94, 0.05), rgba(59, 130, 246, 0.05)); border-left: 3px solid #22c55e; transition: all 0.3s ease;",
            "card_hover": "background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(59, 130, 246, 0.1)); border-left-width: 5px; transform: translateX(4px);",
            "layout": "dashboard",
            "badge_style": "background: linear-gradient(135deg, #22c55e, #3b82f6); box-shadow: 0 0 20px rgba(34, 197, 94, 0.3); font-family: 'Roboto Mono', monospace;",
            "section_decoration": "border-left: 3px solid #22c55e; border-bottom: 1px solid rgba(34, 197, 94, 0.3); padding-left: 1.5rem; padding-bottom: 0.5rem;"
        }
    }
    
    def __init__(self):
        pass
    
    def run(self, user_data: Dict[str, Any], archetype: Dict[str, Any]) -> Tuple[str, Dict]:
        """
        Genera HTML e JSON del portfolio.
        """
        
        # Prepara i dati strutturati
        portfolio_data = self._prepare_data(user_data, archetype)
        
        # Genera HTML
        html = self._generate_html(portfolio_data, archetype)
        
        return html, portfolio_data
    
    def _prepare_data(self, user_data: Dict, archetype: Dict) -> Dict:
        """Prepara i dati strutturati per il portfolio"""
        
        return {
            "meta": {
                "generated_at": datetime.now().isoformat(),
                "archetype": archetype,
                "version": "1.0"
            },
            "identity": {
                "name": f"{user_data.get('nome', '')} {user_data.get('cognome', '')}".strip(),
                "tagline": archetype.get('tagline', ''),
                "superpotere": user_data.get('superpotere', ''),
                "presentazione": user_data.get('presentazione', ''),
                "links": user_data.get('links', [])
            },
            "decision_log": {
                "against_current": user_data.get('against_data', ''),
                "projects": user_data.get('projects', []),
                "worst_decision": user_data.get('worst_decision', '')
            },
            "anti_skills": {
                "heresy": user_data.get('heresy', ''),
                "never_again": user_data.get('never_again', ''),
                "wont_do": user_data.get('anti_skills', ''),
                "red_flags": user_data.get('red_flags', '')
            },
            "failure_museum": {
                "biggest": user_data.get('biggest_failure', ''),
                "pattern": user_data.get('pattern_failure', ''),
                "belief_killed": user_data.get('belief_murdered', ''),
                "brutal_feedback": user_data.get('feedback_brutal', '')
            },
            "human_delta": {
                "ai_guilty": user_data.get('ai_guilty', ''),
                "ai_never": user_data.get('ai_never', ''),
                "ai_better": user_data.get('ai_better', ''),
                "human_better": user_data.get('human_better', ''),
                "delta_story": user_data.get('delta_story', '')
            },
            "curiosity_stack": {
                "masterclass": user_data.get('masterclass', ''),
                "books": user_data.get('books', ''),
                "media": user_data.get('media', ''),
                "people": user_data.get('people', ''),
                "unexpected_connection": user_data.get('unexpected_connection', ''),
                "rabbit_hole": user_data.get('rabbit_hole', '')
            },
            "human_api": {
                "communication": user_data.get('communication', ''),
                "feedback_style": user_data.get('feedback_style', ''),
                "crash_triggers": user_data.get('crash_triggers', ''),
                "known_biases": user_data.get('known_biases', ''),
                "ideal_conditions": user_data.get('ideal_conditions', '')
            },
            "whats_next": {
                "learning": user_data.get('learning_next', ''),
                "two_years": user_data.get('two_years', ''),
                "dream_project": user_data.get('dream_project', '')
            }
        }
    
    def _generate_html(self, data: Dict, archetype: Dict) -> str:
        """Genera l'HTML completo del portfolio"""
        
        personality = archetype.get('personality', 'order')
        config = self.PERSONALITY_CONFIGS.get(personality, self.PERSONALITY_CONFIGS['order'])
        
        is_dark = personality in ['chaos', 'rebel', 'data']
        text_color = "#ffffff" if is_dark else "#1a1a2e"
        text_muted = "#94a3b8" if is_dark else "#64748b"
        card_bg = "rgba(255,255,255,0.05)" if is_dark else "rgba(0,0,0,0.03)"
        
        name = data['identity']['name'] or "Professionista"
        
        html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Noofolio | {name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Libre+Baskerville:wght@400;700&family=Space+Mono:wght@400;700&family=Space+Grotesk:wght@400;500;600;700&family=Playfair+Display:wght@400;600;700&family=Merriweather:wght@300;400;700&family=Roboto+Mono:wght@400;500&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes pulse {{
            0%, 100% {{
                transform: scale(1);
            }}
            50% {{
                transform: scale(1.05);
            }}
        }}

        @keyframes glitch {{
            0%, 90%, 100% {{
                transform: translate(0);
            }}
            92% {{
                transform: translate(-2px, 2px);
            }}
            94% {{
                transform: translate(2px, -2px);
            }}
            96% {{
                transform: translate(-2px, -2px);
            }}
            98% {{
                transform: translate(2px, 2px);
            }}
        }}

        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateX(-20px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}

        body {{
            font-family: {config['font_main']};
            background: {config['bg_gradient']};
            color: {text_color};
            line-height: 1.7;
            min-height: 100vh;
            animation: fadeInUp 0.6s ease-out;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }}
        
        /* Header */
        .header {{
            text-align: {"left" if personality == "rebel" else "center"};
            margin-bottom: 4rem;
            {"border-left: 4px solid " + config['accent'] + "; padding-left: 2rem;" if personality == "rebel" else ""}
        }}
        
        .header h1 {{
            font-family: {config['font_heading']};
            font-size: {"2.5rem" if personality == "minimal" else "3.5rem"};
            font-weight: 700;
            margin-bottom: 0.5rem;
            {"text-transform: uppercase; letter-spacing: 0.1em;" if personality == "rebel" else ""}
            {"color: " + config['accent'] + ";" if personality in ["rebel", "chaos"] else ""}
        }}
        
        .tagline {{
            font-size: 1.25rem;
            color: {config['accent']};
            margin-bottom: 1rem;
            {"font-style: italic;" if personality in ["minimal", "warm"] else ""}
        }}
        
        .archetype-badge {{
            display: inline-block;
            color: #fff;
            padding: 0.75rem 1.75rem;
            border-radius: {"0" if personality == "rebel" else "30px"};
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            {"text-transform: uppercase;" if personality == "rebel" else ""}
            {config['badge_style']}
        }}
        
        /* Section */
        .section {{
            margin-bottom: 3rem;
        }}
        
        .section {{
            animation: slideIn 0.6s ease-out;
            animation-fill-mode: both;
        }}

        .section:nth-child(1) {{ animation-delay: 0.1s; }}
        .section:nth-child(2) {{ animation-delay: 0.2s; }}
        .section:nth-child(3) {{ animation-delay: 0.3s; }}
        .section:nth-child(4) {{ animation-delay: 0.4s; }}
        .section:nth-child(5) {{ animation-delay: 0.5s; }}

        .section-title {{
            font-family: {config['font_heading']};
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: {config['accent']};
            display: flex;
            align-items: center;
            gap: 0.75rem;
            {config['section_decoration']}
            {"text-transform: uppercase; letter-spacing: 0.1em;" if personality == "rebel" else ""}
        }}
        
        .section-title .icon {{
            font-size: 1.25rem;
        }}
        
        /* Cards */
        .card {{
            background: {card_bg};
            border: 1px solid {"rgba(255,255,255,0.1)" if is_dark else "rgba(0,0,0,0.08)"};
            border-radius: {"0" if personality == "rebel" else "12px"};
            padding: 1.5rem;
            margin-bottom: 1rem;
            {config['card_style']}
        }}

        .card:hover {{
            {config['card_hover']}
        }}

        .card-title {{
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: {config['accent2']};
            font-size: 1.05rem;
        }}

        .card p {{
            color: {text_muted};
            white-space: pre-line;
        }}
        
        /* Grid Layout */
        .grid-2 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
        }}
        
        /* Quote */
        .quote {{
            font-size: 1.25rem;
            font-style: italic;
            padding: 1.5rem;
            border-left: 4px solid {config['accent']};
            background: {card_bg};
            margin: 2rem 0;
            {"font-family: " + config['font_heading'] + ";" if personality in ["minimal", "warm"] else ""}
        }}
        
        /* Tags */
        .tag {{
            display: inline-block;
            background: {config['accent']}20;
            color: {config['accent']};
            padding: 0.25rem 0.75rem;
            border-radius: {"0" if personality == "rebel" else "15px"};
            font-size: 0.85rem;
            margin: 0.25rem;
            {"border: 1px solid " + config['accent'] + ";" if personality == "rebel" else ""}
        }}
        
        /* Links */
        .links {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: {"flex-start" if personality == "rebel" else "center"};
            margin-top: 1.5rem;
        }}
        
        .links a {{
            color: {config['accent']};
            text-decoration: none;
            padding: 0.5rem 1rem;
            border: 1px solid {config['accent']};
            border-radius: {"0" if personality == "rebel" else "8px"};
            transition: all 0.3s ease;
        }}
        
        .links a:hover {{
            background: {config['accent']};
            color: {"#000" if personality in ["warm", "order"] else "#fff"};
        }}
        
        /* Delta Section */
        .delta-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0;
        }}
        
        .delta-col {{
            padding: 1.5rem;
        }}
        
        .delta-col.ai {{
            background: {"rgba(239, 68, 68, 0.1)" if is_dark else "#fee2e2"};
            border-radius: {"0" if personality == "rebel" else "12px 0 0 12px"};
        }}
        
        .delta-col.human {{
            background: {"rgba(34, 197, 94, 0.1)" if is_dark else "#dcfce7"};
            border-radius: {"0" if personality == "rebel" else "0 12px 12px 0"};
        }}
        
        .delta-col h4 {{
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 1rem;
        }}
        
        .delta-col.ai h4 {{
            color: #ef4444;
        }}
        
        .delta-col.human h4 {{
            color: #22c55e;
        }}
        
        /* Human API */
        .api-item {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            align-items: flex-start;
        }}
        
        .api-icon {{
            font-size: 1.5rem;
            min-width: 40px;
        }}
        
        .api-content h4 {{
            font-weight: 600;
            margin-bottom: 0.25rem;
        }}
        
        .api-content p {{
            color: {text_muted};
            font-size: 0.95rem;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 3rem 0;
            margin-top: 3rem;
            border-top: 1px solid {"rgba(255,255,255,0.1)" if is_dark else "rgba(0,0,0,0.1)"};
            color: {text_muted};
            font-size: 0.9rem;
        }}
        
        .footer a {{
            color: {config['accent']};
            text-decoration: none;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .container {{
                padding: 2rem 1rem;
            }}
            .header h1 {{
                font-size: 2rem;
            }}
            .delta-grid {{
                grid-template-columns: 1fr;
            }}
            .delta-col {{
                border-radius: {"0" if personality == "rebel" else "12px"} !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <header class="header">
            <h1>{name}</h1>
            <p class="tagline">{data['identity']['tagline'] or archetype.get('tagline', '')}</p>
            <span class="archetype-badge">{archetype.get('combo_display', archetype.get('combo', 'Professional'))}</span>
            
            {self._render_links(data['identity'].get('links', []))}
        </header>
        
        {self._render_superpotere(data['identity'], config, card_bg)}
        
        {self._render_decision_log(data['decision_log'], config, card_bg)}
        
        {self._render_anti_skills(data['anti_skills'], config, card_bg)}
        
        {self._render_failure_museum(data['failure_museum'], config, card_bg)}
        
        {self._render_human_delta(data['human_delta'], config)}
        
        {self._render_curiosity_stack(data['curiosity_stack'], config, card_bg)}
        
        {self._render_human_api(data['human_api'], config)}
        
        {self._render_whats_next(data['whats_next'], config, card_bg)}
        
        <!-- FOOTER -->
        <footer class="footer">
            <p>Generated by <a href="#">Noofolio</a> — Your work, not your role.</p>
            <p style="margin-top: 0.5rem; opacity: 0.7;">From the noosphere: decisions, judgment, and proof.</p>
        </footer>
    </div>
</body>
</html>"""
        
        return html
    
    def _render_links(self, links):
        if not links:
            return ""
        
        html = '<div class="links">'
        for link in links:
            if link.get('url'):
                icon = {
                    'LinkedIn': '💼',
                    'GitHub': '💻',
                    'Behance': '🎨',
                    'Articolo': '📝',
                    'Altro': '🔗'
                }.get(link.get('type', 'Altro'), '🔗')
                html += f'<a href="{link["url"]}" target="_blank">{icon} {link.get("type", "Link")}</a>'
        html += '</div>'
        return html
    
    def _render_superpotere(self, identity, config, card_bg):
        if not identity.get('superpotere') and not identity.get('presentazione'):
            return ""
        
        html = '<section class="section">'
        
        if identity.get('superpotere'):
            html += f'''
            <div class="quote">
                ⚡ {identity['superpotere']}
            </div>
            '''
        
        if identity.get('presentazione'):
            html += f'''
            <div class="card">
                <p>{identity['presentazione']}</p>
            </div>
            '''
        
        html += '</section>'
        return html
    
    def _render_decision_log(self, data, config, card_bg):
        if not any([data.get('against_current'), data.get('projects'), data.get('worst_decision')]):
            return ""
        
        html = '''
        <section class="section">
            <h2 class="section-title"><span class="icon">🌳</span> Decision Log</h2>
        '''
        
        if data.get('against_current'):
            html += f'''
            <div class="card">
                <div class="card-title">Decisione Contro Corrente</div>
                <p>{data['against_current']}</p>
            </div>
            '''
        
        projects = data.get('projects', [])
        if projects:
            for proj in projects:
                if proj.get('name'):
                    html += f'''
                    <div class="card">
                        <div class="card-title">📁 {proj['name']}</div>
                        <p>{proj.get('fork', '')}</p>
                        {f'<p style="margin-top: 0.5rem;"><a href="{proj["proof"]}" target="_blank" style="color: {config["accent"]};">🔗 Proof</a></p>' if proj.get('proof') else ''}
                    </div>
                    '''
        
        if data.get('worst_decision'):
            html += f'''
            <div class="card">
                <div class="card-title">💀 Peggior Decisione</div>
                <p>{data['worst_decision']}</p>
            </div>
            '''
        
        html += '</section>'
        return html
    
    def _render_anti_skills(self, data, config, card_bg):
        if not any(data.values()):
            return ""
        
        html = '''
        <section class="section">
            <h2 class="section-title"><span class="icon">🚫</span> Anti-Skills & Fit Check</h2>
            <div class="grid-2">
        '''
        
        if data.get('heresy'):
            html += f'''
            <div class="card">
                <div class="card-title">🔥 Eresia Professionale</div>
                <p>{data['heresy']}</p>
            </div>
            '''
        
        if data.get('wont_do'):
            html += f'''
            <div class="card">
                <div class="card-title">🛑 Cosa NON Faccio</div>
                <p>{data['wont_do']}</p>
            </div>
            '''
        
        if data.get('never_again'):
            html += f'''
            <div class="card">
                <div class="card-title">⛔ Mai Più</div>
                <p>{data['never_again']}</p>
            </div>
            '''
        
        if data.get('red_flags'):
            html += f'''
            <div class="card">
                <div class="card-title">🚩 Red Flags</div>
                <p>{data['red_flags']}</p>
            </div>
            '''
        
        html += '</div></section>'
        return html
    
    def _render_failure_museum(self, data, config, card_bg):
        if not any(data.values()):
            return ""
        
        html = '''
        <section class="section">
            <h2 class="section-title"><span class="icon">💀</span> Failure Museum</h2>
        '''
        
        if data.get('biggest'):
            html += f'''
            <div class="card">
                <div class="card-title">💥 Il Fallimento</div>
                <p>{data['biggest']}</p>
            </div>
            '''
        
        if data.get('pattern'):
            html += f'''
            <div class="card">
                <div class="card-title">🔄 Pattern Ricorrente</div>
                <p>{data['pattern']}</p>
            </div>
            '''
        
        if data.get('belief_killed'):
            html += f'''
            <div class="card">
                <div class="card-title">💔 Credenza Assassinata</div>
                <p>{data['belief_killed']}</p>
            </div>
            '''
        
        if data.get('brutal_feedback'):
            html += f'''
            <div class="card">
                <div class="card-title">🔪 Feedback Brutale</div>
                <p>{data['brutal_feedback']}</p>
            </div>
            '''
        
        html += '</section>'
        return html
    
    def _render_human_delta(self, data, config):
        if not any(data.values()):
            return ""
        
        html = '''
        <section class="section">
            <h2 class="section-title"><span class="icon">🤖</span> The Human Delta</h2>
            <div class="delta-grid">
                <div class="delta-col ai">
                    <h4>🤖 AI</h4>
        '''
        
        if data.get('ai_guilty'):
            html += f'<p><strong>Uso per:</strong><br>{data["ai_guilty"]}</p>'
        
        if data.get('ai_better'):
            html += f'<p style="margin-top: 1rem;"><strong>È meglio di me:</strong><br>{data["ai_better"]}</p>'
        
        html += '''
                </div>
                <div class="delta-col human">
                    <h4>🧠 IO</h4>
        '''
        
        if data.get('ai_never'):
            html += f'<p><strong>Mai delegato:</strong><br>{data["ai_never"]}</p>'
        
        if data.get('human_better'):
            html += f'<p style="margin-top: 1rem;"><strong>Sono meglio io:</strong><br>{data["human_better"]}</p>'
        
        html += '</div></div>'
        
        if data.get('delta_story'):
            html += f'''
            <div class="card" style="margin-top: 1rem;">
                <div class="card-title">📖 La Storia del Delta</div>
                <p>{data['delta_story']}</p>
            </div>
            '''
        
        html += '</section>'
        return html
    
    def _render_curiosity_stack(self, data, config, card_bg):
        if not any(data.values()):
            return ""
        
        html = '''
        <section class="section">
            <h2 class="section-title"><span class="icon">📚</span> Curiosity Stack</h2>
            <p style="opacity: 0.7; margin-bottom: 1.5rem; font-style: italic;">La mia Intellectual Supply Chain: da dove vengono le idee</p>
        '''
        
        if data.get('masterclass'):
            html += f'''
            <div class="card">
                <div class="card-title">🎓 Masterclass Non-Lavorativa</div>
                <p>{data['masterclass']}</p>
            </div>
            '''
        
        # Input grid
        inputs = []
        if data.get('books'):
            inputs.append(('📚 Libri', data['books']))
        if data.get('media'):
            inputs.append(('🎬 Media', data['media']))
        if data.get('people'):
            inputs.append(('👤 Mentori', data['people']))
        
        if inputs:
            html += '<div class="grid-2">'
            for title, content in inputs:
                html += f'''
                <div class="card">
                    <div class="card-title">{title}</div>
                    <p>{content}</p>
                </div>
                '''
            html += '</div>'
        
        if data.get('unexpected_connection'):
            html += f'''
            <div class="card">
                <div class="card-title">🔗 Connessione Inaspettata</div>
                <p>{data['unexpected_connection']}</p>
            </div>
            '''
        
        if data.get('rabbit_hole'):
            html += f'''
            <div class="card">
                <div class="card-title">🐇 Rabbit Hole Attuale</div>
                <p>{data['rabbit_hole']}</p>
            </div>
            '''
        
        html += '</section>'
        return html
    
    def _render_human_api(self, data, config):
        if not any(data.values()):
            return ""
        
        html = '''
        <section class="section">
            <h2 class="section-title"><span class="icon">🧬</span> Human API — My OS</h2>
            <p style="opacity: 0.7; margin-bottom: 1.5rem; font-style: italic;">Come interfacciarsi con me: il mio manuale d'uso</p>
        '''
        
        items = [
            ('💬', 'Comunicazione', data.get('communication', '')),
            ('📝', 'Feedback', data.get('feedback_style', '')),
            ('💥', 'Crash Triggers', data.get('crash_triggers', '')),
            ('⚠️', 'Bias Noti', data.get('known_biases', '')),
            ('✨', 'Condizioni Ideali', data.get('ideal_conditions', ''))
        ]
        
        for icon, title, content in items:
            if content:
                html += f'''
                <div class="api-item">
                    <div class="api-icon">{icon}</div>
                    <div class="api-content">
                        <h4>{title}</h4>
                        <p>{content}</p>
                    </div>
                </div>
                '''
        
        html += '</section>'
        return html
    
    def _render_whats_next(self, data, config, card_bg):
        if not any(data.values()):
            return ""
        
        html = '''
        <section class="section">
            <h2 class="section-title"><span class="icon">🚀</span> What's Next</h2>
        '''
        
        if data.get('learning'):
            html += f'''
            <div class="card">
                <div class="card-title">📖 Voglio Imparare</div>
                <p>{data['learning']}</p>
            </div>
            '''
        
        if data.get('two_years'):
            html += f'''
            <div class="card">
                <div class="card-title">🔮 Tra 2 Anni</div>
                <p>{data['two_years']}</p>
            </div>
            '''
        
        if data.get('dream_project'):
            html += f'''
            <div class="card">
                <div class="card-title">🌟 Progetto dei Sogni</div>
                <p>{data['dream_project']}</p>
            </div>
            '''
        
        html += '</section>'
        return html
