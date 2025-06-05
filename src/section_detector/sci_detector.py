from .util_func import classify_text_by_regex, normalize_section_title

# This section name is used to check with the json keyword section name
SECTION = "Statement of Comprehensive Income"
def sci_detector(blocks):
    detected_block = []
    for block in blocks:
        if block["type"] == "paragragh":
            block_section = classify_text_by_regex(block["text"])
            # If the block is identified as the designated section, then it will be marked as the beginning of the section
            if block_section == SECTION:
                detected_block.append(block["index"])
            # If the block is identified as the other section, then it will be marked as the end of the section
            # Anything in between and not identified, it will be considered as part of the section
            # elif block_section != SECTION and block_section != "":
            #     break
        elif block["type"] == "table":
            data = block["data"]
            for r in data:
                for c in r:
                    block_section = classify_text_by_regex(c)
                    if (block_section == SECTION):
                        detected_block.append(block["index"])

    return {
        "section_header": SECTION,
        "normalized_section": normalize_section_title(SECTION),
        "start_index": min(detected_block),
        "end_index": max(detected_block)
    }