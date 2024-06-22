import flet as ft

from database import DatabaseConnection


class LegendsData:
    def __init__(self):
        self.db_name = 'database.db'

    def create_table(self):
        with DatabaseConnection(self.db_name) as db:
            db.execute('''
            CREATE TABLE IF NOT EXISTS Legends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                color TEXT NOT NULL,
                description TEXT
            )
            ''')
    
    def insert_legend(self, color, description):
        with DatabaseConnection(self.db_name) as db:
            db.execute('''
            INSERT INTO Legends (color, description)
            VALUES (?, ?)
            ''', (color, description))
    
    def insert_legends(self, legends):
        with DatabaseConnection(self.db_name) as db:
            db.executemany('''
            INSERT INTO Legends (color, description)
            VALUES (?, ?)
            ''', legends)
    
    def delete_legend(self, color):
        with DatabaseConnection(self.db_name) as db:
            db.execute('''
            DELETE FROM Legends WHERE color == ?
            ''', (color,))


    def fetch_all_legends(self):
        with DatabaseConnection(self.db_name) as db:
            db.execute('SELECT color, description FROM Legends')
            rows = db.fetchall()
            legends_dict = {color: description for color, description in rows}
            return legends_dict

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
        self.legends_data = LegendsData()
        self.legends_data.create_table()

        self.padding = 10
        self.adaptive = False
        self.shadow = ft.BoxShadow(
            spread_radius=1, blur_radius=1, blur_style=ft.ShadowBlurStyle.OUTER,
            color=ft.colors.with_opacity(0.05, ft.colors.ON_BACKGROUND),
        )
        self.border_radius = 10
        self.colors = self.legends_data.fetch_all_legends()
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
        color = e.control.parent.controls[1].color
        text = e.control.parent.controls[1].text

        principle = Principle(color, text)

        self.page.dialog = ft.AlertDialog(
            adaptive=True, 
            title=ft.Text("Удалить принцип"),
            actions_alignment=ft.MainAxisAlignment.END,
            content=ft.Column(controls=[ft.Text("Данный принцип будет удален и его невозможно будет восстановить, удалить?"), principle]),
            actions=[
                ft.TextButton("Нет", on_click=lambda _: self.page.close_dialog()),
                ft.TextButton("Да", on_click=lambda _: (
                        self.principles.remove(e.control.parent), 
                        self.page.close_dialog(), self.page.update(),
                        self.legends_data.delete_legend(color), (self.colors.pop(color) if color in self.colors else color)
                    )
                ),
            ],
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
        self.principles.append(
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
            )
        )
        self.page.update()
        self.legends_data.insert_legend(color, text)

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
