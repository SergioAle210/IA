import openai
import markdown
import pdfkit
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtén la clave API desde la variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

# Tu currículum en formato Markdown
md_resume = """
# Sergio Orellana

## Experiencia Profesional

### Compañía ABC
- Descripción de tu rol y responsabilidades.

### Compañía XYZ
- Descripción de tu rol y logros.
"""

# Descripción del trabajo al que estás aplicando
job_description = """
Estamos buscando un desarrollador backend con experiencia en Python, bases de datos SQL, y desarrollo de APIs. Se valorará experiencia con microservicios y tecnologías en la nube.
"""

# Plantilla del prompt
prompt = f"""
Tengo un currículum en formato Markdown y una descripción de trabajo. \
Por favor, adapta mi currículum para que se alinee mejor con los requisitos del trabajo, \
manteniendo un tono profesional. Adapta mis habilidades, experiencias y logros para resaltar \
los puntos más relevantes para la posición. Asegúrate de que mi currículum siga reflejando \
mis calificaciones y fortalezas únicas, pero enfatiza las habilidades y experiencias que coinciden con la descripción del trabajo.

### Aquí está mi currículum en Markdown:
{md_resume}

### Aquí está la descripción del trabajo:
{job_description}

Por favor, modifica el currículum para:
- Utilizar palabras clave y frases de la descripción del trabajo.
- Ajustar los puntos de cada rol para enfatizar habilidades y logros relevantes.
- Asegurarte de que mis experiencias estén presentadas de manera que coincidan con las calificaciones requeridas.
- Mantener claridad, concisión y profesionalismo en todo el documento.

Devuélveme el currículum actualizado en formato Markdown.
"""

# Llamada a la API de OpenAI usando el nuevo método ChatCompletion
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # Asegúrate de usar el modelo correcto
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.25
)

# Extraer el currículum actualizado
updated_resume = response['choices'][0]['message']['content']

# Convertir el currículum actualizado de Markdown a HTML
html_resume = markdown.markdown(updated_resume)

# Convertir el currículum en HTML a PDF
pdfkit.from_string(html_resume, 'updated_resume.pdf')
print("Currículum actualizado y exportado como PDF.")
