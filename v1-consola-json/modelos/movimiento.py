from datetime import datetime

class Movimiento:
    
    def __init__(self, tipo, cantidad, categoria, fecha=None):
        self.tipo = tipo
        self.cantidad = cantidad
        self.categoria = categoria
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")
    

    def to_dict(self):
        return {
            "tipo": self.tipo,
            "cantidad": self.cantidad,
            "categoria": self.categoria,
            "fecha": self.fecha
        }



