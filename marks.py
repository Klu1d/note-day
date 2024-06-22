import flet as ft

from database import DatabaseConnection

#ты думал тут, как все сделать.
#в том плане, как сделать серверную часть заметки Note
class MarksData:
    def __init__(self):
        self.db_name = 'database.db'

    def create_table(self):
        with DatabaseConnection(self.db_name) as db:
            db.execute('''
            CREATE TABLE IF NOT EXISTS Marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                color TEXT NOT NULL,
                description TEXT
            )
            ''')
    
    def insert_legend(self, color, description):
        with DatabaseConnection(self.db_name) as db:
            db.execute('''
            INSERT INTO Marks (color, description)
            VALUES (?, ?)
            ''', (color, description))
    
    def insert_marks(self, marks):
        with DatabaseConnection(self.db_name) as db:
            db.executemany('''
            INSERT INTO Marks (color, description)
            VALUES (?, ?)
            ''', marks)
    
    def delete_legend(self, color):
        with DatabaseConnection(self.db_name) as db:
            db.execute('''
            DELETE FROM Marks WHERE color == ?
            ''', (color,))


    def fetch_all_marks(self):
        with DatabaseConnection(self.db_name) as db:
            db.execute('SELECT color, description FROM Marks')
            rows = db.fetchall()
            marks_dict = {color: description for color, description in rows}
            return marks_dict

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
