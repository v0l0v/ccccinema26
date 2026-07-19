import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import time
import re

MOVIES = [
    {"date": "Viernes, 31 de julio", "title": "Joey Breaker", "year": 1993, "country": "Estados Unidos", "duration": "92 minutos"},
    {"date": "Sábado, 1 de agosto", "title": "El artista", "year": 2008, "country": "Argentina-Italia", "duration": "100 minutos"},
    {"date": "Domingo, 2 de agosto", "title": "Mr. Belvedere Goes to College", "year": 1949, "country": "Estados Unidos", "duration": "83 minutos"},
    {"date": "Martes, 4 de agosto", "title": "Mátenme porque me muero", "year": 1951, "country": "México", "duration": "99 minutos"},
    {"date": "Miércoles, 5 de agosto", "title": "Things Change", "year": 1988, "country": "Estados Unidos", "duration": "100 minutos"},
    {"date": "Jueves, 6 de agosto", "title": "El destino no tiene favoritos", "year": 2003, "country": "Perú", "duration": "90 minutos"},
    {"date": "Viernes, 7 de agosto", "title": "Dim Sum: A Little Bit of Heart", "year": 1985, "country": "Estados Unidos", "duration": "84 minutos"},
    {"date": "Sábado, 8 de agosto", "title": "Safety Last!", "year": 1923, "country": "Estados Unidos", "duration": "74 minutos"},
    {"date": "Domingo, 9 de agosto", "title": "Plaff (Demasiado miedo a la vida)", "year": 1988, "country": "Cuba", "duration": "110 minutos"},
    {"date": "Martes, 11 de agosto", "title": "Bluff", "year": 2007, "country": "Colombia", "duration": "95 minutos"},
    {"date": "Miércoles, 12 de agosto", "title": "Little Shop of Horrors", "year": 1986, "country": "Estados Unidos", "duration": "104 minutos"},
    {"date": "Jueves, 13 de agosto", "title": "Culpa cero", "year": 2024, "country": "Argentina", "duration": "106 minutos"},
    {"date": "Viernes, 14 de agosto", "title": "The Sure Thing", "year": 1985, "country": "Estados Unidos", "duration": "100 minutos"},
    {"date": "Sábado, 15 de agosto", "title": "Denominación de origen", "year": 2024, "country": "Chile", "duration": "86 minutos"},
    {"date": "Domingo, 16 de agosto", "title": "Defending Your Life", "year": 1991, "country": "Estados Unidos", "duration": "112 minutos"},
    {"date": "Martes, 18 de agosto", "title": "De noche vienes, Esmeralda", "year": 1997, "country": "México", "duration": "103 minutos"},
    {"date": "Miércoles, 19 de agosto", "title": "She’s Gotta Have It", "year": 1986, "country": "Estados Unidos", "duration": "84 minutos"},
    {"date": "Jueves, 20 de agosto", "title": "Lisbela e o Prisioneiro", "year": 2003, "country": "Brasil", "duration": "106 minutos"},
    {"date": "Viernes, 21 de agosto", "title": "While We’re Young", "year": 2014, "country": "Estados Unidos", "duration": "97 minutos"},
    {"date": "Sábado, 22 de agosto", "title": "Doble discurso", "year": 2023, "country": "Argentina", "duration": "113 minutos"},
    {"date": "Domingo, 23 de agosto", "title": "Ella McCay", "year": 2025, "country": "Estados Unidos", "duration": "115 minutos"},
    {"date": "Martes, 25 de agosto", "title": "Never Give a Sucker an Even Break", "year": 1941, "country": "Estados Unidos", "duration": "71 minutos"},
    {"date": "Miércoles, 26 de agosto", "title": "1987", "year": 2014, "country": "Canadá", "duration": "105 minutos"},
    {"date": "Jueves, 27 de agosto", "title": "A New Leaf", "year": 1971, "country": "Estados Unidos", "duration": "102 minutos"},
    {"date": "Viernes, 28 de agosto", "title": "La práctica", "year": 2023, "country": "Argentina-Chile-Alemania-Portugal", "duration": "89 minutos"},
    {"date": "Sábado, 29 de agosto", "title": "Film Geek", "year": 2005, "country": "Estados Unidos", "duration": "78 minutos"},
    {"date": "Domingo, 30 de agosto", "title": "Un poeta", "year": 2025, "country": "Colombia-Alemania-Suecia", "duration": "123 minutos"}
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'
}

def search_tmdb(title, expected_year):
    search_url = f"https://www.themoviedb.org/search?query={urllib.parse.quote(title)}"
    try:
        r = requests.get(search_url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            print(f"TMDB Search error {r.status_code} for {title}")
            return None
        
        soup = BeautifulSoup(r.text, 'html.parser')
        cards = soup.find_all('div', class_='comp:media-card')
        
        best_href = None
        first_href = None
        
        for card in cards:
            link = card.find('a', href=lambda h: h and '/movie/' in h)
            if not link:
                continue
            
            href = link.get('href')
            if not href or href.endswith('/new'):
                continue
            
            if not first_href:
                first_href = href
                
            # Get text from spans to find the title and release date
            spans = [s.text.strip() for s in card.find_all('span') if s.text.strip()]
            
            # Find a date pattern in spans, e.g. "28 de mayo de 2009"
            year_found = None
            for span in spans:
                # Look for 4 consecutive digits
                match = re.search(r'\b(19\d{2}|20\d{2})\b', span)
                if match:
                    year_found = int(match.group(1))
                    break
            
            if year_found and abs(year_found - expected_year) <= 1:
                print(f"Match found! Year {year_found} vs expected {expected_year} for {href}")
                return f"https://www.themoviedb.org{href}"
                
        if first_href:
            print(f"Fallback to first result for {title}: {first_href}")
            return f"https://www.themoviedb.org{first_href}"
            
    except Exception as e:
        print(f"Search exception for {title}: {e}")
    return None

def extract_tmdb_details(tmdb_url):
    try:
        r = requests.get(tmdb_url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            print(f"Failed to fetch {tmdb_url}: {r.status_code}")
            return {}
        
        soup = BeautifulSoup(r.text, 'html.parser')
        details = {}
        
        # Parse JSON-LD
        script = soup.find('script', type='application/ld+json')
        if script:
            text = script.string.strip()
            if text.startswith('/* <![CDATA[ */'):
                text = text[len('/* <![CDATA[ */'):].strip()
            if text.endswith('/* ]]> */'):
                text = text[:-len('/* ]]> */')].strip()
            try:
                data = json.loads(text)
                details['tmdb_title'] = data.get('name')
                details['synopsis'] = data.get('description')
                details['poster_url'] = data.get('image')
                details['genres'] = data.get('genre', [])
            except Exception as ex:
                print(f"Error parsing JSON-LD: {ex}")
        
        # Find Director
        directors = []
        for p in soup.find_all('li', class_='profile'):
            text = p.text.strip().replace('\n', ' ')
            if 'Director' in text or 'director' in text:
                # E.g. "Steven Starr Director, Writer" -> strip out jobs
                # We split by 'Director'
                name = text.split('Director')[0].strip()
                if name and name not in directors:
                    directors.append(name)
        details['directors'] = directors
        
        # Find Cast
        cast = []
        for a in soup.find_all('a'):
            href = a.get('href', '')
            if '/person/' in href and a.text.strip():
                parent_classes = [c for parent in a.parents for c in parent.get('class', [])]
                if 'card' in parent_classes or 'people' in parent_classes:
                    name = a.text.strip()
                    if name not in cast and name not in directors:
                        cast.append(name)
        details['cast'] = cast[:8]  # Limit to 8 main actors
        
        return details
    except Exception as e:
        print(f"Error extracting TMDB details from {tmdb_url}: {e}")
    return {}

def main():
    scraped_data = []
    for idx, movie in enumerate(MOVIES):
        print(f"\n[{idx+1}/{len(MOVIES)}] Searching: {movie['title']} ({movie['year']})...")
        tmdb_url = search_tmdb(movie['title'], movie['year'])
        print(f"Selected URL: {tmdb_url}")
        
        details = {}
        if tmdb_url:
            details = extract_tmdb_details(tmdb_url)
            
        merged = {
            "date": movie["date"],
            "title": movie["title"],
            "year": movie["year"],
            "country": movie["country"],
            "duration": movie["duration"],
            "tmdb_url": tmdb_url,
            "genres": details.get("genres", []),
            "directors": details.get("directors", []),
            "cast": details.get("cast", []),
            "synopsis": details.get("synopsis", ""),
            "poster_url": details.get("poster_url", "")
        }
        print(f"Success! Directors: {merged['directors']}, Cast: {merged['cast'][:3]}")
        scraped_data.append(merged)
        
        # Save after each movie
        with open('movies_data.json', 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, ensure_ascii=False, indent=2)
            
        time.sleep(1.0) # Be polite

if __name__ == '__main__':
    main()
