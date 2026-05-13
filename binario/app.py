import tkinter as tk
from tkinter import font


def converter():
    valor = entrada.get().strip()
    if not valor:
        resultado.config(text="", fg="#aaaaaa")
        return

    caracteres_invalidos = sorted(set(c for c in valor if c not in ("0", "1")))
    if caracteres_invalidos:
        invalidos = ", ".join(f'"{c}"' for c in caracteres_invalidos)
        resultado.config(
            text=f"Entrada inválida: {invalidos}\nUse apenas 0 e 1.",
            fg="#e63946",
        )
    else:
        decimal = int(valor, 2)
        resultado.config(
            text=f"{valor}  →  {decimal}",
            fg="#2dc653",
        )


root = tk.Tk()
root.title("Conversor Binário → Decimal")
root.geometry("400x220")
root.resizable(False, False)
root.configure(bg="#0e1117")

titulo_font = font.Font(family="Segoe UI", size=14, weight="bold")
label_font = font.Font(family="Segoe UI", size=11)
resultado_font = font.Font(family="Segoe UI", size=13, weight="bold")

tk.Label(root, text="Conversor Binário → Decimal", font=titulo_font,
         bg="#0e1117", fg="#ffffff").pack(pady=(20, 4))

tk.Label(root, text="Digite um número binário:", font=label_font,
         bg="#0e1117", fg="#aaaaaa").pack()

entrada = tk.Entry(root, font=label_font, width=28, justify="center",
                   bg="#1e222a", fg="#ffffff", insertbackground="#ffffff",
                   relief="flat", bd=6)
entrada.pack(pady=8)
entrada.bind("<KeyRelease>", lambda e: converter())

resultado = tk.Label(root, text="", font=resultado_font,
                     bg="#0e1117", fg="#aaaaaa", wraplength=360)
resultado.pack(pady=12)

entrada.focus()
root.mainloop()
