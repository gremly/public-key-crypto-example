public-key-crypto-example
=========================

Ejemplo de cifrado asimétrico usando llaves RSA, exponiendo servicios Rest usando
django_restframework y M2Crypto.

# Instalación

Para la instalación completa de las librerías se recomienda la creación de un entorno
virtual con virtualenv o virtualenvwrapper:

    mkvirtualenv pkey_env

A continuación se lleva a cabo la instalación de las dependencias usando el archivo
requirements.pip.

    pip install -r requirements.pip

Este proyecto usa la librería M2Crypto, acá su página principal con las instrucciones de
instalación: http://chandlerproject.org/Projects/MeTooCrypto.

# Configuración

Definir los parámetros definidos para bases de dátos y demás configuraciones necesarias
dentro del fichero settings.py.

# Instrucciones de uso.

Antes de comenzar puede generar sus llaves RSA, pública y privada, mediante openssl de la siguiente manera:

    openssl genrsa -out privkey.pem 1024
    openssl rsa -in privkey.pem -pubout -out pubkey.pem


Lanzar el servidor django, que por defecto escucha en localhost:8000, para exponer los servicios, sincronizando antes la base de datos
para creación de las tablas necesarias:

    $ workon pkey_env
    (pkey_env)$ python manage.py syncdb
    (pkey_env)$ python manage.py runserver

En el momento el API cuenta con dos recursos que son accedidos únicamente usando el método POST:

    /register --> Permite enviar una llave pública al servidor y almacenarla recibiendo un ID único para su acceso.
    /validate --> Permite verificar que un texto ha sido cifrado correctamente usando la llave privada asociada al
                  una llave pública registrada en el servidor. 

Para usar los recursos anteriormente descritos puede usarse un cliente o librería como curl.

## Registrar llave pública. (/register)

Este recurso recibe como parámetro un objeto JSON con la siguiente estructura:

    {"key": "Some RSA public key"}

Retorna un identificador único para la llave almacenada:

    {"id": "fpoadisuf"}


Ejemplo usando curl:

    curl vvv -X POST -H "Content-Type: application/json" http://localhost:8000/api/register/ -d '{"key": "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC42D5HVR5UOzYShZ8ZirzRJrVN\nj3AJqa03HyxcfBwWhpXv12oOZ4zxzo4w4KWkZ7hcKXF8zdf6W5YbfWtwOJzIfmC/\nkMwGxlIfSxsM3otF0pnpCZN/3n0BKgCD1CjnNDlx/HAnjqsWJCXns7I/JKl5I5+3\njTyQfXSPAkl0eZ/ybQIDAQAB\n-----END PUBLIC KEY-----"}'

El resultado luce de la siguiente manera:

    Hostname was NOT found in DNS cache
    Adding handle: conn: 0x2461d80
    Adding handle: send: 0
    Adding handle: recv: 0
    Curl_addHandleToPipeline: length: 1
    - Conn 0 (0x2461d80) send_pipe: 1, recv_pipe: 0
      Trying 127.0.0.1...
    Connected to localhost (127.0.0.1) port 8000 (#0)
    POST /api/register/ HTTP/1.1
    User-Agent: curl/7.34.0
    Host: localhost:8000
    Accept: */*
    Content-Type: application/json
    Content-Length: 287
    
    upload completely sent off: 287 out of 287 bytes
    HTTP 1.0, assume close after body
    HTTP/1.0 201 CREATED
    Date: Tue, 14 Jan 2014 05:59:12 GMT
    Server: WSGIServer/0.1 Python/2.7.6
    Vary: Accept, Cookie
    X-Frame-Options: SAMEORIGIN
    Content-Type: application/json
    Allow: POST, OPTIONS
    
    Closing connection 0

    {"id": "tAI5ReEg8fkpocpWplf33SDsfdA"}

## Verificar cifrado con llave privada. (/validate)

Este recurso recibe como parámetro un objeto JSON con la siguiente estructura:

    {"id": "Id public key", "clear": "Clear text to verify", "crypted": "OIYFIGFYRADFLFVB"}

El texto cifrado deberá estár codificado en base64 para evitar problemas con el envío al servidor.

Retorna en los encabezados código http 200 si el cifrado es correcto, de lo contrario retorna el código http 400.

Ejemplo usando curl:

    curl vvv -X POST -H "Content-Type: application/json" http://localhost:8000/api/validate/ -d '{"id": "tAI5ReEg8fkpocpWplf33SDsfdA", "clear": "Some clear text", "crypted": "g88JSC6/MYhucEmCd0BE8nJRApz+Y/eTnkBNv7Icca3wYC3w8z2ciuEiUaG2vwXs7Sgwif+v+D93IZWSs1kKL7aBo4xhaDmARmuEIqNPbbbYP"}'


Librería para firmado.
======================

Esta librería se encuentra bajo el directorio lib. Permite al usuario ingresar un texto y lo retorna firmado
haciendo uso de una llave RSA privada especificada.

# Instalación

Es necesario tener instalada en el sistema la librería M2Crypto.


# Configuración

En el fichero config.py se encuentran las variables que permitirán el trabajo del script para firmado.

*PRIMARY_KEY*: Define la ruta al archivo contenedor de la llave privada.

*ENCODED_RESULT*: Un booleano que le permite al usuario decidir si el resultado es codificado en base64 o no.

# Instrucciones de uso

La siguiente línea bastará en una terminal para realizar el firmado con la llave privada definida.

    $ python signtext.py 'Algun texto por firmar usando llave primaria'

    jdVenhyMANKmjVoy3OoyQSc6XTCgCuKdI..... <-- Texto firmado digitalmente con privkey.pem.


Licencia
========

Este trabajo es liberado al dominio público bajo la licencia Creative Commons.
![](https://i.creativecommons.org/l/by/4.0/88x31.png)
