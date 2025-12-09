"""
Módulo de transcripción de audio usando Whisper local.
"""

import whisper
import os
from typing import List, Dict, Optional
import tempfile

# Modelo global (se carga una vez)
_MODEL = None
_MODEL_SIZE = "base"  # tiny, base, small, medium, large

def load_whisper_model(model_size: str = "base"):
    """
    Carga el modelo Whisper.
    
    Modelos disponibles:
    - tiny: ~39M params, más rápido, menos preciso
    - base: ~74M params, buen balance (RECOMENDADO para español)
    - small: ~244M params, mejor calidad
    - medium: ~769M params, muy buena calidad
    - large: ~1550M params, máxima calidad (muy lento sin GPU)
    """
    global _MODEL, _MODEL_SIZE
    
    if _MODEL is None or _MODEL_SIZE != model_size:
        print(f"🔄 Cargando modelo Whisper '{model_size}'...")
        _MODEL = whisper.load_model(model_size)
        _MODEL_SIZE = model_size
        print(f"✅ Modelo Whisper '{model_size}' cargado")
    
    return _MODEL


def transcribe_audio(
    audio_path: str, 
    language: str = "es",
    model_size: str = "base"
) -> Dict:
    """
    Transcribe un archivo de audio.
    
    Args:
        audio_path: Ruta al archivo de audio
        language: Código de idioma (es, en, fr, etc.)
        model_size: Tamaño del modelo Whisper
    
    Returns:
        {
            "text": str,  # Transcripción completa
            "segments": [...],  # Segmentos con timestamps
            "language": str  # Idioma detectado
        }
    """
    model = load_whisper_model(model_size)
    
    print(f"🎤 Transcribiendo: {os.path.basename(audio_path)}")
    
    # Transcribir
    result = model.transcribe(
        audio_path, 
        language=language,
        fp16=False  # Desactivar FP16 para compatibilidad CPU
    )
    
    print(f"✅ Transcripción completada: {len(result['text'])} caracteres")
    
    return result


def transcribe_multiple(
    audio_files: List[str],
    language: str = "es",
    model_size: str = "base"
) -> List[Dict]:
    """
    Transcribe múltiples archivos de audio.
    
    Returns:
        [
            {
                "filename": str,
                "transcription": str,
                "segments": [...],
                "duration": float
            },
            ...
        ]
    """
    results = []
    total = len(audio_files)
    
    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n📁 Procesando {i}/{total}: {os.path.basename(audio_file)}")
        
        try:
            result = transcribe_audio(audio_file, language, model_size)
            
            results.append({
                "filename": os.path.basename(audio_file),
                "transcription": result["text"],
                "segments": result["segments"],
                "language": result.get("language", language),
                "duration": result["segments"][-1]["end"] if result["segments"] else 0
            })
        except Exception as e:
            print(f"❌ Error transcribiendo {audio_file}: {e}")
            results.append({
                "filename": os.path.basename(audio_file),
                "error": str(e),
                "transcription": ""
            })
    
    return results


def format_transcription_with_timestamps(segments: List[Dict]) -> str:
    """
    Formatea la transcripción con timestamps.
    
    Returns:
        [00:00:00] Texto del segmento 1
        [00:00:05] Texto del segmento 2
        ...
    """
    formatted = []
    
    for segment in segments:
        start = segment["start"]
        text = segment["text"].strip()
        
        # Convertir segundos a HH:MM:SS
        hours = int(start // 3600)
        minutes = int((start % 3600) // 60)
        seconds = int(start % 60)
        
        timestamp = f"[{hours:02d}:{minutes:02d}:{seconds:02d}]"
        formatted.append(f"{timestamp} {text}")
    
    return "\n".join(formatted)


def save_transcription(
    transcription: Dict,
    output_path: str,
    include_timestamps: bool = False
) -> str:
    """
    Guarda la transcripción en un archivo de texto.
    
    Args:
        transcription: Resultado de transcribe_audio()
        output_path: Ruta del archivo de salida
        include_timestamps: Si incluir timestamps en el formato
    
    Returns:
        Ruta del archivo guardado
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        if include_timestamps and "segments" in transcription:
            content = format_transcription_with_timestamps(transcription["segments"])
        else:
            content = transcription["text"]
        
        f.write(content)
    
    print(f"💾 Transcripción guardada en: {output_path}")
    return output_path
