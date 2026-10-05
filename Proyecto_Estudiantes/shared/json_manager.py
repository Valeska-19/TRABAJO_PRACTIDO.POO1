"""Persistencia sencilla mediante archivos JSON."""

import json
import os

class GestorJSON:
    def __init__(self, ruta):
        self._ruta = ruta
        carpeta = os.path.dirname(ruta)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)

    @property
    def ruta(self):
        return self._ruta

    def leer(self):
        if not os.path.isfile(self._ruta):
            return []
        try:
            with open(self._ruta, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)
                return contenido if isinstance(contenido, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    def guardar(self, datos):
        try:
            with open(self._ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=4)
            return True
        except (OSError, TypeError):
            return False
