
import os
import sys
import json
import logging
from pathlib import Path
from tqdm import tqdm

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# Import backend modules
from backend.service import analyze_individual_interview
from backend.document_parser import process_document, parse_docx
from backend.protocol_parser import parse_protocol
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(project_root, 'batch_processing.log')),
        logging.StreamHandler()
    ]
)

def main():
    # Load env vars
    load_dotenv(os.path.join(project_root, ".env"))

    data_dir = os.path.join(project_root, "data", "entrevistas_limpias")
    results_dir = os.path.join(project_root, "analysis_results")
    os.makedirs(results_dir, exist_ok=True)

    # 1. Load Protocol
    protocol_path = os.path.join(data_dir, "Protocolo_Entrevista_Microfenomenologica_LIMENS.docx")
    protocol_data = None
    
    if os.path.exists(protocol_path):
        logging.info(f"Loading protocol from {protocol_path}")
        try:
            parsed_protocol_doc = parse_docx(protocol_path)
            protocol_text = parsed_protocol_doc["text"]
            protocol_data = parse_protocol(protocol_text)
            logging.info("Protocol loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to parse protocol: {e}")
    else:
        logging.warning("Protocol file not found. Proceeding without protocol.")

    # 1.5 Load Context
    context_path = os.path.join(project_root, "data", "demo", "context.json")
    context_data = None
    
    if os.path.exists(context_path):
        logging.info(f"Loading context from {context_path}")
        try:
            with open(context_path, 'r', encoding='utf-8') as f:
                context_data = json.load(f)
            logging.info("Context loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to parse context: {e}")
    else:
        logging.warning("Context file not found. Proceeding without context.")

    # 2. List files to process
    files = [f for f in os.listdir(data_dir) if f.endswith(".docx") or f.endswith(".doc")]
    # Exclude protocol itself if it was in the list
    if "Protocolo_Entrevista_Microfenomenologica_LIMENS.docx" in files:
        files.remove("Protocolo_Entrevista_Microfenomenologica_LIMENS.docx")
    
    files.sort()
    
    logging.info(f"Found {len(files)} interviews to process.")

    # 3. Process each interview
    for filename in tqdm(files, desc="Processing Interviews"):
        file_path = os.path.join(data_dir, filename)
        participant_id = os.path.splitext(filename)[0]
        
        # Check if already processed
        result_path = os.path.join(results_dir, f"{participant_id}.json")
        if os.path.exists(result_path):
            logging.info(f"Skipping {participant_id} (already processed)")
            continue
            
        logging.info(f"Processing {participant_id}...")
        
        try:
            # Parse document
            # process_document returns {raw_text, structure, analysis_ready_text, ...}
            file_type = "docx" if filename.endswith(".docx") else "doc"
            doc_data = process_document(file_path, file_type)
            
            # Use analysis_ready_text which filters participant text if structure found
            interview_text = doc_data["analysis_ready_text"]
            
            # Run analysis
            # analyze_individual_interview(text, participant_id, context, protocol)
            analysis_result = analyze_individual_interview(
                text=interview_text,
                participant_id=participant_id,
                context=context_data,
                protocol=protocol_data
            )
            
            # Save result
            with open(result_path, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=2)
                
            logging.info(f"Successfully processed {participant_id}")
            
        except Exception as e:
            logging.error(f"Error processing {participant_id}: {str(e)}")
            # Continue to next file even if one fails

    logging.info("Batch processing complete.")

if __name__ == "__main__":
    main()
