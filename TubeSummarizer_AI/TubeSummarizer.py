import re
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtén la clave API desde la variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

# Función para extraer el ID del video de YouTube
def extract_video_id(youtube_url):
    video_id_regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(video_id_regex, youtube_url)
    if match:
        return match.group(1)
    else:
        return None

# Función para extraer la transcripción del video
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text_list = [transcript[i]['text'] for i in range(len(transcript))]
        transcript_text = '\n'.join(text_list)
        return transcript_text
    except Exception as e:
        print(f"Error al obtener la transcripción: {str(e)}")
        return None

# Función para resumir el texto utilizando el modelo de OpenAI
def summarize_text(transcript_text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Resumen de los puntos clave del siguiente texto:\n\n{transcript_text}",
            max_tokens=150,
            temperature=0.5,
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        print(f"Error al generar el resumen: {str(e)}")
        return None

# Enlace del video de YouTube
youtube_url = "https://www.youtube.com/watch?v=DQzg_t6G6Js&t=61s"

# Ejecuta las funciones para obtener el resumen
video_id = extract_video_id(youtube_url)
if video_id:
    transcript = get_transcript(video_id)
    if transcript:
        summary = summarize_text(transcript)
        if summary:
            print("Resumen generado:")
            print(summary)
else:
    print("No se pudo extraer el ID del video.")