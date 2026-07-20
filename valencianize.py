import json
import re

def valencianize(text):
    if not isinstance(text, str):
        return text
    
    # Simple dictionary replacements for common Catalan -> Valencian traits
    replacements = [
        (r'\bseva\b', 'seua'),
        (r'\bseves\b', 'seues'),
        (r'\bteva\b', 'teua'),
        (r'\bteves\b', 'teues'),
        (r'\bmeva\b', 'meua'),
        (r'\bmeves\b', 'meues'),
        (r'\bSeva\b', 'Seua'),
        (r'\bSeves\b', 'Seues'),
        (r'\bTeva\b', 'Teua'),
        (r'\bTeves\b', 'Teues'),
        (r'\bMeva\b', 'Meua'),
        (r'\bMeves\b', 'Meues'),
        (r'\bsortir\b', 'eixir'),
        (r'\bsurt\b', 'eix'),
        (r'\bsurten\b', 'eixen'),
        (r'\bSortir\b', 'Eixir'),
        (r'\bSurt\b', 'Eix'),
        (r'\bSurten\b', 'Eixen'),
        (r'\bavui\b', 'hui'),
        (r'\bAvui\b', 'Hui'),
        (r'\bnoi\b', 'xic'),
        (r'\bnoia\b', 'xica'),
        (r'\bnois\b', 'xics'),
        (r'\bnoies\b', 'xiques'),
        (r'\bNoi\b', 'Xic'),
        (r'\bNoia\b', 'Xica'),
        (r'\bNois\b', 'Xics'),
        (r'\bNoies\b', 'Xiques'),
        (r'\bdesar\b', 'guardar'),
        (r'\bDesar\b', 'Guardar'),
        (r'\baquest\b', 'este'),
        (r'\baquesta\b', 'esta'),
        (r'\baquests\b', 'estos'),
        (r'\baquestes\b', 'estes'),
        (r'\bAquest\b', 'Este'),
        (r'\bAquesta\b', 'Esta'),
        (r'\bAquests\b', 'Estos'),
        (r'\bAquestes\b', 'Estes'),
        # Fix the article if necessary but we will skip complex grammar fixes
    ]
    
    for old, new in replacements:
        text = re.sub(old, new, text)
        
    return text

def main():
    with open('movies_data_va.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        if 'synopsis' in item:
            item['synopsis'] = valencianize(item['synopsis'])
            
    with open('movies_data_va.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print("Valencianized movies_data_va.json successfully!")

if __name__ == "__main__":
    main()
