##


* Las dependencias se pueden instalar con "pip install -r requirements.txt"

* run.sh ejecuta los scrapers que persisten en una base SQLite y los scripts para generar reporte en csv

* Los reportes *(directorio samples)* estan ordenados por precio y por X feature. e.g, en caso de TV, se agrupan por tamaño, por precio.

* fravega.com redirecciona a shopping.fravega.com

* TODO: para algun caso, en garbarino es necesario crawlear un nivel más para buscar ciertos datos

* En el caso de los AC, muchos no tienen modelo cargado, por lo que ese campo se lo excluye del csv.

* Lo ideal sería tener URLS precargadas por otro crawler, para hacer requests asincronicos y evitar ir descubriendo paginas