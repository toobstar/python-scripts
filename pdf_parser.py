import sys
import pymupdf4llm
import pathlib


def is_invoice(text: str) -> bool:
    invoice_indicators = [
        'invoice', 'bill', 'payment', 'due date', 'total amount',
        'invoice number', 'invoice date', 'billed to', 'payment terms'
    ]
    text_lower = text.lower()

    matches = sum(1 for indicator in invoice_indicators if indicator in text_lower)

    # If >2 indicators are present it likely to be an invoice
    return matches >= 2


def parse_file(file_path: str, write_markdown: bool) -> str:
    # Parse file & convert to markdown
    md_text = pymupdf4llm.to_markdown(file_path)    
    
    if write_markdown:
        pathlib.Path('static/output.md').write_bytes(md_text.encode())

    return md_text


def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Enter the path to the file: ")

    if not file_path:
        file_path = 'static/invoice.pdf'

    try: 
        markdown = parse_file(file_path, False)
        print("is invoice? ", is_invoice(markdown))

    except (FileNotFoundError, IOError) as e:
        print(e)

if __name__ == "__main__":
    main()
