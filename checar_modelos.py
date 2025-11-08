import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio

# --- Configuração ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if GEMINI_API_KEY is None:
    print("ERRO: Não achei a GOOGLE_API_KEY no seu arquivo .env")
    exit()

genai.configure(api_key=GEMINI_API_KEY)

# --- Função para Listar os Modelos ---
async def listar_modelos():
    print("--- Tentando listar os modelos disponíveis ---")
    try:
        # Loop para listar todos os modelos
        for m in genai.list_models():
            # Vamos checar se o modelo suporta 'generateContent'
            if 'generateContent' in m.supported_generation_methods:
                print(f"Nome do Modelo: {m.name}")
                print(f"   Descrição: {m.description}\n")
    except Exception as e:
        print(f"\nOcorreu um erro ao tentar listar os modelos: {e}")
        print("\nVerifique se sua chave de API (GOOGLE_API_KEY) no .env está 100% correta.")

    print("--- Fim da lista ---")

# Roda a função
if __name__ == "__main__":
    asyncio.run(listar_modelos())