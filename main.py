# main.py
import json
import requests

def main(context):
    try:
        payload = json.loads(context.req.body)
        text_to_translate = payload.get('text', '')

        if not text_to_translate:
            return context.res.json({'translatedText': ''})

        # --- NOVA LÓGICA DE TRADUÇÃO USANDO A API DO LIBRETRANSLATE ---
        url = 'https://libretranslate.com/translate'
        
        # Envia a requisição POST para a API
        response = requests.post(
            url,
            json={
                "q": text_to_translate,
                "source": "en",
                "target": "pt",
                "format": "text",
                "api_key": ""
            }
        )
        
        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status() 
        
        data = response.json()
        translated_text = data['translatedText']
        # -----------------------------------------------------------------
        
        return context.res.json({
            'translatedText': translated_text
        })

    except requests.exceptions.RequestException as e:
        context.log(f"Erro ao chamar a API de tradução: {e}")
        return context.res.json({
            'error': 'Erro de comunicação com o serviço de tradução.'
        }, 500)
    except Exception as e:
        context.log(f"Erro na função: {str(e)}")
        return context.res.json({
            'error': 'Ocorreu um erro interno na função.'
        }, 500)
