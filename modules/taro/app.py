#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Col·lectiu 9 Barris Imatge
# Llicència i avisos (fitxer LICENSE a l'arrel del repositori)
"""
modules/taro/app.py — Router WSGI del bundle «taro»
====================================================
Monta les 3 aplicacions sota un sol punt de muntatge, sota /taro/:

    /taro/health           → health NET del router (sense cap app)
    /taro/autopublica/…    → dispatch a modules/taro/autopublica/app.py
    /taro/votacio/…        → dispatch a modules/taro/votacio/app.py
    /taro/formularis/…     → dispatch a modules/taro/formularis/app.py

Cada submòdul llegeix el SEU config.ini de la SEVA carpeta, exactament
com quan funcionen sols: el router només encamina (PATH_INFO) i reenvia
SCRIPT_NAME perquè cada app sàpiga on és. Per això cada submòdul ha de
poder instal·lar-se separat i sense res del router al voltant.
"""

import importlib.util
import os
import sys

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

_APPS = {}


def load_app(name):
    """carrega el submòdul des del camí del fitxer i en torna el callable.

    Els tres submòduls es diuen app.py, així que NO es poden importar pel
    nom: el segon i el tercer retornarien el primer de sys.modules i tots
    acabarien servint la mateixa aplicació. Els carreguem per camí, amb un
    nom propi a sys.modules, i els desem a la memòria per no tornar a
    executar-los a cada petició."""
    if name in _APPS:
        return _APPS[name]
    path = os.path.join(MODULE_DIR, name, "app.py")
    mod_name = "taro_app_" + name
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError("no s'ha pogut carregar " + path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    _APPS[name] = getattr(module, "application")
    return _APPS[name]


def dispatch(app_dir, environ, start_response):
    """carrega l'aplicació del submòdul i li delega la petició (amb el
    PATH_INFO ja reescrit: uns vindran com /taro/autopublica/… i d'altres
    com /autopublica/… segons com configuri el SCRIPT_NAME/PATH_INFO)"""
    return load_app(app_dir)(environ, start_response)


def application(environ, start_response):
    path_info = environ.get("PATH_INFO", "")
    script_name = environ.get("SCRIPT_NAME", "")

    # 1. tot el que comença per /taro/ — Li treiem el prefix del router
    if path_info.startswith("/taro"):
        path_info = path_info[len("/taro"):] or "/"
        script_name = script_name + "/taro"

    # 2. health propi del router (pre-encaminament, sense despatxar cap app)
    if path_info.rstrip("/") == "/health":
        body = b"ok"
        start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8"),
                                  ("Content-Length", str(len(body)))])
        return [body]

    # 3. dispatch per prefix
    prefixes = [("autopublica", "/autopublica"), ("votacio", "/votacio"),
                ("formularis", "/formularis")]
    for name, prefix in prefixes:
        if path_info == prefix or path_info.startswith(prefix + "/"):
            inner = path_info[len(prefix):] or "/"
            environ["PATH_INFO"] = inner
            environ["SCRIPT_NAME"] = script_name + prefix
            return dispatch(name, environ, start_response)

    # 4. res coincident
    body = b"not found"
    start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8"),
                                     ("Content-Length", str(len(body)))])
    return [body]
