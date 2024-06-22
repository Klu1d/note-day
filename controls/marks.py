import flet as ft
from fletmint import DatePicker

class Marks(ft.Row):
    def __init__(self):
        super().__init__()
        self.spacing = 1
        self.colors = {'blue': False}
        self.marks = {}

    def build(self):
        self.page.dialog = ft.AlertDialog(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        height = 35, width = 35,
                        bgcolor = color, border_radius = 10,
                        on_click = self.on_click_add_mark
                    ) if not self.colors[color] else ft.Container(
                        height = 35, width = 35,
                        bgcolor = color, border_radius = 10,
                        content=ft.Icon(ft.icons.CHECK, color='green')
                    )
                    for color in self.colors
                ]
            ),
            on_dismiss=lambda e: print("Dialog dismissed!")
        )

        self.controls = [
            ft.Container(
                content = ft.Icon('add', size=25),
                width = 20, height = 20,
                on_click=lambda _: self.page.show_dialog(self.page.dialog),
            ),
        ]
    
    def on_click_add_mark(self, e: ft.ControlEvent):
        mark_button = ft.TextButton(
            width = 20, height = 20,
            on_click = self.on_click_delete_mark,
            style = ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=3),
                bgcolor=e.control.bgcolor,
            )
        )
        self.controls.insert(
            len(self.controls) - 1, 
            mark_button
        )
        
        
        e.control.content=ft.Container(
            ft.Icon(ft.icons.CHECK, color=ft.colors.GREEN_ACCENT_700), 
            bgcolor=ft.colors.BLACK38,
            on_click=lambda _: self.on_click_delete_mark(e),
        )
        e.control.on_click=None
        e.control.update()
        self.update()

    def on_click_delete_mark(self, e: ft.ControlEvent):
        print(e)
        # ind = self.controls.index(e.control)
        # del self.controls[ind]
        # self.update()