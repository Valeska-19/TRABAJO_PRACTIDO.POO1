"""Funciones de interfaz de consola."""

import os

PALETA = {
    "rojo": "\033[91m",
    "verde": "\033[92m",
    "azul": "\033[94m",
    "amarillo": "\033[93m",
    "cyan": "\033[96m",
    "normal": "\033[0m",
}

SI = {"s", "si", "sí", "y", "yes"}

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def pintar(texto, tono="normal"):
    print(f"{PALETA.get(tono, PALETA['normal'])}{texto}{PALETA['normal']}")

def encabezado(texto):
    limpiar_pantalla()
    print("=" * 72)
    print(texto.center(72))
    print("=" * 72)
    print()

def exito(texto):
    pintar(f"[OK] {texto}", "verde")

def error(texto):
    pintar(f"[!] {texto}", "rojo")

def aviso(texto):
    pintar(f"[i] {texto}", "cyan")

def confirmar(texto):
    return input(f"{texto} (s/n): ").strip().lower() in SI

def esperar():
    input("\nPresione Enter para continuar...")
