from .util_func import classify_text_by_regex, normalize_section_title

# This section name is used to check with the json keyword section name
SECTION = "Cover page"
def cover_page_detector(blocks):
    detected_block = []
    for block in blocks:
        if block["type"] == "paragragh":
            block_section = classify_text_by_regex(block["text"])
            # If the block is identified as the designated section, then it will be marked as the beginning of the section
            if block_section == SECTION:
                detected_block.append(block["index"])
            # If the block is identified as the other section, then it will be marked as the end of the section
            # Anything in between and not identified, it will be considered as part of the section
            elif block_section != SECTION and block_section != "":
                break
        else:
            break
    return {
        "section_header": SECTION,
        "normalized_section": normalize_section_title(SECTION),
        "start_block": min(detected_block),
        "end_block": max(detected_block)
    }