import sys
import os
import json
# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

# Add parent directory to path to import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from backend.service import analyze_with_pipeline
from backend.qdpx_parser import extract_codes_from_qdpx

def run_live_test():
    print("\n=== LIVE TEST: PHENOMENOLOGICAL ANALYSIS PIPELINE ===\n")
    
    # 1. Extract Codes from QDPX
    qdpx_path = "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/data/simulated_interviews/suicidio_rv_06_12_25.qdpx"
    print(f"-> Extracting codes from: {qdpx_path}")
    try:
        codes = extract_codes_from_qdpx(qdpx_path)
        print(f"   Success! Found {len(codes)} codes.")
        print(f"   Sample: {[c['name'] for c in codes[:3]]}")
    except Exception as e:
        print(f"   Error extracting codes: {e}")
        return

    # 2. Load Interviews (P01 to P10)
    interview_files = [f"formatted_interview_P{i:02d}.txt" for i in range(1, 11)]
    base_dir = "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/data/simulated_interviews"
    
    results = []
    
    print(f"-> Processing {len(interview_files)} interviews for Cross-Case Synthesis...")
    
    for filename in interview_files:
        file_path = os.path.join(base_dir, filename)
        if not os.path.exists(file_path):
            print(f"   Skipping {filename} (not found)")
            continue
            
        print(f"\n-> Analyzing: {filename}")
        
        try:
            with open(file_path, 'r') as f:
                text = f.read()
            
            # 3. Run Analysis Pipeline (Individual)
            result = analyze_with_pipeline(
                text=text,
                context={
                    "research_question": "Experiencia fenomenológica de suicidio en Realidad Virtual",
                    "phenomenological_approach": "Micro-phenomenology"
                },
                custom_codes=codes
            )
            
            # Add ID for synthesis
            result['id'] = filename
            
            results.append({
                "filename": filename,
                "result": result
            })
            
            print(f"   - Codes: {len(result.get('phase1_codes', {}).get('codes', []))}")
            
        except Exception as e:
            print(f"   Error processing {filename}: {e}")

    # 4. Perform Cross-Case Synthesis
    print("\n=== RUNNING CROSS-CASE SYNTHESIS ===")
    from backend.service import synthesize_structure
    
    # Extract just the analysis result dicts
    analyses_list = [r['result'] for r in results]
    
    try:
        synthesis_result = synthesize_structure(analyses_list)
        print("-> Synthesis Complete!")
        print(f"   - Common Phases: {len(synthesis_result.get('common_phases', []))}")
        print(f"   - Profiles Identified: {len(synthesis_result.get('profiles', []))}")
    except Exception as e:
        print(f"-> Synthesis Failed: {e}")
        synthesis_result = {}

    # 5. Save and Summary Output
    print("\n=== SAVING RESULTS ===")
    output_dir = "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/analysis_results"
    
    # Save raw JSON
    full_data = {
        "individual_analyses": results,
        "synthesis": synthesis_result
    }
    with open(os.path.join(output_dir, "results_synthesis.json"), "w") as f:
        json.dump(full_data, f, indent=2)
    print(f"-> Saved full JSON to: {os.path.join(output_dir, 'results_synthesis.json')}")

    # Generate Markdown Report
    report_path = os.path.join(output_dir, "synthesis_report.md")
    with open(report_path, "w") as f:
        f.write("# Phenomenological Cross-Case Synthesis Report\n\n")
        f.write(f"**Date**: {os.popen('date').read().strip()}\n")
        f.write(f"**Interviews Analyzed**: {len(results)}\n\n")
        
        # Synthesis Section
        f.write("## 1. Universal Temporal Structure\n\n")
        f.write("The following phases were identified as common to all participants:\n\n")
        for p in synthesis_result.get('common_phases', []):
            f.write(f"### {p.get('phase_name')}\n")
            f.write(f"- **Description**: {p.get('description')}\n")
            f.write(f"- **Duration**: {p.get('typical_duration')}\n\n")
            
        f.write("## 2. Experiential Profiles\n\n")
        f.write("Distinct patterns of experience identified:\n\n")
        for p in synthesis_result.get('profiles', []):
            f.write(f"### {p.get('profile_name')}\n")
            f.write(f"- **Description**: {p.get('description')}\n")
            f.write(f"- **Key Characteristics**: {', '.join(p.get('key_characteristics', []))}\n")
            f.write(f"- **Distinctive Codes**: {', '.join(p.get('distinctive_codes', []))}\n")
            f.write(f"- **Participants**: {', '.join([str(id) for id in p.get('example_participant_ids', [])])}\n\n")
            
        f.write("---\n\n")
        f.write("## 3. Individual Analysis Summaries\n\n")
        
        for res in results:
            f.write(f"### Interview: {res['filename']}\n")
            codes = res['result'].get('phase1_codes', {}).get('codes', [])
            f.write(f"- **Codes Found**: {len(codes)}\n")
            f.write(f"- **Phases**: {len(res['result'].get('phase2_diachronic', {}).get('phases', []))}\n\n")
            
    print(f"-> Saved readable report to: {report_path}")

if __name__ == "__main__":
    run_live_test()
