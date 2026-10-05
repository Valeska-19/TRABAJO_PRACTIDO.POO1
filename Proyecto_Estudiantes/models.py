"""Modelos principales del sistema."""

class Cliente:
    CAMPOS = ("nombre", "apellido", "email", "telefono", "ciudad", "direccion")
    OBLIGATORIOS = ("nombre", "apellido", "email")
    total_creados = 0

    def __init__(self, id_cliente, nombre, apellido, email,
                 telefono="", ciudad="", direccion=""):
        self._id = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.ciudad = ciudad
        self.direccion = direccion
        Cliente.total_creados += 1

    @staticmethod
    def limpiar(valor):
        return str(valor).strip()

    @staticmethod
    def es_email_valido(valor):
        valor = Cliente.limpiar(valor)
        partes = valor.split("@")
        return (
            len(partes) == 2 and
            bool(partes[0]) and
            "." in partes[1] and
            not partes[1].startswith(".") and
            not partes[1].endswith(".")
        )

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self.limpiar(valor)
        if not valor:
            raise ValueError("El nombre es obligatorio")
        self._nombre = valor.title()

    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, valor):
        valor = self.limpiar(valor)
        if not valor:
            raise ValueError("El apellido es obligatorio")
        self._apellido = valor.title()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        valor = self.limpiar(valor)
        if not self.es_email_valido(valor):
            raise ValueError("El correo electrónico no es válido")
        self._email = valor.lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = self.limpiar(valor)
        if valor and not valor.isdigit():
            raise ValueError("El teléfono debe contener solamente números")
        self._telefono = valor

    @property
    def ciudad(self):
        return self._ciudad

    @ciudad.setter
    def ciudad(self, valor):
        self._ciudad = self.limpiar(valor).title()

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        self._direccion = self.limpiar(valor)

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    @property
    def dominio_email(self):
        return self.email.split("@", 1)[1]

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "ciudad": self.ciudad,
            "direccion": self.direccion,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"], datos["nombre"], datos["apellido"],
            datos["email"], datos.get("telefono", ""),
            datos.get("ciudad", ""), datos.get("direccion", "")
        )

    def __str__(self):
        return f"#{self.id} | {self.nombre_completo} | {self.email}"


class Estudiante:
    CAMPOS = ("nombre", "apellido", "email", "carnet")
    OBLIGATORIOS = CAMPOS
    NOTA_MINIMA = 0
    NOTA_MAXIMA = 20
    total_creados = 0

    def __init__(self, id_estudiante, nombre, apellido, email, carnet,
                 notas=None, materias=None):
        self._id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet
        self._notas = {str(k): list(v) for k, v in (notas or {}).items()}
        self._materias = set(materias or [])
        Estudiante.total_creados += 1

    @staticmethod
    def limpiar(valor):
        return str(valor).strip()

    @classmethod
    def es_nota_valida(cls, nota):
        return isinstance(nota, (int, float)) and cls.NOTA_MINIMA <= nota <= cls.NOTA_MAXIMA

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self.limpiar(valor)
        if not valor:
            raise ValueError("El nombre es obligatorio")
        self._nombre = valor.title()

    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, valor):
        valor = self.limpiar(valor)
        if not valor:
            raise ValueError("El apellido es obligatorio")
        self._apellido = valor.title()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        valor = self.limpiar(valor)
        if "@" not in valor:
            raise ValueError("El correo electrónico no es válido")
        self._email = valor.lower()

    @property
    def carnet(self):
        return self._carnet

    @carnet.setter
    def carnet(self, valor):
        valor = self.limpiar(valor).upper()
        if len(valor) < 4:
            raise ValueError("El carnet debe tener al menos 4 caracteres")
        self._carnet = valor

    @property
    def materias(self):
        return set(self._materias)

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    @property
    def promedio(self):
        notas = [nota for lista in self._notas.values() for nota in lista]
        return round(sum(notas) / len(notas), 2) if notas else 0

    @property
    def estado(self):
        return "Aprobado" if self.promedio >= 14 else "Reprobado"

    def inscribir_materia(self, materia):
        materia = self.limpiar(materia).title()
        if not materia:
            raise ValueError("La materia no puede quedar vacía")
        self._materias.add(materia)
        self._notas.setdefault(materia, [])
        return materia

    def agregar_nota(self, materia, nota):
        if not self.es_nota_valida(nota):
            raise ValueError(f"La nota debe estar entre {self.NOTA_MINIMA} y {self.NOTA_MAXIMA}")
        materia = self.inscribir_materia(materia)
        self._notas[materia].append(float(nota))

    def notas_de(self, materia):
        return list(self._notas.get(self.limpiar(materia).title(), []))

    def materias_en_comun(self, otro):
        return self.materias.intersection(otro.materias)

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self._notas,
            "materias": sorted(self._materias)
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"], datos["nombre"], datos["apellido"],
            datos["email"], datos["carnet"],
            datos.get("notas", {}), datos.get("materias", [])
        )

    def __str__(self):
        return f"{self.carnet} - {self.nombre_completo} | Promedio: {self.promedio:.2f} | {self.estado}"
