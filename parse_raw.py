import re

with open('output.txt', 'r', encoding='utf-8') as f:
    text = f.read()

pages = text.split('\x0c')
useful_pages = [p for p in pages if 'EMBRIAGADOS DE HUMOR' in p]

print(f"Found {len(useful_pages)} useful pages")

for page_idx, page in enumerate(useful_pages):
    print(f"\n--- PAGE {page_idx + 1} ---")
    lines = [l.strip() for l in page.split('\n')]
    
    # Let's find tech block starts
    tech_starts = []
    for idx, line in enumerate(lines):
        if re.match(r'^(Director|Dirigida|Escrita|Esrita)\b', line, re.IGNORECASE):
            tech_starts.append(idx)
            
    print(f"Tech block starts at lines: {tech_starts}")
    
    for start_idx in tech_starts:
        # Let's find where this tech block ends (a line containing 'min' or 'minutos')
        end_idx = start_idx
        for idx in range(start_idx, len(lines)):
            if re.search(r'\b(min|minutos)\b', lines[idx]):
                end_idx = idx
                break
        
        tech_text = " ".join(lines[start_idx:end_idx+1])
        print(f"Tech: {tech_text[:100]}... [Ends at line {end_idx}]")
        
        # The synopsis starts at end_idx + 1
        # It goes until the next tech block start or the end of the page lines
        next_start = len(lines)
        for ts in tech_starts:
            if ts > start_idx:
                next_start = ts
                break
                
        syn_lines = []
        for idx in range(end_idx + 1, next_start):
            # Clean up page numbers or header leftovers
            l = lines[idx].strip()
            if l and not l.isdigit() and 'EMBRIAGADOS DE HUMOR' not in l:
                syn_lines.append(l)
                
        syn_text = " ".join(syn_lines)
        print(f"Syn: {syn_text[:120]}...")
