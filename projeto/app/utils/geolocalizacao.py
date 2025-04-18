import requests

def buscar_coordenadas_por_endereco(rua, numero, bairro, cidade, estado):
    endereco = f"{rua} {numero}, {bairro}, {cidade}, {estado}, Brasil"
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": endereco,
        "format": "json",
        "limit": 1
    }

    try:
        response = requests.get(url, params=params, headers={"User-Agent": "cpfl-docs"})
        response.raise_for_status()
        data = response.json()

        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        else:
            return None, None

    except Exception as e:
        print(f"[Erro Geolocalização] {e}")
        return None, None
