import tkinter as tk
from tkinter import font


COLORS = {
    "bg":       "#0e1117",
    "display":  "#1e222a",
    "btn":      "#1e222a",
    "btn_op":   "#2a2f3a",
    "btn_eq":   "#2dc653",
    "btn_clr":  "#e63946",
    "fg":       "#ffffff",
    "fg_op":    "#7eb8f7",
    "fg_eq":    "#0e1117",
    "fg_clr":   "#ffffff",
    "hover":    "#2e3340",
    "hover_eq": "#25a844",
    "result":   "#aaaaaa",
}


class Calculadora(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])

        self._expr = ""
        self._just_evaluated = False

        self._build_display()
        self._build_buttons()
        self._bind_keyboard()

    # ------------------------------------------------------------------
    def _build_display(self):
        frame = tk.Frame(self, bg=COLORS["bg"], padx=12, pady=12)
        frame.pack(fill="x")

        self._expr_var = tk.StringVar(value="")
        self._result_var = tk.StringVar(value="0")

        f_expr = font.Font(family="Segoe UI", size=11)
        f_result = font.Font(family="Segoe UI", size=28, weight="bold")

        tk.Label(
            frame, textvariable=self._expr_var, font=f_expr,
            bg=COLORS["display"], fg=COLORS["result"],
            anchor="e", width=22, padx=8, pady=4,
        ).pack(fill="x", pady=(0, 4))

        tk.Label(
            frame, textvariable=self._result_var, font=f_result,
            bg=COLORS["display"], fg=COLORS["fg"],
            anchor="e", width=22, padx=8, pady=8,
        ).pack(fill="x")

    def _build_buttons(self):
        frame = tk.Frame(self, bg=COLORS["bg"], padx=12, pady=8)
        frame.pack()

        layout = [
            [("C", "clr"), ("±", "op"), ("%", "op"), ("÷", "op")],
            [("7", "num"), ("8", "num"), ("9", "num"), ("×", "op")],
            [("4", "num"), ("5", "num"), ("6", "num"), ("−", "op")],
            [("1", "num"), ("2", "num"), ("3", "num"), ("+", "op")],
            [("0", "num_wide"), (".", "num"),            ("=", "eq")],
        ]

        btn_w, btn_h = 5, 2

        for r, row in enumerate(layout):
            col = 0
            for text, kind in row:
                colspan = 2 if kind == "num_wide" else 1

                if kind == "eq":
                    bg, fg, hov = COLORS["btn_eq"], COLORS["fg_eq"], COLORS["hover_eq"]
                elif kind == "clr":
                    bg, fg, hov = COLORS["btn_clr"], COLORS["fg_clr"], "#c62c38"
                elif kind == "op":
                    bg, fg, hov = COLORS["btn_op"], COLORS["fg_op"], COLORS["hover"]
                else:
                    bg, fg, hov = COLORS["btn"], COLORS["fg"], COLORS["hover"]

                f = font.Font(family="Segoe UI", size=13, weight="bold")
                btn = tk.Button(
                    frame, text=text, font=f,
                    bg=bg, fg=fg, activebackground=hov, activeforeground=fg,
                    relief="flat", bd=0,
                    width=btn_w * colspan + (colspan - 1),
                    height=btn_h,
                    command=lambda t=text: self._on_button(t),
                )
                btn.grid(row=r, column=col, columnspan=colspan,
                         padx=3, pady=3, sticky="nsew")
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

        # prevent multiple dots in the current number
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

        # replace trailing operator
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
        result = eval(sanitized, {"__builtins__": {}})  # noqa: S307
        return result

    def _format_num(self, val):
        if isinstance(val, float) and val.is_integer():
            val = int(val)
        if isinstance(val, float):
            # limit to 10 significant digits
            formatted = f"{val:.10g}"
        else:
            formatted = str(val)
        return formatted


if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()
