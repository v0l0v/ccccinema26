import re
import json

def unwrap_text(body_lines):
    """Join all lines into flowing text, with line breaks at natural credit boundaries."""
    text = ' '.join(l.strip() for l in body_lines if l.strip())
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(
        r'\. (?=(?:Director|Directora|Directores|Dirigid[ao]|Escrita|Esrita|'
        r'Gui[óo]n|Guionista|Guionistas|Argumento|Escrito|Basada|Basado|'
        r'Producci[óo]n|Producida|Productor|Fotograf[íi]a|Montaje|'
        r'Casting|Direcci[óo]n art[íi]stica|Director art[íi]stico|'
        r'Diseñ[oa]|Vestuario|Maquillaje|M[úu]sica|Sonido|'
        r'Decorados|Escenograf[íi]a|Efectos|Peluquer[íi]a|Dobles|'
        r'R[ó]tulos|Ayudante|Agradecimientos|Posproducci[óo]n|Escenarios|'
        r'Diseñ[oa] de sonido|M[úu]sica experimental|Con\s))',
        '.\n', text
    )
    return text

def parse_textos(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    blocks = re.split(r'\n\s*\n', text.strip())
    movies = []

    for block in blocks:
        lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
        if len(lines) < 3:
            continue

        date_line = lines[0]

        year_country_idx = next(
            (i for i, l in enumerate(lines) if re.match(r'\d{4}\.\s', l)),
            None
        )
        if year_country_idx is None:
            continue

        title = ' '.join(lines[1:year_country_idx]).strip()
        title_clean = re.sub(r'\s*\([^)]*\)', '', title).strip()

        year_country = lines[year_country_idx]
        yc_match = re.match(r'(\d{4})\.\s*(.*)', year_country)
        year = yc_match.group(1) if yc_match else ''
        country = yc_match.group(2).strip() if yc_match else year_country

        body_lines = lines[year_country_idx + 1:]

        duration = ''
        if body_lines and re.match(r'\d+\s*min(?:utos)?\.?', body_lines[-1], re.IGNORECASE):
            duration = body_lines.pop()

        credits_text = unwrap_text(body_lines)

        movie = {
            'date': date_line,
            'title': title_clean,
            'year': year,
            'country': country,
            'credits_text': credits_text,
            'duration': duration
        }
        movies.append(movie)

    return movies

if __name__ == '__main__':
    result = parse_textos('textos.txt')
    with open('credits_data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Parsed {len(result)} movies. Saved to credits_data.json")
