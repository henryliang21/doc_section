import re
from .util_func import classify_text_by_regex, normalize_section_title

# This section name is used to check with the json keyword section name
SECTION = "Notes to Financial Statements"
SUBSECTION_REGEX = "^\\d[.,]"
def notes_of_financial_statement_detector(blocks):
    sections = []
    for block in blocks:
        if block["type"] == "paragragh":
            block_section = classify_text_by_regex(block["text"])
            # If the block is identified as the designated section, then it will be marked as the beginning of the section
            if block_section == SECTION:
                if (re.search(SUBSECTION_REGEX, block["text"])):
                  sections.append({
                      "section_header": SECTION,
                      "normalized_section": normalize_section_title(re.sub(SUBSECTION_REGEX, "", block["text"])),
                      "note_number": re.match(SUBSECTION_REGEX, block["text"])[0],
                      "block_index": block["index"]
                  })
    result = []
    if sections is not None:
        for i, s in enumerate(sections):
            s["start_index"] = s["block_index"]
            if (i < len(sections) - 1):
                s["end_index"] = sections[i+1]["block_index"] - 1
            else:
                s["end_index"] = len(blocks) - 1
            result.append(s)
    return result