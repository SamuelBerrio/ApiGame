from flask import Flask, request, jsonify, Response
import time
import cv2
import numpy as np
import os

from threading import Thread
from collections import deque

import cv2
from llama_service import (
    generate_multiple_choice_question,
    generate_true_false_question,
    generate_comparison_question,
    evaluate_response
)
from utils import setup_logging, create_error_response
import logging
import os

from flask_cors import CORS
from camera_service import generate_video, get_current_number
# Configurar logging utilizando la función de utils.py
setup_logging()

# Inicializar la aplicación Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
    
def validate_request(data, required_fields):
    """
    Valida que los campos requeridos estén presentes en la solicitud JSON.

    Args:
        data (dict): Datos de la solicitud JSON.
        required_fields (list): Lista de campos requeridos.

    Returns:
        Tuple[bool, Optional[str]]: Una tupla que contiene un booleano indicando si la validación pasó y un mensaje de error si aplica.
    """
    if not data:
        return False, "Solicitud inválida: JSON no proporcionado."
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Campos requeridos faltantes: {', '.join(missing_fields)}."
    return True, None

@app.route('/generate-true-false', methods=['POST'])
def generate_true_false():
    """
    Endpoint para generar una pregunta de Verdadero/Falso sobre un tema específico.
    """
    data = request.get_json()
    is_valid, error_message = validate_request(data, ['topic'])
    if not is_valid:
        logging.warning(f"Solicitud inválida: {error_message}")
        return create_error_response(error_message, 400)

    topic = data['topic']
    question, correct_answer = generate_true_false_question(topic)

    if not question:
        logging.error("Error al generar la pregunta de Verdadero/Falso.")
        return create_error_response("No se pudo generar la pregunta de Verdadero/Falso.", 500)

    response = {
        'question': question,
        'correct_answer': correct_answer
    }
    return jsonify(response), 200

@app.route('/generate-multiple-choice', methods=['POST'])
def generate_multiple_choice():
    """
    Endpoint para generar una pregunta de opción múltiple con una sola respuesta correcta sobre un tema específico.
    """
    data = request.get_json()
    is_valid, error_message = validate_request(data, ['topic'])
    if not is_valid:
        logging.warning(f"Solicitud inválida: {error_message}")
        return create_error_response(error_message, 400)

    topic = data['topic']
    question, options, correct_option = generate_multiple_choice_question(topic)

    if not question:
        logging.error("Error al generar la pregunta de opción múltiple.")
        return create_error_response("No se pudo generar la pregunta de opción múltiple.", 500)

    response = {
        'question': question,
        'options': {key: value for key, value in options},
        'correct_option': correct_option
    }
    return jsonify(response), 200

@app.route('/generate-comparison', methods=['POST'])
def generate_comparison():
    """
    Endpoint para generar una pregunta de comparación entre dos conceptos específicos dentro de un tema.
    """
    data = request.get_json()
    is_valid, error_message = validate_request(data, ['topic'])
    if not is_valid:
        logging.warning(f"Solicitud inválida: {error_message}")
        return create_error_response(error_message, 400)

    topic = data['topic']
    question, expected_comparison = generate_comparison_question(topic)

    if not question:
        logging.error("Error al generar la pregunta de comparación.")
        return create_error_response("No se pudo generar la pregunta de comparación.", 500)

    response = {
        'question': question,
        'expected_comparison': expected_comparison
    }
    return jsonify(response), 200

@app.route('/evaluate-response', methods=['POST'])
def evaluate_user_response():
    """
    Endpoint para evaluar la respuesta de un usuario comparándola con la respuesta correcta.
    """
    data = request.get_json()
    required_fields = ['user_response', 'topic', 'original_question', 'correct_answer']
    is_valid, error_message = validate_request(data, required_fields)
    if not is_valid:
        logging.warning(f"Solicitud inválida: {error_message}")
        return create_error_response(error_message, 400)

    user_response = data['user_response']
    topic = data['topic']
    original_question = data['original_question']
    correct_answer = data['correct_answer']

    is_correct, explanation = evaluate_response(user_response, topic, original_question, correct_answer)

    if explanation in ["Error al evaluar la respuesta.", "No se pudo evaluar la respuesta."]:
        return create_error_response(explanation, 500)

    response = {
        'is_correct': is_correct,
        'explanation': explanation
    }
    return jsonify(response), 200


@app.route('/video')
def video():
    return Response(generate_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get-score')
def puntaje():
    return jsonify(get_current_number())   


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.errorhandler(404)
def not_found(error):
    """
    Manejador para rutas no encontradas.
    """
    logging.warning(f"Ruta no encontrada: {request.url}")
    return create_error_response("Endpoint no encontrado.", 404)

@app.errorhandler(405)
def method_not_allowed(error):
    """
    Manejador para métodos HTTP no permitidos.
    """
    logging.warning(f"Método no permitido: {request.method} en {request.url}")
    return create_error_response("Método HTTP no permitido.", 405)

@app.errorhandler(500)
def internal_error(error):
    """
    Manejador para errores internos del servidor.
    """
    logging.error(f"Error interno del servidor: {error}")
    return create_error_response("Error interno del servidor.", 500)