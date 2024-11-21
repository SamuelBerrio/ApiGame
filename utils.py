# utils.py

import logging
from flask import jsonify

def setup_logging():
    """
    Configura el sistema de logging con un formato detallado y niveles apropiados.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def create_error_response(message: str, status_code: int = 400):
    """
    Crea una respuesta JSON para errores.

    Args:
        message (str): Mensaje de error.
        status_code (int, opcional): Código de estado HTTP. Por defecto es 400.

    Returns:
        Response: Objeto de respuesta Flask.
    """
    response = jsonify({'error': message})
    response.status_code = status_code
    return response
