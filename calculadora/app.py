import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

COLORS = {
    "bg":       "#0e1117",
    "display":  "#161b22",
    "btn":      "#1e222a",
    "btn_op":   "#1e2d45",
    "btn_eq":   "#2dc653",
    "btn_clr":  "#c0392b",
    "fg":       "#ffffff",
    "fg_op":    "#7eb8f7",
    "fg_eq":    "#0e1117",
    "hover":    "#2e3340",
    "hover_op": "#1e3d65",
    "hover_eq": "#25a844",
    "hover_clr":"#e74c3c",
    "expr":     "#6b7280",
}


class Calculadora(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg"])

        self._expr = ""
        self._just_evaluated = False

        self._build_display()
        self._build_buttons()
        self._bind_keyboard()

    # ------------------------------------------------------------------
    def _build_display(self):
        frame = ctk.CTkFrame(self, fg_color=COLORS["display"], corner_radius=12)
        frame.pack(fill="x", padx=16, pady=(16, 8))

        self._expr_var = ctk.StringVar(value="")
        self._result_var = ctk.StringVar(value="0")

        ctk.CTkLabel(
            frame, textvariable=self._expr_var,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=COLORS["expr"], anchor="e",
            fg_color="transparent",
        ).pack(fill="x", padx=16, pady=(12, 0))

        ctk.CTkLabel(
            frame, textvariable=self._result_var,
            font=ctk.CTkFont(family="Segoe UI", size=36, weight="bold"),
            text_color=COLORS["fg"], anchor="e",
            fg_color="transparent",
        ).pack(fill="x", padx=16, pady=(0, 14))

    def _build_buttons(self):
        frame = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        frame.pack(padx=12, pady=(0, 14))

        PAD = 5
        W, H = 68, 52

        layout = [
            [("C", "clr"), ("±", "op"), ("%", "op"), ("÷", "op")],
            [("7", "num"), ("8", "num"), ("9", "num"), ("×", "op")],
            [("4", "num"), ("5", "num"), ("6", "num"), ("−", "op")],
            [("1", "num"), ("2", "num"), ("3", "num"), ("+", "op")],
            [("0", "num_wide"), (".", "num"),           ("=", "eq")],
        ]

        for r, row in enumerate(layout):
            col = 0
            for text, kind in row:
                colspan = 2 if kind == "num_wide" else 1
                width = W * colspan + PAD * (colspan - 1)

                if kind == "eq":
                    fg, hover, tc = COLORS["btn_eq"], COLORS["hover_eq"], COLORS["fg_eq"]
                elif kind == "clr":
                    fg, hover, tc = COLORS["btn_clr"], COLORS["hover_clr"], COLORS["fg"]
                elif kind == "op":
                    fg, hover, tc = COLORS["btn_op"], COLORS["hover_op"], COLORS["fg_op"]
                else:
                    fg, hover, tc = COLORS["btn"], COLORS["hover"], COLORS["fg"]

                btn = ctk.CTkButton(
                    frame, text=text,
                    font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                    fg_color=fg, hover_color=hover, text_color=tc,
                    corner_radius=10,
                    width=width, height=H,
                    command=lambda t=text: self._on_button(t),
                )
                btn.grid(row=r, column=col, columnspan=colspan,
                         padx=PAD // 2, pady=PAD // 2)
                col += colspan

    def _bind_keyboard(self):
        self.bind("<Key>", self._on_key)

    # ------------------------------------------------------------------
    def _on_key(self, event):
        k = event.char
        key_map = {"*": "×", "/": "÷", "-": "−"}
        k = key_map.get(k, k)

        if k in "0123456789.":
            self._on_button(k)
        elif k in ("+", "×", "÷", "−"):
            self._on_button(k)
        elif k in ("\r", "\n"):
            self._on_button("=")
        elif event.keysym == "BackSpace":
            self._backspace()
        elif k.lower() == "c" or event.keysym == "Escape":
            self._on_button("C")
        elif k == "%":
            self._on_button("%")

    def _on_button(self, text):
        if text == "C":
            self._clear()
        elif text == "=":
            self._evaluate()
        elif text == "±":
            self._negate()
        elif text == "%":
            self._percent()
        elif text in ("+", "−", "×", "÷"):
            self._append_op(text)
        else:
            self._append_digit(text)

    # ------------------------------------------------------------------
    def _clear(self):
        self._expr = ""
        self._just_evaluated = False
        self._expr_var.set("")
        self._result_var.set("0")

    def _backspace(self):
        if self._just_evaluated:
            self._clear()
            return
        self._expr = self._expr[:-1]
        self._update_preview()

    def _append_digit(self, ch):
        if self._just_evaluated:
            self._expr = ""
            self._just_evaluated = False

        if ch == ".":
            parts = self._expr.replace("×", "÷").replace("−", "÷").replace("+", "÷").split("÷")
            current = parts[-1] if parts else ""
            if "." in current:
                return
            if not current or current in ("", "-"):
                ch = "0."

        self._expr += ch
        self._update_preview()

    def _append_op(self, op):
        self._just_evaluated = False
        if not self._expr:
            if op == "−":
                self._expr = "−"
                self._update_preview()
            return
        if self._expr[-1] in ("+", "−", "×", "÷"):
            self._expr = self._expr[:-1]
        self._expr += op
        self._update_preview()

    def _negate(self):
        if not self._expr:
            return
        try:
            val = self._eval_expr(self._expr)
            self._expr = self._format_num(-val)
            self._just_evaluated = False
            self._update_preview()
        except Exception:
            pass

    def _percent(self):
        if not self._expr:
            return
        try:
            val = self._eval_expr(self._expr)
            self._expr = self._format_num(val / 100)
            self._just_evaluated = False
            self._update_preview()
        except Exception:
            pass

    def _evaluate(self):
        if not self._expr:
            return
        try:
            result = self._eval_expr(self._expr)
            self._expr_var.set(self._expr + " =")
            self._result_var.set(self._format_num(result))
            self._expr = self._format_num(result)
            self._just_evaluated = True
        except ZeroDivisionError:
            self._result_var.set("Erro: div/0")
            self._expr = ""
            self._just_evaluated = True
        except Exception:
            self._result_var.set("Erro")
            self._expr = ""
            self._just_evaluated = True

    def _update_preview(self):
        self._expr_var.set(self._expr)
        try:
            val = self._eval_expr(self._expr)
            self._result_var.set(self._format_num(val))
        except Exception:
            pass

    # ------------------------------------------------------------------
    def _eval_expr(self, expr):
        sanitized = (
            expr
            .replace("×", "*")
            .replace("÷", "/")
            .replace("−", "-")
        )
        return eval(sanitized, {"__builtins__": {}})  # noqa: S307

    def _format_num(self, val):
        if isinstance(val, float) and val.is_integer():
            val = int(val)
        return f"{val:.10g}" if isinstance(val, float) else str(val)


if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()
