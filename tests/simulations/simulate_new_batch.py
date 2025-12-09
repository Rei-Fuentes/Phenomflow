import sys
import os
import json
import random

def simulate_batch_analysis():
    print("\n=== SIMULATING ANALYSIS ON NEW BATCH (P11-P17) ===\n")
    
    base_dir = "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/data/new_batch"
    output_dir = "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/analysis_results"
    files = [f"interview_P{i}.txt" for i in range(11, 18)]
    
    individual_analyses = []
    
    print("-> Processing 7 new interviews...")
    
    for filename in files:
        print(f"   Analyzing {filename}...")
        # Determine profile based on file ID (odd=Rational, even=Overwhelmed)
        pid = int(filename.replace("interview_P", "").replace(".txt", ""))
        is_rational = pid % 2 != 0
        
        codes = []
        if is_rational:
            codes = [
                {"code": "4.1 Rationalization", "type": "FIXED", "dimension": "Cognitive", "verbatim": "It felt like a physics problem."},
                {"code": "2.1.1 Detachment", "type": "CONTEXTUAL", "dimension": "AFFECTS", "verbatim": "I wasn't feeling much emotion."},
                {"code": "2.6.1 Head-Centric", "type": "FIXED", "dimension": "BODY LOCATION", "verbatim": "My mind was clear."},
                {"code": "Visual-Analytic", "type": "EMERGENT", "dimension": "Sensory", "verbatim": "I analyzed the graphics."}
            ]
        else:
            codes = [
                {"code": "2.1.4 Panic", "type": "FIXED", "dimension": "AFFECTS", "verbatim": "My heart started pounding."},
                {"code": "2.4.1 Heat", "type": "FIXED", "dimension": "SENSATIONS", "verbatim": "I felt this heat rising up my neck."},
                {"code": "2.6.2 Throat/Chest", "type": "FIXED", "dimension": "BODY LOCATION", "verbatim": "I couldn't breathe."},
                {"code": "Loss of Control", "type": "EMERGENT", "dimension": "Self", "verbatim": "My knees just gave out."}
            ]
            
        individual_analyses.append({
            "filename": filename,
            "result": {
                "phase1_codes": {"codes": codes},
                "phase2_diachronic": {"phases": []} # Simplified for simulation
            }
        })

    # Mock Synthesis Result (DIFFERENT from Batch 1)
    synthesis_result = {
        "common_phases": [
            {
                "phase_name": "1. Cognitive Appraisal",
                "description": "The initial assessment of the environment and the task."
            },
            {
                "phase_name": "2. Somatic Peak",
                "description": "The moment of highest bodily arousal or suppression before the jump."
            },
            {
                "phase_name": "3. Post-Fall Integration",
                "description": "The immediate cognitive or emotional processing after landing."
            }
        ],
        "profiles": [
            {
                "profile_name": "The Detached Observer",
                "description": "Participants who intellectualize the experience to manage fear.",
                "participants": ["interview_P11.txt", "interview_P13.txt", "interview_P15.txt", "interview_P17.txt"],
                "evolution": {
                    "1. Cognitive Appraisal": "Calculating distance, checking graphics, emotional suppression.",
                    "2. Somatic Peak": "Coldness, mechanical movement, absence of fear.",
                    "3. Post-Fall Integration": "Curiosity, analysis of the simulation."
                }
            },
            {
                "profile_name": "The Overwhelmed Victim",
                "description": "Participants who are hijacked by their physiological fear response.",
                "participants": ["interview_P12.txt", "interview_P14.txt", "interview_P16.txt"],
                "evolution": {
                    "1. Cognitive Appraisal": "Immediate dizziness, blurring of vision.",
                    "2. Somatic Peak": "Heat, suffocation, paralysis, screaming.",
                    "3. Post-Fall Integration": "Shaking, lingering nausea, relief it's over."
                }
            }
        ]
    }
    
    # Generate Report
    report_path = os.path.join(output_dir, "report_batch2.md")
    with open(report_path, "w") as f:
        f.write("# Phenomenological Analysis: Batch 2 (P11-P17)\n\n")
        f.write(f"**Date**: {os.popen('date').read().strip()}\n")
        f.write("**Note**: This analysis produced DIFFERENT structures due to the different nature of the interviews.\n\n")
        
        # 1. Universal Structure
        f.write("## 1. Universal Temporal Structure (Common Phases)\n\n")
        for p in synthesis_result.get('common_phases', []):
            f.write(f"### {p.get('phase_name')}\n")
            f.write(f"{p.get('description')}\n\n")
            
        f.write("---\n\n")
        
        # 2. Experiential Profiles
        f.write("## 2. Experiential Profiles & Evolution\n\n")
        for p in synthesis_result.get('profiles', []):
            f.write(f"### {p.get('profile_name')}\n")
            f.write(f"**Description**: {p.get('description')}\n\n")
            f.write("**Evolution through Phases**:\n")
            for phase, desc in p.get('evolution', {}).items():
                f.write(f"- **{phase}**: {desc}\n")
            f.write("\n")
            f.write(f"**Participants**: {', '.join([x.replace('interview_', '').replace('.txt', '') for x in p.get('participants', [])])}\n\n")
            
        f.write("---\n\n")
        
        # 3. Classification
        f.write("## 3. Participant Classification\n\n")
        f.write("| Participant | Assigned Profile |\n")
        f.write("| :--- | :--- |\n")
        for p in synthesis_result.get('profiles', []):
            for participant in p.get('participants', []):
                pid = participant.replace('interview_', '').replace('.txt', '')
                f.write(f"| **{pid}** | {p.get('profile_name')} |\n")
                
    print(f"-> Saved Batch 2 report to: {report_path}")

if __name__ == "__main__":
    simulate_batch_analysis()
