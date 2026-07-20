import json
import urllib.parse
import os

def main():
    if not os.path.exists('movies_data_va.json'):
        print("Error: movies_data_va.json not found!")
        return

    with open('movies_data_va.json', 'r', encoding='utf-8') as f:
        movies = json.load(f)

    # Generate movie cards HTML
    cards_html = ""
    for idx, m in enumerate(movies):
        # Join genres
        genres_badges = "".join([f'<span class="genre-badge" onclick="event.stopPropagation(); filterByGenre(\'{g}\')">{g}</span>' for g in m['genres']])
        
        # Format directors and cast
        directors = ", ".join(m['directors']) if m['directors'] else "No disponible"
        cast = ", ".join(m['cast'][:5]) if m['cast'] else "No disponible"
        
        # Prepare share messages
        # URL-encoded text
        share_title = m['title']
        share_director = m['directors'][0] if m['directors'] else "director desconocido"
        imdb_link = m['imdb_url'] or m['tmdb_url'] or "https://www.imdb.com"
        
        whatsapp_text = urllib.parse.quote(f"🎥 *{share_title}* ({m['year']})\n📅 {m['date']}\n🎬 Dirigida por: {share_director}\n⏱️ Duración: {m['duration']}\n🔍 Más info: {imdb_link}")
        # Compartir (ahora genera entradas visuales)
        card_id = f"card-{{idx}}"
        
        # Dynamic poster fallback
        poster_src = m['poster_url'] if m['poster_url'] else 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80'
        
        # Extract short day name and date for visual badge
        # e.g., "Viernes, 31 de julio" -> Day: "Vie", Date: "31 Jul"
        date_parts = m['date'].split(',')
        day_name = date_parts[0][:3].upper() if len(date_parts) > 0 else "FILM"
        date_num = date_parts[1].strip().replace(" de ", " ") if len(date_parts) > 1 else ""
        # Shorten month name if possible
        date_num = date_num.replace("julio", "Jul").replace("agosto", "Ago")
        
        youtube_id = m.get('youtube_id', '')
        yt_thumb = f'https://img.youtube.com/vi/{youtube_id}/maxresdefault.jpg' if youtube_id else poster_src
        cards_html += f"""
        <div class="movie-card" onclick="openModal({idx})" data-title="{m['title'].lower()}" data-director="{directors.lower()}" data-genres="{','.join(m['genres']).lower()}" data-country="{m['country'].lower()}" data-date="{m['date'].lower()}" data-cast="{','.join(m['cast']).lower() if m['cast'] else ''}">
            <div class="card-header-img">
                <img class="poster-img" src="{poster_src}" alt="Pòster de {m['title']}" loading="lazy">
                <div class="thumb-overlay" data-yt-id="{youtube_id}" style="background-image: url('{yt_thumb}')"></div>
                <button class="bookmark-btn" onclick="event.stopPropagation(); toggleBookmark({idx})" data-idx="{idx}" title="Guardar al Meu Diari" aria-label="Guardar al Meu Diari">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>
                </button>
                <div class="date-badge">
                    <span class="day">{day_name}</span>
                    <span class="num">{date_num}</span>
                </div>
                <div class="duration-pill">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                    {m['duration']}
                </div>
            </div>
            
            <div class="card-body">
                <div class="title-section">
                    <h3 class="movie-title">{m['title']} <span class="movie-year">({m['year']})</span></h3>
                    <p class="movie-country">{m['country']}</p>
                </div>
                
                <div class="genres-container">
                    {genres_badges}
                </div>
                

                
                <div class="tech-spec-grid">
                    <div class="spec-item">
                        <span class="spec-label">Director:</span>
                        <span class="spec-value">{directors}</span>
                    </div>
                    <div class="spec-item">
                        <span class="spec-label">Repartiment principal:</span>
                        <span class="spec-value">{cast}</span>
                    </div>
                </div>
            </div>
            
            <div class="card-footer">
                <div class="links-row">
                    <button class="details-btn" onclick="event.stopPropagation(); openModal({idx})">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                        Vore Detalls
                    </button>
                </div>
                <div class="share-row">
                    <span class="share-label">Generar Entrada:</span>
                    <div class="share-buttons">
                        <button onclick="event.stopPropagation(); generateAndShareTicket({idx})" class="share-btn whatsapp" title="Compartir Entrada per WhatsApp" aria-label="Compartir per WhatsApp">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.012 2c-5.506 0-9.989 4.478-9.99 9.984a9.96 9.96 0 0 0 1.335 4.963L2 22l5.233-1.371a9.948 9.948 0 0 0 4.779 1.218h.004c5.502 0 9.99-4.478 9.99-9.988.002-2.67-1.034-5.177-2.92-7.062C17.199 3.013 14.691 2 12.012 2zm4.72 13.568c-.26.732-1.503 1.35-2.065 1.415-.561.066-1.125.107-1.912-.139a11.516 11.516 0 0 1-5.158-3.177 12.19 12.19 0 0 1-2.203-3.666 4.3 4.3 0 0 1-.225-1.92c.166-.889.585-1.38.868-1.745.283-.365.617-.456.822-.456.205 0 .41.002.589.012.192.01.442-.074.693.528.26.626.884 2.144.962 2.302.078.158.13.342.026.55-.104.208-.156.342-.312.521-.156.18-.328.401-.468.538-.156.152-.32.318-.138.63.182.312.812 1.337 1.737 2.164.925.826 1.704 1.08 2.029 1.215.325.135.513.114.707-.107.195-.221.844-.981 1.071-1.317.227-.336.455-.28.766-.165.311.115 1.97.928 2.307 1.096.337.168.562.25.642.387.08.137.08.795-.18 1.527z"/></svg>
                        </button>
                        <button onclick="event.stopPropagation(); generateAndShareTicket({idx})" class="share-btn telegram" title="Compartir Entrada per Telegram" aria-label="Compartir per Telegram">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-1-.65-.35-1 .22-1.6.15-.15 2.72-2.5 2.77-2.7.01-.03.01-.15-.06-.21-.07-.06-.17-.04-.25-.02-.11.02-1.92 1.23-5.43 3.59-.51.35-.97.52-1.37.51-.44-.01-1.29-.25-1.92-.45-.77-.25-1.38-.39-1.33-.82.03-.22.33-.45.92-.69 3.6-1.57 6-2.6 7.2-3.1 3.42-1.42 4.12-1.67 4.59-1.68.1 0 .33.02.48.15.12.1.16.24.18.34.02.09.02.26 0 .31z"/></svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        """

    # Read base index.html template and insert
    html_content = f"""<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cine Club CCC - Ciclo de Agosto 2026</title>
    
    <!-- Meta tags for SEO & Sharing -->
    <meta name="description" content="Descubre la cartelera completa del Ciclo de Cine CCC para agosto de 2026. Fichas técnicas, sinopsis, imágenes y enlaces de compartir para WhatsApp y Telegram.">
    <meta property="og:title" content="Cine Club CCC - Ciclo de Agosto 2026">
    <meta property="og:description" content="Programación completa de películas desde el 31 de julio hasta el 30 de agosto de 2026. Tarjetas interactivas de películas para compartir.">
    <meta property="og:image" content="https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800&q=80">
    <meta property="og:type" content="website">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,600&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --bg-primary: #122d2a;      /* verde muy oscuro basado en el cartel */
            --bg-secondary: #1a423e;
            --bg-card: rgba(29, 70, 66, 0.6);
            --bg-card-hover: rgba(19, 120, 82, 0.3);
            --accent: #d22c36;          /* granate/rojo carmesí del macetero/boca */
            --accent-glow: rgba(210, 44, 54, 0.4);
            --teal: #137852;            /* verde medio de las hojas */
            --teal-light: #4db579;      /* verde claro de los detalles de las hojas */
            --cream: #f7f0e1;           /* crema del fondo del cartel */
            --text-main: #f7f0e1;
            --text-muted: #a6c4b5;
            --text-dark: #6a9680;
            --border-color: rgba(77, 181, 121, 0.15);
            --shadow-glow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            
            --whatsapp: #25d366;
            --telegram: #0088cc;
            --imdb: #f5c518;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            background-color: var(--bg-primary);
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
            line-height: 1.6;
            overflow-x: hidden;
            background-image: 
                radial-gradient(ellipse at 15% 0%, rgba(19, 120, 82, 0.25) 0%, transparent 50%),
                radial-gradient(ellipse at 85% 10%, rgba(210, 44, 54, 0.15) 0%, transparent 45%);
            background-attachment: fixed;
        }}
        
        #app-bg {{
            position: fixed;
            top: -20%;
            left: -20%;
            width: 140%;
            height: 140%;
            background-image: url('poster.png');
            background-size: cover;
            background-position: center;
            filter: blur(33px);
            opacity: 0.25;
            transform: rotate(-12deg) scale(1.1);
            z-index: -10;
            pointer-events: none;
        }}
        
        header {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 4rem 2rem 3rem;
            display: grid;
            grid-template-columns: 1fr auto;
            align-items: center;
            gap: 3rem;
            text-align: left;
        }}
        
        .header-content {{
            min-width: 0;
        }}
        
        .header-poster {{
            flex-shrink: 0;
            width: 220px;
            position: relative;
        }}
        
        .header-poster img {{
            width: 100%;
            border-radius: 8px;
            box-shadow:
                0 4px 6px rgba(0,0,0,0.2),
                0 20px 60px rgba(0,0,0,0.5),
                0 0 0 1px rgba(255,255,255,0.06);
            transform: rotate(2deg);
            transition: transform 0.4s ease;
        }}
        
        .header-poster img:hover {{
            transform: rotate(0deg) scale(1.03);
        }}
        
        .download-program-link {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            margin-top: 1.5rem;
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 500;
            opacity: 0.7;
            transition: all 0.2s ease;
        }}

        .download-program-link:hover {{
            opacity: 1;
            color: var(--cream);
            transform: translateY(-2px);
        }}
        
        .header-eyebrow {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.25rem;
        }}
        
        .header-logo {{
            font-size: 0.9rem;
            font-weight: 800;
            letter-spacing: 0.12rem;
            color: var(--text-muted);
            text-transform: uppercase;
        }}
        
        .header-divider {{
            width: 1px;
            height: 1rem;
            background: var(--border-color);
        }}
        
        .header-tag {{
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 0.2rem;
            font-weight: 700;
            font-size: 0.78rem;
            display: inline-block;
        }}
        
        .lang-switcher {{
            margin-left: auto;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.1rem;
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }}
        
        .lang-switcher a {{
            color: var(--text-muted);
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        .lang-switcher a:hover {{
            color: var(--cream);
        }}
        
        .lang-switcher span.active {{
            color: var(--accent);
        }}
        
        .ambient-btn {{
            background: rgba(11, 15, 25, 0.4);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8rem;
            cursor: pointer;
            margin-left: 12px;
            transition: all 0.3s;
            font-family: 'Space Grotesk', sans-serif;
            letter-spacing: 1px;
            backdrop-filter: blur(4px);
        }}
        .ambient-btn:hover {{
            border-color: var(--primary-color);
            color: var(--primary-color);
        }}
        
        h1 {{
            font-family: 'Barlow Condensed', sans-serif;
            font-size: clamp(3.5rem, 7vw, 6.5rem);
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.1em;
            line-height: 0.92;
            color: var(--cream);
            /* Subtle double-color effect like the poster */
            background: none;
            -webkit-text-fill-color: var(--cream);
        }}
        
        .header-subtitle-edition {{
            font-family: 'Barlow Condensed', sans-serif;
            font-size: clamp(2.5rem, 5vw, 4.2rem);
            font-weight: 800;
            letter-spacing: 0.02em;
            text-transform: uppercase;
            color: var(--accent);
            margin-top: -0.1em;
            margin-bottom: 1.5rem;
            line-height: 1;
            text-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }}
        
        .subtitle {{
            color: var(--text-muted);
            max-width: 560px;
            margin-bottom: 1.75rem;
            font-size: 0.95rem;
            font-weight: 300;
            line-height: 1.7;
        }}
        
        .header-info-pills {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.6rem;
            margin-bottom: 1.75rem;
        }}
        
        .info-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-muted);
            padding: 0.4rem 0.9rem;
            border-radius: 50px;
            font-size: 0.82rem;
            font-weight: 500;
        }}
        
        .info-pill svg {{
            width: 0.85rem;
            height: 0.85rem;
            color: var(--accent);
            flex-shrink: 0;
        }}
        
        /* Share program banner */
        .share-program-container {{
            margin-top: 0;
        }}
        .share-program-btn {{
            background: rgba(200, 54, 43, 0.12);
            border: 1px solid var(--accent);
            color: var(--accent);
            padding: 0.6rem 1.2rem;
            border-radius: 50px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .share-program-btn:hover {{
            background: var(--accent);
            color: #fff;
            box-shadow: 0 0 20px var(--accent-glow);
            transform: translateY(-2px);
        }}
        
        @media (max-width: 768px) {{
            header {{
                grid-template-columns: 1fr;
                text-align: center;
                padding: 3rem 1.5rem 2rem;
                gap: 2rem;
            }}
            .header-poster {{
                width: 160px;
                margin: 0 auto;
            }}
            .header-eyebrow, .header-info-pills {{
                justify-content: center;
            }}
            .subtitle {{ max-width: 100%; }}
        }}
        
        /* Filters and Search */
        .controls-wrapper {{
            max-width: 1200px;
            margin: 0 auto 3rem;
            padding: 0 1.5rem;
        }}
        
        .controls-card {{
            background: rgba(30, 41, 59, 0.2);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: var(--shadow-glow);
            display: flex;
            flex-direction: column;
            gap: 1.2rem;
        }}
        
        .search-row {{
            position: relative;
            width: 100%;
        }}
        
        .search-input {{
            width: 100%;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            padding: 1rem 3.5rem 1rem 3rem;
            border-radius: 12px;
            color: var(--text-main);
            font-size: 1rem;
            font-family: inherit;
            transition: all 0.3s ease;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 10px rgba(245, 158, 11, 0.15);
            background: rgba(15, 23, 42, 0.8);
        }}
        
        .search-icon {{
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            width: 1.2rem;
            height: 1.2rem;
            color: var(--text-dark);
            pointer-events: none;
        }}
        
        .filters-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            align-items: center;
            justify-content: center;
        }}
        
        .filter-label {{
            color: var(--text-muted);
            font-size: 0.9rem;
            font-weight: 500;
            margin-right: 0.5rem;
        }}
        
        .filter-chip {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 0.4rem 1rem;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .filter-chip:hover {{
            background: rgba(255, 255, 255, 0.1);
            color: var(--text-main);
        }}
        
        .filter-chip.active {{
            background: var(--accent);
            border-color: var(--accent);
            color: var(--bg-primary);
            font-weight: 600;
            box-shadow: 0 0 10px var(--accent-glow);
        }}
        
        .stats-row {{
            color: var(--text-muted);
            font-size: 0.85rem;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1.5rem;
            border-top: 1px solid var(--border-color);
            padding-top: 0.75rem;
            text-align: center;
        }}
        
        .clear-filters-btn {{
            color: var(--accent);
            background: none;
            border: none;
            font-family: inherit;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.85rem;
            transition: opacity 0.2s;
        }}
        
        .clear-filters-btn:hover {{
            text-decoration: underline;
        }}
        
        .filter-saved-btn {{
            position: absolute;
            right: 0.5rem;
            top: 50%;
            transform: translateY(-50%);
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-muted);
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .filter-saved-btn svg {{
            width: 1.4rem;
            height: 1.4rem;
        }}
        
        .filter-saved-btn:hover {{
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }}
        
        .filter-saved-btn.active {{
            color: var(--accent);
            background: rgba(210, 44, 54, 0.15);
            border-color: rgba(210, 44, 54, 0.3);
        }}
        
        .filter-saved-btn.active svg {{
            fill: var(--accent);
            stroke: var(--accent);
        }}
        
        /* Grid */
        .movies-grid {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem 5rem;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 2.5rem 2rem;
            transition: all 0.3s ease;
        }}
        
        /* Movie Card */
        .movie-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: var(--shadow-glow);
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            height: 100%;
        }}
        
        .movie-card:hover {{
            transform: translateY(-8px);
            border-color: rgba(245, 158, 11, 0.4);
            background: var(--bg-card-hover);
            box-shadow: 0 20px 38px rgba(0,0,0,0.5), 0 0 20px rgba(245,158,11,0.05);
        }}
        
        .card-header-img {{
            position: relative;
            height: 480px;
            overflow: hidden;
        }}
        
        /* Ken Burns: poster zoom on hover */
        .card-header-img img.poster-img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.8s cubic-bezier(0.165, 0.84, 0.44, 1), opacity 0.6s ease;
            transform-origin: center center;
        }}
        
        .movie-card:hover .card-header-img img.poster-img {{
            transform: scale(1.12);
        }}

        /* YouTube thumbnail overlay with Ken Burns */
        @keyframes kenBurns {{
            0%   {{ transform: scale(1.05) translate(0, 0); }}
            33%  {{ transform: scale(1.12) translate(-1.5%, 1%); }}
            66%  {{ transform: scale(1.1)  translate(1.5%, -0.5%); }}
            100% {{ transform: scale(1.05) translate(0, 0); }}
        }}
        
        .thumb-overlay {{
            position: absolute;
            top: -5%;
            left: -5%;
            width: 110%;
            height: 110%;
            z-index: 1;
            background-size: cover;
            background-position: center;
            opacity: 0;
            transition: opacity 0.8s ease;
            transform: scale(1.05);
            pointer-events: none;
        }}
        
        .movie-card:hover .thumb-overlay {{
            opacity: 1;
            animation: kenBurns 8s ease-in-out infinite;
        }}
        
        .card-header-img::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 40%;
            background: linear-gradient(to top, var(--bg-primary) 0%, transparent 100%);
            pointer-events: none;
            z-index: 2;
        }}
        
        /* Bookmark Button */
        .bookmark-btn {{
            position: absolute;
            top: 1.25rem;
            right: 1.25rem;
            z-index: 5;
            background: rgba(11, 15, 25, 0.7);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #fff;
            width: 38px;
            height: 38px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        
        .bookmark-btn svg {{
            width: 1.2rem;
            height: 1.2rem;
        }}
        
        .bookmark-btn:hover {{
            transform: scale(1.1);
            background: rgba(11, 15, 25, 0.9);
        }}
        
        .bookmark-btn.saved {{
            background: var(--accent);
            border-color: var(--accent);
        }}
        
        .bookmark-btn.saved svg {{
            fill: #fff;
            color: var(--accent);
            stroke: #fff;
        }}

        /* Badge Date */
        .date-badge {{
            position: absolute;
            top: 1.25rem;
            left: 1.25rem;
            z-index: 2;
            background: rgba(11, 15, 25, 0.85);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid var(--border-color);
            padding: 0.6rem 0.9rem;
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            z-index: 2;
        }}
        
        .date-badge .day {{
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--accent);
            letter-spacing: 0.1rem;
            text-transform: uppercase;
        }}
        
        .date-badge .num {{
            font-size: 0.95rem;
            font-weight: 800;
            color: var(--text-main);
            margin-top: 0.1rem;
        }}
        
        /* Duration Pill */
        .duration-pill {{
            position: absolute;
            bottom: 1.25rem;
            right: 1.25rem;
            z-index: 2;
            background: rgba(11, 15, 25, 0.75);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            border: 1px solid var(--border-color);
            padding: 0.4rem 0.8rem;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 0.4rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            z-index: 2;
        }}
        
        .duration-pill svg {{
            width: 0.85rem;
            height: 0.85rem;
            color: var(--accent);
        }}
        
        /* Card Body */
        .card-body {{
            padding: 1.75rem;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
            background: linear-gradient(to bottom, var(--bg-primary) 0%, rgba(19, 26, 44, 0.3) 100%);
        }}
        
        .title-section {{
            margin-bottom: 1rem;
        }}
        
        .movie-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            font-weight: 700;
            line-height: 1.3;
            color: var(--text-main);
            margin-bottom: 0.25rem;
        }}
        
        .movie-year {{
            color: var(--text-muted);
            font-weight: 400;
            font-size: 1.1rem;
        }}
        
        .movie-country {{
            font-size: 0.85rem;
            color: var(--accent);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05rem;
        }}
        
        /* Genre list */
        .genres-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            margin-bottom: 1.25rem;
        }}
        
        .genre-badge {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            font-size: 0.75rem;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .genre-badge:hover {{
            background: var(--accent-glow);
            color: var(--accent);
            border-color: var(--accent);
        }}
        
        /* Synopsis */
        .synopsis-container {{
            margin-bottom: 1.5rem;
            position: relative;
        }}
        
        .synopsis-text {{
            font-size: 0.9rem;
            color: var(--text-muted);
        }}
        
        /* Technical details */
        .tech-spec-grid {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            border-top: 1px solid var(--border-color);
            padding-top: 1.25rem;
            margin-top: auto;
        }}
        
        .spec-item {{
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }}
        
        .spec-label {{
            font-size: 0.75rem;
            color: var(--text-dark);
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.05rem;
        }}
        
        .spec-value {{
            font-size: 0.9rem;
            color: var(--text-main);
            font-weight: 400;
        }}
        
        /* Footer Actions */
        .card-footer {{
            padding: 1.25rem 1.75rem;
            background: rgba(11, 15, 25, 0.4);
            border-top: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        .links-row {{
            display: flex;
            width: 100%;
        }}
        
        .imdb-btn {{
            width: 100%;
            background: var(--imdb);
            color: #000;
            font-weight: 700;
            text-decoration: none;
            padding: 0.7rem;
            border-radius: 12px;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(245, 197, 24, 0.15);
        }}
        
        .imdb-btn:hover {{
            background: #fff;
            box-shadow: 0 6px 18px rgba(255, 255, 255, 0.25);
            transform: translateY(-1px);
        }}
        
        .imdb-btn svg {{
            width: 1.2rem;
            height: 1.2rem;
        }}
        
        .share-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 0.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.03);
        }}
        
        .share-label {{
            font-size: 0.8rem;
            color: var(--text-dark);
            text-transform: uppercase;
            font-weight: 700;
        }}
        
        .share-buttons {{
            display: flex;
            gap: 0.6rem;
        }}
        
        .share-btn {{
            width: 2.2rem;
            height: 2.2rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            color: #fff;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
        }}
        
        .share-btn svg {{
            width: 1.1rem;
            height: 1.1rem;
        }}
        
        .share-btn.whatsapp:hover {{
            background: var(--whatsapp);
            border-color: var(--whatsapp);
            box-shadow: 0 0 12px rgba(37, 211, 102, 0.4);
            transform: scale(1.1);
        }}
        
        .share-btn.telegram:hover {{
            background: var(--telegram);
            border-color: var(--telegram);
            box-shadow: 0 0 12px rgba(0, 136, 204, 0.4);
            transform: scale(1.1);
        }}
        
        .share-btn.native {{
            display: none;
            border: none;
            cursor: pointer;
        }}
        
        .share-btn.native:hover {{
            background: rgba(255, 255, 255, 0.15);
            transform: scale(1.1);
        }}
        
        @media (max-width: 768px) {{
            .share-btn.native {{
                display: flex;
            }}
        }}
        
        /* Empty State */
        .empty-state {{
            grid-column: 1 / -1;
            text-align: center;
            padding: 4rem 2rem;
            color: var(--text-muted);
            display: none;
        }}
        
        .empty-state svg {{
            width: 4rem;
            height: 4rem;
            margin-bottom: 1.5rem;
            color: var(--text-dark);
            stroke-width: 1.5;
        }}
        
        .empty-state h3 {{
            font-size: 1.5rem;
            color: var(--text-main);
            margin-bottom: 0.5rem;
        }}
        

        
        /* Toast notification */
        .toast {{
            position: fixed;
            bottom: 2rem;
            left: 50%;
            background: var(--bg-secondary);
            border: 1px solid var(--accent);
            color: var(--text-main);
            padding: 0.8rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            gap: 0.6rem;
            z-index: 2000;
            opacity: 0;
            pointer-events: none;
            transform: translateX(-50%) translateY(150px);
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        
        .toast.show {{
            transform: translateX(-50%) translateY(0);
            opacity: 1;
            pointer-events: auto;
        }}
        
        .toast svg {{
            color: var(--accent);
            width: 1.2rem;
            height: 1.2rem;
        }}
        
        /* Poster Modal */
        #poster-modal {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }}
        .poster-modal-img {{
            max-width: 100%;
            max-height: 95vh;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8);
            transform: scale(0.95);
            transition: transform 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
            cursor: zoom-out;
        }}
        #poster-modal.open .poster-modal-img {{
            transform: scale(1);
        }}
        
        /* Modal Detail View Overlay */
        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(3, 7, 18, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            z-index: 1000;
            display: block;
            padding: 4rem 1rem;
            overflow-y: auto;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.4s ease;
        }}
        
        .modal-overlay.open {{
            opacity: 1;
            pointer-events: all;
        }}
        
        .modal-container {{
            position: relative;
            width: 100%;
            max-width: 1000px;
            background: #0e1322;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            transform: scale(0.95) translateY(10px);
            transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            margin: 0 auto;
        }}
        
        .modal-overlay.open .modal-container {{
            transform: scale(1) translateY(0);
        }}
        
        .modal-close-btn {{
            position: absolute;
            top: 1.5rem;
            right: 1.5rem;
            z-index: 1100;
            width: 3rem;
            height: 3rem;
            border-radius: 50%;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        }}
        
        .modal-close-btn:hover {{
            background: var(--accent);
            border-color: var(--accent);
            color: #000;
            transform: rotate(90deg);
            box-shadow: 0 0 15px var(--accent);
        }}
        
        .modal-video-header {{
            position: relative;
            width: 100%;
            display: flex;
            flex-direction: column;
            background: #000;
            overflow: hidden;
        }}
        
        .video-wrapper {{
            position: relative;
            width: 100%;
            padding-bottom: 50.25%; /* 16:9 Aspect Ratio */
        }}
        
        .video-wrapper iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
            pointer-events: none;
            opacity: 0;
            transition: opacity 1.5s ease-in;
        }}
        
        .video-wrapper iframe.fade-in {{
            opacity: 1;
        }}
        
        .video-overlay-gradient {{
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 50%;
            background: linear-gradient(to top, #0e1322, transparent);
            pointer-events: none;
        }}
        
        .modal-header-info {{
            position: absolute;
            bottom: 2rem;
            left: 3rem;
            right: 3rem;
            z-index: 2;
            pointer-events: none;
        }}
        
        .modal-date-badge {{
            font-size: 0.8rem;
            color: var(--accent);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.15rem;
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid var(--accent);
            padding: 0.35rem 0.8rem;
            border-radius: 50px;
            display: inline-block;
        }}
        
        .modal-title {{
            font-family: 'Playfair Display', serif;
            font-size: 2.8rem;
            font-weight: 800;
            text-shadow: 0 4px 12px rgba(0,0,0,0.6);
            line-height: 1.2;
            margin-top: 0.6rem;
            color: #fff;
        }}
        
        .modal-subtitle {{
            font-size: 1.1rem;
            color: var(--text-muted);
            font-weight: 300;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            margin-top: 0.25rem;
        }}
        
        .modal-body {{
            padding: 3rem;
            background: #0e1322;
        }}
        
        .modal-grid {{
            display: grid;
            grid-template-columns: 240px 1fr;
            gap: 3rem;
        }}
        
        .modal-poster-wrapper {{
            width: 100%;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 12px 24px rgba(0,0,0,0.5);
            background: rgba(255,255,255,0.02);
            aspect-ratio: 2/3;
        }}
        
        .modal-poster-wrapper img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .modal-meta-pills {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin-top: 1.5rem;
        }}
        
        .meta-pill-item {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255,255,255,0.05);
            padding: 0.75rem 1rem;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }}
        
        .pill-label {{
            font-size: 0.7rem;
            text-transform: uppercase;
            color: var(--text-dark);
            font-weight: 700;
            letter-spacing: 0.05rem;
        }}
        
        .pill-value {{
            font-size: 0.95rem;
            color: var(--text-main);
            font-weight: 500;
        }}
        
        .modal-main-content {{
            display: flex;
            flex-direction: column;
            gap: 2.2rem;
        }}
        
        .modal-section {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }}
        
        .section-title {{
            font-size: 0.8rem;
            text-transform: uppercase;
            color: var(--accent);
            font-weight: 700;
            letter-spacing: 0.12rem;
            border-left: 3px solid var(--accent);
            padding-left: 0.75rem;
            line-height: 1;
        }}
        
        .modal-synopsis {{
            font-size: 1.05rem;
            color: var(--text-muted);
            line-height: 1.7;
            font-weight: 300;
        }}
        
        .spec-value-large {{
            font-size: 1.1rem;
            color: var(--text-main);
            font-weight: 400;
        }}
        
        .modal-section-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }}
        
        .resources-section {{
            border-top: 1px solid rgba(255,255,255,0.06);
            padding-top: 1.5rem;
        }}
        
        .resources-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .resource-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s;
        }}
        
        .resource-btn.imdb {{
            background: rgba(245, 197, 24, 0.1);
            border: 1px solid #f5c518;
            color: #f5c518;
        }}
        
        .resource-btn.imdb:hover {{
            background: #f5c518;
            color: #000;
            box-shadow: 0 0 15px rgba(245, 197, 24, 0.3);
        }}
        
        .resource-btn.tmdb {{
            background: rgba(3, 180, 228, 0.1);
            border: 1px solid #03b4e4;
            color: #03b4e4;
        }}
        
        .resource-btn.tmdb:hover {{
            background: #03b4e4;
            color: #000;
            box-shadow: 0 0 15px rgba(3, 180, 228, 0.3);
        }}
        
        .resource-btn.share {{
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.1);
            color: #fff;
        }}
        
        .resource-btn.share:hover {{
            background: #fff;
            color: #000;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
        }}
        
        /* Details button style for cards */
        .details-btn {{
            width: 100%;
            background: var(--cream);
            border: 1px solid var(--cream);
            color: var(--bg-primary);
            font-weight: 800;
            cursor: pointer;
            padding: 0.7rem;
            border-radius: 12px;
            font-size: 0.95rem;
            font-family: inherit;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
        }}
        
        .details-btn:hover {{
            background: var(--accent);
            border-color: var(--accent);
            color: var(--cream);
            box-shadow: 0 4px 15px var(--accent-glow);
            transform: translateY(-2px);
        }}
        
        .details-btn svg {{
            width: 1.2rem;
            height: 1.2rem;
        }}

        /* Make cards cursor pointer and liftable */
        .movie-card {{
            cursor: pointer;
        }}
        
        /* Responsive design adjustments */
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2.2rem;
            }}
            .header-subtitle-edition {{
                font-size: 1.8rem;
            }}
            header {{
                padding: 3rem 1rem 1.5rem;
            }}
            .card-header-img {{
                height: 400px;
            }}
            .movies-grid {{
                grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
                gap: 1.5rem;
                padding: 0 1rem 4rem;
            }}
            .controls-wrapper {{
                padding: 0 1rem;
            }}
            .modal-overlay {{
                padding: 1rem;
            }}
            .modal-container {{
                border-radius: 16px;
            }}
            .modal-close-btn {{
                top: 1rem;
                right: 1rem;
                width: 2.5rem;
                height: 2.5rem;
            }}
            .modal-video-header {{
                background: var(--bg-primary); /* match body background */
            }}
            .video-wrapper {{
                padding-bottom: 56.25%; /* normal 16:9 on mobile */
                order: 1; /* place before title */
            }}
            .video-overlay-gradient {{
                display: none; /* remove gradient on mobile since text doesn't overlap */
            }}
            .modal-title {{
                font-size: 1.8rem;
            }}
            .modal-header-info {{
                position: relative; /* no longer absolute */
                bottom: auto;
                left: auto;
                right: auto;
                padding: 1.5rem; /* space around text */
                order: 2; /* place after video */
                z-index: 2;
                padding-bottom: 0; /* Connect tightly with body */
            }}
            .modal-body {{
                padding: 1.5rem;
                padding-top: 1rem;
            }}
            .modal-grid {{
                grid-template-columns: 1fr;
                gap: 2rem;
            }}
            .modal-poster-wrapper {{
                display: none; /* Hide poster on mobile to prioritize metadata */
            }}
            .modal-meta-pills {{
                flex-direction: row;
                flex-wrap: wrap;
                justify-content: center;
                gap: 0.5rem;
            }}
            .meta-pill-item {{
                flex: 1 1 calc(50% - 1rem);
                text-align: center;
                padding: 0.5rem;
            }}
            .modal-section-grid {{
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }}
            .resources-buttons {{
                flex-direction: column;
            }}
            .resource-btn {{
                width: 100%;
                justify-content: center;
            }}
        }}
        .site-footer {{
            text-align: center;
            padding: 3rem 1.5rem;
            margin-top: 2rem;
            border-top: 1px solid var(--border-color);
            color: var(--text-muted);
            font-size: 0.85rem;
            background: rgba(18, 45, 42, 0.4);
        }}
        
        .site-footer p {{
            margin-bottom: 0.5rem;
        }}
        
        .site-footer .footer-highlight {{
            color: var(--cream);
            font-weight: 500;
        }}
        
        /* Cinematic Roulette Overlay */
        .roulette-overlay {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(11, 15, 25, 0.95);
            z-index: 3000;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.4s ease;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            overflow: hidden;
        }}
        
        .roulette-overlay.active {{
            opacity: 1;
            pointer-events: auto;
        }}
        
        .roulette-content {{
            text-align: center;
            transform: scale(0.8);
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        
        .roulette-overlay.active .roulette-content {{
            transform: scale(1);
        }}
        
        .roulette-title {{
            font-size: 2rem;
            color: var(--accent);
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 4px;
            text-shadow: 0 0 10px rgba(210, 44, 54, 0.5);
            animation: pulse-title 1s infinite alternate;
        }}
        
        @keyframes pulse-title {{
            from {{ opacity: 0.7; }}
            to {{ opacity: 1; text-shadow: 0 0 20px rgba(210, 44, 54, 0.8); }}
        }}
        
        .roulette-frame {{
            position: relative;
            width: 250px;
            height: 350px;
            margin: 0 auto;
            border: 4px solid #fff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(255,255,255,0.2);
            background: #000;
        }}
        
        .roulette-frame img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: opacity 0.1s;
        }}
        
        .film-grain {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: url('data:image/svg+xml;utf8,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E');
            opacity: 0.3;
            pointer-events: none;
            mix-blend-mode: overlay;
        }}
        
        /* Floating Action Button - Surprise Me */
        .fab-surprise {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            z-index: 900;
            background: transparent;
            color: white;
            border: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}

        .fab-surprise:hover {{
            transform: translateY(-10px) scale(1.1);
        }}

        .fab-surprise img {{
            width: 80px;
            filter: drop-shadow(0 10px 15px rgba(0,0,0,0.6));
            transition: transform 0.3s ease;
        }}

        .fab-surprise:hover img {{
            animation: plant-breathe 3s ease-in-out infinite;
        }}

        .fab-surprise .fab-text {{
            background: var(--accent);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.95rem;
            font-weight: 800;
            font-family: 'Outfit', sans-serif;
            box-shadow: 0 5px 15px rgba(210, 44, 54, 0.5);
            text-align: center;
            line-height: 1.1;
        }}

        @media (max-width: 768px) {{
            .fab-surprise {{
                bottom: 1.5rem;
                right: 1.5rem;
            }}
            .fab-surprise img {{
                width: 65px;
            }}
            .fab-surprise .fab-text {{
                font-size: 0.8rem;
                padding: 6px 12px;
            }}
        }}
        /* Ticket Generator Overlay */
        .ticket-overlay {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(11, 15, 25, 0.95);
            z-index: 4000;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }}
        
        .ticket-overlay.active {{
            opacity: 1;
            pointer-events: auto;
        }}
        
        .ticket-modal {{
            background: var(--bg-primary);
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid var(--border-color);
            text-align: center;
            max-width: 90%;
            width: 450px;
            position: relative;
            transform: scale(0.9);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        
        .ticket-overlay.active .ticket-modal {{
            transform: scale(1);
        }}
        
        .close-ticket {{
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: #fff;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            font-size: 1.5rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
        }}
        
        .close-ticket:hover {{
            background: rgba(255, 255, 255, 0.2);
        }}

        #film-burn-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 999999;
            opacity: 0;
        }}

        #film-burn-overlay.burning {{
            animation: filmBurnAnim 1.4s ease-in-out forwards;
        }}

        @keyframes filmBurnAnim {{
            0% {{ opacity: 0; background: rgba(255, 100, 0, 0); }}
            15% {{ opacity: 1; background: rgba(255, 150, 0, 0.6); mix-blend-mode: color-dodge; box-shadow: inset 0 0 100px 50px rgba(255,0,0,0.5); }}
            30% {{ background: rgba(255, 255, 255, 1); mix-blend-mode: normal; }}
            60% {{ background: rgba(255, 50, 0, 0.9); mix-blend-mode: overlay; box-shadow: inset 0 0 200px 100px rgba(0,0,0,1); }}
            100% {{ opacity: 0; background: rgba(0, 0, 0, 0); }}
        }}
    </style>
</head>
<body>
    <div id="film-burn-overlay"></div>
    <div id="app-bg"></div>
    <header>
        <div class="header-content">
            <div class="header-eyebrow">
                <span class="header-logo">CCCC · Centre del Carme</span>
                <div class="header-divider"></div>
                <span class="header-tag">CCCCinema d&#39;Estiu 2026</span>
                <div class="lang-switcher">
                    <a href="index.html">CAS</a> <span style="color:var(--border-color)">|</span> <span class="active">VAL</span>
                    <button id="ambient-audio-btn" class="ambient-btn" aria-label="Sonido ambiente">🔇 ASMR</button>
                </div>
            </div>
            
            <h1>Embriagats<br>d'humor</h1>
            <h2 class="header-subtitle-edition">Amèrica i la comèdia</h2>
            
            <p class="subtitle">Un recorregut per la comèdia produïda a Amèrica. Mockumentaries, clàssics incunables, cinema polític i d'autor. Pel·lícules on la personalitat triomfa i el plaer campa al seu aire.</p>
            
            <div class="header-info-pills">
                <span class="info-pill">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                    31 juliol &ndash; 30 agost 2026
                </span>
                <span class="info-pill">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                    A les 22:00 h
                </span>
                <span class="info-pill">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                    C/ Museo, 2 &middot; Valencia
                </span>
                <span class="info-pill">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 12V22H4V12"></path><path d="M22 7H2v5h20V7z"></path><path d="M12 22V7"></path><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"></path><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"></path></svg>
                    Entrada gratuïta
                </span>
                <span class="info-pill">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                    V.O. subtitulada
                </span>
            </div>
        </div>
        
        <div class="header-poster">
            <img src="poster.png" alt="Cartell oficial CCCCinema d'Estiu 2026" title="Vore cartell en gran" style="cursor: pointer;" onclick="openPosterModal()">
            <a href="CCCC-CINEMA-ESTIU-2026-CAS.pdf" target="_blank" class="download-program-link" title="Descarregar programa en PDF">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                Descarregar programa
            </a>
        </div>
    </header>

    <div class="controls-wrapper">
        <div class="controls-card">
            <div class="search-row">
                <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <input type="text" id="search-input" class="search-input" placeholder="Buscar pel·lícula per títol, director, país, data..." oninput="filterMovies()">
                <button id="filter-saved-btn" class="filter-saved-btn" onclick="toggleSavedFilter()" title="Vore el Meu Diari">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>
                </button>
            </div>
            

            <div class="stats-row">
                <span id="results-count">Mostrant 27 de 27 pel·lícules</span>
                <button class="clear-filters-btn" id="clear-btn" onclick="clearFilters()" style="display: none;">Limpiar filtros</button>
            </div>
        </div>
    </div>

    <main class="movies-grid" id="movies-grid">
        {cards_html}
        
        <div class="empty-state" id="empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="8" y1="12" x2="16" y2="12"></line>
            </svg>
            <h3>No s'han trobat pel·lícules</h3>
            <p>Prova a buscar amb altres termes o neteja els filtres actius.</p>
        </div>
    </main>



    <!-- Poster Modal -->
    <div id="poster-modal" class="modal-overlay" onclick="closePosterModal()">
        <img src="poster.png" class="poster-modal-img" alt="Cartel en grande" onclick="event.stopPropagation(); closePosterModal()">
    </div>

    <!-- Movie Details Modal -->
    <div id="movie-modal" class="modal-overlay" onclick="closeModal()">
        <div class="modal-container" onclick="event.stopPropagation()">
            <button class="modal-close-btn" onclick="closeModal()" aria-label="Tancar detalls">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
            
            <!-- Fullscreen Video/Trailer Header -->
            <div class="modal-video-header" id="modal-video-header">
                <div class="video-wrapper">
                    <iframe id="modal-trailer-iframe" src="" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                <div class="video-overlay-gradient"></div>
                <div class="modal-header-info">
                    <span class="modal-date-badge" id="modal-date"></span>
                    <h2 class="modal-title" id="modal-title"></h2>
                    <p class="modal-subtitle" id="modal-subtitle"></p>
                </div>
            </div>
            
            <!-- Modal Body Content -->
            <div class="modal-body">
                <div class="modal-grid">
                    <!-- Left side: Poster & Metadata pills -->
                    <div class="modal-sidebar">
                        <div class="modal-poster-wrapper">
                            <img id="modal-poster" src="" alt="Poster de la película">
                        </div>
                        <div class="modal-meta-pills">
                            <div class="meta-pill-item">
                                <span class="pill-label">Any</span>
                                <span class="pill-value" id="modal-year"></span>
                            </div>
                            <div class="meta-pill-item">
                                <span class="pill-label">País</span>
                                <span class="pill-value" id="modal-country"></span>
                            </div>
                            <div class="meta-pill-item">
                                <span class="pill-label">Durada</span>
                                <span class="pill-value" id="modal-duration"></span>
                            </div>
                            <a id="modal-link-tmdb" href="#" target="_blank" class="meta-pill-item" style="text-decoration:none; cursor:pointer;">
                                <span class="pill-label">Fitxa</span>
                                <span class="pill-value" style="color:var(--primary-color);">TMDb ↗</span>
                            </a>
                        </div>
                    </div>
                    
                    <!-- Right side: Synopsis, Genres, Tech Spec -->
                    <div class="modal-main-content">
                        <div class="modal-section">
                            <h4 class="section-title">Sinopsi</h4>
                            <p class="modal-synopsis" id="modal-synopsis"></p>
                        </div>
                        
                        <div class="modal-section">
                            <h4 class="section-title">Gèneres</h4>
                            <div class="genres-container" id="modal-genres"></div>
                        </div>
                        
                        <div class="modal-section-grid">
                            <div class="modal-section">
                                <h4 class="section-title">Director(s)</h4>
                                <p class="spec-value-large" id="modal-directors"></p>
                            </div>
                            <div class="modal-section">
                                <h4 class="section-title">Repartiment Principal</h4>
                                <p class="spec-value-large" id="modal-cast"></p>
                            </div>
                        </div>
                        
                        <div class="modal-section resources-section" id="modal-ticket-preview-container">
                            <!-- Aquí se inyectará la imagen generada de la entrada dinámicamente -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Toast message -->
    <div class="toast" id="copy-toast">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        <span id="toast-message">Copiado al portapapeles</span>
    </div>

    <!-- Footer -->
    <footer class="site-footer">
        <p class="footer-highlight">© 2026 CCCC · Centre del Carme. Tots els drets reservats.</p>
        <p>Fitxes tècniques i sinopsis oficials extretes del programa del Centre del Carme (CCCC).</p>
        <p>CCCCinema d'Estiu 2026</p>
        <p style="margin-top: 1.5rem; font-size: 0.8rem; opacity: 0.8;">Creat i dissenyat per v0l0v</p>
    </footer>

    <script>
        const moviesData = {json.dumps(movies, ensure_ascii=False)};
        let activeDayFilter = null;
        let activeGenreFilter = null;
        let savedMovies = JSON.parse(localStorage.getItem('cineccc_saved') || '[]');
        let showingOnlySaved = false;
        
        document.addEventListener('DOMContentLoaded', () => {{
            savedMovies.forEach(idx => {{
                const btn = document.querySelector(`.bookmark-btn[data-idx="${{idx}}"]`);
                if (btn) btn.classList.add('saved');
            }});
        }});

        function toggleBookmark(idx) {{
            const btn = document.querySelector(`.bookmark-btn[data-idx="${{idx}}"]`);
            const index = savedMovies.indexOf(idx);
            if (index === -1) {{
                savedMovies.push(idx);
                if (btn) btn.classList.add('saved');
                showToast("Pel·lícula guardada al Meu Diari");
            }} else {{
                savedMovies.splice(index, 1);
                if (btn) btn.classList.remove('saved');
                showToast("Pel·lícula eliminada del Meu Diari");
            }}
            localStorage.setItem('cineccc_saved', JSON.stringify(savedMovies));
            if (showingOnlySaved) filterMovies();
        }}
        
        function toggleSavedFilter() {{
            showingOnlySaved = !showingOnlySaved;
            const btn = document.getElementById('filter-saved-btn');
            if (showingOnlySaved) {{
                btn.classList.add('active');
                showToast("Mostrant només el Meu Diari");
            }} else {{
                btn.classList.remove('active');
                showToast("Mostrant tot el programa");
            }}
            filterMovies();
        }}

        function toggleSynopsis(cardId) {{
            const synopsis = document.getElementById(`syn-${{cardId}}`);
            const btn = document.getElementById(`btn-${{cardId}}`);
            
            if (synopsis.classList.contains('expanded')) {{
                synopsis.classList.remove('expanded');
                btn.textContent = 'Leer más';
            }} else {{
                synopsis.classList.add('expanded');
                btn.textContent = 'Leer menos';
            }}
        }}
        // YouTube thumbnail fallback:
        // maxresdefault.jpg may not exist -> YouTube returns a 120x90 grey placeholder.
        // We detect this by checking naturalWidth and fall back through sddefault -> hqdefault -> poster.
        document.querySelectorAll('.thumb-overlay[data-yt-id]').forEach(el => {{
            const ytId = el.getAttribute('data-yt-id');
            if (!ytId) return;
            
            const fallbacks = [
                `https://img.youtube.com/vi/${{ytId}}/maxresdefault.jpg`,
                `https://img.youtube.com/vi/${{ytId}}/sddefault.jpg`,
                `https://img.youtube.com/vi/${{ytId}}/hqdefault.jpg`,
            ];
            
            function tryNext(index) {{
                if (index >= fallbacks.length) return; // keep poster as bg
                const img = new Image();
                img.onload = function() {{
                    if (this.naturalWidth <= 120) {{
                        // YouTube 404 placeholder is 120x90
                        tryNext(index + 1);
                    }} else {{
                        el.style.backgroundImage = `url('${{fallbacks[index]}}')`;
                    }}
                }};
                img.onerror = () => tryNext(index + 1);
                img.src = fallbacks[index];
            }}
            tryNext(0);
        }});


        function toggleDayFilter(day, element) {{
            const chips = document.querySelectorAll('.filters-row .filter-chip');
            
            if (activeDayFilter === day) {{
                activeDayFilter = null;
                element.classList.remove('active');
            }} else {{
                activeDayFilter = day;
                chips.forEach(c => c.classList.remove('active'));
                element.classList.add('active');
            }}
            
            filterMovies();
        }}

        function filterByGenre(genre) {{
            // Custom filtering by genre badge click
            activeGenreFilter = genre;
            // Let's set the search input or handle genre filter directly
            document.getElementById('search-input').value = genre;
            filterMovies();
            showToast(`Filtrado por género: ${{genre}}`);
        }}

        function filterMovies() {{
            const query = document.getElementById('search-input').value.toLowerCase().trim();
            const cards = document.querySelectorAll('.movie-card');
            let visibleCount = 0;
            
            cards.forEach(card => {{
                const title = card.getAttribute('data-title');
                const director = card.getAttribute('data-director');
                const genres = card.getAttribute('data-genres');
                const country = card.getAttribute('data-country');
                const date = card.getAttribute('data-date');
                const cast = card.getAttribute('data-cast') || '';
                
                let matchesSearch = !query || 
                    title.includes(query) || 
                    director.includes(query) || 
                    genres.includes(query) || 
                    country.includes(query) ||
                    date.includes(query) ||
                    cast.includes(query);
                    
                let matchesSaved = true;
                if (showingOnlySaved) {{
                    const btn = card.querySelector('.bookmark-btn');
                    matchesSaved = btn && btn.classList.contains('saved');
                }}
                    
                let matchesDay = true;
                if (activeDayFilter) {{
                    // check if the date attribute starts with the activeDayFilter
                    matchesDay = date.startsWith(activeDayFilter);
                }}
                
                if (matchesSearch && matchesDay && matchesSaved) {{
                    card.style.display = 'flex';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            // Show/hide empty state
            const emptyState = document.getElementById('empty-state');
            if (visibleCount === 0) {{
                emptyState.style.display = 'block';
            }} else {{
                emptyState.style.display = 'none';
            }}
            
            // Update results text
            const resultsText = document.getElementById('results-count');
            resultsText.textContent = `Mostrando ${{visibleCount}} de ${{cards.length}} películas`;
            
            // Show clear button if filters or search are active
            const clearBtn = document.getElementById('clear-btn');
            if (query || activeDayFilter) {{
                clearBtn.style.display = 'inline-block';
            }} else {{
                clearBtn.style.display = 'none';
            }}
        }}

        function clearFilters() {{
            document.getElementById('search-input').value = '';
            activeDayFilter = null;
            activeGenreFilter = null;
            
            const chips = document.querySelectorAll('.filters-row .filter-chip');
            chips.forEach(c => c.classList.remove('active'));
            
            filterMovies();
        }}

        function copyFullProgramInvite() {{
            const inviteText = `🎬 *CICLO DE CINE CCC - AGOSTO 2026* 🎬\n\nTe invito a ver la cartelera de películas programada para este mes. Aquí tienes los detalles del ciclo completo:\n\n🔗 Web Oficial: ${{window.location.origin + window.location.pathname}}\n\n📅 ¡Elige tus días favoritos y acompáñanos!`;
            
            navigator.clipboard.writeText(inviteText).then(() => {{
                showToast("Invitación copiada al portapapeles 📋");
            }}).catch(err => {{
                console.error('Error copying text: ', err);
            }});
        }}

        function showToast(message) {{
            const toast = document.getElementById('copy-toast');
            const msgEl = document.getElementById('toast-message');
            msgEl.textContent = message;
            toast.classList.add('show');
            
            setTimeout(() => {{
                toast.classList.remove('show');
            }}, 3000);
        }}

        let currentMovieIndex = null;

        function openModal(idx) {{
            const filmBurn = document.getElementById('film-burn-overlay');
            filmBurn.classList.remove('burning');
            void filmBurn.offsetWidth; // Force reflow para reiniciar animacion
            filmBurn.classList.add('burning');
            
            setTimeout(() => {{
                const movie = moviesData[idx];
                currentMovieIndex = idx;
                
                document.getElementById('modal-title').innerText = movie.title;
            document.getElementById('modal-subtitle').innerText = `${{movie.year}} · ${{movie.country}} · ${{movie.duration}}`;
            document.getElementById('modal-date').innerText = movie.date;
            document.getElementById('modal-poster').src = movie.poster_url || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80';
            document.getElementById('modal-poster').alt = `Pòster de ${{movie.title}}`;
            document.getElementById('modal-country').innerText = movie.country;
            document.getElementById('modal-duration').innerText = movie.duration;
            document.getElementById('modal-synopsis').innerText = movie.synopsis;
            
            // Genres
            const genresContainer = document.getElementById('modal-genres');
            genresContainer.innerHTML = movie.genres.map(g => `<span class="genre-badge" onclick="closeModalAndFilterGenre('${{g}}')">${{g}}</span>`).join('');
            
            // Directors & Cast
            document.getElementById('modal-directors').innerText = movie.directors.join(', ') || 'No disponible';
            document.getElementById('modal-cast').innerText = movie.cast.join(', ') || 'No disponible';
            
            // Meta pills values & Links
            document.getElementById('modal-year').innerText = movie.year;
            
            const tmdbEl = document.getElementById('modal-link-tmdb');
            if (!movie.tmdb_url) {{
                tmdbEl.style.display = 'none';
            }} else {{
                tmdbEl.href = movie.tmdb_url;
                tmdbEl.style.display = 'flex';
            }}
            
            // Set YouTube Trailer Iframe source
            const iframe = document.getElementById('modal-trailer-iframe');
            iframe.classList.remove('fade-in');
            
            // Generate ticket preview dynamically
            const ticketPreviewContainer = document.getElementById('modal-ticket-preview-container');
            ticketPreviewContainer.innerHTML = '<p style="text-align: center; font-size: 0.9rem; opacity: 0.7;">Generando tu entrada...</p>';
            
            generateTicketCanvas(idx).then(canvas => {{
                if(canvas) {{
                    const dataUrl = canvas.toDataURL('image/png');
                    ticketPreviewContainer.innerHTML = `
                        <h4 class="section-title" style="text-align:left;">Comparteix la teua assistència</h4>
                        <p style="text-align:left; font-size:0.9rem; margin-top:-10px; margin-bottom:15px; opacity:0.8;">Fes clic a la teua entrada (souvenir virtual) per avisar els teus amics de l'esdeveniment.</p>
                        <img src="${{dataUrl}}" alt="Entrada Generada" style="width:100%; max-width:500px; display:block; margin: 0; border-radius:10px; cursor:pointer; box-shadow: 0 5px 25px rgba(0,0,0,0.5); transition: transform 0.2s ease; transform-origin: left center;" 
                        onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'"
                        onclick="generateAndShareTicket(${{idx}})" title="Fes clic per compartir">
                    `;
                }}
            }});
            
            if (movie.youtube_id) {{
                // Añadimos parámetros para ocultar la interfaz lo máximo posible: rel=0 (solo sugerencias del mismo canal), modestbranding=1 (sin logo de YT), iv_load_policy=3 (sin anotaciones)
                iframe.src = `https://www.youtube.com/embed/${{movie.youtube_id}}?autoplay=1&mute=0&controls=0&loop=1&playlist=${{movie.youtube_id}}&rel=0&modestbranding=1&iv_load_policy=3&disablekb=1&fs=0`;
                setTimeout(() => {{
                    iframe.classList.add('fade-in');
                }}, 600);
            }} else {{
                iframe.src = '';
            }}
            
            // Open Modal
            const modal = document.getElementById('movie-modal');
            
            // Bajar volumen ASMR si está sonando
            if (window.ambientAudio && window.isAmbientPlaying) {{
                window.ambientAudio.volume = 0.05;
            }}
            
            modal.style.display = 'block';
            // Force reflow for transitions
            modal.offsetHeight;
            modal.classList.add('open');
            document.body.style.overflow = 'hidden'; // prevent scrolling behind
            
            // Update URL hash without jumping page
            history.pushState(null, null, `#movie-${{idx}}`);
            }}, 500); // 500ms delay para sincronizar con el fogonazo de película
        }}

        function openPosterModal() {{
            document.getElementById('poster-modal').classList.add('open');
            document.body.style.overflow = 'hidden';
        }}
        
        function closePosterModal() {{
            document.getElementById('poster-modal').classList.remove('open');
            document.body.style.overflow = '';
        }}

        async function generateTicketCanvas(idx) {{
            const m = moviesData[idx];
            if (!m) return null;
            
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            const scale = 2; // Duplicar tamaño y resolución
            const tWidth = 1000;
            const tHeight = 430;
            
            canvas.width = tWidth * scale;
            canvas.height = tHeight * scale;
            ctx.scale(scale, scale);
            
            const darkColor = '#463b36';
            const lightColor = '#eedfcc';
            
            // 1. Fondo claro (base)
            ctx.fillStyle = lightColor;
            ctx.fillRect(0, 0, tWidth, tHeight);
            
            // 2. Forma oscura de la izquierda (incluyendo los bordes que apuntan hacia el centro)
            ctx.fillStyle = darkColor;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(480, 0);
            ctx.lineTo(240, tHeight / 2);
            ctx.lineTo(480, tHeight);
            ctx.lineTo(0, tHeight);
            ctx.fill();
            
            // 4. Logo del festival (izquierda)
            const logoSrc = "soloplanta.png";
            
            try {{
                const img = await loadImage(logoSrc);
                
                ctx.save();
                
                // Calcular tamaño para que encaje bien en el espacio izquierdo
                const pHeight = 320; // Buen tamaño para que destaque
                const pWidth = pHeight * (img.width / img.height); // Mantener ratio
                const pX = 15; // Margen izquierdo más pequeño para pegar la planta a la izquierda
                const pY = tHeight / 2 - pHeight / 2; // Centrado verticalmente
                
                // Sombra suave para que resalte sobre el fondo oscuro
                ctx.shadowColor = 'rgba(0, 0, 0, 0.4)';
                ctx.shadowBlur = 10;
                ctx.shadowOffsetX = 2;
                ctx.shadowOffsetY = 4;
                
                // Dibujamos el logo tal cual, sin filtros que alteren sus colores
                ctx.drawImage(img, pX, pY, pWidth, pHeight);
                
                ctx.restore();
            }} catch (err) {{
                console.log("No se pudo cargar el logo del festival para la entrada");
            }}

            // 3. Perforaciones de película (arriba y abajo) AHORA CON TRANSPARENCIA REAL
            ctx.save();
            ctx.globalCompositeOperation = 'destination-out';
            ctx.fillStyle = '#000000'; // Transparencia real
            for(let x = 12; x < tWidth; x += 32) {{
                ctx.fillRect(x, 12, 16, 22);
                ctx.fillRect(x, tHeight - 34, 16, 22);
            }}
            ctx.restore();
            
            ctx.fillStyle = lightColor;
            ctx.font = '22px "Trebuchet MS", Arial, sans-serif';
            ctx.textAlign = 'left';
            const ticketNum = Math.floor(Math.random() * 9000000 + 1000000);
            ctx.fillText("№ " + ticketNum, 55, tHeight - 55);
            
            // 5. Línea de corte (más a la derecha)
            ctx.strokeStyle = darkColor;
            ctx.lineWidth = 2;
            ctx.setLineDash([8, 8]);
            ctx.beginPath();
            ctx.moveTo(880, 0);
            ctx.lineTo(880, tHeight);
            ctx.stroke();
            ctx.setLineDash([]);
            
            // 6. Textos centrales (alineados a la derecha)
            const textRightX = 850; // Margen derecho, pegado a la línea de corte (880)
            
            ctx.fillStyle = darkColor;
            ctx.textAlign = 'right'; // Alineado a la derecha
            ctx.textBaseline = 'middle';
            
            ctx.font = 'bold 32px "Trebuchet MS", Arial, sans-serif';
            ctx.fillText("CCCCINEMA D'ESTIU 2026", textRightX, 105);
            
            ctx.font = 'bold 16px "Trebuchet MS", Arial, sans-serif';
            ctx.fillText("EMBRIAGADOS DE HUMOR AMÉRICA Y LA COMEDIA", textRightX, 135);
            
            let fontSize = 85;
            const title = m.title.toUpperCase();
            if (title.length > 25) fontSize = 50;
            else if (title.length > 15) fontSize = 65;
            
            ctx.font = `bold ${{fontSize}}px "Impact", "Arial Black", sans-serif`;
            ctx.fillText(title, textRightX, 215, 550); // max-width
            
            ctx.font = 'bold 32px "Trebuchet MS", Arial, sans-serif';
            ctx.fillText("CCCC · CENTRE DEL CARME", textRightX, 305);
            
            // Fecha y hora
            ctx.font = 'bold 22px "Trebuchet MS", Arial, sans-serif';
            ctx.fillText(m.date.toUpperCase() + " · 22:00 H", textRightX, 345);
            
            // 7. Stub derecho (texto sin código de barras para que destaque la mordida)
            ctx.save();
            ctx.translate(900, tHeight / 2); // Movido más hacia la izquierda, pegado a la línea de corte
            ctx.rotate(-Math.PI / 2);
            ctx.fillStyle = darkColor;
            ctx.font = 'bold 26px "Impact", "Arial Black", sans-serif'; // fuente más pequeña para que quepa bien el texto largo
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText("RECUERDO PROMOCIONAL", 0, 0);
            
            // Subtítulo aclaratorio (más a la derecha visualmente, que equivale a Y positiva tras la rotación)
            ctx.font = '12px "Arial", sans-serif'; // fuente más pequeña y normal
            ctx.fillText("ENTRADA SIN VALIDEZ", 0, 30);
            ctx.restore();
            
            // 8. ¡EL MORDISCO DE LA PLANTA CARNÍVORA! (Borde derecho masticado)
            const numTeeth = 6;
            const toothHeight = tHeight / numTeeth;
            const teethPoints = [];
            
            for (let i = 0; i < numTeeth; i++) {{
                const depth = Math.random() * 60 + 30; // Entra hacia el ticket
                const tipY = (i * toothHeight) + (toothHeight / 2) + (Math.random() * 30 - 15);
                teethPoints.push({{x: tWidth - depth, y: tipY}});
                teethPoints.push({{x: tWidth, y: (i + 1) * toothHeight}});
            }}
            
            ctx.save();
            ctx.globalCompositeOperation = 'destination-out';
            ctx.beginPath();
            ctx.moveTo(tWidth, 0);
            for (const pt of teethPoints) {{
                ctx.lineTo(pt.x, pt.y);
            }}
            ctx.lineTo(tWidth + 100, tHeight);
            ctx.lineTo(tWidth + 100, 0);
            ctx.fill();
            ctx.restore();
            
            // Dibujar el borde de las "marcas de dientes"
            ctx.save();
            ctx.strokeStyle = darkColor;
            ctx.lineWidth = 6;
            ctx.lineJoin = 'miter';
            ctx.beginPath();
            ctx.moveTo(tWidth, 0);
            for (const pt of teethPoints) {{
                ctx.lineTo(pt.x, pt.y);
            }}
            ctx.stroke();
            ctx.restore();
            return canvas;
        }}

        async function generateAndShareTicket(idx) {{
            const m = moviesData[idx];
            if (!m) return;
            
            showToast("🎟️ Generando tu entrada...");
            const canvas = await generateTicketCanvas(idx);
            if (!canvas) return;
            
            canvas.toBlob(async (blob) => {{
                if (!blob) return;
                
                const file = new File([blob], `entrada-${{m.title.replace(/\\s+/g, '-').toLowerCase()}}.png`, {{ type: 'image/png' }});
                
                if (navigator.canShare && navigator.canShare({{ files: [file] }})) {{
                    try {{
                        await navigator.share({{
                            files: [file],
                            title: `Entrada para ${{m.title}}`,
                            text: `¡Tengo mi entrada para ver ${{m.title}} en el CCCC Cinema d'Estiu!`
                        }});
                    }} catch (err) {{
                        console.log("Error al compartir nativo:", err);
                        showTicketModal(canvas.toDataURL());
                    }}
                }} else {{
                    showTicketModal(canvas.toDataURL());
                }}
            }}, 'image/png');
        }}
        
        function loadImage(src) {{
            return new Promise((resolve, reject) => {{
                const img = new Image();
                if (src.startsWith('http')) {{
                    img.crossOrigin = 'Anonymous';
                }}
                img.onload = () => resolve(img);
                img.onerror = reject;
                img.src = src;
            }});
        }}
        
        function showTicketModal(dataUrl) {{
            let overlay = document.getElementById('ticket-overlay');
            if (!overlay) {{
                overlay = document.createElement('div');
                overlay.id = 'ticket-overlay';
                overlay.className = 'ticket-overlay';
                overlay.innerHTML = `
                    <div class="ticket-modal">
                        <button class="close-ticket" onclick="document.getElementById('ticket-overlay').classList.remove('active')">&times;</button>
                        <h3 style="color:#fff; margin-bottom: 1rem;">La teua entrada està llesta!</h3>
                        <p style="color:var(--text-muted); margin-bottom: 1rem; font-size: 0.9rem;">Mantingues premuda la imatge per a enviar-la, o utilitza el botó de descarregar.</p>
                        <img id="ticket-result" src="" alt="Ticket generado" style="max-width:100%; max-height:60vh; border-radius:8px; box-shadow:0 10px 25px rgba(0,0,0,0.5);">
                        <br><br>
                        <a id="ticket-download-btn" href="" download="entrada-cccc.png" class="details-btn" style="display:inline-flex; width:auto; padding: 0.8rem 2rem; margin-top:1rem;">
                            ⬇️ Descarregar Entrada
                        </a>
                    </div>
                `;
                document.body.appendChild(overlay);
            }}
            
            document.getElementById('ticket-result').src = dataUrl;
            document.getElementById('ticket-download-btn').href = dataUrl;
            
            setTimeout(() => {{
                overlay.classList.add('active');
            }}, 10);
        }}

        function closeModal() {{
            const modal = document.getElementById('movie-modal');
            modal.classList.remove('open');
            document.body.style.overflow = '';
            
            // Recuperar volumen ASMR si estaba sonando
            if (window.ambientAudio && window.isAmbientPlaying) {{
                window.ambientAudio.volume = 0.4;
            }}
            
            // Reset iframe to stop playback
            const iframe = document.getElementById('modal-trailer-iframe');
            iframe.classList.remove('fade-in');
            iframe.src = '';
            
            // Clear URL hash
            history.pushState(null, null, ' ');
            
            setTimeout(() => {{
                modal.style.display = 'none';
            }}, 400);
        }}

        function closeModalAndFilterGenre(genre) {{
            closeModal();
            setTimeout(() => {{
                filterByGenre(genre);
            }}, 450);
        }}

        function shareCurrentMovieModal() {{
            if (currentMovieIndex === null) return;
            const movie = moviesData[currentMovieIndex];
            const shareUrl = `${{window.location.origin + window.location.pathname}}#movie-${{currentMovieIndex}}`;
            const shareText = `🎥 *${{movie.title}}* (${{movie.year}})\n📅 ${{movie.date}}\n🎬 Dirigida por: ${{movie.directors.join(', ')}}\n⏱️ Duración: ${{movie.duration}}\n\n🔗 Ver ficha técnica y trailer completo en:\n${{shareUrl}}`;
            
            navigator.clipboard.writeText(shareText).then(() => {{
                showToast("¡Enlace e invitación a la película copiados! 📋");
            }}).catch(err => {{
                console.error("Error al copiar enlace", err);
            }});
        }}

        // Listen for browser navigation (back button) or initial hash
        window.addEventListener('popstate', () => {{
            const hash = window.location.hash;
            if (hash && hash.startsWith('#movie-')) {{
                const idx = parseInt(hash.replace('#movie-', ''), 10);
                if (!isNaN(idx) && idx >= 0 && idx < moviesData.length) {{
                    openModal(idx);
                }}
            }} else {{
                const modal = document.getElementById('movie-modal');
                if (modal.classList.contains('open')) {{
                    closeModal();
                }}
            }}
        }});

        window.addEventListener('DOMContentLoaded', () => {{
            const hash = window.location.hash;
            if (hash && hash.startsWith('#movie-')) {{
                const idx = parseInt(hash.replace('#movie-', ''), 10);
                if (!isNaN(idx) && idx >= 0 && idx < moviesData.length) {{
                    setTimeout(() => {{
                        openModal(idx);
                    }}, 400);
                }}
            }}
        }});
        function surpriseMe() {{
            if (!moviesData || moviesData.length === 0) return;
            
            const overlay = document.getElementById('roulette-overlay');
            const posterEl = document.getElementById('roulette-poster');
            overlay.classList.add('active');
            
            let counter = 0;
            // Aumentamos los "ticks" para que dure el doble
            const maxTicks = 35; 
            let interval = 40; // Comienza MUY rápido
            
            function tick() {{
                const tempIdx = Math.floor(Math.random() * moviesData.length);
                const tempPoster = moviesData[tempIdx].poster_url || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80';
                posterEl.src = tempPoster;
                document.getElementById('roulette-bg').style.backgroundImage = `url('${{tempPoster}}')`;
                
                counter++;
                
                if (counter < maxTicks) {{
                    // Ralentizar progresivamente pero más fuerte al final
                    if (counter > maxTicks * 0.8) {{
                        interval += 80; // Frena bruscamente en los últimos ticks
                    }} else if (counter > maxTicks * 0.5) {{
                        interval += 20; // Empieza a frenar
                    }}
                    setTimeout(tick, interval);
                }} else {{
                    const finalIdx = Math.floor(Math.random() * moviesData.length);
                    const finalPoster = moviesData[finalIdx].poster_url || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80';
                    posterEl.src = finalPoster;
                    document.getElementById('roulette-bg').style.backgroundImage = `url('${{finalPoster}}')`;
                    
                    posterEl.style.opacity = '0';
                    setTimeout(() => {{ posterEl.style.opacity = '1'; }}, 50);
                    
                    setTimeout(() => {{
                        overlay.classList.remove('active');
                        setTimeout(() => {{
                            openModal(finalIdx);
                        }}, 400);
                    }}, 1200);
                }}
            }}
            
            tick();
        }}
        // Lógica de Sonido Ambiente ASMR
        const ambientBtn = document.getElementById('ambient-audio-btn');
        window.ambientAudio = null;
        window.isAmbientPlaying = false;
        
        ambientBtn.addEventListener('click', () => {{
            if (!window.ambientAudio) {{
                // Audio local (asegúrate de subir 'asmrcccc.mp3' a la carpeta assets/audio/)
                window.ambientAudio = new Audio('assets/audio/asmrcccc.mp3');
                window.ambientAudio.loop = true;
                window.ambientAudio.volume = 0.4;
            }}
            
            if (window.isAmbientPlaying) {{
                window.ambientAudio.pause();
                ambientBtn.innerHTML = '🔇 ASMR';
                ambientBtn.style.color = 'var(--text-color)';
                ambientBtn.style.borderColor = 'var(--border-color)';
                window.isAmbientPlaying = false;
            }} else {{
                window.ambientAudio.play().catch(e => console.error("Error al reproducir:", e));
                ambientBtn.innerHTML = '🔊 ASMR';
                ambientBtn.style.color = 'var(--primary-color)';
                ambientBtn.style.borderColor = 'var(--primary-color)';
                window.isAmbientPlaying = true;
            }}
        // Easter Egg: Planta Bailarina
        let easterEggSequence = "planta";
        let currentSequenceIndex = 0;
        document.addEventListener('keydown', (e) => {{
            if (e.key.toLowerCase() === easterEggSequence[currentSequenceIndex]) {{
                currentSequenceIndex++;
                if (currentSequenceIndex === easterEggSequence.length) {{
                    triggerEasterEgg();
                    currentSequenceIndex = 0;
                }}
            }} else {{
                currentSequenceIndex = 0;
            }}
        }});
        
        function triggerEasterEgg() {{
            const container = document.getElementById('easter-egg-container');
            const video = document.getElementById('easter-egg-video');
            container.style.display = 'flex';
            video.volume = 0.8;
            video.play().catch(err => console.log(err));
        }}
        
        function closeEasterEgg() {{
            const container = document.getElementById('easter-egg-container');
            const video = document.getElementById('easter-egg-video');
            container.style.display = 'none';
            video.pause();
            video.currentTime = 0;
        }}
        }});
    </script>
    <!-- Cinematic Roulette Overlay -->
    <div id="roulette-overlay" class="roulette-overlay">
        <div id="roulette-bg" style="position: absolute; top: -10%; left: -10%; width: 120%; height: 120%; background-size: cover; background-position: center; filter: blur(30px) brightness(0.35); z-index: -2; transition: background-image 0.1s ease-out;"></div>
        <style>
            @keyframes plant-breathe {{
                0% {{ transform: scale(1) translateY(0) rotate(0deg); }}
                50% {{ transform: scale(1.05) translateY(-5px) rotate(2deg); }}
                100% {{ transform: scale(1) translateY(0) rotate(0deg); }}
            }}
        </style>
        <div class="roulette-content">
            <div style="position: relative; display: inline-block;">
                <div style="position: absolute; left: -360px; top: 30%; z-index: 0; pointer-events: none; transform: translateY(-50%);">
                    <img src="soloplanta.png" alt="Planta carnívora" style="width: 550px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9)); animation: plant-breathe 2.5s ease-in-out infinite;">
                </div>
                <div class="roulette-frame" style="position: relative; z-index: 10; box-shadow: 0 10px 50px rgba(0,0,0,0.9); border-color: var(--accent);">
                    <img id="roulette-poster" src="" alt="Triant...">
                    <div class="film-grain"></div>
                </div>
            </div>
        </div>
    </div>
    <!-- Surprise Me FAB -->
    <button class="fab-surprise" onclick="surpriseMe()" aria-label="Tria pel·lícula a l'atzar">
        <img src="soloplanta.png" alt="Planta carnívora hambrienta">
        <div class="fab-text">MENGEM-NOS<br>UNA PEL·LI!</div>
    </button>
    <!-- Easter Egg Video -->
    <div id="easter-egg-container" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 9999999; background: rgba(0,0,0,0.95); justify-content: center; align-items: center; cursor: pointer; flex-direction: column;" onclick="closeEasterEgg()">
        <video id="easter-egg-video" src="assets/video/planta.mp4" style="max-width: 90vw; max-height: 80vh; border-radius: 50%; box-shadow: 0 0 100px 50px rgba(0,0,0,1) inset, 0 0 50px rgba(50,255,50,0.2); -webkit-mask-image: radial-gradient(circle, black 40%, transparent 70%); mask-image: radial-gradient(circle, black 40%, transparent 70%); filter: contrast(1.3) saturate(1.5);" loop></video>
        <p style="color: #fff; opacity: 0.5; font-family: 'Courier New', Courier, monospace; margin-top: 20px; letter-spacing: 2px;">[ HAZ CLIC PARA VOLVER ]</p>
    </div>
</body>
</html>
"""

    with open('index_va.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("index_va.html generated successfully!")

if __name__ == '__main__':
    main()
