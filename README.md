# API de Generación y Evaluación de Preguntas Educativas

Esta API REST, construida con Flask, permite gestionar la generación y evaluación de preguntas educativas utilizando la API de Llama. Las funcionalidades principales incluyen:

- Generar preguntas de opción múltiple sobre un tema específico.
- Generar preguntas abiertas o casos de estudio relacionados con un tema.
- Evaluar respuestas de usuarios comparándolas con un concepto clave del tema.

## Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecutar el Servidor](#ejecutar-el-servidor)
- [Endpoints de la API](#endpoints-de-la-api)
  - [POST /generate-multiple-choice](#post-generate-multiple-choice)
  - [POST /generate-open-ended](#post-generate-open-ended)
  - [POST /evaluate-response](#post-evaluate-response)
- [Ejemplos de Uso](#ejemplos-de-uso)
  - [Usando curl](#usando-curl)
  - [Usando Postman](#usando-postman)
- [Notas Adicionales](#notas-adicionales)

## Requisitos Previos

- **Python 3.7+** instalado en tu máquina. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
- **pip** (gestor de paquetes de Python).
- **Git** para clonar el repositorio (opcional).

## Instalación

1. **Clona el repositorio** (si aplica):

    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio/project
    ```

2. **Crea un entorno virtual** usando `venv`:

    ```bash
    python3 -m venv venv
    ```

3. **Activa el entorno virtual**:

    - En **Linux/MacOS**:

        ```bash
        source venv/bin/activate
        ```

    - En **Windows**:

        ```bash
        venv\Scripts\activate
        ```

4. **Instala las dependencias** desde `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

## Configuración

1. **Crea un archivo `.env`** en la raíz del proyecto y añade tu token de la API de Llama:

    ```plaintext
    LLAMA_API_TOKEN=tu_token_de_llama_api_aquí
    ```

    > **Nota:** Asegúrate de reemplazar `tu_token_de_llama_api_aquí` con tu token real. Nunca compartas este archivo públicamente.

## Ejecutar el Servidor

Con el entorno virtual activado y estando en la raíz del proyecto, ejecuta:

```bash
python app.py
