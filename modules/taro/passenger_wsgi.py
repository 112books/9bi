#!/usr/bin/env python3
"""
modules/taro/passenger_wsgi.py — Punt d'entrada Passenger per al bundle «taro».
Passenger espera un WSGI callable anomenat «application» en aquest mòdul.
El router és «app.py» de la MATEIXA carpeta (mateix patró que
modules/autopublica/passenger_wsgi.py i modules/votacio/passenger_wsgi.py,
que ja funcionen a Passenger).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import application
