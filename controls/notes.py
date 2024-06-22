import locale
import datetime

import flet as ft
import fletmint as fm

from controls.legenda import Legenda
from controls.marks import Marks


locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

today = datetime.datetime.now()
day = today.strftime('%d')
month = today.strftime('%B')


class Notes(Legenda):
    def __init__(self):
        super().__init__()
        self.adaptive = False
        self.border_radius = 10
        self.marks = Marks(self.colors)
        

    def build(self):
        self.content = ft.Column(
            spacing=1, scroll = True,
            controls=[
                ft.TextField(
                    max_lines=100, text_size=25, border_radius=5, hint_text='Заголовок', visible=False,
                    capitalization=ft.TextCapitalization.SENTENCES, dense=True, cursor_color='black',
                    border=ft.InputBorder.NONE, keyboard_type=ft.KeyboardType.TEXT,
                    content_padding=ft.padding.symmetric(vertical=0, horizontal=0),
                ),
                ft.Column(
                    spacing=3,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Row(controls=[ft.Text(day + ' ' + month.capitalize(), size=22), self.marks], wrap=True),
                        ft.TextField(
                            max_lines=100, text_size=20, border_radius=5, hint_text='Что нового?', opacity=0.8,
                            capitalization=ft.TextCapitalization.SENTENCES, dense=True, cursor_color='black',
                            border=ft.InputBorder.NONE, keyboard_type=ft.KeyboardType.TEXT,
                            content_padding=ft.padding.symmetric(vertical=0, horizontal=10),
                        )
                    ]
                )
            ]
        )


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




class Marks(ft.Row):
    def __init__(self, colors):
        super().__init__()
        self.spacing = 5
        self.wrap = True
        self.colors = colors
        self.select_colors = {}

    def build(self):
        self.page.dialog = ft.AlertDialog(
            adaptive=True,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        height = 35, width = 35,
                        bgcolor = color, border_radius = 10,
                        on_click = self.on_click_add_mark
                    ) for color in self.colors if color not in self.select_colors
                ]
            )
        )

        self.controls = [
            ft.Container(
                content = ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE_OUTLINED, size=25),
                width = 25, height=25, opacity=0.7, padding=0,
                on_click=lambda _: self.page.show_dialog(self.page.dialog),
            ),
        ]
    
    def on_click_add_mark(self, e: ft.ControlEvent):
        e.control.visible = False
        
        self.controls.insert(len(self.controls) - 1, 
            ft.ElevatedButton(
                width=25, height=25, bgcolor=e.control.bgcolor,
                on_click=self.on_click_delete_mark,
                style = ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=7),
                )
            )
        )

        #устанавливается выбранный цвет и его значение из легенды.
        self.select_colors[e.control.bgcolor] = self.colors[e.control.bgcolor]

        if len(self.controls)-1 == len(self.colors):
            self.controls[-1].visible = False
            self.page.close_dialog()

        print(self.select_colors)
        self.page.update()

    def on_click_delete_mark(self, e: ft.ControlEvent):
        ind = self.controls.index(e.control)
        self.page.dialog.content.controls.append(
            ft.Container(height = 35, width = 35, on_click = self.on_click_add_mark,
                bgcolor = e.control.bgcolor, border_radius = 10)
        )
        del self.controls[ind]

        if len(self.controls)-1 < len(self.colors):
            self.controls[-1].visible = True

        self.page.update()

    

    