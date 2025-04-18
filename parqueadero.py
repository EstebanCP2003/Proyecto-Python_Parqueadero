from datetime import datetime

class RegistroParqueadero:
    def __init__(self):
        self.registros = []

    def agregar_registro(self, nombre, placa, telefono, tipo):
        if not (nombre and placa and telefono):
            raise ValueError("Todos los campos son obligatorios.")
        
        nuevo = {
            "nombre": nombre,
            "placa": placa,
            "telefono": telefono,
            "tipo": tipo,
            "hora_entrada": datetime.now()
        }
        self.registros.append(nuevo)
        return nuevo

    def editar_registro(self, placa_original, nombre, placa, telefono, tipo):
        for r in self.registros:
            if r["placa"] == placa_original:
                r["nombre"] = nombre
                r["placa"] = placa
                r["telefono"] = telefono
                r["tipo"] = tipo
                return r
        raise ValueError("Registro no encontrado para editar.")

    def eliminar_registro(self, placa):
        for r in self.registros:
            if r["placa"] == placa:
                self.registros.remove(r)
                return r
        raise ValueError("Registro no encontrado para eliminar.")

    def buscar_registros(self, query):
        query = query.lower()
        return [
            r for r in self.registros
            if query in r["nombre"].lower() or query in r["placa"].lower()
        ]

    def calcular_pago(self, placa):
        for r in self.registros:
            if r["placa"] == placa:
                hora_salida = datetime.now()
                tiempo = hora_salida - r["hora_entrada"]
                segundos = tiempo.total_seconds()
                horas = int(segundos // 3600)
                minutos = int((segundos % 3600) // 60)

                horas_para_cobro = max(1, int((segundos + 3599) // 3600))

                tarifa = 2000 if "Moto" in r["tipo"] else 2500 if "Carro" in r["tipo"] else 4000
                total = horas_para_cobro * tarifa

                return {
                    "registro": r,
                    "hora_salida": hora_salida,
                    "tiempo": tiempo,
                    "total": total,
                    "tiempo_str": f"{horas} hora(s) y {minutos} minuto(s)"
                }
        raise ValueError("Registro no encontrado para calcular salida.")
