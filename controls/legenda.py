import flet as ft
from customs import IconButton


class Legenda(ft.Container):
    def __init__(self):
        super().__init__()
        self.adaptive = False
        
        self.padding = 10
        self.border_radius = 10
        self.colors = {'orange':'orange', 'red':'red'}
        self.bgcolor='purple, 0.225'

        self.title = 'Легенда'
        self.title_vision = False
    
    def build(self):
        self.content=ft.Row(
            wrap=True,
            controls=[
                ft.Column(
                    spacing=0, 
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    bgcolor=color, 
                                    width=20, height=20, 
                                    border_radius=5, margin=ft.margin.only(0,0,0,0),
                                    shadow=ft.BoxShadow(
                                        spread_radius=-1, blur_radius=2, color=ft.colors.BLACK, 
                                        offset=ft.Offset(0, 1), blur_style=ft.ShadowBlurStyle.OUTER,
                                    ),
                                ),
                                ft.TextField(
                                    value=color_value, show_cursor=True,
                                    dense=True, content_padding=ft.padding.only(0,0,0,6),
                                    border=ft.InputBorder.NONE, 
                                    color=ft.colors.ON_BACKGROUND,
                                    cursor_color=ft.colors.ON_BACKGROUND,
                                )
                            ]
                        ) for color, color_value in self.colors.items()
                    ]           
                )
            ]
        )
        
    
    def change_value(self, e: ft.ControlEvent):
        e.control.content.disabled = False
        e.control.content.focus()
        e.control.update()

    def add_color(self, color: str, value: str):
        self.colors[color] = value
        self.build()
        self.update()

