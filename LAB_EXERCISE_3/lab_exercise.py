from llama_cpp import Llama
import gradio as gr
import os

# Carga del modelo LLM en local
MODEL_PATH = "models/mistral-7b-instruct.gguf"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=35  # Usa GPU si tienes una compatible
)

# Prompt system para el modelo instruct
SYSTEM_PROMPT = "You are a helpful assistant that improves and corrects texts in Spanish."

# Función de mejora de texto
def improve_text(user_input):
    prompt = f"""[INST] <<SYS>>
{SYSTEM_PROMPT}
<</SYS>>
Corrige y mejora este texto: "{user_input}"
[/INST]"""
    response = llm(prompt, max_tokens=512, temperature=0.7)
    return response["choices"][0]["text"].strip()

# Interfaz Gradio
iface = gr.Interface(
    fn=improve_text,
    inputs=gr.Textbox(lines=10, label="Texto para corregir y mejorar"),
    outputs=gr.Textbox(lines=10, label="Texto corregido"),
    title="Corrector inteligente de texto (offline)",
    description="Escribe o pega tu texto en español y será corregido y mejorado por un LLM local."
)

if __name__ == "__main__":
    iface.launch()
