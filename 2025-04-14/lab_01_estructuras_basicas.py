# lab_01_estructuras_basicas.py
# Autor: Rafael Mata
# Fecha: 14 de abril, 2025
# Tema: Estructuras básicas en Python

# 1. Listas
frutas = ["manzana", "banana", "cereza"]
frutas.append("kiwi")
print("Lista de frutas:", frutas)

# 2. Diccionarios
contacto = {
    "nombre": "Rafa",
    "email": "rafa@example.com"
}
print("Nombre del contacto:", contacto["nombre"])

# 3. Tuplas
coordenadas = (10.5, -84.3)
print("Latitud:", coordenadas[0], "Longitud:", coordenadas[1])

# 4. Conjuntos (sets)
numeros = {1, 2, 3, 2, 1}
print("Set de números únicos:", numeros)

# 5. Estructuras de control
for fruta in frutas:
    if fruta.startswith("b"):
        print(f"{fruta} empieza con 'b'")

# 6. While loop
contador = 3
while contador > 0:
    print("Contando...", contador)
    contador -= 1

# 7. Try / Except
try:
    division = 10 / 0
except ZeroDivisionError:
    print("¡Error! No se puede dividir entre cero.")
