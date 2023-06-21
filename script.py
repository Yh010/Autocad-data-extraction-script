import fitz
import os
import re

def extract_cable_info_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    cable_info = {}

    for page in doc:
        words = page.get_text_words()

        for i in range(len(words) - 1):
            word = words[i][4]  # Extract the text from the word tuple

            # Check if the word matches the cable name format
            if re.match(r"(?i)(M-CT\d+|M-CTV\d+|M-UT\d+|A\d+-CT\d+|A\d+-CTV\d+|A\d+-UT\d+|S\d+-CT\d+|S-CTV\d+)", word):
                # Extract the cable name
                cable_name = word.strip()

                # Extract the cable length
                cable_length = ""
                j = i + 1
                while j < len(words) and not re.match(r"(?i)(M-CT\d+|M-CTV\d+|M-UT\d+|A\d+-CT\d+|A\d+-CTV\d+|A\d+-UT\d+|S\d+-CT\d+|S-CTV\d+)", words[j][4]):
                    cable_length += words[j][4]
                    j += 1

                # Remove any non-numeric characters from the cable length
                cable_length = re.sub(r"[^0-9.]", "", cable_length)

                # Check if the extracted length is a valid floating-point value
                if re.match(r"^\d+(\.\d+)?$", cable_length):
                    # Add cable name and length to the cable_info dictionary
                    if cable_name not in cable_info:
                        cable_info[cable_name] = float(cable_length)

    doc.close()

    # Print the extracted cable names and lengths
    for cable_name, cable_length in cable_info.items():
        print(f"Cable Name: {cable_name}, Length: {cable_length}")

# Example usage
pdf_file = os.path.join('/content', '0220-01-DWG-2001_(01 OF 02)_R4_ (2)-Model.pdf')
extract_cable_info_from_pdf(pdf_file)
