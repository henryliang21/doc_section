import re
import json
from lxml import etree
# from .section_detector import cover_page_detector
from .section_detector.util_func import *


# Word XML Namespaces
PKG_NS = "http://schemas.microsoft.com/office/2006/xmlPackage"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"pkg": PKG_NS, "w": W_NS}
NSMAP = {"w": W_NS}

def normalize_section(title):
    normalized = title.lower().replace(" ", "_")
    return normalized

def extract_blocks(file_path):
    with open(file_path, "rb") as f:
        root = etree.fromstring(f.read())

    doc_part = root.xpath('//pkg:part[@pkg:name="/word/document.xml"]', namespaces=NS)[0]
    xml_data = doc_part.find("pkg:xmlData", namespaces=NS)
    body = xml_data.find(".//w:body", namespaces=NS)

    blocks = []
    index = 0
    for block in body.xpath("w:p | w:tbl", namespaces=NS):
        if block.tag.endswith("p"):
            texts = block.xpath(".//w:t", namespaces=NS)
            para_text = "".join(t.text for t in texts if t is not None).strip()

            p_pr = block.find("w:pPr", namespaces=NS)
            style = None
            outline_level = None
            alignment = None
            if p_pr is not None:
                p_style = p_pr.find("w:pStyle", namespaces=NS)
                if p_style is not None:
                    style = p_style.attrib.get(f"{{{W_NS}}}val")
                o_lvl = p_pr.find("w:outlineLvl", namespaces=NS)
                if o_lvl is not None:
                    outline_level = o_lvl.attrib.get(f"{{{W_NS}}}val")
                p_alignment = p_pr.find("w:jc", namespaces=NS)
                if p_alignment is not None:
                    alignment = p_alignment.attrib.get(f"{{{W_NS}}}val")

            if (para_text is not None and para_text != ""):
                blocks.append({
                    "index": index,
                    "text": para_text,
                    "style": style,
                    "outline_level": outline_level,
                    "alignment": alignment,
                    "type": "paragragh"
                })
                index += 1
        elif block.tag.endswith("tbl"):
            table_data = []
            # Iterate over table rows
            for row in block.findall("w:tr", namespaces=NSMAP):
                row_data = []

                # Iterate over cells in the row
                for cell in row.findall("w:tc", namespaces=NSMAP):
                    # Extract all text in the cell
                    texts = cell.xpath(".//w:t", namespaces=NSMAP)
                    cell_text = "".join(t.text for t in texts if t is not None).strip()
                    row_data.append(cell_text)

                table_data.append(row_data)
            blocks.append({
                "index": index,
                "type": "table",
                "data": table_data
            })
            index += 1
    return blocks



# def detect_statement_section(blocks, start_idx):
#     block = blocks[start_idx]
#     if "Heading" in (block.get("style") or ""):
#         title = block["text"].lower()
#         if "statement of financial position" in title:
#             return {
#                 "section_type": "statement_of_financial_position",
#                 "start_block": start_idx,
#                 "end_block": start_idx + 5  # dummy rule: next 5 blocks
#             }
#         elif "statement of comprehensive income" in title:
#             return {
#                 "section_type": "statement_of_comprehensive_income",
#                 "start_block": start_idx,
#                 "end_block": start_idx + 1  # dummy rule
#             }
#     return None

# def detect_note_section(blocks, start_idx):
#     text = blocks[start_idx]["text"]
#     match = re.match(r"(Note\s*)?(\d+)[\.:]?\s*(.+)", text, re.IGNORECASE)
#     if match:
#         note_number = int(match.group(2))
#         title = match.group(3).strip()
#         # dummy rule: note ends after 7 blocks
#         return {
#             "section_type": f"note_{note_number}",
#             "note_number": note_number,
#             "normalized_section": title,
#             "start_block": start_idx,
#             "end_block": start_idx + 6
#         }
#     return None

def detect_sections(blocks):
    sections = []
    current_section = None

    # section_detectors = [
    #     cover_page_detector,
    #     # ,detect_statement_section
    #     # ,detect_note_section
    # ]

    # for detector in section_detectors:
    #     result = detector(blocks)
    #     sections.append(result)

    for block in blocks:
        if block["type"] == "paragragh":
            section = classify_text_by_regex(block)
            block['section'] = section

    print(json.dumps(blocks, indent=2))
    return sections