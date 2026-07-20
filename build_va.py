import os

replacements = {
    "movies_data.json": "movies_data_va.json",
    "index.html generated successfully!": "index_va.html generated successfully!",
    "with open('index.html',": "with open('index_va.html',",
    "lang=\"es\"": "lang=\"ca\"",
    "Embriagados<br>de humor": "Embriagats<br>d'humor",
    "América y la comedia": "Amèrica i la comèdia",
    "Un recorrido por la comedia producida en América. Mockumentaries, clásicos incúnables, cine político y de autor. Películas donde la personalidad triunfa y el placer campa a sus anchas.": "Un recorregut per la comèdia produïda a Amèrica. Mockumentaries, clàssics incunables, cinema polític i d'autor. Pel·lícules on la personalitat triomfa i el plaer campa al seu aire.",
    "31 julio &ndash; 30 agosto 2026": "31 juliol &ndash; 30 agost 2026",
    "A las 22:00 h": "A les 22:00 h",
    "Entrada gratuita": "Entrada gratuïta",
    "Descargar programa": "Descarregar programa",
    "Buscar película por título, director, país, fecha...": "Buscar pel·lícula per títol, director, país, data...",
    "Películas Encontradas": "Pel·lícules Trobades",
    "Director:": "Director:",
    "Elenco principal:": "Repartiment principal:",
    "Ver Detalles": "Veure Detalls",
    "Generar Entrada:": "Generar Entrada:",
    "Compartir Entrada por WhatsApp": "Compartir Entrada per WhatsApp",
    "Compartir por WhatsApp": "Compartir per WhatsApp",
    "Compartir Entrada por Telegram": "Compartir Entrada per Telegram",
    "Compartir por Telegram": "Compartir per Telegram",
    "No se encontraron películas": "No s'han trobat pel·lícules",
    "Prueba a buscar con otros términos o limpia los filtros activos.": "Prova a buscar amb altres termes o neteja els filtres actius.",
    "Fichas técnicas y sinopsis oficiales extraídas del programa del Centre del Carme (CCCC).": "Fitxes tècniques i sinopsis oficials extretes del programa del Centre del Carme (CCCC).",
    "Creado y diseñado por v0l0v": "Creat i dissenyat per v0l0v",
    "¡COMÁMONOS<br>UNA PELI!": "MENGEM-NOS<br>UNA PEL·LI!",
    "Eligiendo...": "Triant...",
    "Elegir película al azar": "Tria pel·lícula a l'atzar",
    "Ver cartel en grande": "Veure cartell en gran",
    "Descargar programa en PDF": "Descarregar programa en PDF",
    "Guardar en Mi Diario": "Guardar al Meu Diari",
    "Todos los derechos reservados.": "Tots els drets reservats.",
    "Cerrar detalles": "Tancar detalls",
    "Compartir": "Compartir",
    "Generar": "Generar",
    "Descargar la entrada para compartir en redes sociales": "Descarregar l'entrada per compartir en xarxes socials",
    "Descargar Imagen": "Descarregar Imatge",
    "AÑO": "ANY",
    "PAÍS": "PAÍS",
    "DURACIÓN": "DURADA",
    "Cartel oficial CCCCinema d'Estiu 2026": "Cartell oficial CCCCinema d'Estiu 2026",
    "Póster de ": "Pòster de ",
    "Sinopsis": "Sinopsi",
    "Géneros": "Gèneres",
    "Director(es)": "Director(s)",
    "Reparto Principal": "Repartiment Principal",
    "Comparte tu asistencia": "Comparteix la teua assistència",
    "Haz clic en tu entrada (souvenir virtual) para avisar a tus amigos del evento.": "Fes clic a la teua entrada (souvenir virtual) per avisar els teus amics de l'esdeveniment.",
    "Haz clic para compartir": "Fes clic per compartir",
    "Año<": "Any<",
    "País<": "País<",
    "Duración<": "Durada<",
    "Ficha<": "Fitxa<",
    "Mostrando 27 de 27 películas": "Mostrant 27 de 27 pel·lícules",
    "Mostrando solo Mi Diario": "Mostrant només el Meu Diari",
    "Mostrando todo el programa": "Mostrant tot el programa",
    "Mostrando ${visibleCount} de ${cards.length} películas": "Mostrant ${visibleCount} de ${cards.length} pel·lícules",
    "<span class=\"active\">CAS</span> <span style=\"color:var(--border-color)\">|</span> <a href=\"index_va.html\">VAL</a>": "<a href=\"index.html\">CAS</a> <span style=\"color:var(--border-color)\">|</span> <span class=\"active\">VAL</span>"
}

def main():
    with open("generate_html.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open("generate_html_va.py", "w", encoding="utf-8") as f:
        f.write(content)
        
    print("generate_html_va.py created.")

if __name__ == "__main__":
    main()
