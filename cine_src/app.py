import os

from flask import Flask, jsonify
from mysql.connector import Error as MySQLError

from cine_src.errors import ApiError
from cine_src.routes.servicios import servicios_bp
from cine_src.routes.consumos import consumos_bp


def crear_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY')
    if not app.secret_key:
        raise RuntimeError('Es necesario configurar FLASK_SECRET_KEY')
    app.register_blueprint(servicios_bp, url_prefix='/api')
    app.register_blueprint(consumos_bp, url_prefix='/api')

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
