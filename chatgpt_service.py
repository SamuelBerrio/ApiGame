# chatgpt_service.py

import os
import logging
import random
from typing import Optional, Tuple, List, Dict
import openai
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

# Configuración básica del logging para registrar información y errores
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Obtener el token de la API de OpenAI de las variables de entorno
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    logging.error("Token de API de OpenAI no encontrado en las variables de entorno.")
    raise EnvironmentError("OPENAI_API_KEY no está configurado.")

# Establecer la clave de API de OpenAI
openai.api_key = OPENAI_API_KEY

# Constante para el nombre del modelo
MODEL_NAME = "gpt-3.5-turbo"  # Puedes usar "gpt-4" si tienes acceso

def call_openai_api(prompt: str, max_tokens: int = 1000) -> Optional[str]:
    """
    Realiza una solicitud a la API de OpenAI y devuelve la respuesta.

    Args:
        prompt (str): El texto del prompt para enviar a la API.
        max_tokens (int, opcional): El número máximo de tokens para la respuesta.

    Returns:
        Optional[str]: La respuesta de la API si tiene éxito, None en caso contrario.
    """
    logging.info(f"Enviando solicitud a la API de OpenAI con max_tokens={max_tokens}.")
    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
            n=1,
            stop=None,
        )
        content = response.choices[0].message['content']
        logging.info("Respuesta recibida de la API de OpenAI.")
        return content.strip()
    except openai.error.OpenAIError as e:
        logging.error(f"Error al conectar con la API de OpenAI: {e}")
    except Exception as e:
        logging.error(f"Error inesperado al llamar a la API de OpenAI: {e}")
    return None

def parse_api_response(content: str, required_keys: List[str]) -> Optional[Dict[str, str]]:
    """
    Parsea la respuesta de la API para extraer claves y valores específicos.

    Args:
        content (str): El contenido de la respuesta de la API.
        required_keys (List[str]): Las claves requeridas para una respuesta válida.

    Returns:
        Optional[Dict[str, str]]: Un diccionario con las claves y valores extraídos si son válidos, None en caso contrario.
    """
    try:
        lines = content.strip().split('\n')
        data = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
            elif ')' in line:
                key, value = line.split(')', 1)
                data[key.strip()] = value.strip()
        if all(key in data for key in required_keys):
            return data
        else:
            missing_keys = [key for key in required_keys if key not in data]
            logging.error(f"Faltan claves en la respuesta de la API: {missing_keys}")
    except Exception as e:
        logging.error(f"Error al parsear la respuesta: {e}")
    return None

def generate_true_false_question(topic: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Genera una pregunta de Verdadero/Falso sobre un tema específico.

    Args:
        topic (str): El tema sobre el cual se generará la pregunta.

    Returns:
        Tuple[Optional[str], Optional[str]]:
            Una tupla que contiene la pregunta y la respuesta correcta ('Verdadero' o 'Falso').
    """
    prompt = (
        f"Eres un experto en diseño educativo. Crea una pregunta de Verdadero/Falso sobre el tema '{topic}'. "
        f"Utiliza el siguiente formato EXACTO, sin variaciones:\n"
        f"Pregunta: [Texto de la pregunta] (Verdadero/Falso)\n"
        f"Respuesta Correcta: [Verdadero o Falso]\n"
        f"Evita explicaciones adicionales y asegúrate de que la pregunta sea clara y adecuada para estudiantes de nivel medio."
    )

    content = call_openai_api(prompt, max_tokens=200)
    if not content:
        logging.error("No se pudo generar la pregunta de Verdadero/Falso.")
        return None, None

    required_keys = ['Pregunta', 'Respuesta Correcta']
    data = parse_api_response(content, required_keys)
    if not data:
        logging.error("Formato de respuesta inválido al generar pregunta de Verdadero/Falso.")
        return None, None

    question = data['Pregunta']
    correct_answer = data['Respuesta Correcta']

    logging.info(f"Pregunta de Verdadero/Falso generada: {question}")
    logging.info(f"Respuesta correcta: {correct_answer}")

    return question, correct_answer

def generate_multiple_choice_question(topic: str) -> Tuple[Optional[str], Optional[List[Tuple[str, str]]], Optional[str]]:
    """
    Genera una pregunta de opción múltiple con una sola respuesta correcta sobre un tema específico.

    Args:
        topic (str): El tema sobre el cual se generará la pregunta.

    Returns:
        Tuple[Optional[str], Optional[List[Tuple[str, str]]], Optional[str]]:
            Una tupla que contiene la pregunta, las opciones y la opción correcta.
    """
    prompt = (
        f"Eres un experto en diseño educativo. Crea una pregunta de opción múltiple con una sola respuesta correcta sobre el tema '{topic}'. "
        f"Utiliza el siguiente formato EXACTO, sin variaciones:\n"
        f"Pregunta: [Texto de la pregunta]\n"
        f"A: [Opción A]\n"
        f"B: [Opción B]\n"
        f"C: [Opción C]\n"
        f"D: [Opción D]\n"
        f"Respuesta Correcta: [Letra de la opción correcta]\n"
        f"Evita explicaciones adicionales y asegúrate de que la pregunta sea clara y adecuada para estudiantes de nivel medio."
    )

    content = call_openai_api(prompt, max_tokens=250)
    if not content:
        logging.error("No se pudo generar la pregunta de opción múltiple.")
        return None, None, None

    required_keys = ['Pregunta', 'A', 'B', 'C', 'D', 'Respuesta Correcta']
    data = parse_api_response(content, required_keys)
    if not data:
        logging.error("Formato de respuesta inválido al generar pregunta de opción múltiple.")
        return None, None, None

    question = data['Pregunta']
    options = [('A', data['A']), ('B', data['B']), ('C', data['C']), ('D', data['D'])]
    correct_option = data['Respuesta Correcta']

    logging.info(f"Pregunta de Opción Múltiple generada: {question}")
    logging.info(f"Opciones: {options}")
    logging.info(f"Opción correcta: {correct_option}")

    return question, options, correct_option

def generate_comparison_question(topic: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Genera una pregunta de comparación entre dos conceptos específicos dentro de un tema.

    Args:
        topic (str): El tema sobre el cual se generará la pregunta de comparación.

    Returns:
        Tuple[Optional[str], Optional[str]]:
            Una tupla que contiene la pregunta de comparación y la respuesta esperada.
    """
    prompt = (
        f"Eres un experto en diseño educativo especializado en preguntas de comparación. "
        f"Crea una pregunta de comparación sobre el tema '{topic}' utilizando el siguiente formato EXACTO, sin variaciones:\n"
        f"Pregunta: [Texto de la pregunta de comparación]\n"
        f"Respuesta Esperada: [Respuesta detallada comparando los dos conceptos]\n"
        f"Evita explicaciones adicionales y asegúrate de que la pregunta sea clara y adecuada para estudiantes de nivel medio, solicitando la comparación entre dos conceptos clave dentro del tema."
    )

    content = call_openai_api(prompt, max_tokens=500)
    if not content:
        logging.error("No se pudo generar la pregunta de comparación.")
        return None, None

    required_keys = ['Pregunta', 'Respuesta Esperada']
    data = parse_api_response(content, required_keys)
    if not data:
        logging.error("Formato de respuesta inválido al generar pregunta de comparación.")
        return None, None

    question = data['Pregunta']
    expected_comparison = data['Respuesta Esperada']

    logging.info(f"Pregunta de Comparación generada: {question}")
    logging.info(f"Respuesta esperada: {expected_comparison}")

    return question, expected_comparison

def evaluate_response(user_response: str, topic: str, original_question: str) -> Tuple[bool, str]:
    """
    Evalúa la respuesta del usuario comparándola con el concepto del tema.

    Args:
        user_response (str): La respuesta proporcionada por el usuario.
        topic (str): El tema relacionado con la pregunta.
        original_question (str): La pregunta original que se le hizo al usuario.

    Returns:
        Tuple[bool, str]:
            Una tupla que contiene un booleano indicando si es correcta y una explicación.
    """
    prompt = (
        f"Eres un evaluador educativo experto. Evalúa la siguiente respuesta proporcionada por un estudiante en relación con la pregunta original.\n"
        f"Pregunta: {original_question}\n"
        f"Respuesta del Estudiante: {user_response}\n"
        f"Tema: {topic}\n"
        f"Proporciona la evaluación en el siguiente formato EXACTO, sin variaciones:\n"
        f"Evaluación: [Correcta/Incorrecta]\n"
        f"Explicación: [Explicación clara y detallada sobre por qué la respuesta es correcta o incorrecta, incluyendo recomendaciones o correcciones si aplica]\n"
        f"Evita cualquier texto adicional fuera del formato especificado."
    )

    content = call_openai_api(prompt, max_tokens=500)
    if not content:
        logging.error("No se pudo evaluar la respuesta.")
        return False, "Error al evaluar la respuesta."

    required_keys = ['Evaluación', 'Explicación']
    data = parse_api_response(content, required_keys)
    if not data:
        logging.error("Formato de evaluación inválido.")
        return False, "No se pudo evaluar la respuesta."

    evaluation = data['Evaluación']
    explanation = data.get('Explicación', '')

    is_correct = evaluation.lower() == 'correcta'

    # Agregar mensajes de felicitación o explicación adicional
    if is_correct:
        feedback = f"¡Felicidades! {explanation}"
    else:
        feedback = f"{explanation}"

    logging.info(f"Evaluación: {evaluation}")
    logging.info(f"Explicación: {explanation}")

    return is_correct, feedback
