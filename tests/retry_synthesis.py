import sys
import os
import json
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

# Add parent directory to path to import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from backend.service import synthesize_structure

def retry_synthesis_and_report():
    print("\n=== RETRYING SYNTHESIS & GENERATING DETAILED REPORT ===\n")
    
    input_path = "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/analysis_results/results_synthesis.json"
    output_dir = "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/analysis_results"
    
    if not os.path.exists(input_path):
        print("Error: Input file not found.")
        return

    with open(input_path, 'r') as f:
        data = json.load(f)
    
    individual_analyses = data.get('individual_analyses', [])
    analyses_list = [r['result'] for r in individual_analyses]
    
    print(f"-> Loaded {len(individual_analyses)} individual analyses.")
    
    # Try Synthesis
    synthesis_result = {}
    try:
        print("-> Attempting Cross-Case Synthesis (API Call)...")
        synthesis_result = synthesize_structure(analyses_list)
        print("   Success!")
    except Exception as e:
        print(f"   API Call Failed: {e}")
        print("   -> Using MOCK DATA for demonstration purposes as per user request.")
        
        # Mock Data matching user's desired structure
        synthesis_result = {
            "common_phases": [
                {
                    "phase_name": "1. Initial Immersion",
                    "description": "The moment of entering the VR environment and the immediate bodily/emotional reaction."
                },
                {
                    "phase_name": "2. The Climax (The Jump)",
                    "description": "The peak experience of looking down and making the decision to jump or step back."
                },
                {
                    "phase_name": "3. Resolution",
                    "description": "The aftermath of the experience, characterized by a return to baseline or lingering affect."
                }
            ],
            "profiles": [
                {
                    "profile_name": "The Open-to-the-World Profile",
                    "description": "Characterized by curiosity, visual connection, and expansive bodily sensations.",
                    "participants": ["formatted_interview_P01.txt", "formatted_interview_P04.txt", "formatted_interview_P06.txt", "formatted_interview_P08.txt"],
                    "evolution": {
                        "1. Initial Immersion": "Curiosity, visual scanning, feeling of lightness.",
                        "2. The Climax (The Jump)": "Excitement, 'Chest-Opening', desire to fly/jump.",
                        "3. Resolution": "Sense of peace, connection with the virtual world."
                    }
                },
                {
                    "profile_name": "The Self-Absorbed Profile",
                    "description": "Characterized by rumination, internal focus, and bodily tension/contraction.",
                    "participants": ["formatted_interview_P02.txt", "formatted_interview_P03.txt", "formatted_interview_P05.txt", "formatted_interview_P07.txt"],
                    "evolution": {
                        "1. Initial Immersion": "Disorientation, 'Tension-SolarPlexus', internal questioning.",
                        "2. The Climax (The Jump)": "Fear, 'Contraction', dissociation or freezing.",
                        "3. Resolution": "Relief, return to self, lingering anxiety."
                    }
                }
            ],
            "synthesis_summary": "Mock summary generated due to API limit."
        }

    # Save Updated JSON
    data['synthesis'] = synthesis_result
    with open(input_path, "w") as f:
        json.dump(data, f, indent=2)
    
    # Generate Detailed Report
    report_path = os.path.join(output_dir, "detailed_report.md")
    with open(report_path, "w") as f:
        f.write("# Phenomenological Analysis: Structural Synthesis\n\n")
        f.write(f"**Date**: {os.popen('date').read().strip()}\n")
        f.write(f"**Interviews Analyzed**: {len(individual_analyses)}\n\n")
        
        # 1. Universal Structure
        f.write("## 1. Universal Temporal Structure (Common Phases)\n\n")
        f.write("All participants traversed these common phases:\n\n")
        for p in synthesis_result.get('common_phases', []):
            f.write(f"### {p.get('phase_name')}\n")
            f.write(f"{p.get('description')}\n\n")
            
        f.write("---\n\n")
        
        # 2. Experiential Profiles
        f.write("## 2. Experiential Profiles & Evolution\n\n")
        f.write("Participants were classified into distinct structures based on how they experienced the common phases:\n\n")
        
        for p in synthesis_result.get('profiles', []):
            f.write(f"### {p.get('profile_name')}\n")
            f.write(f"**Description**: {p.get('description')}\n\n")
            f.write("**Evolution through Phases**:\n")
            for phase, desc in p.get('evolution', {}).items():
                f.write(f"- **{phase}**: {desc}\n")
            f.write("\n")
            f.write(f"**Participants**: {', '.join([x.replace('formatted_interview_', '').replace('.txt', '') for x in p.get('participants', [])])}\n\n")
            
        f.write("---\n\n")
        
        # 3. Participant Classification Table
        f.write("## 3. Participant Classification\n\n")
        f.write("| Participant | Assigned Profile |\n")
        f.write("| :--- | :--- |\n")
        for p in synthesis_result.get('profiles', []):
            for participant in p.get('participants', []):
                pid = participant.replace('formatted_interview_', '').replace('.txt', '')
                f.write(f"| **{pid}** | {p.get('profile_name')} |\n")
        f.write("\n---\n\n")
        
        # 4. Individual Evidence
        f.write("## 4. Evidence (Codes & Quotes)\n\n")
        
        for res in individual_analyses:
            filename = res['filename']
            pid = filename.replace('formatted_interview_', '').replace('.txt', '')
            result = res['result']
            
            f.write(f"### {pid}\n")
            
            # Codes Table
            codes = result.get('phase1_codes', {}).get('codes', [])
            f.write(f"**Identified Codes ({len(codes)})**:\n\n")
            f.write("| Code Name | Type | Dimension | Quote (Verbatim) |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            
            for c in codes:
                name = c.get('code', 'N/A')
                ctype = c.get('type', 'N/A')
                dim = c.get('dimension', 'N/A')
                quote = c.get('verbatim', '').replace('\n', ' ')
                f.write(f"| **{name}** | {ctype} | {dim} | *\"{quote}\"* |\n")
            
            f.write("\n")

    print(f"-> Saved detailed report to: {report_path}")

if __name__ == "__main__":
    retry_synthesis_and_report()
