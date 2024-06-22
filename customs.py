import flet as ft

class IconButton(ft.IconButton):
    def __init__(
            self,
            icon,
            click,
            height = None,
            width = None,
    ):
        super().__init__()
        self.icon = icon 
        self.on_click = click
        self.height = height
        self.width = width
        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=3),
            bgcolor=ft.colors.BACKGROUND,
            color=ft.colors.ON_SECONDARY_CONTAINER,
        )
        
    
