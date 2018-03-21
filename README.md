# Chinchilla
Explorador de bloques oficial del Proyecto Chaucha

## Ejemplo

Puedes visitar [explorer.chaucha.cl](http://explorer.chaucha.cl) para ver en funcionamiento el sistema sobre la [Red Chaucha](https://www.chaucha.cl/).

## Instalación

Este sistema fue programado para funcionar en Python 3.6 junto con las extensiones [Flask](http://flask.pocoo.org), [Ukuku](https://github.com/proyecto-chaucha/ukuku) y [PyMongo](https://api.mongodb.com/python/current/).

Si quieres ejecutar en un vps es necesario utilizar [Gunicorn](http://gunicorn.org) para redirigir el flujo web a la ip del servidor.

```
gunicorn -b <IP>:80 chinchilla:app --daemon
```