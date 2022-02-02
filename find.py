import requests


def params(toponym_to_find, *pt):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    pt = '~'.join(list(map(lambda x: f"{float(x[0])},{float(x[1])},flag", pt)))
    if pt:
        pt = '~' + pt
    response = requests.get(geocoder_api_server, params=geocoder_params)

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    points = [list(map(float, toponym["boundedBy"]["Envelope"]["lowerCorner"].split())),
              list(map(float, toponym["boundedBy"]["Envelope"]["upperCorner"].split()))]
    toponym_size = [str(points[1][0] - points[0][0]), str(points[1][1] - points[0][1])]
    map_params = {
        "l": "map",
        "pt": f"{float(toponym_longitude)},{float(toponym_lattitude)},flag" + pt
    }
    return map_params


def pharmacy(toponym_to_find):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" \
                       f"{toponym_to_find}&format=json&results=1"
    toponym = requests.get(geocoder_request).json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coords = ','.join(toponym["Point"]["pos"].split())

    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": toponym_coords,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    return response.json()["features"][0]["geometry"]["coordinates"]
