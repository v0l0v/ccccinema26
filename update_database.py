import re
import json
import os

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

def extract_cast(tech):
    con_match = re.search(r'\bCon\b\s*', tech)
    if not con_match:
        return []
    
    start_pos = con_match.end()
    
    dur_match = re.search(r'\b\d+\s*(min|minutos)\b', tech[start_pos:], re.IGNORECASE)
    if dur_match:
        end_pos = start_pos + dur_match.start()
    else:
        end_pos = len(tech)
        
    cast_text = tech[start_pos:end_pos].strip()
    parts = re.split(r',|\by\b|;', cast_text)
    cast = [clean_name(p) for p in parts if clean_name(p)]
    return cast

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def main():
    if not os.path.exists('output.txt'):
        print("Error: output.txt not found. Convert PDF first.")
        return
        
    if not os.path.exists('movies_data.json'):
        print("Error: movies_data.json not found.")
        return
        
    with open('output.txt', 'r', encoding='utf-8') as f:
        raw_content = f.read()

    pages = raw_content.split('\x0c')
    useful_pages = [p for p in pages if 'EMBRIAGADOS DE HUMOR' in p]

    extracted = []
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
            
            next_start = len(lines)
            for ts in tech_starts:
                if ts > start_idx:
                    next_start = ts
                    break
                    
            syn_lines = []
            for idx in range(end_idx + 1, next_start):
                l = lines[idx].strip()
                if l and not l.isdigit() and 'EMBRIAGADOS DE HUMOR' not in l:
                    syn_lines.append(l)
                    
            syn_block = " ".join(syn_lines)
            
            extracted.append({
                "tech": clean_text(tech_block),
                "synopsis": clean_text(syn_block)
            })

    if len(extracted) != 27:
        print(f"Warning: Expected 27 movies, but extracted {len(extracted)}.")

    with open('movies_data.json', 'r', encoding='utf-8') as f:
        movies = json.load(f)

    # Let's update each movie in the json
    for i, m in enumerate(movies):
        if i < len(extracted):
            pdf_data = extracted[i]
            
            # Parse specs
            dirs = extract_directors(pdf_data["tech"])
            cast = extract_cast(pdf_data["tech"])
            syn = pdf_data["synopsis"]
            
            m["directors"] = dirs
            m["cast"] = cast
            m["synopsis"] = syn
            
            # Fix Joey Breaker year
            if m["title"] == "Joey Breaker":
                m["year"] = 1992
                
            # For 1987, the PDF has year 2009 in header but the text is about 2014. Let's keep 2014.
            
            print(f"Updated: {m['title']}")

    with open('movies_data.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

    print("movies_data.json updated successfully!")

if __name__ == '__main__':
    main()
