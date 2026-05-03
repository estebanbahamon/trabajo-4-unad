#grupo 287

from abc import ABC, abstractmethod
from datetime import datetime

# -------------------------
# 1. REGISTRO DE LOGS
# -------------------------
def guardar_log(mensaje):
    """Guarda eventos y errores en logs.txt con marca de tiempo."""
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {mensaje}\n")

# -------------------------
# 2. EXCEPCIONES PERSONALIZADAS
# -------------------------
class ErrorSistema(Exception):
    """Excepción para errores controlados del negocio."""
    pass

# -------------------------
# 3. ABSTRACCIÓN Y ENCAPSULAMIENTO
# -------------------------
class Entidad(ABC):
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def mostrar(self):
        pass

class Cliente(Entidad):
    def __init__(self, id, nombre, documento):
        super().__init__(id)
        # El uso de los setters asegura validación desde la creación
        self.nombre = nombre
        self.documento = documento

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor.strip():
            raise ErrorSistema("Validación: El nombre no puede estar vacío.")
        self.__nombre = valor

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if not valor.isdigit():
            raise ErrorSistema("Validación: El documento debe ser numérico.")
        self.__documento = valor

    def mostrar(self):
        return f"ID: {self.id} | Cliente: {self.nombre} | Doc: {self.documento}"

# -------------------------
# 4. POLIMORFISMO (SERVICIOS)
# -------------------------
class Servicio(ABC):
    def __init__(self, tipo, precio_base):
        self.tipo = tipo
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, **kwargs):
        pass

    @abstractmethod
    def descripcion(self):
        pass

class ReservaSala(Servicio):
    def __init__(self, horas):
        super().__init__("Reserva de Sala", 50000)
        self.horas = horas

    def calcular_costo(self, descuento=0):
        if self.horas <= 0: raise ErrorSistema("Horas de sala inválidas.")
        total = self.precio_base * self.horas
        return total * (1 - descuento)

    def descripcion(self):
        return f"{self.tipo} por {self.horas} horas"

class AlquilerEquipo(Servicio):
    def __init__(self, dias):
        super().__init__("Alquiler de Equipo", 30000)
        self.dias = dias

    def calcular_costo(self, impuesto=0.19):
        if self.dias <= 0: raise ErrorSistema("Días de alquiler inválidos.")
        total = self.precio_base * self.dias
        return total * (1 + impuesto)

    def descripcion(self):
        return f"{self.tipo} por {self.dias} días"

class Asesoria(Servicio):
    def __init__(self, nivel):
        super().__init__("Asesoría", 80000)
        self.nivel = nivel # 'basica' o 'especializada'

    def calcular_costo(self):
        if self.nivel == "especializada":
            return self.precio_base * 1.5
        return self.precio_base

    def descripcion(self):
        return f"{self.tipo} Nivel: {self.nivel}"

# -------------------------
# 5. GESTIÓN DE RESERVAS (TRY/EXCEPT/ELSE/FINALLY)
# -------------------------
class Reserva:
    def __init__(self, cliente, servicio):
        if not isinstance(cliente, Cliente):
            raise ErrorSistema("La reserva requiere un cliente válido.")
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "pendiente"

    def confirmar(self):
        self.estado = "confirmada"
        guardar_log(f"Reserva confirmada para {self.cliente.nombre}")

    def procesar_pago(self):
        try:
            print(f"--- Procesando pago para: {self.cliente.nombre} ---")
            if self.estado != "confirmada":
                raise ErrorSistema("No se puede pagar una reserva pendiente.")
            
            total = self.servicio.calcular_costo()
            
        except ErrorSistema as e:
            guardar_log(f"ERROR EN PAGO: {e}")
            print(f"Error detectado: {e}")
        else:
            # Solo se ejecuta si no hubo excepciones
            mensaje = f"Pago exitoso: ${total:.2f} por {self.servicio.descripcion()}"
            guardar_log(mensaje)
            print(mensaje)
            self.estado = "pagada"
        finally:
            # Se ejecuta siempre (limpieza o cierre)
            print("Finalizando ciclo de transacción.\n")

# -------------------------
# 6. SIMULACIÓN DE 10 OPERACIONES (ANEXO 3)
# -------------------------
if __name__ == "__main__":
    print("=== SISTEMA SOFTWARE FJ - FASE 4 ===\n")
    
    # Lista para guardar clientes exitosos
    clientes = []

    # OPERACIÓN 1: Registro válido
    try:
        c1 = Cliente(1, "Esteban Bahamon", "1075123")
        clientes.append(c1)
        print("Op 1: Cliente creado con éxito.")
    except ErrorSistema as e: print(e)

    # OPERACIÓN 2: Registro inválido (Nombre vacío)
    try:
        c2 = Cliente(2, "", "999")
    except ErrorSistema as e:
        guardar_log(e)
        print(f"Op 2: Error controlado -> {e}")

    # OPERACIÓN 3: Registro inválido (Doc no numérico)
    try:
        c3 = Cliente(3, "Juan", "ABC123")
    except ErrorSistema as e:
        guardar_log(e)
        print(f"Op 3: Error controlado -> {e}")

    # OPERACIÓN 4: Crear servicio Sala (Bien)
    s1 = ReservaSala(3)
    print("Op 4: Servicio de sala creado.")

    # OPERACIÓN 5: Crear servicio Equipo (Días inválidos)
    try:
        s2 = AlquilerEquipo(-1)
        s2.calcular_costo()
    except ErrorSistema as e:
        guardar_log(e)
        print(f"Op 5: Error en parámetros de servicio -> {e}")

    # OPERACIÓN 6: Crear Reserva Exitosa
    reserva1 = Reserva(clientes[0], s1)
    reserva1.confirmar()
    reserva1.procesar_pago() # Op 6

    # OPERACIÓN 7: Intentar pagar sin confirmar
    s3 = Asesoria("basica")
    reserva2 = Reserva(clientes[0], s3)
    print("Op 7: Intento de pago sin confirmar...")
    reserva2.procesar_pago() 

    # OPERACIÓN 8: Servicio con Polimorfismo (Asesoría Especializada)
    s4 = Asesoria("especializada")
    reserva3 = Reserva(clientes[0], s4)
    reserva3.confirmar()
    reserva3.procesar_pago() # Op 8

    # OPERACIÓN 9: Cálculo con método sobrecargado (Descuento en Sala)
    print(f"Op 9: Costo sala con descuento: ${s1.calcular_costo(descuento=0.1)}")

    # OPERACIÓN 10: Validación de objeto cliente en reserva
    try:
        reserva_fallida = Reserva("No Soy Un Objeto", s1)
    except ErrorSistema as e:
        guardar_log(e)
        print(f"Op 10: Error de integridad -> {e}")

    print("\n=== Simulación terminada. Revisa 'logs.txt' para el historial. ===")