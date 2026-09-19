#!/usr/bin/env python3
"""Punt d'entrada per a Phusion Passenger (Dinahosting/cPanel)."""
import os
import sys

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MODULE_DIR)

from app import application

application = application