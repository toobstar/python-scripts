import pymupdf4llm
import pathlib

# Parse file
md_text = pymupdf4llm.to_markdown("static/invoice.pdf")
print(md_text)

# Convert to markdown
pathlib.Path("static/output.md").write_bytes(md_text.encode())

