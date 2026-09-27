class Venta:
    def __init__(self, id_venta: str, username_cliente: str, id_producto: str, fecha: str):
        self.id_venta = str(id_venta).strip()
        self.username_cliente = str(username_cliente).strip()
        self.id_producto = str(id_producto).strip()
        self.fecha = str(fecha).strip()

    def to_dict(self) -> dict:
        return {
            "id_venta": self.id_venta,
            "username_cliente": self.username_cliente,
            "id_producto": self.id_producto,
            "fecha": self.fecha
        }

    @staticmethod
    def from_dict(data: dict):
        return Venta(
            id_venta=data["id_venta"],
            username_cliente=data.get("username_cliente", ""),
            id_producto=data.get("id_producto", ""),
            fecha=data.get("fecha", "")
        )
