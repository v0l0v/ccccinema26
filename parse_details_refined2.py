import re

def clean_name(n):
    n = n.strip('.,:;()[]{}* ')
    n = re.sub(r'^(por|y|and)\b', '', n, flags=re.IGNORECASE).strip()
    n = re.sub(r'\b(y|and)$', '', n, flags=re.IGNORECASE).strip()
    return n

def extract_directors(tech):
    prefix_match = re.match(r'^(Director y guionista|Director|Dirigida por|Escrita y dirigida por|Esrita y dirigida por|Dirigida y escrita por|Escrita y dirigida)\b\s*:?\s*', tech, re.IGNORECASE)
    if not prefix_match:
        return []
    
    start_pos = prefix_match.end()
    
    # Expanded end markers to include variations of guionista
    end_markers = ['producción', 'producida', 'guión', 'guion', 'guionistas', 'guionista', 'productor', 'fotografía', 'casting', 'diseño', 'argumento', 'escrita', 'esrita', 'adaptación', 'música', 'rótulos', 'vestuario']
    pattern = r'\b(' + '|'.join(end_markers) + r')\b'
    
    end_match = re.search(pattern, tech[start_pos:], re.IGNORECASE)
    if end_match:
        end_pos = start_pos + end_match.start()
    else:
        end_pos = len(tech)
        
    dir_text = tech[start_pos:end_pos].strip()
    parts = re.split(r',|\by\b|\band\b', dir_text, flags=re.IGNORECASE)
    directors = [clean_name(p) for p in parts if clean_name(p)]
    return directors

# Test on test_extraction output
with open('output.txt', 'r', encoding='utf-8') as f:
    raw_content = f.read()

pages = raw_content.split('\x0c')
useful_pages = [p for p in pages if 'EMBRIAGADOS DE HUMOR' in p]

extracted_movies = []
for page_idx, page in enumerate(useful_pages):
    lines = [l.strip() for l in page.split('\n')]
    tech_starts = []
    for idx, line in enumerate(lines):
        if re.match(r'^(Director|Dirigida|Escrita|Esrita)\b', line, re.IGNORECASE):
            if not any(x in line.lower() for x in ['casting', 'artístico', 'artística', 'producción', 'vestuario', 'fotografía', 'sonido', 'escenografía']):
                tech_starts.append(idx)
                
    for start_idx in tech_starts:
        end_idx = start_idx
        for idx in range(start_idx, len(lines)):
            if re.search(r'\b(min|minutos)\b', lines[idx]):
                end_idx = idx
                break
        tech_block = " ".join(lines[start_idx:end_idx+1])
        extracted_movies.append(tech_block)

for idx, tech in enumerate(extracted_movies):
    dirs = extract_directors(tech)
    print(f"Movie {idx+1}: {dirs}")
