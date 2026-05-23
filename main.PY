import flet as ft
import sympy as sp
import sqlite3
import datetime

# --- إدارة قاعدة البيانات ---
class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("data.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, query TEXT, result TEXT, timestamp TEXT)")
        self.conn.commit()

    def log(self, query, result):
        self.cursor.execute("INSERT INTO history (query, result, timestamp) VALUES (?, ?, ?)", 
                           (query, result, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()

# --- محرك الحسابات ---
class ComputationEngine:
    @staticmethod
    def solve(expr_str):
        try:
            x = sp.Symbol('x')
            expr = sp.sympify(expr_str)
            sol1 = str(sp.solve(expr, x))
            deriv = str(sp.diff(expr, x))
            return f"Algebraic: {sol1}\nCalculus (Derivative): {deriv}", True
        except Exception as e:
            return str(e), False

# --- الواجهة الرئيسية ---
def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121212"
    page.padding = 0
    db = DatabaseManager()

    input_field = ft.TextField(value="", bgcolor="#1E1E1E", color="white", border_color="#3498DB", read_only=True)
    result_text = ft.Text("Result", size=18, color="#3498DB")

    def on_key_click(e):
        val = e.control.content.value
        if val == "=":
            res, success = ComputationEngine.solve(input_field.value)
            result_text.value = res
            if success: db.log(input_field.value, res)
        elif val == "C":
            input_field.value = ""
        else:
            input_field.value += val
        page.update()

    # لوحة المفاتيح
    keys = ['7','8','9','/', '4','5','6','*', '1','2','3','-', '0','.','sqrt(','+', 'sin(','cos(','log(','=','C']
    grid = ft.GridView(expand=False, runs_count=4, max_extent=80, child_aspect_ratio=1.0, spacing=5)
    
    for k in keys:
        grid.controls.append(ft.Container(
            content=ft.Text(k, size=16), bgcolor="#1E1E1E", 
            alignment=ft.alignment.center, on_click=on_key_click, border_radius=10
        ))

    # التخطيط
    page.add(
        ft.Container(padding=20, content=ft.Column([
            ft.Text("CALCES PROFESSIONAL", size=20, weight="bold"),
            input_field,
            result_text,
            ft.Divider(),
            grid
        ]))
    )

ft.app(target=main)