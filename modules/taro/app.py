#!/usr/bin/env python3
"""
modules/taro/app.py — Router WSGI del bundle «taro» (9 Barris Imatge)
=====================================================================
Monta 3 aplicacions Passatger existents sota un sol punt de muntatge,
sota /taro/:

    /taro/health           → health NET del router (sense cap app)
    /taro/autopublica/…    → dispatch a modules/taro/autopublica/app.py
    /taro/votacio/…        → dispatch a modules/taro/votacio/app.py
    /taro/formularis/…     → dispatch a modules/taro/formularis/app.py

Cada submòdul llegeix el SEU config.ini de la SEVA carpeta, exactament
com quan funcionen sols: el router només encamina (PATH_INFO) i reenvia
SCRIPT_NAME perquè cada app sàpiga on és.
"""

import os
import sys

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


def dispatch(app_dir, environ, start_response):
    """carrega l'aplicació del submòdul i li delega la petició (amb el
    PATH_INFO ja reescrit: uns vindran com /taro/autopublica/… i d'altres
    com /autopublica/… segons com configuri Passenger el SCRIPT_NAME/PATH_INFO)"""
    path = os.path.join(MODULE_DIR, app_dir)
    if path not in sys.path:
        sys.path.insert(0, path)
    app = getattr(__import__("app"), "application", None)
    if app is None:
        app = getattr(__import__("app"), "app")
    # en alguns app.py el callable es diu "application", en d'altres "app"
    return app(environ, start_response)


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
