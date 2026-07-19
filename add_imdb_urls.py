import json

with open('movies_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

imdb_ids = {
    "Joey Breaker": "tt0107273",
    "El artista": "tt1321381",
    "Mr. Belvedere Goes to College": "tt0041664",
    "Mátenme porque me muero": "tt0138629",
    "Things Change": "tt0096259",
    "El destino no tiene favoritos": "tt0383307",
    "Dim Sum: A Little Bit of Heart": "tt0089028",
    "Safety Last!": "tt0014429",
    "Plaff (Demasiado miedo a la vida)": "tt0095874",
    "Bluff": "tt0830768",
    "Little Shop of Horrors": "tt0091419",
    "Culpa cero": "tt32422731",
    "The Sure Thing": "tt0090097",
    "Denominación de origen": "tt8215836",
    "Defending Your Life": "tt0101684",
    "De noche vienes, Esmeralda": "tt0118941",
    "She’s Gotta Have It": "tt0091939",
    "Lisbela e o Prisioneiro": "tt0379354",
    "While We’re Young": "tt1791682",
    "Doble discurso": "tt27825595",
    "Ella McCay": "tt30095066",
    "Never Give a Sucker an Even Break": "tt0033945",
    "1987": "tt3496058",
    "A New Leaf": "tt0067482",
    "La práctica": "tt28233306",
    "Film Geek": "tt0478148",
    "Un poeta": "tt31835694"
}

for movie in data:
    title = movie["title"]
    if title in imdb_ids:
        movie["imdb_url"] = f"https://www.imdb.com/title/{imdb_ids[title]}/"
    else:
        movie["imdb_url"] = None

with open('movies_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("IMDb URLs added successfully!")
