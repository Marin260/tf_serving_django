# DOCKER COMPOSE

Stvaranje kompozicije koja za projekt sa Tensorflow Servingom, Djangom, Postgresom i Redisom.

## Lokalno postavljanje projekta

Stvaranje novog radnog direktorija

```shell
$ mkdir tf_serving && cd $_
```

Stvaranje i aktiviranje novog virtualnog okruženja

```shell
$ python3 -m venv venv
$ source ./venv/bin/activate
```

Instaliranje potrebnih python paketa

```shell 
$ pip install Django
$ pip install requests
$ pip install psycopg[binary]
```

Stvaranje novog Django projekta

```shell
$ django-admin startproject projectName
```

### Postgres

Potrebno prethodno instalirati Postgres

Potrebne izmjene u `settings.py` Django projekta kako bi mogli koristit postgress bazu podataka.

> napomena: naknadno će se ove postavke morati dodatno mijenjati za rad sa Dockerom

`settings.py` prije promijena:

```py
# projectName/settings.py
...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}
```

promjene stvaramo prema sljedećem boilerplateu:

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<db_name>',
        'USER': '<db_username>',
        'PASSWORD': '<password>',
        'HOST': '<db_hostname_or_ip>',
        'PORT': '<db_port>',
    }
}
```


`settings.py` nakon promijena:

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'tf_postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

sada mozemo izvršiti migracije i stvoriti novog superusera:

```shell
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py createsuperuser
```

### Redis

Potrebno prethodno instalirati Redis

Pokrenuti redis server:

```shell
$ redis-server
```

Provjera ispravnosti rada:

```shell
$ redis-cli ping
```

U `settings.py` možemo zaljepiti sljedeće postavke:

```py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
    }
}
```

### Tensorflow Serving

Za potrebu projekta koristiti će se modeli već unutar TF Serving repozitorija.

Tokom razvoja aplikacije koriti će se Docker slika Tensorflow Servinga koja će izložiti API endpoint koji možemo konzumirati našom Django aplikacijom

```shell
$ docker pull tensorflow/serving
$ TESTDATA="$(pwd)/serving/tensorflow_serving/servables/tensorflow/testdata"

$ docker run -t --rm -p 8501:8501 \
    -v "$TESTDATA/saved_model_half_plus_two_cpu:/models/half_plus_two" \
    -e MODEL_NAME=half_plus_two \
    tensorflow/serving &
```

Nakon pokretanja može se provjeriti radi li kontejner ispravno uz pomoć alata `curl`:

```shell
curl -d '{"instances": [1.0, 2.0, 5.0]}' \
    -X POST http://localhost:8501/v1/models/half_plus_two:predict
```

## Konzumiranje API-a unutar Django projekta

Stvorena je forma u koju User može upisati njegov upit modelu. Upit tada stvaramo i šaljemo uz pomoć paketa requests.

Stvaranje requesta sa formom:

```py
def half_plus_three(request):
    if request.method == 'POST':
        request_timestamp = timezone.now()
        form = RequestsFormField(request.POST)

        if form.is_valid():
            data = request.POST['request']
            payload = [float(x) for x in data.split(',')]
            tf_request = tf_api_request(payload)            

            reqInstance = Request(request=data, response=tf_request['response'], request_time=request_timestamp, response_time=tf_request['response_time'])
            reqInstance.save()


    form = RequestsFormField()
    context = {'form': form}
    return redirect('request-list')
```

Slanje upita:

```py
def tf_api_request(payload: list):
    tf_request_data = {"instances": payload}

    url = 'http://localhost:8501/v1/models/half_plus_two:predict'
    response = requests.post(url, json=tf_request_data)
    
    response_timestamp = timezone.now()
    tf_api_response = response.json()
    return {'response': tf_api_response, 'response_time':
```

Odgovor spremamo u bazu i prikazujemo na stranici.

## Dockeriziranje projekta

U `requirements.txt` spremamo sve potrebne pakete (engl. dependencies) koji su potrebni za normalan rad naseg projekta.


### Pokretanje projekta

```shell
sudo docker-compose build
docker-compose up
```
