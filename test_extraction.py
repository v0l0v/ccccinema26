import re
import json

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

with open('output.txt', 'r', encoding='utf-8') as f:
    raw_content = f.read()

# Split into pages by form feed character
pages = raw_content.split('\x0c')
useful_pages = [p for p in pages if 'EMBRIAGADOS DE HUMOR' in p]

extracted_movies = []

for page_idx, page in enumerate(useful_pages):
    lines = [l.strip() for l in page.split('\n')]
    
    # Find start lines of the main technical blocks
    tech_starts = []
    for idx, line in enumerate(lines):
        if re.match(r'^(Director|Dirigida|Escrita|Esrita)\b', line, re.IGNORECASE):
            # Exclude false positives like "Director de casting" or "Director artístico"
            if not any(x in line.lower() for x in ['casting', 'artístico', 'artística', 'producción', 'vestuario', 'fotografía', 'sonido', 'escenografía']):
                tech_starts.append(idx)
                
    for start_idx in tech_starts:
        # Find where this technical block ends
        end_idx = start_idx
        for idx in range(start_idx, len(lines)):
            if re.search(r'\b(min|minutos)\b', lines[idx]):
                end_idx = idx
                break
                
        tech_block = " ".join(lines[start_idx:end_idx+1])
        
        # The synopsis starts at end_idx + 1 and goes until the next technical block start or end of lines
        next_start = len(lines)
        for ts in tech_starts:
            if ts > start_idx:
                next_start = ts
                break
                
        syn_lines = []
        for idx in range(end_idx + 1, next_start):
            l = lines[idx].strip()
            # Skip page numbers, header lines, and blank lines
            if l and not l.isdigit() and 'EMBRIAGADOS DE HUMOR' not in l:
                syn_lines.append(l)
                
        syn_block = " ".join(syn_lines)
        
        extracted_movies.append({
            "tech": clean_text(tech_block),
            "synopsis": clean_text(syn_block)
        })

print(f"Extracted {len(extracted_movies)} movies.")
for i, m in enumerate(extracted_movies):
    print(f"\n--- Movie {i+1} ---")
    print(f"Tech: {m['tech'][:120]}...")
    print(f"Synopsis: {m['synopsis'][:150]}...")
