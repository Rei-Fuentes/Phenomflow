"""
Parser de protocolos de entrevista.
Extrae preguntas y estructura del protocolo para orientar el análisis.
"""

import re
from typing import List, Dict, Optional


def parse_protocol(protocol_text: str) -> Dict:
    """
    Extrae preguntas y estructura del protocolo de entrevista.
    
    Args:
        protocol_text: Texto del protocolo (puede ser PDF parseado o texto plano)
    
    Returns:
        {
            "questions": [
                {
                    "number": int,
                    "text": str,
                    "type": "opening" | "core" | "probing" | "closing"
                },
                ...
            ],
            "total_questions": int,
            "themes": List[str]  # Temas identificados
        }
    """
    questions = []
    themes = set()
    
    # Patrones para detectar preguntas
    patterns = [
        r"^\d+[\.\)]\s*(.+\?)",  # 1. ¿Pregunta? o 1) ¿Pregunta?
        r"^[-•]\s*(.+\?)",        # - ¿Pregunta? o • ¿Pregunta?
        r"^[A-Z]\.\s*(.+\?)",     # A. ¿Pregunta?
        r"^P\d+:\s*(.+\?)",       # P1: ¿Pregunta?
    ]
    
    lines = protocol_text.split('\n')
    question_number = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Intentar detectar pregunta
        question_text = None
        for pattern in patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                question_text = match.group(1).strip()
                break
        
        # Si no hay match con patrones, buscar líneas que terminen en ?
        if not question_text and line.endswith('?'):
            question_text = line
        
        if question_text:
            question_number += 1
            question_type = classify_question(question_text)
            
            questions.append({
                "number": question_number,
                "text": question_text,
                "type": question_type
            })
            
            # Extraer temas
            extracted_themes = extract_themes(question_text)
            themes.update(extracted_themes)
    
    return {
        "questions": questions,
        "total_questions": len(questions),
        "themes": sorted(list(themes))
    }


def classify_question(question: str) -> str:
    """
    Clasifica el tipo de pregunta según su contenido.
    
    Returns:
        "opening" | "core" | "probing" | "closing"
    """
    q_lower = question.lower()
    
    # Preguntas de apertura
    opening_keywords = [
        "cuéntame", "describe", "cómo empezó", "cómo comenzó",
        "podrías contarme", "me gustaría que", "para empezar"
    ]
    
    # Preguntas centrales (experiencia directa)
    core_keywords = [
        "sentiste", "experimentaste", "qué pasó", "qué sucedió",
        "cómo fue", "qué viviste", "cómo lo viviste", "percibiste"
    ]
    
    # Preguntas de profundización
    probing_keywords = [
        "puedes dar un ejemplo", "específicamente", "en ese momento",
        "qué más", "y luego", "después de eso", "cómo así"
    ]
    
    # Preguntas de cierre
    closing_keywords = [
        "para terminar", "finalmente", "algo más que", "quieres agregar",
        "hay algo que no hayamos"
    ]
    
    if any(kw in q_lower for kw in opening_keywords):
        return "opening"
    elif any(kw in q_lower for kw in core_keywords):
        return "core"
    elif any(kw in q_lower for kw in probing_keywords):
        return "probing"
    elif any(kw in q_lower for kw in closing_keywords):
        return "closing"
    else:
        # Por defecto, si tiene palabras interrogativas, es probing
        if any(word in q_lower for word in ["qué", "cómo", "cuándo", "dónde", "por qué"]):
            return "probing"
        return "core"


def extract_themes(question: str) -> List[str]:
    """
    Extrae temas potenciales de una pregunta.
    
    Busca sustantivos clave que indiquen el tema de la pregunta.
    """
    themes = []
    q_lower = question.lower()
    
    # Temas comunes en investigación fenomenológica
    theme_keywords = {
        "experiencia": ["experiencia", "vivencia"],
        "emoción": ["emoción", "sentimiento", "afecto"],
        "cuerpo": ["cuerpo", "corporal", "físico", "sensación"],
        "pensamiento": ["pensamiento", "pensar", "reflexión", "idea"],
        "tiempo": ["tiempo", "momento", "duración", "temporalidad"],
        "relación": ["relación", "otro", "otros", "vínculo", "interacción"],
        "espacio": ["espacio", "lugar", "entorno", "ambiente"],
        "acción": ["acción", "hacer", "actuar", "comportamiento"],
        "significado": ["significado", "sentido", "importancia"],
    }
    
    for theme, keywords in theme_keywords.items():
        if any(kw in q_lower for kw in keywords):
            themes.append(theme)
    
    return themes


def format_protocol_for_prompt(protocol_data: Dict) -> str:
    """
    Formatea el protocolo parseado para incluirlo en el prompt de análisis.
    
    Returns:
        String formateado listo para incluir en el prompt
    """
    if not protocol_data or not protocol_data.get("questions"):
        return ""
    
    questions = protocol_data["questions"]
    themes = protocol_data.get("themes", [])
    
    formatted = "PROTOCOLO DE ENTREVISTA:\n\n"
    formatted += f"Total de preguntas: {len(questions)}\n"
    
    if themes:
        formatted += f"Temas principales: {', '.join(themes)}\n"
    
    formatted += "\nPreguntas guía:\n"
    
    for q in questions:
        formatted += f"{q['number']}. [{q['type'].upper()}] {q['text']}\n"
    
    formatted += "\n" + "="*80 + "\n\n"
    formatted += """INSTRUCCIÓN PARA EL ANÁLISIS:
Al codificar la transcripción, ten en cuenta las preguntas del protocolo:
1. Relaciona los códigos emergentes con las preguntas que los elicitaron
2. Identifica qué aspectos fenomenológicos surgen de cada tipo de pregunta
3. Verifica si todas las áreas del protocolo fueron exploradas en la entrevista
4. Nota cualquier tema emergente que NO esté en el protocolo (emergencia genuina)

Esto ayudará a distinguir entre:
- Contenido directamente elicitado por las preguntas
- Contenido emergente espontáneo del participante
"""
    
    return formatted


def get_protocol_summary(protocol_data: Dict) -> str:
    """
    Genera un resumen breve del protocolo para mostrar en la UI.
    """
    if not protocol_data or not protocol_data.get("questions"):
        return "No protocol loaded"
    
    total = protocol_data["total_questions"]
    types = {}
    
    for q in protocol_data["questions"]:
        qtype = q["type"]
        types[qtype] = types.get(qtype, 0) + 1
    
    summary = f"{total} questions: "
    summary += ", ".join([f"{count} {qtype}" for qtype, count in types.items()])
    
    return summary
