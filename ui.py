import flet as ft 
from utils import Parse

class App(ft.Column):
    def __init__(self, page_):
        super().__init__()
        self.page_ = page_
        self.parse = Parse()
     
         
        #self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.width = 1600
        self.height = 1200
                
        #self.page_.overlay.append(self.file_picker)
        self.search_value = ""

        self.search_field = ft.TextField(
            hint_text="Поиск по SSID",
            width=300,
            dense=True,
            on_change=self.on_search,
        )
        
        self.info_coll = ft.Container(
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=ft.BorderRadius.all(10),
            width=350,
            #expand=True,
            content=ft.Column(
                    self.build_()
            ),
            padding=ft.Padding.symmetric(horizontal=5, vertical=5),
            animate_size=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
        )
        
                
        self.info_rows = ft.Container(
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=ft.BorderRadius.all(10),
            width=350,
            expand=True,
            content=ft.Row(

            ),
            padding=ft.Padding.symmetric(horizontal=5, vertical=5),
            animate_size=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
        )
        
        self.appbar = ft.AppBar(
        title=self.search_field,
        actions=[
            ft.IconButton(ft.Icons.FOLDER_OPEN, tooltip="Открыть файлы", on_click=self.open_files),
            ft.IconButton(ft.Icons.REFRESH, tooltip="Обновить", on_click=self.reset),
            ft.IconButton(ft.Icons.SETTINGS, tooltip="Настройки", on_click=self.show_dialog),
            ft.IconButton(ft.Icons.INFO, tooltip="О программе"),
            ],
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        )

        self.main_area = ft.Row(
            controls=[
                self.info_coll,
                self.devices_tables(),
            ],
            spacing=10,
            expand=True,
        )

        self.controls = [
            self.appbar,
            self.main_area,
        ]

    def devices_panel(self, title, devices):
        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=ft.BorderRadius.all(10),
            padding=10,
            content=ft.Column(
                controls=[
                    ft.Text(
                        title,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),

                    ft.Row(
                        controls=[
                            ft.Text("MAC", expand=True, weight=ft.FontWeight.BOLD),
                            ft.Text("SSID", expand=True, weight=ft.FontWeight.BOLD),
                            ft.Text("Кол-во", width=70, weight=ft.FontWeight.BOLD),
                        ]
                    ),

                    ft.Divider(height=1),

                    ft.ListView(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(item["row"][1], expand=True),
                                    ft.Text(item["row"][2], expand=True),
                                    ft.Text(str(item["count"]), width=70),
                                ]
                            )
                            for item in devices
                        ],
                        spacing=6,
                        expand=True,
                    ),
                ],
                expand=True,
            ),
        )
    def devices_tables(self):
        return ft.Row(
            controls=[
                self.devices_panel("Стационарные", self.filter_by_ssid(self.parse.stationary)),
                self.devices_panel("Случайные", self.filter_by_ssid(self.parse.randoms)),
                self.devices_panel("Нарушители", self.filter_by_ssid(self.parse.intruders)),
            ],
            spacing=10,
            expand=True,
        )
        
    def info_text(self, text = "Отсутствует", collor = ft.Colors.SURFACE, size = 100, color_text = ft.Colors.WHITE, rad = ft.BorderRadius.all(10), size_text = 20):
            return ft.Container(
                bgcolor=collor,
                height=size,
                border_radius=rad,
                content = ft.Row(
                    controls=[
                        ft.Text(text, 
                                size=size_text, 
                                weight=ft.FontWeight.BOLD,
                                align=ft.Alignment.CENTER,
                                color=color_text,
                                ),
                        ],
                    alignment=ft.MainAxisAlignment.CENTER,

                )
            )
            
    def build_(self):
        return [
            self.info_text(text = "Информационная панель", collor = ft.Colors.SURFACE_TINT, size = 30, color_text = ft.Colors.BLACK, rad = ft.BorderRadius.all(0), size_text=18),
            self.info_text(text = f"Количество файлов: {len(self.parse.filenames)}"),
            self.info_text(text = f"Загруженные файлы:\n{self.parse.files_ui}",size = 100 + (len(self.parse.filenames) * 25) ),
            self.info_text(text = f"Количество записей: {self.parse.summary}"),
            self.info_text(text = f"Стационарные устройства:\t{len(self.parse.stationary)}", collor=ft.Colors.GREEN, color_text=ft.Colors.BLACK,size_text = 20),
            self.info_text(text = f"Случайные устройства:\t{len(self.parse.randoms)}", collor=ft.Colors.YELLOW, color_text=ft.Colors.BLACK, size_text=20),
            self.info_text(text = f"Нарушители:\t{len(self.parse.intruders)}",collor=ft.Colors.RED, color_text=ft.Colors.BLACK, size_text=20),
        ]
    
    async def open_files(self, e=None):
        files = await ft.FilePicker.pick_files(
            ft.FilePicker(),
            allow_multiple=True,
            allowed_extensions=["html"]
            )

        if not files:
            return

        self.parse.filenames = [file.path for file in files]
        self.parse.parse_ui()
        self.parse.files_ui = "\n".join(file.name for file in files)
        
        self.update_()
    
    async def info_prog(self):
        pass#await self.page.window.ba
    
    def reset(self):
        self.parse.reset()
        self.info_coll.content.controls = self.build_()
        self.main_area.controls = [
            self.info_coll,
            self.devices_tables(),
        ]
        self.update()
    
    def update_(self):
        self.info_coll.content.controls = self.build_()
        self.main_area.controls = [
            self.info_coll,
            self.devices_tables(),
        ]
        self.update()
    
    async def on_files_selected(self, e):
        if not await e.files:
            return

        self.parse.filenames = [file.path for file in e.files]
        self.parse.files_ui = "\n".join(file.name for file in e.files)

        self.reset()
        self.show_dialog(e)

    
    def show_dialog(self, e):
        dialog = ft.AlertDialog(
            title=ft.Text("Информация"),
            content=ft.Text("Настройки :)"),
            actions=[
                ft.TextButton("Закрыть", on_click=lambda _: self.close_dialog(e, dialog))
            ],
        )
        e.page.overlay.append(dialog)
        dialog.open = True
        e.page.update()

    
    def close_dialog(self, e, dialog):
        dialog.open = False
        e.page.update()
    
    def filter_by_ssid(self, devices):
        if not self.search_value:
            return devices

        search = self.search_value.lower()

        return [
            item for item in devices
            if len(item["row"]) > 2 and search in item["row"][2].lower()
        ]
    
    def on_search(self, e):
        self.search_value = e.control.value
        self.update_()
        
def app_(page: ft.Page):
    #page.appbar =     
    
    async def close_app():
        await page.window.close()
    
    page.window.title_bar_hidden = True
    page.window.title_bar_buttons_hidden = True
    
    custom_title_bar = ft.WindowDragArea(
        content=ft.Container(
            padding=ft.Padding.symmetric(horizontal=5, vertical=5),
            content=ft.Row(
                controls=[
                    
                    ft.Text(
                        "Курсовая работа. Остапов Александр Владимирович.", 
                        size=16, 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.Colors.WHITE
                    ),
                    
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.MINIMIZE, 
                                icon_color=ft.Colors.WHITE,
                                on_click=lambda e: setattr(page.window, "minimized", True)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.EXIT_TO_APP, 
                                icon_color=ft.Colors.RED_ACCENT, 
                                on_click=close_app 
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  
            )
        )
    )

    page.add(custom_title_bar)
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window.width = 1600
    page.window.height = 1200
    #page.window.resizable = False

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    app_interface = App(page_=page)
    page.add(app_interface)
    
    