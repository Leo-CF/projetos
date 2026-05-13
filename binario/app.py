import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

COLORS = {
    "bg":      "#0e1117",
    "display": "#161b22",
    "fg":      "#ffffff",
    "hint":    "#6b7280",
    "valid":   "#2dc653",
    "error":   "#e63946",
}


class ConversorBinario(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Conversor Binário → Decimal")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg"])

        self._build_ui()

    def _build_ui(self):
        frame = ctk.CTkFrame(self, fg_color=COLORS["display"], corner_radius=14)
        frame.pack(padx=24, pady=24)

        ctk.CTkLabel(
            frame,
            text="Conversor Binário → Decimal",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=COLORS["fg"],
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            frame,
            text="Digite um número binário:",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COLORS["hint"],
        ).pack()

        self._entrada = ctk.CTkEntry(
            frame,
            font=ctk.CTkFont(family="Segoe UI", size=18),
            width=280, height=44,
            justify="center",
            corner_radius=8,
            placeholder_text="ex: 1010",
        )
        self._entrada.pack(pady=16)
        self._entrada.bind("<KeyRelease>", lambda e: self._converter())

        self._resultado = ctk.CTkLabel(
            frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=COLORS["hint"],
            wraplength=280,
        )
        self._resultado.pack(pady=(0, 24))

        self._entrada.focus()

    def _converter(self):
        valor = self._entrada.get().strip()

        if not valor:
            self._resultado.configure(text="", text_color=COLORS["hint"])
            return

        invalidos = sorted(set(c for c in valor if c not in ("0", "1")))
        if invalidos:
            chars = ", ".join(f'"{c}"' for c in invalidos)
            self._resultado.configure(
                text=f"Entrada inválida: {chars}\nUse apenas 0 e 1.",
                text_color=COLORS["error"],
            )
        else:
            decimal = int(valor, 2)
            self._resultado.configure(
                text=f"{valor}  →  {decimal}",
                text_color=COLORS["valid"],
            )


if __name__ == "__main__":
    app = ConversorBinario()
    app.mainloop()
