import flet as ft

def testing(page: ft.Page):
    page.title = "Test"
    page.bgcolor = "#111111"
    page.add(ft.Text("Flet çalışıyor di mi?", color="white", size=24, """align=ft.TextAlign.CENTER"""))
    # şu align bir türlü çalışmıyor. main.pyde de çözene kadar canım çıktı. 
    page.update()

ft.app(target=testing)