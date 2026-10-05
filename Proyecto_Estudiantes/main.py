"""Interfaz principal del proyecto de gestión de estudiantes."""

from shared.herramientas import encabezado, exito, error, aviso, confirmar, esperar
from views import EstudianteController


class AplicacionEstudiantes:
    def __init__(self):
        self.controlador = EstudianteController
        self.ejecutando = True

    @staticmethod
    def entero(mensaje):
        try:
            return int(input(mensaje))
        except ValueError:
            return None

    @staticmethod
    def decimal(mensaje):
        try:
            return float(input(mensaje))
        except ValueError:
            return None

    def resultado(self, estado, mensaje):
        (exito if estado else error)(mensaje)

    def menu(self):
        encabezado("PORTAL ACADÉMICO | GESTIÓN DE ESTUDIANTES")
        opciones = [
            ("1", "Registrar estudiante"),
            ("2", "Mostrar estudiantes"),
            ("3", "Buscar estudiante"),
            ("4", "Consultar ficha"),
            ("5", "Editar estudiante"),
            ("6", "Eliminar estudiante"),
            ("7", "Registrar calificación"),
            ("8", "Consultar promedio"),
            ("9", "Comparar materias"),
            ("A", "Resumen estadístico"),
            ("0", "Cerrar programa"),
        ]
        for clave, texto in opciones:
            print(f" [{clave}] {texto}")
        print()

    def registrar(self):
        encabezado("NUEVO ESTUDIANTE")
        datos = {}
        for campo in self.controlador.MODELO.CAMPOS:
            datos[campo] = input(f"{campo.capitalize()}: ").strip()
        self.resultado(*self.controlador.crear(datos))
        esperar()

    def mostrar(self):
        encabezado("ESTUDIANTES REGISTRADOS")
        lista = self.controlador.listar()
        if not lista:
            aviso("No hay estudiantes registrados.")
        else:
            print(f"{'ID':<5}{'CARNET':<14}{'ESTUDIANTE':<28}{'PROM.':<8}{'ESTADO'}")
            print("-" * 70)
            for e in lista:
                print(f"{e.id:<5}{e.carnet:<14}{e.nombre_completo:<28}{e.promedio:<8.2f}{e.estado}")
            print("-" * 70)
            print(f"Total: {len(lista)}")
        esperar()

    def buscar(self):
        encabezado("BÚSQUEDA")
        termino = input("Nombre, apellido, correo o carnet: ")
        resultados = self.controlador.buscar(termino)
        if resultados:
            for e in resultados:
                print(f"{e.id}. {e}")
        else:
            aviso("No se encontraron coincidencias.")
        esperar()

    def ficha(self):
        encabezado("FICHA DEL ESTUDIANTE")
        identificador = self.entero("ID: ")
        estudiante = self.controlador.obtener(identificador) if identificador is not None else None
        if estudiante is None:
            error("ID no válido o estudiante inexistente.")
        else:
            print(f"Nombre:     {estudiante.nombre_completo}")
            print(f"Correo:     {estudiante.email}")
            print(f"Carnet:     {estudiante.carnet}")
            print(f"Materias:   {', '.join(sorted(estudiante.materias)) or 'Ninguna'}")
            print(f"Promedio:   {estudiante.promedio:.2f}")
            print(f"Estado:     {estudiante.estado}")
            print("Notas:")
            for materia in sorted(estudiante.materias):
                print(f"  - {materia}: {estudiante.notas_de(materia)}")
        esperar()

    def editar(self):
        encabezado("ACTUALIZAR DATOS")
        identificador = self.entero("ID del estudiante: ")
        estudiante = self.controlador.obtener(identificador) if identificador is not None else None
        if estudiante is None:
            error("Estudiante no encontrado.")
            esperar()
            return

        print("Deje vacío un campo para conservar su valor.")
        cambios = {}
        for campo in self.controlador.MODELO.CAMPOS:
            actual = getattr(estudiante, campo)
            nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
            if nuevo:
                cambios[campo] = nuevo

        self.resultado(*self.controlador.actualizar(identificador, cambios))
        esperar()

    def eliminar(self):
        encabezado("ELIMINAR ESTUDIANTE")
        identificador = self.entero("ID: ")
        estudiante = self.controlador.obtener(identificador) if identificador is not None else None
        if estudiante is None:
            error("Estudiante no encontrado.")
        elif confirmar(f"¿Eliminar a {estudiante.nombre_completo}?"):
            self.resultado(*self.controlador.eliminar(identificador))
        else:
            aviso("Operación cancelada.")
        esperar()

    def registrar_nota(self):
        encabezado("NUEVA CALIFICACIÓN")
        identificador = self.entero("ID del estudiante: ")
        if identificador is None:
            error("El ID debe ser entero.")
            esperar()
            return
        materia = input("Materia: ").strip()
        nota = self.decimal("Nota (0-20): ")
        if nota is None:
            error("La nota debe ser numérica.")
        else:
            self.resultado(*self.controlador.agregar_nota(identificador, materia, nota))
        esperar()

    def promedio(self):
        encabezado("CONSULTA DE PROMEDIO")
        identificador = self.entero("ID: ")
        estudiante = self.controlador.obtener(identificador) if identificador is not None else None
        if estudiante:
            print(f"Estudiante: {estudiante.nombre_completo}")
            print(f"Promedio:   {estudiante.promedio:.2f}")
            print(f"Estado:     {estudiante.estado}")
        else:
            error("Estudiante no encontrado.")
        esperar()

    def comparar(self):
        encabezado("MATERIAS COMPARTIDAS")
        a = self.entero("Primer ID: ")
        b = self.entero("Segundo ID: ")
        if a is None or b is None:
            error("Los IDs deben ser números enteros.")
        else:
            comunes = self.controlador.materias_en_comun(a, b)
            if comunes is None:
                error("Uno de los estudiantes no existe.")
            elif comunes:
                exito("Materias en común: " + ", ".join(sorted(comunes)))
            else:
                aviso("No tienen materias en común.")
        esperar()

    def estadisticas(self):
        encabezado("RESUMEN ACADÉMICO")
        datos = self.controlador.estadisticas()
        print(f"Estudiantes: {datos['total']}")
        print(f"Aprobados:   {datos['aprobados']}")
        print(f"Reprobados:  {datos['reprobados']}")
        print(f"Materias:    {', '.join(datos['materias']) or 'Ninguna'}")
        esperar()

    def ejecutar(self):
        acciones = {
            "1": self.registrar, "2": self.mostrar, "3": self.buscar,
            "4": self.ficha, "5": self.editar, "6": self.eliminar,
            "7": self.registrar_nota, "8": self.promedio,
            "9": self.comparar, "A": self.estadisticas
        }
        while self.ejecutando:
            self.menu()
            opcion = input("Seleccione una opción: ").strip().upper()
            if opcion == "0":
                self.ejecutando = False
                aviso("Programa cerrado. ¡Hasta luego!")
            elif opcion in acciones:
                acciones[opcion]()
            else:
                error("Opción no reconocida.")
                esperar()


if __name__ == "__main__":
    try:
        AplicacionEstudiantes().ejecutar()
    except KeyboardInterrupt:
        print("\nPrograma detenido por el usuario.")
