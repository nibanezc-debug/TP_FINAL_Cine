import os

from flask import Flask, jsonify
from mysql.connector import Error as MySQLError

from errors import ApiError
from routes.servicios import servicios_bp
from routes.consumos import consumos_bp
from routes.locales import locales_bp
from routes.salas import salas_bp
from routes.butacas import butacas_bp
from routes.peliculas import peliculas_bp
from routes.usuarios import usuarios_bp
from routes.funciones import funciones_bp
from routes.entradas import entradas_bp

def crear_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY')
    if not app.secret_key:
        raise RuntimeError('Es necesario configurar FLASK_SECRET_KEY')
    app.register_blueprint(servicios_bp, url_prefix='/api')
    app.register_blueprint(consumos_bp, url_prefix='/api')
    app.register_blueprint(locales_bp, url_prefix='/api')
    app.register_blueprint(salas_bp, url_prefix='/api')
    app.register_blueprint(butacas_bp, url_prefix='/api')
    app.register_blueprint(peliculas_bp, url_prefix='/api')
    app.register_blueprint(usuarios_bp, url_prefix='/api')
    app.register_blueprint(funciones_bp, url_prefix="/api")
    app.register_blueprint(entradas_bp, url_prefix='/api')

    @app.errorhandler(ApiError)
    def manejar_error(error):
        return jsonify({'error': error.mensaje}), error.estado

    @app.errorhandler(MySQLError)
    def manejar_error_db(error):
        app.logger.error('Error de base de datos: %s', type(error).__name__)
        return jsonify({'error': 'No se pudo acceder a la base de datos'}), 503

    return app


if __name__ == '__main__':
    crear_app().run(host='127.0.0.1', port=5000)
