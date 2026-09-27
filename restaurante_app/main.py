import os
import tkinter as tk
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Restaurante App - Sistema de Gestión")
        self.geometry("850x550")
        self.minsize(800, 500)
        self._configurar_icono()

        self.servicio = RestauranteServicio()
        self.withdraw()  # Ocultar ventana principal hasta autenticar

        # Abrir Login
        LoginView(self, self.servicio, self._al_autenticar_exito)

    def _configurar_icono(self):
        # Usa el logotipo de assets/ como icono de la ventana principal.
        ruta_icono = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "assets", "logo", "icono.png"
        )
        if not os.path.exists(ruta_icono):
            return
        try:
            self.icono_app = tk.PhotoImage(file=ruta_icono)
            self.iconphoto(True, self.icono_app)
        except tk.TclError:
            pass

    def _al_autenticar_exito(self, usuario):
        # Mostrar de nuevo la ventana principal
        self.deiconify()
        self.lift()
        self.focus_force()

        # MainView recibe: (parent, usuario_actual, servicio)
        MainView(self, usuario, self.servicio)


if __name__ == "__main__":
    app = App()
    app.mainloop()