import json
from deep_translator import GoogleTranslator

def translate_to_va(text):
    if not text:
        return text
    try:
        # Translate Spanish to Catalan (Valencian is a variant of Catalan, Google Translate handles it via Catalan 'ca')
        return GoogleTranslator(source='es', target='ca').translate(text)
    except Exception as e:
        print(f"Error translating: {e}")
        return text

def main():
    with open('movies_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        print(f"Translating {item.get('title')}...")
        # Translate date (e.g. "Viernes, 31 de julio" -> "Divendres, 31 de juliol")
        item['date'] = translate_to_va(item.get('date', ''))
        
        # Translate title
        # item['title'] = translate_to_va(item.get('title', ''))  # Usually leave title as is!
        
        # Translate country
        item['country'] = translate_to_va(item.get('country', ''))
        
        # Translate duration
        item['duration'] = translate_to_va(item.get('duration', ''))
        
        # Translate genres
        item['genres'] = [translate_to_va(g) for g in item.get('genres', [])]
        
        # Translate synopsis
        item['synopsis'] = translate_to_va(item.get('synopsis', ''))

    with open('movies_data_va.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("Done!")

if __name__ == "__main__":
    main()
