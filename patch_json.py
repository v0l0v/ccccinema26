import json

with open('movies_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix 19: While We're Young
data[18] = {
    "date": "Viernes, 21 de agosto",
    "title": "While We’re Young",
    "year": 2014,
    "country": "Estados Unidos",
    "duration": "97 minutos",
    "tmdb_url": "https://www.themoviedb.org/movie/252512-while-we-re-young",
    "genres": ["Comedia", "Drama"],
    "directors": ["Noah Baumbach"],
    "cast": ["Ben Stiller", "Naomi Watts", "Adam Driver", "Amanda Seyfried", "Charles Grodin", "Adam Horovitz", "Maria Dizzia", "Beastie Boys"],
    "synopsis": "Josh y Cornelia Srebnick son una pareja casada de cuarentones que no consiguen tener hijos. Mientras intentan revitalizar su matrimonio, conocen a una joven y carismática pareja de veinteañeros, Jamie y Darby, que los arrastran a su espontáneo estilo de vida libre de preocupaciones.",
    "poster_url": "https://image.tmdb.org/t/p/w500/qgmIadxcSjUKqb3KjfbBJ9t1ZyZ.jpg"
}

# Fix 23: 1987 (Canadá)
data[22] = {
    "date": "Miércoles, 26 de agosto",
    "title": "1987",
    "year": 2014,
    "country": "Canadá",
    "duration": "105 minutos",
    "tmdb_url": "https://www.themoviedb.org/movie/280218-1987",
    "genres": ["Comedia", "Drama"],
    "directors": ["Ricardo Trogi"],
    "cast": ["Jean-Carl Boucher", "Sandrine Bisson", "Claudio Colangelo", "Shadi Janho", "Laurent-Christophe De Ruelle", "Pier-Luc Funk"],
    "synopsis": "En el verano de 1987, Ricardo tiene 17 años y una apretada agenda de adolescente: perder la virginidad, comprar un coche y encontrar la forma de entrar en los clubes nocturnos. Para conseguir dinero rápido, decide delinquir junto a sus amigos, pero el atajo resulta ser más peligroso de lo esperado.",
    "poster_url": "https://image.tmdb.org/t/p/w500/h5Od9rVwDBJ9FEtfyxJxjakaoZA.jpg"
}

# Apply Spanish translations for English synopses
translations = {
    "Joey Breaker": "Joey es un astuto e influyente agente de talentos cinematográficos en Nueva York. Si hay un trato por cerrar, él lo cerrará. Si surge un nuevo talento, será el primero en la fila. Sin embargo, su vida hiperprogramada da un vuelco total debido a una serie de eventos inesperados que culminan en un romance fortuito con una extraordinaria joven jamaicana, enseñándole finalmente a vivir.",
    "Dim Sum: A Little Bit of Heart": "En el barrio de Richmond en San Francisco, una viuda de 62 años da la bienvenida al Año Nuevo chino con el deseo de viajar a China para rendir respeto a sus antepasados, convencida por un adivino de que este será el año de su muerte. Mientras tanto, su hija Geraldine sigue soltera, debatiéndose entre el matrimonio y el temor de dejar sola a su anciana madre. El alegre cuñado de la viuda, el tío Tam, intentará ayudar a resolver la situación.",
    "Lisbela e o Prisioneiro": "Lisbela es una joven soñadora que ama el cine. Leléu es un pícaro y divertido estafador que viaja de pueblo en pueblo ofreciendo espectáculos. Tras meterse en problemas por un romance con la esposa de un temible asesino a sueldo, Leléu huye y llega a una nueva ciudad, donde conoce y se enamora a primera vista de Lisbela. Sin embargo, ella está comprometida con Douglas, un hombre de campo que finge ser un sofisticado habitante de Río de Janeiro.",
    "Never Give a Sucker an Even Break": "Es una comedia disparatada de 1941 sobre un hombre (W.C. Fields) que intenta vender un guion absurdo a una gran productora cinematográfica. En su camino se enfrenta a situaciones surrealistas, camareras insolentes y todo tipo de contratiempos. Representa el último papel protagónico del legendario comediante W.C. Fields en un largometraje.",
    "Film Geek": "Narra la historia de Scotty Pelk, un dependiente de videoclub socialmente inepto y obsesionado con el cine que, tras ser despedido de su trabajo, se convirte inesperadamente en una sensación de internet como crítico cinematográfico en línea."
}

for movie in data:
    title = movie["title"]
    if title in translations:
        movie["synopsis"] = translations[title]

with open('movies_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Patch applied successfully!")
