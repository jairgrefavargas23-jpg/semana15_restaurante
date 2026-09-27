import os
import tkinter as tk
from tkinter import ttk, messagebox


class LoginView(tk.Toplevel):
    def __init__(self, parent, servicio, on_login_success):
        super().__init__(parent)
        self.parent = parent
        self.servicio = servicio
        self.on_login_success = on_login_success
        self.logo = None

        self.title("Acceso al Sistema - Restaurante App")
        self.geometry("380x380")
        self.resizable(False, False)

        self._crear_interfaz()
        self._centrar()

        # Si cierran el login con la X, se cierra toda la app
        self.protocol("WM_DELETE_WINDOW", self._cerrar_app)

        # Enter para ingresar
        self.bind("<Return>", lambda event: self._ingresar())

        # Asegurar que la ventana se vea antes de tomar el foco exclusivo
        self.lift()
        self.focus_force()
        self.wait_visibility()
        self.grab_set()

    def _crear_interfaz(self):
        container = ttk.Frame(self, padding=20)
        container.pack(fill=tk.BOTH, expand=True)

        logo = self._cargar_logo()
        if logo is not None:
            ttk.Label(container, image=logo).pack(pady=(0, 10))

        lbl_titulo = ttk.Label(container, text="Iniciar Sesión", font=("Helvetica", 14, "bold"))
        lbl_titulo.pack(pady=(0, 15))

        lbl_user = ttk.Label(container, text="Usuario:")
        lbl_user.pack(anchor=tk.W, pady=(5, 0))
        self.txt_user = ttk.Entry(container, width=30)
        self.txt_user.pack(fill=tk.X, pady=(0, 10))
        self.txt_user.focus()

        lbl_pass = ttk.Label(container, text="Contraseña:")
        lbl_pass.pack(anchor=tk.W, pady=(5, 0))
        self.txt_pass = ttk.Entry(container, show="*", width=30)
        self.txt_pass.pack(fill=tk.X, pady=(0, 15))

        btn_ingresar = ttk.Button(container, text="Ingresar", command=self._ingresar)
        btn_ingresar.pack(fill=tk.X)

    def _centrar(self):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"+{x}+{y}")

    def _cargar_logo(self):
        # Carga el logotipo del sistema desde la carpeta assets/.
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_logo = os.path.join(ruta_base, "assets", "logo", "logo.png")

        if not os.path.exists(ruta_logo):
            return None

        self.logo = tk.PhotoImage(file=ruta_logo).subsample(2, 2)
        return self.logo

    def _cerrar_app(self):
        self.parent.destroy()

    def _ingresar(self):
        usuario = self.txt_user.get().strip()
        clave = self.txt_pass.get().strip()

        if not usuario or not clave:
            messagebox.showwarning("Atención", "Por favor ingrese usuario y contraseña.", parent=self)
            return

        user_obj = self.servicio.autenticar(usuario, clave)
        if user_obj:
            self.grab_release()
            self.destroy()
            self.on_login_success(user_obj)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.", parent=self)