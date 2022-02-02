import sys
from io import BytesIO
import requests
from PIL import Image

import find


map_api_server = "http://static-maps.yandex.ru/1.x/"
toponym_to_find = " ".join(sys.argv[1:])
map_params = find.params(toponym_to_find, find.pharmacy(toponym_to_find))
response = requests.get(map_api_server, params=map_params)

map_file = "map.png"
open(map_file, "wb").write(response.content)

Image.open(BytesIO(response.content)).show()