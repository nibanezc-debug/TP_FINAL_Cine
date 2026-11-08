class ApiError(Exception):

    def __init__(self, mensaje: str, estado: int=400):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.estado = estado
