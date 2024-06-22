import locale
import datetime

import flet as ft
from flet_contrib.color_picker import ColorPicker




locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

today = datetime.datetime.now()
day = today.strftime('%d')
month = today.strftime('%B')


class Principle(ft.Container):
    def __init__(self, color: str, text: str):
        super().__init__()
        self.color = color 
        self.text = text
        self.adaptive = False
        self.animate_size = ft.animation.Animation(400, 'decelerate')


        self.content = ft.Row(
            spacing=0,
            controls=[
                #self.remove_icon,
                ft.ElevatedButton(
                    width=23, height=23, bgcolor=self.color,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5), padding=0)
                ),
                ft.TextField(
                    data=color,
                    dense=True, 
                    disabled=True,
                    value=self.text,
                    border=ft.InputBorder.NONE,
                    color=ft.colors.ON_BACKGROUND,
                    cursor_color=ft.colors.ON_BACKGROUND,
                    content_padding=ft.padding.only(10, 0, 0, 6),
                    on_change=self.on_change_text
                )
            ]
        )
        
    
    def on_change_text(self, e):
        if len(e.control.value) >= 23:
            e.control.value = e.control.value[0:23]
            self.text = e.control.value
        else:
            self.text = e.control.value
        self.page.update()
        
    
    def on_click_set_color(self, e):
        pass

class Legends(ft.Container):
    def __init__(self):
        super().__init__()
        self.padding = 10
        self.adaptive = False
        self.shadow = ft.BoxShadow(
            spread_radius=1, blur_radius=1, blur_style=ft.ShadowBlurStyle.OUTER,
            color=ft.colors.with_opacity(0.05, ft.colors.ON_BACKGROUND),
        )
        self.border_radius = 10
        self.colors = {'orange': 'orange', 'red': 'red', 'green':'green', 'blue':'blue'}
        self.principles = [
            ft.Row(
                spacing=0,
                controls=[
                    ft.Container( 
                        margin=ft.margin.only(left=0, right=5), width=0,
                        animate_size=ft.animation.Animation(400, 'decelerate'),
                        on_click=self.on_click_remove_principle,
                        content=ft.Icon(ft.icons.REMOVE_CIRCLE, size=0, color='error'),
                    ),
                    Principle(color, text)
                ]
            )for color, text in self.colors.items()
        ]


    def build(self):
        self.content = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    expand=8,
                    content=ft.Column(
                        spacing=0, scroll=True,
                        controls=self.principles
                    )
                ),
                ft.Container(
                    content=ft.Icon(ft.icons.HISTORY_EDU, color=ft.colors.ON_BACKGROUND, size=25), 
                    width=30, height=30, bgcolor=self.bgcolor, border_radius=10,
                    on_click=self.on_click_show_settings, shadow=ft.BoxShadow(
                        color=ft.colors.with_opacity(0.05, ft.colors.ON_BACKGROUND),
                    )
                )
            ]
        )
    
    def on_click_remove_principle(self, e):
        principle = Principle(e.control.parent.controls[1].color, e.control.parent.controls[1].text)

        self.page.dialog = ft.AlertDialog(
            adaptive=True, data=e.control.parent,
            title=ft.Text("Удалить принцип"),
            content=ft.Column(controls=[ft.Text("Уверен что хочешь удалить?"), principle]),
            actions=[
                ft.TextButton("Нет", on_click=lambda _: self.page.close_dialog()),
                ft.TextButton("Да", on_click=lambda _: (self.principles.remove(e.control.parent), self.page.close_dialog(), self.page.update())),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog.open = True
        self.page.update()

    def on_click_show_settings(self, e):
        e.control.on_click = self.on_click_close_settings
        e.control.content.name = ft.icons.CLOSE
        self._toogle_settings()
        self.page.update()

    def on_click_close_settings(self, e):
        e.control.on_click = self.on_click_show_settings
        e.control.content.name = ft.icons.HISTORY_EDU
        self._toogle_settings()
        self.page.update()

    def add_principle(self, color, text):
        self.principles.append(Principle(color, text))
        self.page.update()

    def _toogle_settings(self):
        for principle in self.principles:
            remove_icon = principle.controls[0]
            principle = principle.controls[1]
            if remove_icon.width == 0:
                remove_icon.width = 25
                remove_icon.content.size = 25
                
                principle.content.controls[0].content = ft.Icon(ft.icons.BRUSH_ROUNDED, size=20)
                principle.content.controls[0].on_click = principle.on_click_set_color
                principle.content.controls[1].disabled = False
            else:
                remove_icon.width = 0
                remove_icon.content.size = 0
                
                principle.content.controls[0].content = None
                principle.content.controls[0].on_click = None
                principle.content.controls[1].disabled = True

                self.colors[principle.color] = principle.text

class Marks(ft.Container):
    def __init__(self, legends, text_visible: bool = True):
        super().__init__()
        self.marks = {}
        self.text_visible = text_visible
        self.expand = False
        self.padding = 0
        self.legends = legends
        self.shadow = None
        self.select_marks_button = ft.Container(
            content=ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE_OUTLINED, size=25, color=ft.colors.ON_BACKGROUND),
            width=30, height=30, opacity=1, bgcolor=self.bgcolor, border_radius=10,
            on_click=self.on_click_select_marks, shadow=ft.BoxShadow(
                color=ft.colors.with_opacity(0.05, ft.colors.ON_BACKGROUND),
            )
        )
    
    def on_click_select_marks(self, e):
        self.page.dialog = ft.AlertDialog(
            adaptive=True,
            actions_padding=0,
            action_button_padding=0,
            actions_overflow_button_spacing=0,
            actions_alignment=ft.MainAxisAlignment.CENTER,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        height=35, width=35,
                        bgcolor=color, data=text,
                        border_radius=10,
                        on_click=self.on_click_add_mark
                    ) for color, text in self.legends.colors.items() if color not in self.marks
                ]
            )
        )
        self.page.dialog.open = True
        self.page.update()

    def build(self):
        self.legend_buttons = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    height=35, width=35,
                    bgcolor=color, data=text,
                    border_radius=10,
                    on_click=self.on_click_add_mark
                ) for color, text in self.legends.colors.items() if color not in self.marks
            ]
        )

        self.dialog_legend_buttons = ft.AlertDialog(
            adaptive=True,
            actions_padding=0,
            action_button_padding=0,
            actions_overflow_button_spacing=0,
            actions_alignment=ft.MainAxisAlignment.CENTER,
            content=self.legend_buttons
        )

    def create_mark(self, color, text):
        return ft.Container(
            data=text, 
            bgcolor=color, 
            border_radius=5, 
            height=25, 
            width=25 + (100 * (len(text) * 0.08)) if self.text_visible else 25,
            on_click=self.on_click_delete_mark,
            alignment=ft.alignment.center,
            content=ft.Text(
                text, weight=ft.FontWeight.BOLD, 
                max_lines=1, visible=self.text_visible
            ),
            shadow=ft.BoxShadow(
                spread_radius=-1, blur_radius=2,
                offset=ft.Offset(0, 1), blur_style=ft.ShadowBlurStyle.OUTER,
            ),
        )
        
    def on_click_add_mark(self, e: ft.ControlEvent):
        e.control.visible = False
        self.padding = 5
        self.shadow = ft.BoxShadow(
            spread_radius=1, blur_radius=1, blur_style=ft.ShadowBlurStyle.OUTER,
            color=ft.colors.with_opacity(0.05, ft.colors.ON_BACKGROUND),
        )
        self.content = ft.Row(wrap=True,
            controls=[self.create_mark(color, text) for color, text in self.marks.items()]
        )

        text = e.control.data
        color = e.control.bgcolor
        self.marks[color] = text
        self.update_marks()

    def on_click_delete_mark(self, e: ft.ControlEvent):
        text = e.control.data
        color = e.control.bgcolor

        self.legend_buttons.controls.append(
            ft.Container(
                border_radius=10,
                height=35, width=35,
                bgcolor=color, data=text,
                on_click=self.on_click_add_mark
            )
        )

        del self.marks[color]
        self.update_marks()
    
    def update_marks(self):
        self.content = ft.Row(wrap=True,
            controls=[self.create_mark(color, text) for color, text in self.marks.items()])
        #self.content.controls.append(self.select_marks_button)

        if len(self.marks) == 0:
            self.padding = 0
        if len(self.marks) == len(self.legends.colors):
            self.select_marks_button.visible = False
            self.page.close_dialog()
        else:
            self.select_marks_button.visible = True

        self.page.update()

class Notes(ft.Container):
    notes_list = []
    def __init__(self):
        super().__init__()
        Notes.notes_list.append(self)
        self.adaptive = False
        self.padding = 10
        self.border_radius = 10

        self.shadow = ft.BoxShadow(
            spread_radius=1, blur_radius=1, blur_style=ft.ShadowBlurStyle.OUTER,
            color=ft.colors.with_opacity(0.05, ft.colors.ON_BACKGROUND),
        )
        
    # def build(self):
    #     self.content = ft.ListView(
    #         spacing=10,
    #         controls=[
    #             Note(title='Заголовок', marks=Marks(text_visible=True), text='text',date='25 Марта'),
    #             Note(title='Заголовок', marks=Marks(text_visible=True), text='text',date='54 Марта')
    #         ]
    #     )

class Note(Notes):
    def __init__(
        self,
        date: str,
        title: str = None,
        text: str = None,
        title_visible: bool = False,
    ):
        #note settings
        super().__init__()
        self.expand = 8

        #user settings
        self.title_visible = title_visible
        
        #user data
        self.title = title
        self.marks = Marks(Legends())
        self.text = text
        self.date = date

    
    def build(self):
        self.content = ft.Column(
            scroll=True,
            controls = [
                ft.TextField(
                    border=ft.InputBorder.NONE, border_radius=5, value=self.title,
                    capitalization=ft.TextCapitalization.SENTENCES, dense=True,
                    content_padding=ft.padding.symmetric(vertical=0, horizontal=0),
                    keyboard_type=ft.KeyboardType.TEXT, max_lines=100, text_size=25, 
                    hint_text='Заголовок', cursor_color='onbackground', visible=self.title_visible,
                ),
                ft.Column(
                    spacing=0,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(self.date.capitalize(), size=22), 
                                self.marks.select_marks_button
                            ], 
                        ),
                        ft.Row(wrap=True,
                            controls=[self.create_mark(color, text) for color, text in self.marks.items()]
                        ),
                        ft.TextField(
                            border=ft.InputBorder.NONE, border_radius=5, value=self.text,
                            capitalization=ft.TextCapitalization.SENTENCES, dense=True,
                            hint_text='Что нового?', cursor_color='onbackground',
                            keyboard_type=ft.KeyboardType.TEXT, max_lines=100, text_size=20, 
                            content_padding=ft.padding.symmetric(vertical=0, horizontal=10),
                        )
                    ]
                )
            ]
        )


class MarksOne(ft.Container):
    def __init__(self, legends: Legends, text_visible: bool = True):
        super().__init__()
        self.marks = {}
        self.legends = legends
        self.text_visible = text_visible

        self.expand = False
        self.padding = 0

    def build(self):
        self.select_marks_button = ft.Container(
            content=ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE_OUTLINED, size=25, color=ft.colors.ON_BACKGROUND),
            width=30, height=30, opacity=1, bgcolor=self.bgcolor, border_radius=10,
            on_click=self.on_click_select_marks, shadow=ft.BoxShadow(
                color=ft.colors.with_opacity(0.05, ft.colors.ON_BACKGROUND),
            )
        )

    def on_click_select_marks(self, e):
        self.page.dialog = ft.AlertDialog(
            adaptive=True,
            actions_padding=0,
            action_button_padding=0,
            actions_overflow_button_spacing=0,
            actions_alignment=ft.MainAxisAlignment.CENTER,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        height=35, width=35,
                        bgcolor=color, data=text,
                        border_radius=10,
                        on_click=self.on_click_add_mark
                    ) for color, text in self.legends.colors.items() if color not in self.marks
                ]
            )
        )
        self.page.dialog.open = True
        self.page.update()


class StoryView(ft.View):
    def __init__(self):
        super().__init__()
        self.route = '/story'
        self.appbar = ft.AppBar(
            adaptive=True,
            toolbar_height=45, 
            bgcolor='black',
            actions=[
                ft.Container(content=ft.Text('История ',  color='white',size=28, weight=ft.FontWeight.BOLD))
            ],
        )

    def build(self):
        return super().build()
    
class LegendView(ft.View):
    def __init__(self):
        super().__init__()
        self.route = '/'
        self.appbar = ft.AppBar(
            leading=ft.Row(
                controls=[
                    ft.Container(ft.Text('Легенда', color='white', size=28, weight=ft.FontWeight.BOLD), padding=ft.padding.only(0,0,0,0)),
                    ft.Container(
                        content=ft.Icon(ft.icons.ADD, size=25, color='white'), 
                        height=30, width=30, border_radius=10, margin=ft.margin.only(0,0,5,1),
                        on_click=self.on_click_append_principle, bgcolor='grey, 0.2',
                    ),
                ]
            ),
            adaptive=True,
            bgcolor='black',
            toolbar_height=45,
            center_title=False,
            actions=[
                ft.Container(
                    content=ft.Icon(ft.icons.SETTINGS_ROUNDED, size=25, color='white'), 
                    height=30, width=30, border_radius=10,  margin=ft.margin.only(0,0,5,1),
                    on_click= lambda _: print('Настройки'), bgcolor='grey, 0.2',
                ),
            ],
        )
    

    def build(self):
        self.legenda = Legends()
        self.note = Note(date='54 Марта', title_visible=True)
        self.marks = Marks(legends=self.legenda)
        self.controls = [
            self.legenda,
            ft.Row(
                controls=[
                    ft.Text(' Событие', size=28, weight=ft.FontWeight.BOLD, color=ft.colors.ON_BACKGROUND),
                    ft.Container(
                        content=ft.Icon(ft.icons.HISTORY, size=25, color=ft.colors.ON_BACKGROUND), 
                        height=30, width=30, border_radius=10, margin=ft.margin.only(0,0,5,1),
                        on_click=lambda _: self.page.go('/story'), bgcolor='grey, 0.2',
                    ),
                ]
            ),
            self.marks.select_marks_button,
            self.marks,
            
            ft.ElevatedButton('click', on_click=lambda _: print(self.legenda.colors)),
           
            
        ]
    
    def on_click_append_principle(self, e):
        self.page.dialog = ft.AlertDialog(
            adaptive=True, data=e.control.parent,
            title=ft.Text("Новый принцип"),
            content=ft.Column(controls=[ft.Text("Добавить")]),
            
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog.open = True
        self.page.update()

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.WHITE,   
            
        )
    )


    def route_change(route):
        page.views.clear()
        page.views.append(LegendView())
        if page.route == "/story":
            page.views.append(StoryView())
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.adaptive = True
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)
