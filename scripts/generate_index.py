import os
import re

def get_title(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
                elif line.startswith('#'):
                    return line[1:].strip()
    except Exception:
        pass
    return os.path.basename(file_path)

def generate_index(docs_dir, output_file):
    print(f"🔍 Scanning {docs_dir} for markdown files...")
    
    index_content = "# Hermes Agent Documentation Index\n\n"
    index_content += "This index is automatically generated to help troubleshoot and navigate Hermes Agent documentation.\n\n"
    
    # Walk through the directories
    for root, dirs, files in os.walk(docs_dir):
        # Skip the output file itself if it's in the same directory
        files = [f for f in files if f.endswith('.md') and f != os.path.basename(output_file)]
        if not files:
            continue
            
        relative_path = os.path.relpath(root, docs_dir)
        if relative_path == ".":
            header = "## Root"
        else:
            header = f"## {relative_path.replace(os.sep, ' / ').title()}"
            
        index_content += f"{header}\n\n"
        
        for file in sorted(files):
            file_path = os.path.join(root, file)
            title = get_title(file_path)
            link_path = os.path.relpath(file_path, docs_dir)
            index_content += f"*   [{title}]({link_path})\n"
            
        index_content += "\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✅ Index generated: {output_file}")

if __name__ == "__main__":
    DOCS_DIR = "references"
    OUTPUT_FILE = os.path.join(DOCS_DIR, "index.md")
    generate_index(DOCS_DIR, OUTPUT_FILE)
