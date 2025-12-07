from typing import Dict, List, Any
from pypdf import PdfReader
from docx import Document
import re

def parse_pdf(file_path: str) -> Dict[str, Any]:
    """Extract text from PDF with line numbers"""
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    
    lines = full_text.split('\n')
    return {
        "text": full_text,
        "lines": [{"line_number": i+1, "content": line} for i, line in enumerate(lines) if line.strip()],
        "total_lines": len(lines)
    }

def parse_docx(file_path: str) -> Dict[str, Any]:
    """Extract text from Word document with line numbers"""
    doc = Document(file_path)
    lines = []
    line_number = 1
    
    for para in doc.paragraphs:
        if para.text.strip():
            lines.append({"line_number": line_number, "content": para.text})
            line_number += 1
    
    full_text = "\n".join([line["content"] for line in lines])
    return {
        "text": full_text,
        "lines": lines,
        "total_lines": len(lines)
    }

def identify_interview_structure(text: str, lines: List[Dict]) -> Dict[str, Any]:
    """
    Identify interview structure: participants, roles, dialogue turns
    """
    # Common patterns for interview transcripts
    patterns = {
        "interviewer_markers": [
            r"^(Entrevistador|Interviewer|E|I):\s*(.+)",
            r"^(Investigador|Researcher|R):\s*(.+)",
        ],
        "participant_markers": [
            r"^(Participante|Participant|P|Entrevistado):\s*(.+)",
            r"^(P\d+):\s*(.+)",  # P1, P2, etc.
        ],
        "metadata_markers": [
            r"Código:\s*(.+)",
            r"Participant ID:\s*(.+)",
            r"Fecha:\s*(.+)",
            r"Date:\s*(.+)",
        ]
    }
    
    dialogue_turns = []
    metadata = {}
    participant_code = None
    
    for line_data in lines:
        line = line_data["content"]
        line_num = line_data["line_number"]
        
        # Check for metadata
        for pattern in patterns["metadata_markers"]:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                key = pattern.split(r":\s*")[0].replace("\\", "")
                metadata[key] = match.group(1).strip()
                if "código" in key.lower() or "participant id" in key.lower():
                    participant_code = match.group(1).strip()
        
        # Check for interviewer
        for pattern in patterns["interviewer_markers"]:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                dialogue_turns.append({
                    "line_number": line_num,
                    "speaker": "interviewer",
                    "speaker_label": match.group(1),
                    "content": match.group(2).strip()
                })
                break
        
        # Check for participant
        for pattern in patterns["participant_markers"]:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                dialogue_turns.append({
                    "line_number": line_num,
                    "speaker": "participant",
                    "speaker_label": match.group(1),
                    "content": match.group(2).strip()
                })
                break
    
    # Extract participant-only text for analysis
    participant_text = "\n".join([
        turn["content"] for turn in dialogue_turns if turn["speaker"] == "participant"
    ])
    
    return {
        "metadata": metadata,
        "participant_code": participant_code,
        "dialogue_turns": dialogue_turns,
        "participant_text": participant_text,
        "total_turns": len(dialogue_turns),
        "interviewer_turns": len([t for t in dialogue_turns if t["speaker"] == "interviewer"]),
        "participant_turns": len([t for t in dialogue_turns if t["speaker"] == "participant"])
    }

def process_document(file_path: str, file_type: str) -> Dict[str, Any]:
    """
    Main function to process uploaded document
    """
    # Parse document
    if file_type == "pdf":
        parsed = parse_pdf(file_path)
    elif file_type in ["docx", "doc"]:
        parsed = parse_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    # Identify structure
    structure = identify_interview_structure(parsed["text"], parsed["lines"])
    
    return {
        "raw_text": parsed["text"],
        "lines": parsed["lines"],
        "total_lines": parsed["total_lines"],
        "structure": structure,
        "analysis_ready_text": structure["participant_text"] if structure["participant_text"] else parsed["text"]
    }
