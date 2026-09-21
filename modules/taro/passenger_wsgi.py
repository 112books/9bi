"""
modules/taro/passenger_wsgi.py — Punt d'entrada Passenger per al bundle «taro».
Passenger espera un WSGI callable anomenat «application» en aquest mòdul.
Molts dels nostres app.py ja defineixen «application»; per seguretat s'importa
tant «application» com «app» i es normalitza aquí.
"""
from taro.app import application
