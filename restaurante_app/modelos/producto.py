class Producto:
    def __init__(self, id_producto: str, nombre: str, categoria: str, precio: float, disponible: bool = True):
        self.id_producto = str(id_producto).strip()
        self.nombre = nombre.strip()
        self.categoria = categoria.strip()
        self.precio = float(precio)
        self.disponible = disponible

    def to_dict(self) -> dict:
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "disponible": self.disponible
        }

    @staticmethod
    def from_dict(data: dict):
        return Producto(
            id_producto=data["id_producto"],
            nombre=data["nombre"],
            categoria=data["categoria"],
            precio=data["precio"],
            disponible=data.get("disponible", True)
        )