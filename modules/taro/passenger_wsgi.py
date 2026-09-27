#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Col·lectiu 9 Barris Imatge
"""Punt d'entrada Phusion Passenger per al bundle «taro» (modules/taro/).
Passenger espera un WSGI callable anomenat «application» en aquest mòdul.
El router és app.py de la MATEIXA carpeta — el mateix patró que fan els
passenger_wsgi.py de cada mòdul individual (autopublica, votacio,
formularis), que es poden instal·lar per separat.

IMPORTANT — Passenger carrega AQUEST fitxer i executa el codi que hi ha.
Passenger pot PASSAR DE PASSAR el PATH_INFO que li arriba (passant per
/taro/… gairebé segur, perquè el mòdul Passenger s'ha de configurar per
a aquest punt de muntatge). El router assumeix que el prefix «/taro» ja
l'ha tret Passenger; si algun dia no el treu, ho veuràs als logs de
Passenger i cal Adjustar-ho.
"""
import os
import sys

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MODULE_DIR)

from app import application
