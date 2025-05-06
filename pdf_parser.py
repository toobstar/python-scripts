import os
import sys
import pymupdf4llm
import pathlib
from openai import OpenAI


PROMPT = "If the following text is an invoice can you return a JSON modelled object containing all the elements you can identify?  \n\n"

def is_invoice(text: str) -> bool:
    invoice_indicators = [
        'bill', 'billed to', 'payment terms', 'tax', 'GST', 'VAT'
        'invoice', 'invoice date', 'payment', 'due date', 'total amount',
        
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


def query_openai_text(text: str) -> str:
    # client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))
    client = OpenAI()
    # response = client.responses.create(
    #     model="gpt-4.1",
    #     input="Write a one-sentence bedtime story about a unicorn."
    # )
    # print(text, response.output_text)

    response = client.responses.create(
        model="o4-mini",
        reasoning={"effort": "medium"},
        input=[
            {
                "role": "user", 
                "content": PROMPT + text
            }
        ]
    )

    return response.output_text


def query_openai_pdf(file_path: str):
    client = OpenAI()

    file = client.files.create(
        file=open(file_path, "rb"),
        purpose="user_data"
    )

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "file_id": file.id,
                    },
                    {
                        "type": "input_text",
                        "text": PROMPT,
                    },
                ]
            }
        ]
    )
    return response.output_text

def main():
        
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Enter the path to the file: ")

    if not file_path:
        file_path = 'static/invoice.pdf'

    try: 
        markdown = parse_file(file_path, False)

        print("Method 1: basic pattern matching ", is_invoice(markdown))
        print("Method 2: openai text parsing     ", query_openai_text(markdown))
        print("Method 3: openai PDF parsing", query_openai_pdf('static/invoice.pdf'))

    except (FileNotFoundError, IOError) as e:
        print(e)

if __name__ == "__main__":
    main()
