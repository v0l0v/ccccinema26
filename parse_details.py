import re

def clean_name(n):
    n = re.sub(r'^(por|y|de)\b', '', n, flags=re.IGNORECASE)
    n = n.strip('.,:;()[]{}* y ')
    return n

def extract_directors(tech):
    # Remove prefix
    prefix_match = re.match(r'^(Director y guionista|Director|Dirigida por|Escrita y dirigida por|Esrita y dirigida por|Dirigida y escrita por|Escrita y dirigida)\b\s*:?\s*', tech, re.IGNORECASE)
    if not prefix_match:
        return []
    
    start_pos = prefix_match.end()
    
    # We find where the next block starts (e.g. Producción, Guión, Fotografía, etc.)
    end_match = re.search(r'\b(Producción|Producida|Guión|Guion|Productor|Fotografía|Casting|Diseño)\b', tech[start_pos:])
    if end_match:
        end_pos = start_pos + end_match.start()
    else:
        end_pos = len(tech)
        
    dir_text = tech[start_pos:end_pos].strip()
    # Split by comma and " y "
    parts = re.split(r',|\by\b', dir_text)
    directors = [clean_name(p) for p in parts if clean_name(p)]
    return directors

def extract_cast(tech):
    # Cast is after "Con " and before " \d+ min" or " \d+ minutos"
    con_match = re.search(r'\bCon\b\s*', tech)
    if not con_match:
        return []
    
    start_pos = con_match.end()
    
    # Find duration at the end
    dur_match = re.search(r'\b\d+\s*(min|minutos)\b', tech[start_pos:])
    if dur_match:
        end_pos = start_pos + dur_match.start()
    else:
        end_pos = len(tech)
        
    cast_text = tech[start_pos:end_pos].strip()
    # Split by comma, " y ", and maybe semi-colon
    parts = re.split(r',|\by\b|;', cast_text)
    cast = [clean_name(p) for p in parts if clean_name(p)]
    return cast

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

print(f"Extracted {len(extracted_movies)} blocks.")
for idx, tech in enumerate(extracted_movies):
    dirs = extract_directors(tech)
    cast = extract_cast(tech)
    print(f"\nMovie {idx+1}:")
    print(f"  Directors: {dirs}")
    print(f"  Cast (first 5): {cast[:5]} (Total: {len(cast)})")
