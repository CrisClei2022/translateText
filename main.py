# main.py
# Certifique-se de instalar as bibliotecas necessárias no arquivo requirements.txt
from transformers import pipeline
import json

# Este código será executado no Appwrite Cloud.
def main(context):
    try:
        # Pega o texto do payload da requisição.
        # O Appwrite passa o payload do cliente front-end para a sua função.
        payload = json.loads(context.req.body)
        text_to_translate = payload.get('text', '')

        if not text_to_translate:
            return context.res.json({'translatedText': ''})

        # --- A LÓGICA DE TRADUÇÃO COM MODELO PRÉ-TREINADO ---
        # Instancie o pipeline de tradução.
        # O modelo será baixado na primeira execução da função.
        translator = pipeline("translation_en_to_pt", model="Helsinki-NLP/opus-mt-en-pt")

        # Use o pipeline para traduzir o texto.
        translated_text = translator(text_to_translate)[0]['translation_text']
        # ----------------------------------------------------

        # Retorna a resposta para o cliente.
        return context.res.json({
            'translatedText': translated_text
        })

    except Exception as e:
        # Em caso de erro, retorne uma resposta de erro.
        context.log(f"Erro na função: {str(e)}")
        return context.res.json({
            'error': 'Ocorreu um erro na tradução. Verifique o log da função no Appwrite.'
        }, 500) # Retorna um status de erro 500
