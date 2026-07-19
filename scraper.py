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

def search_ddg(query):
    url = f'https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}'
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            links = soup.find_all('a', class_='result__url')
            results = []
            for l in links:
                href = l.get('href', '')
                if href:
                    results.append(href)
            return results
    except Exception as e:
        print(f"Error searching DDG for query '{query}': {e}")
    return []

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
                # Let's split by job words
                name = text.split('Director')[0].strip()
                directors.append(name)
        details['directors'] = directors
        
        # Find Cast
        cast = []
        for a in soup.find_all('a'):
            href = a.get('href', '')
            if '/person/' in href and a.text.strip():
                # Check if parent contains 'card' or 'people'
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
        print(f"\n[{idx+1}/{len(MOVIES)}] Processing: {movie['title']} ({movie['year']})...")
        
        # 1. Search TMDB URL
        tmdb_query = f"{movie['title']} {movie['year']} site:themoviedb.org/movie/"
        tmdb_links = search_ddg(tmdb_query)
        tmdb_url = None
        for link in tmdb_links:
            # We want the clean movie link, not cast/releases/etc
            if '/movie/' in link and not link.endswith('/cast') and not link.endswith('/releases') and not link.endswith('/images') and not link.endswith('/translations'):
                tmdb_url = link
                break
        
        if not tmdb_url and tmdb_links:
            # Fallback to first movie link
            for link in tmdb_links:
                if '/movie/' in link:
                    tmdb_url = link
                    break
        
        print(f"Found TMDB URL: {tmdb_url}")
        time.sleep(1.5)  # Be nice to DDG
        
        # 2. Search IMDb URL
        imdb_query = f"{movie['title']} {movie['year']} site:imdb.com/title/"
        imdb_links = search_ddg(imdb_query)
        imdb_url = None
        for link in imdb_links:
            if '/title/tt' in link:
                # extract tt number
                match = re.search(r'tt\d+', link)
                if match:
                    imdb_url = f"https://www.imdb.com/title/{match.group(0)}/"
                    break
        
        print(f"Found IMDb URL: {imdb_url}")
        time.sleep(1.5)
        
        # 3. Extract details from TMDB
        details = {}
        if tmdb_url:
            details = extract_tmdb_details(tmdb_url)
            time.sleep(1.5)  # Be nice to TMDB
        
        # 4. Merge details
        merged = {
            "date": movie["date"],
            "title": movie["title"],
            "year": movie["year"],
            "country": movie["country"],
            "duration": movie["duration"],
            "imdb_url": imdb_url,
            "tmdb_url": tmdb_url,
            "genres": details.get("genres", []),
            "directors": details.get("directors", []),
            "cast": details.get("cast", []),
            "synopsis": details.get("synopsis", ""),
            "poster_url": details.get("poster_url", "")
        }
        print(f"Scraped details: Director: {merged['directors']}, Cast size: {len(merged['cast'])}")
        scraped_data.append(merged)
        
        # Periodic save
        with open('movies_data_raw.json', 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, ensure_ascii=False, indent=2)

    print("\nAll done!")

if __name__ == '__main__':
    main()
