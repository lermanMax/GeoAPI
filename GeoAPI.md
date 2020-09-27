# GEOAPI 
Тестовое задание для стажера на позицию «Аналитик (python)»

Автор: Лерман Максим

## Введение
Реализовать HTTP-сервер для предоставления информации по географическим объектам.
Данные взять из географической базы данных GeoNames.

## Доступные объекты
### City
Этот объект представляет собой информацию о городе. 
Он представлен объектом JSON.

| Параметр | Тип данных | Описание | 
|----------------|----------------|----------------|
| geonameid | Integer | id of record in geonames database |
| name | String | name of geographical point |
| asciiname | String | name of geographical point in plain ascii characters |
| alternatenames | String | alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table | 
| latitude | Float | latitude in decimal degrees |
| longitude | Float | longitude in decimal degrees | 
| feature class | String | see http://www.geonames.org/export/codes.html |
| feature code | String | see http://www.geonames.org/export/codes.html |
| country code | String | ISO-3166 2-letter country code |
| cc2 | String | alternate country codes, comma separated, ISO-3166 2-letter country code |
| admin1 code | String | fipscode (subject to change to iso code), see exceptions below | 
| admin2 code | String | code for the second administrative division |
| admin3 code | String | code for third level administrative division |
| admin4 code | String | code for fourth level administrative division |
| population | Integer | population |
| elevation | Integer | elevation in meters |
| dem  | String | digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat. | 
| timezone          | String | the iana timezone id |     
| modification date | String | date of last modification in yyyy-MM-dd format |


## Методы
_____
### :black_medium_square: findCityByID
Метод возвращает информацию о городе по идентификатору.

#### HTTP Request
```
GET http://127.0.0.1:8000/findCityByID
```

HEADERS
```
Content-Type: application/json
```
BODY
```
{
  "geonameid": 111111
}
```

| Параметр | Тип данных | Описание | 
|----------------|----------------|----------------|
| geonameid | Integer | id города который нужно получить |

#### Response
Метод возвращает JSON следующей структуры
```
{
    "geonameid": "1",
    "name": "Name",
    "asciiname": "Name",
    "alternatenames": "Name2, Name3", 
    "latitude": "11.11111", 
    "longitude": "11.11111", 
    "feature class": "P", 
    "feature code": "PPLC", 
    "country code": "RU",
    "cc2": "", 
    "admin1 code": "1", 
    "admin2 code": "", 
    "admin3 code": "", 
    "admin4 code": "",    
    "population": "1", 
    "elevation": "1",
    "dem": "1", 
    "timezone": "Continent/City",     
    "modification date": "2020-01-01"
}
```
_____
### pageOfCities
Метод возвращает массив городов на заданной странице с учетом количества городов на страницу    

#### HTTP Request
```
GET http://127.0.0.1:8000/pageOfCities
```

HEADERS
```
Content-Type: application/json
```
BODY
```
{
  "page": 1,
  "count": 1
}
```

| Параметр | Тип данных | Описание | 
|----------------|----------------|----------------|
| page | Integer | номер страницы, которую неоходимо вернуть |
| count | Integer | количество городов на одну страницу |

#### Response
Метод возвращает JSON следующей структуры
```
{
  "page_of_cities": [ 
    {    
      "geonameid": "1",
      "name": "Name",
      "asciiname": "Name",
      "alternatenames": "Name2, Name3", 
      "latitude": "11.11111", 
      "longitude": "11.11111", 
      "feature class": "P", 
      "feature code": "PPLC", 
      "country code": "RU",
      "cc2": "", 
      "admin1 code": "1", 
      "admin2 code": "", 
      "admin3 code": "", 
      "admin4 code": "",    
      "population": "1", 
      "elevation": "1",
      "dem": "1", 
      "timezone": "Continent/City",     
      "modification date": "2020-01-01"
    }, 
    ...
  ]
}
```


