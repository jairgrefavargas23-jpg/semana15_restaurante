class Usuario:
    def __init__(self, username: str, password: str, nombre: str, rol: str):
        self.username = username.strip()
        self.password = password.strip()
        self.nombre = nombre.strip()
        self.rol = rol.strip()

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password,
            "nombre": self.nombre,
            "rol": self.rol
        }

    @staticmethod
    def from_dict(data: dict):
        return Usuario(
            username=data["username"],
            password=data["password"],
            nombre=data["nombre"],
            rol=data.get("rol", "Empleado")
        )