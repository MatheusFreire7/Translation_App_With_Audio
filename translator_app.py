import streamlit as st
from googletrans import Translator
from gtts import gTTS
import tempfile
import os
import pandas as pd

st.title("Tradutor de Idiomas com Áudio")

# Inicializa o tradutor
translator = Translator()

# Mapeamento de códigos de idioma para nomes compreensíveis
language_names = {
    "en": "Inglês",
    "es": "Espanhol",
    "fr": "Francês",
    "de": "Alemão",
    "it": "Italiano",
    "pt": "Português",
    "ja": "Japonês",
    "zh": "Chinês",
    "ru": "Russo",
    "ar": "Árabe",
    "af": "Africâner",
    "el": "Grego",
    "ko": "Coreano",
    "sv": "Sueco",
    "he": "Hebraico",
    "th": "Tailandês",
    "nl": "Holandês",
    "pt-br": "Português Brasileiro",
    "en-gb": "Inglês Britânico",
    "hi": "Hindi",
    "tr": "Turco",
    "pl": "Polonês",
    "vi": "Vietnamita",
    "fi": "Finlandês",
    "uk": "Ucraniano",
    "no": "Norueguês",
}

# Adiciona um seletor de idioma de origem
source_lang = st.selectbox("Selecione o idioma de origem", ["Auto"] + list(language_names.values()))

# Adiciona um seletor de idioma de destino
target_lang = st.selectbox("Selecione o idioma para Traduzir", list(language_names.values()))

# Cria um dicionário reverso para mapear nomes de idiomas de volta para códigos de idioma
reverse_language_names = {nome_idioma: codigo_idioma for codigo_idioma, nome_idioma in language_names.items()}

input_text = st.text_area("Digite o texto para traduzir:")

# Inicializa o histórico de traduções usando a sessão do Streamlit
if "translation_history" not in st.session_state:
    st.session_state.translation_history = pd.DataFrame(columns=["Origem", "Destino", "Texto Original", "Tradução"])

if st.button("Traduzir"):
    if not input_text:
        st.warning("Por favor, insira o texto para traduzir.")
    else:
        try:
            source_lang_code = reverse_language_names.get(source_lang, "auto")
            target_lang_code = reverse_language_names[target_lang]

            if source_lang == "Auto":
                # Detecta automaticamente o idioma de origem
                detected_lang = translator.detect(input_text).lang
                source_lang_display = language_names.get(detected_lang, "Auto Detectado")
            else:
                source_lang_display = language_names.get(source_lang_code, source_lang_code)

            target_lang_display = language_names.get(target_lang_code, target_lang_code)

            translation_text = st.empty()
            spinner_translate = st.empty()

            translation_text.text("Traduzindo...")
            with spinner_translate:
                translated_text = translator.translate(input_text, src=source_lang_code, dest=target_lang_code).text

            translation_text.empty()
            spinner_translate.empty()

            st.subheader(f"Tradução de {source_lang_display} para {target_lang_display}:")
            st.write(translated_text)

            # Adiciona tradução ao histórico
            new_translation = pd.DataFrame({
            "Origem": [source_lang_display],
                "Destino": [target_lang_display],
                "Texto Original": [input_text],
                "Tradução": [translated_text]
            })
            st.session_state.translation_history = pd.concat([st.session_state.translation_history, new_translation], ignore_index=True)
            st.write("Histórico de Traduções:")
            st.write(st.session_state.translation_history)
            
            audio_text = st.empty()
            spinner_audio = st.empty()

            audio_text.text("Criando áudio...")

            # Criação do áudio do texto traduzido
            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts = gTTS(translated_text, lang=target_lang_code)
            tts.save(audio_file.name)
            audio_path = os.path.abspath(audio_file.name)
            st.audio(audio_path, format="audio/mp3")

            audio_text.empty()
            spinner_audio.empty()
        except Exception as e:
            st.error("Erro ao traduzir o texto. Certifique-se de que os códigos de idioma são válidos e tente novamente.")