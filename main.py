import sys
from src.financial_report_analyzer import *

# Main script
if __name__ == "__main__":
    if sys.argv is None or sys.argv[1] == "":
        print("Please provide source xml file path")
        exit
    input_path = sys.argv[1]
    output_path = "bestco_structured_output.json"

    blocks = extract_blocks(input_path)
    sections = detect_sections(blocks)

    print(json.dumps(sections, indent=2))