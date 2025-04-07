import tkinter as tk
from tkinter import filedialog, messagebox
from llama_cpp import Llama
import threading

# Carga del modelo GGUF (ajusta el path a donde lo tengas guardado)
llm = Llama(
    model_path="models/mistral-7b-instruct-v0.1.Q4_0.gguf",
    n_ctx=2048,
    n_threads=6,
    n_gpu_layers=30  # Si tienes GPU, puedes ajustarlo
)

# Función para interactuar con el modelo
def mejorar_texto(prompt_usuario):
    prompt = f"[INST] Mejora y corrige el siguiente texto en español, manteniendo el sentido original: {prompt_usuario} [/INST]"
    respuesta = llm(prompt, max_tokens=512, temperature=0.7, stop=["</s>"])
    return respuesta["choices"][0]["text"].strip()

# Función que corre en un hilo
def procesar_texto():
    texto = entrada_texto.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Aviso", "Introduce un texto para procesar.")
        return

    boton.config(state=tk.DISABLED)
    salida_texto.delete("1.0", tk.END)
    salida_texto.insert(tk.END, "Procesando...")

    def tarea():
        try:
            resultado = mejorar_texto(texto)
            salida_texto.delete("1.0", tk.END)
            salida_texto.insert(tk.END, resultado)
        except Exception as e:
            salida_texto.delete("1.0", tk.END)
            salida_texto.insert(tk.END, f"Error: {str(e)}")
        finally:
            boton.config(state=tk.NORMAL)

    threading.Thread(target=tarea).start()

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Mejorador de Textos con LLM")
ventana.geometry("800x600")

tk.Label(ventana, text="Introduce tu texto:").pack(pady=5)
entrada_texto = tk.Text(ventana, height=10, wrap=tk.WORD)
entrada_texto.pack(fill=tk.BOTH, expand=True, padx=10)

boton = tk.Button(ventana, text="Mejorar texto", command=procesar_texto)
boton.pack(pady=10)

tk.Label(ventana, text="Texto mejorado:").pack()
salida_texto = tk.Text(ventana, height=10, wrap=tk.WORD)
salida_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

ventana.mainloop()
