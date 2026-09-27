import json
import os

class ArchivoServicio:
    @staticmethod
    def cargar_json(ruta_archivo: str) -> list:
        if not os.path.exists(ruta_archivo):
            return []
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    @staticmethod
    def guardar_json(ruta_archivo: str, datos: list) -> bool:
        try:
            os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
            with open(ruta_archivo, 'w', encoding='utf-8') as file:
                json.dump(datos, file, indent=4, ensure_ascii=False)
            return True
        except OSError:
            return False