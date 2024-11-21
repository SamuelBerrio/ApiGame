# test.py

import sys
from llama_service import (
    generate_true_false_question,
    generate_multiple_choice_question,
    generate_comparison_question,
    evaluate_response
)

def print_menu():
    print("\n===== Generador y Evaluador de Preguntas =====")
    print("Seleccione el tipo de pregunta que desea generar:")
    print("1. Verdadero/Falso")
    print("2. Opción Múltiple")
    print("3. Comparación")
    print("4. Salir")

def get_topic():
    topic = input("Ingrese el tema para la pregunta: ").strip()
    return topic

def handle_true_false():
    topic = get_topic()
    question, correct_answer = generate_true_false_question(topic)
    if question and correct_answer is not None:
        print(f"\nPregunta (Verdadero/Falso):\n{question}")
        user_response = input("Ingrese su respuesta (Verdadero/Falso): ").strip().capitalize()
        is_correct, feedback = evaluate_response(user_response, topic, question, correct_answer)
        print(f"Evaluación: {'Correcta' if is_correct else 'Incorrecta'}")
        print(f"Comentarios: {feedback}")
    else:
        print("Error al generar la pregunta de Verdadero/Falso.")

def handle_multiple_choice():
    topic = get_topic()
    question, options, correct_option = generate_multiple_choice_question(topic)
    if question and options and correct_option:
        print(f"\nPregunta (Opción Múltiple):\n{question}")
        for opt in options:
            print(f"{opt[0]}. {opt[1]}")
        user_response = input("Ingrese la letra de la respuesta correcta (A/B/C/D): ").strip().upper()
        is_correct, feedback = evaluate_response(user_response, topic, question, correct_option)
        print(f"Evaluación: {'Correcta' if is_correct else 'Incorrecta'}")
        print(f"Comentarios: {feedback}")
    else:
        print("Error al generar la pregunta de Opción Múltiple.")

def handle_comparison():
    topic = get_topic()
    question, expected_comparison = generate_comparison_question(topic)
    if question and expected_comparison:
        print(f"\nPregunta de Comparación:\n{question}")
        user_response = input("Ingrese su respuesta: ").strip()
        is_correct, feedback = evaluate_response(user_response, topic, question, expected_comparison)
        print(f"Evaluación: {'Correcta' if is_correct else 'Incorrecta'}")
        print(f"Comentarios: {feedback}")
    else:
        print("Error al generar la pregunta de Comparación.")

def main():
    while True:
        print_menu()
        choice = input("Ingrese el número de su elección: ").strip()
        
        if choice == '1':
            handle_true_false()
        elif choice == '2':
            handle_multiple_choice()
        elif choice == '3':
            handle_comparison()
        elif choice == '4':
            print("Saliendo del generador de preguntas. ¡Hasta luego!")
            sys.exit(0)
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
