#!/usr/bin/env python3
"""Punt d'entrada Phusion Passenger per al bundle «taro» (modules/taro/).
Passenger espera un WSGI callable anomenat «application» en aquest mòdul.
El router és app.py de la MATEIXA carpeta — exactament el mateix patró
que ja fan els passenger_wsgi.py de modules/autopublica, modules/votacio
i modules/formularis (que funcionen en producció).

IMPORTANT — Passenger carrega AQUEST fitxer i executa el codi que hi ha.
Passenger PASSARÀ DE PASSAR el PATH_INFO que els arriba (passant per
/taro/… gairebé segur, perquè el mòdul Passenger s'ha de configurar per
aquest punt de muntatge a Dinahosting). El router assumeix que el prefix
«/taro» ja l'ha tret Passenger; si algun dia no el treu, ho veuràs en
els logs de Passenger i ho ajustem.
"""
import os
import sys

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MODULE_DIR)

from app import application
