import os
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

import file_carver_gui
from ui_theme import COLORS, configure_styles, make_card


def create_dashboard(parent, navigate):
    page = ttk.Frame(parent)
    page.columnconfigure((0, 1), weight=1, uniform="feature")

    intro = ttk.Frame(page)
    intro.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(4, 20))
    ttk.Label(intro, text="Welcome to KarvIt", style="Welcome.TLabel").pack(anchor="w")
    ttk.Label(intro, text="Create a forensic image or recover files from an existing disk image.", style="Body.TLabel").pack(anchor="w", pady=(5, 0))

    features = [
        ("▤", "FeatureIconBlue.TLabel", "Disk Imager", "Create a disk image from a connected removable drive with a clearly selected destination.", "Open Disk Imager", "disk_imager"),
        ("⌕", "FeatureIconTeal.TLabel", "File Carver", "Recover PNG, JPEG, PDF, and EVTX files from an existing image.", "Open File Carver", "file_carver"),
    ]
    for column, (icon, icon_style, title, description, action, page_name) in enumerate(features):
        card = make_card(page, 20)
        card.grid(row=1, column=column, sticky="nsew", padx=(0, 10) if column == 0 else (10, 0))
        card.columnconfigure(0, weight=1)
        ttk.Label(card, text=icon, style=icon_style).grid(row=0, column=0, sticky="w", pady=(0, 12))
        ttk.Label(card, text=title, style="CardTitle.TLabel").grid(row=1, column=0, sticky="w")
        ttk.Label(card, text=description, style="CardBody.TLabel", wraplength=280, justify="left").grid(row=2, column=0, sticky="w", pady=(6, 18))
        ttk.Button(card, text=action, style="Primary.TButton", command=lambda name=page_name: navigate(name)).grid(row=3, column=0, sticky="w")

    note = ttk.Frame(page, style="StatusBand.TFrame", padding=(16, 12))
    note.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(16, 0))
    note.columnconfigure(1, weight=1)
    ttk.Label(note, text="●", style="Status.TLabel", background=COLORS["blue_soft"]).grid(row=0, column=0, rowspan=2, sticky="w", padx=(0, 10))
    ttk.Label(note, text="Workspace status", style="StatusBandTitle.TLabel").grid(row=0, column=1, sticky="w")
    ttk.Label(note, text="Processing stays on this device. No recovery history is stored between sessions.", style="StatusBand.TLabel").grid(row=1, column=1, sticky="w", pady=(2, 0))
    return page


def create_history_page(parent):
    page = ttk.Frame(parent)
    page.columnconfigure(0, weight=1)
    card = make_card(page, 20)
    card.pack(fill="x", pady=(4, 0))
    ttk.Label(card, text="◷", style="FeatureIconBlue.TLabel").pack(anchor="w", pady=(0, 12))
    ttk.Label(card, text="No recovery history yet", style="CardTitle.TLabel").pack(anchor="w")
    ttk.Label(card, text="Runs are not saved between sessions, so there are no records to display.", style="CardBody.TLabel", wraplength=680).pack(anchor="w", pady=(5, 0))
    return page


def create_about_page(parent):
    page = ttk.Frame(parent)
    page.columnconfigure((0, 1, 2), weight=1, uniform="about")
    intro = make_card(page, 20)
    intro.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(4, 14))
    ttk.Label(intro, text="KarvIt Digital Forensics", style="CardTitle.TLabel").pack(anchor="w")
    ttk.Label(intro, text="A focused desktop workspace for disk imaging and file recovery. Operations use the existing local tools and workflows.", style="CardBody.TLabel", wraplength=720, justify="left").pack(anchor="w", pady=(5, 0))

    capabilities = [
        ("01", "Acquisition", "Create an image from a connected removable drive."),
        ("02", "Recovery", "Carve PNG, JPEG, PDF, and EVTX signatures."),
        ("03", "Local workflow", "Select evidence and output locations on accessible drives."),
    ]
    for column, (number, title, description) in enumerate(capabilities):
        card = make_card(page, 16)
        card.grid(row=1, column=column, sticky="nsew", padx=(0, 6) if column == 0 else (6, 0))
        ttk.Label(card, text=number, style="CardEyebrow.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text=description, style="CardBody.TLabel", wraplength=180, justify="left").pack(anchor="w", pady=(5, 0))
    return page


def create_unavailable_page(parent, message):
    page = ttk.Frame(parent)
    card = make_card(page, 22)
    card.pack(fill="x", pady=(4, 0))
    ttk.Label(card, text="Disk Imager could not be loaded", style="CardTitle.TLabel").pack(anchor="w")
    ttk.Label(card, text=message, style="CardBody.TLabel", wraplength=650, justify="left").pack(anchor="w", pady=(6, 0))
    return page


def create_main_window():
    root = tk.Tk()
    root.title("KarvIt | Digital Forensics")
    root.geometry("1120x760")
    root.minsize(900, 680)
    root.configure(bg=COLORS["background"])
    configure_styles(root)

    logo_path = os.path.join(os.path.dirname(__file__), "Resources", "KarvIt_Logo.png")
    sidebar_logo = None
    if os.path.isfile(logo_path):
        with Image.open(logo_path) as source_logo:
            logo_image = source_logo.convert("RGBA")
        sidebar_logo = ImageTk.PhotoImage(logo_image.resize((170, 95), Image.Resampling.LANCZOS))
        window_icon = ImageTk.PhotoImage(logo_image.resize((96, 54), Image.Resampling.LANCZOS))
        root.iconphoto(True, window_icon)
        root._karvit_window_icon = window_icon

    shell = ttk.Frame(root)
    shell.pack(fill="both", expand=True)
    shell.columnconfigure(1, weight=1)
    shell.rowconfigure(0, weight=1)

    sidebar = ttk.Frame(shell, style="Sidebar.TFrame", padding=(14, 18))
    sidebar.grid(row=0, column=0, sticky="ns")
    sidebar.configure(width=230)
    sidebar.grid_propagate(False)
    sidebar.columnconfigure(0, weight=1)
    if sidebar_logo is not None:
        logo_label = ttk.Label(sidebar, image=sidebar_logo, background=COLORS["sidebar"])
        logo_label.image = sidebar_logo
        logo_label.grid(row=0, column=0, sticky="w", padx=(2, 0), pady=(4, 22))

    main_area = ttk.Frame(shell, padding=(32, 26, 32, 24))
    main_area.grid(row=0, column=1, sticky="nsew")
    main_area.columnconfigure(0, weight=1)
    main_area.rowconfigure(1, weight=1)

    header = ttk.Frame(main_area)
    header.grid(row=0, column=0, sticky="ew", pady=(0, 26))
    header.columnconfigure(0, weight=1)
    title_label = ttk.Label(header, text="Dashboard", style="Title.TLabel")
    title_label.grid(row=0, column=0, sticky="w")
    description_label = ttk.Label(header, text="Overview of your forensic tools and workspace.", style="Body.TLabel")
    description_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
    status = ttk.Label(header, text="●  LOCAL WORKSPACE", style="LocalStatus.TLabel")
    status.grid(row=0, column=1, rowspan=2, sticky="e", padx=(20, 0))

    viewport = ttk.Frame(main_area)
    viewport.grid(row=1, column=0, sticky="nsew")
    viewport.columnconfigure(0, weight=1)
    viewport.rowconfigure(0, weight=1)

    pages = {}
    page_info = {
        "dashboard": ("Dashboard", "Overview of your forensic tools and workspace."),
        "disk_imager": ("Disk Imager", "Create an image from a connected removable drive."),
        "file_carver": ("File Carver", "Recover known file types from a disk image."),
        "history": ("Recovery History", "Review recovery activity from this workspace."),
        "about": ("About KarvIt", "Application information and capabilities."),
    }
    nav_buttons = {}
    active_page = None

    def open_existing_image(path):
        show_page("file_carver")
        file_carver_gui.file_var.set(path)

    def set_nav_hover(name, is_hovered):
        item, indicator, icon_widget, button, icon, label = nav_buttons[name]
        is_active = name == active_page
        item.configure(style="NavItemActive.TFrame" if is_active else "NavItemHover.TFrame" if is_hovered else "NavItem.TFrame")
        icon_widget.configure(style="NavIconActive.TLabel" if is_active else "NavIconHover.TLabel" if is_hovered else "NavIcon.TLabel")

    def show_page(name):
        nonlocal active_page
        if name not in pages:
            if name == "dashboard":
                pages[name] = create_dashboard(viewport, show_page)
            elif name == "disk_imager":
                try:
                    import disk_imager_gui
                    pages[name] = disk_imager_gui.create_disk_imager_page(viewport, open_existing_image)
                except ModuleNotFoundError as error:
                    if error.name != "psutil":
                        raise
                    pages[name] = create_unavailable_page(viewport, "The existing Disk Imager requires psutil, which is not installed in this Python environment. No package was installed or project dependency changed.")
            elif name == "file_carver":
                pages[name] = file_carver_gui.create_file_carver_page(viewport)
            elif name == "history":
                pages[name] = create_history_page(viewport)
            else:
                pages[name] = create_about_page(viewport)
            pages[name].grid(row=0, column=0, sticky="nsew")
        for page in pages.values():
            page.grid_remove()
        pages[name].grid()
        active_page = name
        title, description = page_info[name]
        title_label.configure(text=title)
        description_label.configure(text=description)
        for key, (item, indicator, icon_widget, button, icon, label) in nav_buttons.items():
            active = key == name
            item.configure(style="NavItemActive.TFrame" if active else "NavItem.TFrame")
            indicator.configure(style="NavIndicatorActive.TFrame" if active else "NavIndicator.TFrame")
            icon_widget.configure(style="NavIconActive.TLabel" if active else "NavIcon.TLabel")
            button.configure(
                style="NavActive.TButton" if active else "Nav.TButton",
            )

    navigation = [
        ("dashboard", "◉", "Dashboard"),
        ("disk_imager", "▤", "Disk Imager"),
        ("file_carver", "⌕", "File Carver"),
        ("history", "◷", "Recovery History"),
        ("about", "ⓘ", "About"),
    ]
    for row, (name, icon, label) in enumerate(navigation, start=1):
        item = ttk.Frame(sidebar, style="NavItem.TFrame")
        item.grid(row=row, column=0, sticky="ew", pady=2)
        item.columnconfigure(2, weight=1)
        indicator = ttk.Frame(item, style="NavIndicator.TFrame", width=3)
        indicator.grid(row=0, column=0, sticky="ns", padx=(0, 8), pady=3)
        indicator.grid_propagate(False)
        icon_widget = ttk.Label(item, text=icon, style="NavIcon.TLabel", width=3, anchor="center")
        icon_widget.grid(row=0, column=1, sticky="ns", padx=(0, 3))
        button = ttk.Button(item, text=label, style="Nav.TButton", command=lambda key=name: show_page(key))
        button.grid(row=0, column=2, sticky="ew")
        nav_buttons[name] = (item, indicator, icon_widget, button, icon, label)
        hover_in = lambda _event, key=name: set_nav_hover(key, True)
        hover_out = lambda _event, key=name: set_nav_hover(key, False)
        navigate_click = lambda _event, key=name: show_page(key)
        item.bind("<Button-1>", navigate_click)
        icon_widget.bind("<Button-1>", navigate_click)
        for widget in (item, icon_widget, button):
            widget.bind("<Enter>", hover_in)
            widget.bind("<Leave>", hover_out)
    show_page("dashboard")
    root.mainloop()


if __name__ == "__main__":
    create_main_window()