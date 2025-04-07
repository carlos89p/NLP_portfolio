# 📚 LLM Text Improver App

## ✅ Overview

This application allows users to enhance and correct texts written in Spanish using a locally running Large Language Model (LLM): **Mistral-7B-Instruct-v0.1** in **GGUF format**. It features a lightweight and accessible **graphical interface built with Tkinter**, and **does not require any internet connection or external APIs**.

The model processes user input using instruction-based prompts and returns a rewritten version that is more fluent, grammatically correct, and stylistically improved, while maintaining the original meaning.

---

## 🧰 Tools Used

| Tool                 | Purpose                                                                 |
|----------------------|-------------------------------------------------------------------------|
| `llama-cpp-python`   | Loads `.gguf` models locally and efficiently on CPU and/or GPU.         |
| `Tkinter`            | Provides a simple, cross-platform GUI without external dependencies.    |
| `Mistral-7B-Instruct`| Open-source LLM optimized for following natural language instructions.  |

---

## 🧠 How It Works

1. The user writes or pastes a Spanish text they want to improve in the top input box.
2. By clicking the **"Improve Text"** button, the application sends the input to the local LLM using an instruction format like:



3. The model generates a corrected and improved version of the text, which is then displayed in the output box below.

---

## 💻 Interface Demo

### 🖋️ Step 1: Enter your text  
The user types or pastes the original text into the top input field.  
![Text input interface](screenshots/image1.png)

---

### 🔁 Step 2: Click "Improve Text"  
Once the button is pressed, the model processes the input and returns a cleaner and more correct version.  
![Text improved result](screenshots/image2.png)

---

## ✅ Advantages

- 💻 **Runs fully offline** — no data is sent to external servers.
- 🔒 **Privacy-first** — everything happens locally.
- ⚡ **Fast and lightweight** — optimized for performance with `llama-cpp-python`.
- 🧠 **Powerful text correction** using one of the best open-source instruction-tuned LLMs.

---

## 📂 Project Structure

