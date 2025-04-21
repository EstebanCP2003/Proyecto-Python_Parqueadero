import customtkinter as ctk
from tkinter import ttk, messagebox as msgbox
from parqueadero import RegistroParqueadero

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Parqueadero")
        self.geometry("1000x600")
        self.parqueadero = RegistroParqueadero()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_formulario()
        self.crear_tabla()

    def crear_formulario(self):
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

        self.input_nombre = self.agregar_campo("Nombre:")
        self.input_placa = self.agregar_campo("Placa:")
        self.input_telefono = self.agregar_campo("Teléfono:")

        ctk.CTkLabel(self.form_frame, text="Tipo de Vehículo:").pack(pady=(10, 0))
        self.tipo_vehiculo = ctk.CTkComboBox(self.form_frame, values=["Moto - $2000", "Carro - $2500", "Grande - $4000"])
        self.tipo_vehiculo.pack(pady=5)
        self.tipo_vehiculo.set("Moto - $2000")

        self.boton_guardar = ctk.CTkButton(self.form_frame, text="Guardar ingreso", command=self.guardar_ingreso)
        self.boton_guardar.pack(pady=(15, 5))

    def crear_tabla(self):
        self.tabla_frame = ctk.CTkFrame(self)
        self.tabla_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.tabla_frame.grid_rowconfigure(1, weight=1)
        self.tabla_frame.grid_columnconfigure(0, weight=1)

        self.input_busqueda = ctk.CTkEntry(self.tabla_frame, placeholder_text="Buscar por nombre o placa")
        self.input_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.boton_buscar = ctk.CTkButton(self.tabla_frame, text="Buscar", command=self.buscar_registro)
        self.boton_buscar.grid(row=0, column=1, padx=10, pady=10)

        columnas = ("Nombre", "Placa", "Teléfono", "Tipo", "Hora de entrada")
        self.tree = ttk.Treeview(self.tabla_frame, columns=columnas, show="headings")
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.grid(row=1, column=0, columnspan=2, sticky="nsew")

        botones_frame = ctk.CTkFrame(self.tabla_frame)
        botones_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        botones_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(botones_frame, text="Calcular salida", command=self.calcular_salida).grid(row=0, column=0, padx=10, sticky="ew")
        ctk.CTkButton(botones_frame, text="Editar entrada", command=self.editar_registro).grid(row=0, column=1, padx=10, sticky="ew")
        ctk.CTkButton(botones_frame, text="Eliminar entrada", fg_color="red", hover_color="#cc0000", command=self.eliminar_registro).grid(row=0, column=2, padx=10, sticky="ew")

    def agregar_campo(self, texto):
        ctk.CTkLabel(self.form_frame, text=texto).pack(pady=(10, 0))
        campo = ctk.CTkEntry(self.form_frame)
        campo.pack(pady=5)
        return campo

    def guardar_ingreso(self):
        try:
            nombre = self.input_nombre.get()
            placa = self.input_placa.get()
            telefono = self.input_telefono.get()
            tipo = self.tipo_vehiculo.get()

            if hasattr(self, "edicion_en_proceso") and self.edicion_en_proceso:
                self.parqueadero.editar_registro(self.placa_original, nombre, placa, telefono, tipo)
                msgbox.showinfo("Actualizado", "Registro actualizado.")
                self.edicion_en_proceso = False
                self.boton_guardar.configure(text="Guardar ingreso")
            else:
                self.parqueadero.agregar_registro(nombre, placa, telefono, tipo)

            self.refrescar_tabla()
            self.limpiar_campos()

        except ValueError as e:
            msgbox.showwarning("Error", str(e))

    def buscar_registro(self):
        query = self.input_busqueda.get()
        resultados = self.parqueadero.buscar_registros(query)
        self.mostrar_en_tabla(resultados)

    def calcular_salida(self):
        seleccion = self.tree.selection()
        if not seleccion:
            msgbox.showwarning("Selecciona un registro", "Selecciona un registro para calcular.")
            return
        placa = self.tree.item(seleccion)["values"][1]
        try:
            data = self.parqueadero.calcular_pago(placa)
            r = data["registro"]
            msgbox.showinfo("Salida",
                f"Nombre: {r['nombre']}\nPlaca: {r['placa']}\nTeléfono: {r['telefono']}\n"
                f"Tipo: {r['tipo']}\nEntrada: {r['hora_entrada'].strftime('%H:%M:%S')}\n"
                f"Salida: {data['hora_salida'].strftime('%H:%M:%S')}\n"
                f"Tiempo: {data['tiempo_str']}\nTotal a pagar: ${data['total']:,}")
        except ValueError as e:
            msgbox.showwarning("Error", str(e))

    def editar_registro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            msgbox.showwarning("Selecciona un registro", "Selecciona un registro para editar.")
            return
        valores = self.tree.item(seleccion)["values"]
        self.input_nombre.delete(0, 'end')
        self.input_placa.delete(0, 'end')
        self.input_telefono.delete(0, 'end')
        self.input_nombre.insert(0, valores[0])
        self.input_placa.insert(0, valores[1])
        self.input_telefono.insert(0, valores[2])
        self.tipo_vehiculo.set(valores[3])
        self.edicion_en_proceso = True
        self.placa_original = valores[1]
        self.boton_guardar.configure(text="Actualizar")

    def eliminar_registro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            msgbox.showwarning("Selecciona un registro", "Selecciona un registro para eliminar.")
            return
        placa = self.tree.item(seleccion)["values"][1]
        confirm = msgbox.askyesno("Confirmar", f"¿Eliminar la placa {placa}?")
        if confirm:
            try:
                self.parqueadero.eliminar_registro(placa)
                self.refrescar_tabla()
                msgbox.showinfo("Eliminado", "Registro eliminado.")
            except ValueError as e:
                msgbox.showwarning("Error", str(e))

    def refrescar_tabla(self):
        self.mostrar_en_tabla(self.parqueadero.registros)

    def mostrar_en_tabla(self, lista):
        self.tree.delete(*self.tree.get_children())
        for r in lista:
            self.tree.insert("", "end", values=(r["nombre"], r["placa"], r["telefono"], r["tipo"], r["hora_entrada"].strftime("%H:%M:%S")))

    def limpiar_campos(self):
        self.input_nombre.delete(0, 'end')
        self.input_placa.delete(0, 'end')
        self.input_telefono.delete(0, 'end')

if __name__ == "__main__":
    app = App()
    app.mainloop()
