import unittest
from parqueadero import RegistroParqueadero
from datetime import datetime, timedelta

class TestRegistroParqueadero(unittest.TestCase):

    def setUp(self):
        self.parqueadero = RegistroParqueadero()

    def test_1_agregar_registro_valido(self):
        print("Test 1: Agregar registro válido")
        r = self.parqueadero.agregar_registro("Juan", "ABC123", "3001234567", "Moto - $2000")
        self.assertEqual(r["nombre"], "Juan")

    def test_2_agregar_registro_faltante(self):
        print("Test 2: Agregar registro con campos faltantes")
        with self.assertRaises(ValueError):
            self.parqueadero.agregar_registro("", "XYZ789", "3009876543", "Carro - $2500")

    def test_3_buscar_por_nombre(self):
        print("Test 3: Buscar por nombre")
        self.parqueadero.agregar_registro("María", "XYZ789", "3009876543", "Carro - $2500")
        resultados = self.parqueadero.buscar_registros("maría")
        self.assertTrue(len(resultados) > 0)

    def test_4_buscar_por_placa(self):
        print("Test 4: Buscar por placa")
        self.parqueadero.agregar_registro("Carlos", "MNO456", "3110000000", "Carro - $2500")
        resultados = self.parqueadero.buscar_registros("mno")
        self.assertTrue(len(resultados) > 0)

    def test_5_editar_registro_existente(self):
        print("Test 5: Editar registro existente")
        self.parqueadero.agregar_registro("Ana", "DEF789", "3123456789", "Moto - $2000")
        editado = self.parqueadero.editar_registro("DEF789", "Ana María", "DEF789", "3123456789", "Carro - $2500")
        self.assertEqual(editado["nombre"], "Ana María")

    def test_6_editar_registro_inexistente(self):
        print("Test 6: Editar registro inexistente")
        with self.assertRaises(ValueError):
            self.parqueadero.editar_registro("XXX000", "Luis", "XXX000", "3000000000", "Moto - $2000")

    def test_7_eliminar_registro_existente(self):
        print("Test 7: Eliminar registro existente")
        self.parqueadero.agregar_registro("Pedro", "AAA111", "3222222222", "Carro - $2500")
        eliminado = self.parqueadero.eliminar_registro("AAA111")
        self.assertEqual(eliminado["placa"], "AAA111")

    def test_8_eliminar_registro_inexistente(self):
        print("Test 8: Eliminar registro inexistente")
        with self.assertRaises(ValueError):
            self.parqueadero.eliminar_registro("NOPE000")

    def test_9_calcular_pago_valido(self):
        print("Test 9: Calcular pago válido")
        self.parqueadero.agregar_registro("Laura", "LMN456", "3011111111", "Grande - $4000")
        resultado = self.parqueadero.calcular_pago("LMN456")
        self.assertIn("total", resultado)

    def test_10_calcular_pago_inexistente(self):
        print("Test 10: Calcular pago inexistente")
        with self.assertRaises(ValueError):
            self.parqueadero.calcular_pago("ZZZ999")

    def test_11_pago_minimo_una_hora(self):
        print("Test 11: Pago mínimo de una hora")
        self.parqueadero.agregar_registro("Mateo", "CDE111", "3003003000", "Moto - $2000")
        for r in self.parqueadero.registros:
            if r["placa"] == "CDE111":
                r["hora_entrada"] = datetime.now() - timedelta(minutes=5)
        salida = self.parqueadero.calcular_pago("CDE111")
        self.assertEqual(salida["total"], 2000)

    def test_12_formato_tiempo_salida(self):
        print("Test 12: Formato del tiempo de salida")
        self.parqueadero.agregar_registro("Lina", "PQR123", "3000000000", "Moto - $2000")
        salida = self.parqueadero.calcular_pago("PQR123")
        self.assertIn("tiempo_str", salida)

    def test_13_buscar_registro_eliminado(self):
        print("Test 13: Buscar registro eliminado")
        self.parqueadero.agregar_registro("David", "OUT999", "3100000000", "Carro - $2500")
        self.parqueadero.eliminar_registro("OUT999")
        resultados = self.parqueadero.buscar_registros("OUT999")
        self.assertEqual(len(resultados), 0)

    def test_14_verificar_edicion(self):
        print("Test 14: Verificar edición de registro")
        self.parqueadero.agregar_registro("Luis", "XYZ123", "3001111111", "Moto - $2000")
        self.parqueadero.editar_registro("XYZ123", "Luis Carlos", "XYZ123", "3001111111", "Carro - $2500")
        r = [r for r in self.parqueadero.registros if r["placa"] == "XYZ123"][0]
        self.assertEqual(r["nombre"], "Luis Carlos")

    def test_15_agregar_multiples(self):
        print("Test 15: Agregar múltiples registros")
        self.parqueadero.agregar_registro("Persona1", "A001", "3000000001", "Moto - $2000")
        self.parqueadero.agregar_registro("Persona2", "A002", "3000000002", "Carro - $2500")
        self.parqueadero.agregar_registro("Persona3", "A003", "3000000003", "Grande - $4000")
        self.assertGreaterEqual(len(self.parqueadero.registros), 3)


if __name__ == '__main__':
    print("EJECUTANDO 15 CASOS DE PRUEBA...\n")
    unittest.main(verbosity=2)
