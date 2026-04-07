import argparse
import os
import sys

def parse_eml(input_path: str) -> str:
    import email
    from email import policy
    with open(input_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)
    
    subject = msg.get("Subject", "No Subject")
    sender = msg.get("From", "Unknown Sender")
    date = msg.get("Date", "Unknown Date")
    
    body = ""
    # Extract body preferring text/plain, then text/html.
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    body_part = part.get_payload(decode=True)
                    if body_part:
                        body += body_part.decode('utf-8', errors='ignore') + "\n"
                except Exception:
                    pass
    else:
        try:
            body_part = msg.get_payload(decode=True)
            if body_part:
                body = body_part.decode('utf-8', errors='ignore')
        except Exception:
            body = msg.get_payload()
            if isinstance(body, list): 
                body = str(body)

    md_content = f"# Email: {subject}\n\n**From:** {sender}\n**Date:** {date}\n\n## Body\n{body}"
    return md_content

def parse_spreadsheet(input_path: str) -> str:
    import pandas as pd
    try:
        # Truncate dataset ingestion to prevent agent token overflow
        if input_path.lower().endswith(".csv"):
            df = pd.read_csv(input_path, nrows=1000)
        else:
            df = pd.read_excel(input_path, nrows=1000)
    except Exception as e:
        return f"Error parsing spreadsheet: {str(e)}"
    
    md_content = f"# Spreadsheet Preview (Top 1000 rows): {os.path.basename(input_path)}\n\n"
    md_content += df.to_markdown(index=False)
    return md_content

def parse_docling(input_path: str) -> str:
    from docling.document_converter import DocumentConverter
    converter = DocumentConverter()
    try:
        result = converter.convert(input_path)
        return result.document.export_to_markdown()
    except Exception as e:
        return f"Error parsing document via docling: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Multi-Format Local Asset Ingestion")
    parser.add_argument("--input", required=True, help="Absolute path to the input asset.")
    parser.add_argument("--output", required=False, help="Optional absolute path to the output markdown file.")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    if not os.path.exists(input_path):
        print(f"Error: Input file does not exist: {input_path}")
        sys.exit(1)

    ext = os.path.splitext(input_path)[1].lower()
    
    sys.stdout.write(f"Normalizing asset: {input_path}...\n")
    
    if ext in ['.pdf', '.docx', '.pptx']:
        sys.stdout.write(f"Routing to docling_parser for {ext}...\n")
        markdown_str = parse_docling(input_path)
    elif ext in ['.xlsx', '.csv']:
        sys.stdout.write(f"Routing to pandas_parser for {ext}...\n")
        markdown_str = parse_spreadsheet(input_path)
    elif ext in ['.eml']:
        sys.stdout.write(f"Routing to eml_parser for {ext}...\n")
        markdown_str = parse_eml(input_path)
    else:
        # Fallback to pure text reading if possible, else error
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            markdown_str = f"```text\n{content}\n```"
        except Exception:
            print(f"Error: Unsupported format {ext} and cannot read as text.")
            sys.exit(1)

    # Determine destination
    if not output_path:
        # Write to local ephemeral tmp if not provided
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'registry', '.tmp', 'normalized'))
        os.makedirs(base_dir, exist_ok=True)
        filename = os.path.basename(input_path) + ".md"
        output_path = os.path.join(base_dir, filename)

    try:
        # Make sure target directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.write(markdown_str)
        print(f"SUCCESS: {output_path}")
    except Exception as e:
        print(f"Error writing to output path {output_path}: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
