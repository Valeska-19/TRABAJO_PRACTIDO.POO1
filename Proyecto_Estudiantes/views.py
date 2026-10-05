"""Capa de operaciones del sistema: CRUD y reglas de estudiantes."""

from models import Cliente, Estudiante
from shared.json_manager import GestorJSON


class ClienteController:
    MODELO = Cliente
    ARCHIVO = "data/clientes.json"
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "telefono", "ciudad")
    _gestor = GestorJSON(ARCHIVO)

    @classmethod
    def _registros(cls):
        return cls._gestor.leer()

    @classmethod
    def siguiente_id(cls):
        return max((r.get("id", 0) for r in cls._registros()), default=0) + 1

    @classmethod
    def emails_registrados(cls, excepto_id=None):
        return {
            r.get("email", "").lower()
            for r in cls._registros()
            if r.get("id") != excepto_id
        }

    @staticmethod
    def _buscar_en(registro, texto, campos):
        texto = texto.lower()
        return any(texto in str(registro.get(campo, "")).lower() for campo in campos)

    @classmethod
    def crear(cls, datos):
        try:
            faltan = [c for c in cls.MODELO.OBLIGATORIOS if not str(datos.get(c, "")).strip()]
            if faltan:
                return False, "Campos obligatorios: " + ", ".join(faltan)

            email = str(datos.get("email", "")).strip().lower()
            if email in cls.emails_registrados():
                return False, "El correo ya está registrado"

            valores = {campo: datos.get(campo, "") for campo in cls.MODELO.CAMPOS}
            nuevo = cls.MODELO(cls.siguiente_id(), **valores)
            registros = cls._registros()
            registros.append(nuevo.a_diccionario())

            if not cls._gestor.guardar(registros):
                return False, "No fue posible guardar el registro"
            return True, f"Registro creado con ID {nuevo.id}"
        except ValueError as exc:
            return False, str(exc)

    @classmethod
    def listar(cls):
        return [cls.MODELO.desde_diccionario(r) for r in cls._registros()]

    @classmethod
    def obtener(cls, identificador):
        for objeto in cls.listar():
            if objeto.id == identificador:
                return objeto
        return None

    @classmethod
    def buscar(cls, termino):
        termino = str(termino).strip()
        if not termino:
            return []
        return [
            cls.MODELO.desde_diccionario(r)
            for r in cls._registros()
            if cls._buscar_en(r, termino, cls.CAMPOS_BUSCABLES)
        ]

    @classmethod
    def actualizar(cls, identificador, cambios):
        if not cambios:
            return False, "No se recibieron cambios"

        invalidos = set(cambios) - set(cls.MODELO.CAMPOS)
        if invalidos:
            return False, "Campos no reconocidos: " + ", ".join(sorted(invalidos))

        objeto = cls.obtener(identificador)
        if objeto is None:
            return False, "No existe ese registro"

        if "email" in cambios:
            nuevo = str(cambios["email"]).strip().lower()
            if nuevo in cls.emails_registrados(identificador):
                return False, "El correo ya pertenece a otro registro"

        try:
            for campo, valor in cambios.items():
                setattr(objeto, campo, valor)

            registros = cls._registros()
            for posicion, registro in enumerate(registros):
                if registro.get("id") == identificador:
                    registros[posicion] = objeto.a_diccionario()
                    break

            if not cls._gestor.guardar(registros):
                return False, "No se pudo guardar la modificación"
            return True, "Registro actualizado correctamente"
        except ValueError as exc:
            return False, str(exc)

    @classmethod
    def eliminar(cls, identificador):
        registros = cls._registros()
        nuevos = [r for r in registros if r.get("id") != identificador]
        if len(nuevos) == len(registros):
            return False, "No existe un registro con ese ID"
        if not cls._gestor.guardar(nuevos):
            return False, "No se pudo eliminar el registro"
        return True, "Registro eliminado"

    @classmethod
    def estadisticas(cls):
        registros = cls._registros()
        return {"total": len(registros)}


class EstudianteController(ClienteController):
    MODELO = Estudiante
    ARCHIVO = "data/estudiantes.json"
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")
    _gestor = GestorJSON(ARCHIVO)

    @classmethod
    def carnets_registrados(cls, excepto_id=None):
        return {
            r.get("carnet", "").upper()
            for r in cls._registros()
            if r.get("id") != excepto_id
        }

    @classmethod
    def crear(cls, datos):
        carnet = str(datos.get("carnet", "")).strip().upper()
        if carnet in cls.carnets_registrados():
            return False, "Ese carnet ya está registrado"
        return super().crear(datos)

    @classmethod
    def actualizar(cls, identificador, cambios):
        if "carnet" in cambios:
            carnet = str(cambios["carnet"]).strip().upper()
            if carnet in cls.carnets_registrados(identificador):
                return False, "Ese carnet pertenece a otro estudiante"
        return super().actualizar(identificador, cambios)

    @classmethod
    def agregar_nota(cls, identificador, materia, nota):
        estudiante = cls.obtener(identificador)
        if estudiante is None:
            return False, "No existe el estudiante"

        try:
            estudiante.agregar_nota(materia, nota)
            registros = cls._registros()
            for i, registro in enumerate(registros):
                if registro.get("id") == identificador:
                    registros[i] = estudiante.a_diccionario()
                    break
            if not cls._gestor.guardar(registros):
                return False, "No se pudo guardar la nota"
            return True, "Nota registrada correctamente"
        except ValueError as exc:
            return False, str(exc)

    @classmethod
    def materias_ofertadas(cls):
        resultado = set()
        for estudiante in cls.listar():
            resultado.update(estudiante.materias)
        return sorted(resultado)

    @classmethod
    def materias_en_comun(cls, primero, segundo):
        a, b = cls.obtener(primero), cls.obtener(segundo)
        if a is None or b is None:
            return None
        return a.materias_en_comun(b)

    @classmethod
    def estadisticas(cls):
        estudiantes = cls.listar()
        aprobados = sum(e.estado == "Aprobado" for e in estudiantes)
        return {
            "total": len(estudiantes),
            "aprobados": aprobados,
            "reprobados": len(estudiantes) - aprobados,
            "materias": cls.materias_ofertadas()
        }
