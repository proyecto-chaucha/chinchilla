# Chinchilla
Explorador de bloques oficial del Proyecto Chaucha

## Instalación

Este sistema fue programado para funcionar en Python ver. 3.6 junto con las extensiones [Flask](http://flask.pocoo.org) y [python-bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc).

```
sudo apt-get install pip3
pip3 install flask, python-bitcoinrpc
```

Luego de esto, es necesario ejecutar la wallet en modo **-server -daemon -txindex** y se debe incluir la configuración para la comunicación RPC en el archivo *config.py* dentro de la carpeta chinchilla.

Para finalizar, se ejecuta el código con python de la siguiente manera.

```
python3 __main__.py
```

Si se quiere ejecutar en un vps es necesario utilizar [Gunicorn](http://gunicorn.org) para redirigir el flujo web a la ip del servidor. Para mantener en funcionamiento el sistema es recomendable usar *nohup*.

```
pip3 install gunicorn
nohup gunicorn -w 4 -b 127.0.0.1:4000 chinchilla:app
```