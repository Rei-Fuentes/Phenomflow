import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.service import run_complete_pipeline

def main():
    # Define the 4 interviews to process
    interview_files = [
        "formatted_interview_P01.txt",
        "formatted_interview_P02.txt",
        "formatted_interview_P03.txt",
        "formatted_interview_P04.txt"
    ]
    
    base_path = "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/data/simulated_interviews"
    transcripts = []
    
    print(f"Loading {len(interview_files)} interviews from {base_path}...")
    
    for filename in interview_files:
        filepath = os.path.join(base_path, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                pid = filename.replace("formatted_interview_", "").replace(".txt", "")
                transcripts.append({
                    "participant_id": pid,
                    "text": content
                })
                print(f"  - Loaded {pid} ({len(content)} chars)")
        except Exception as e:
            print(f"  - Error loading {filename}: {e}")
            
    if not transcripts:
        print("No transcripts loaded. Aborting.")
        return

    # Run the pipeline
    output_dir = "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/analysis_results/v3_real_data_test"
    print(f"\nStarting pipeline execution. Output will be saved to: {output_dir}")
    
    try:
        report_path = run_complete_pipeline(transcripts, output_dir=output_dir)
        print(f"\nSUCCESS! Report generated at: {report_path}")
    except Exception as e:
        print(f"\nFAILURE! Pipeline execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
