import ctypes
import os
from ctypes import wintypes
from tkinter import font as tkfont
from tkinter import ttk


COLORS = {
    "background": "#F5F7FB",
    "sidebar": "#FFFFFF",
    "surface": "#FFFFFF",
    "surface_alt": "#F8FAFD",
    "border": "#E5EAF2",
    "text": "#172033",
    "muted": "#667085",
    "blue": "#356AE6",
    "blue_hover": "#2859CD",
    "blue_soft": "#EDF3FF",
    "teal": "#0D9488",
    "teal_soft": "#E8F6F4",
    "success": "#15803D",
    "warning": "#B45309",
    "error": "#DC2626",
    "body": "#4B5563",
}


FONT_FALLBACKS = {
    "ui": ("Inter", "Segoe UI Variable", "Segoe UI", "system-ui", "sans-serif"),
    "mono": ("JetBrains Mono", "Consolas", "monospace"),
    "symbols": ("Segoe UI Symbol", "Segoe UI", "sans-serif"),
}

TYPOGRAPHY = {
    "page_title": {"size_px": 28, "weight": 700, "line_height": 1.2},
    "section_heading": {"size_px": 22, "weight": 600, "line_height": 1.2},
    "card_title": {"size_px": 18, "weight": 600, "line_height": 1.2},
    "body": {"size_px": 14, "weight": 400, "line_height": 1.5, "color": COLORS["body"]},
    "sidebar_nav": {"size_px": 14, "weight": 500},
    "sidebar_nav_active": {"size_px": 14, "weight": 600},
    "button": {"size_px": 14, "weight": 600},
    "badge": {"size_px": 12, "weight": 600, "letter_spacing": 0.5, "uppercase": True},
    "supporting": {"size_px": 12, "weight": 400},
    "monospace": {"size_px": 13, "weight": 400},
    "feature_icon": {"size_px": 17, "weight": 400},
    "nav_icon": {"size_px": 12, "weight": 400},
}

_REGISTERED_FONT_PATHS = set()
_FONT_WEIGHT_FAMILIES = {}


def _load_bundled_fonts(root):
    if os.name != "nt":
        return
    font_directory = os.path.join(os.path.dirname(__file__), "Resources", "fonts")
    add_font = ctypes.windll.gdi32.AddFontResourceExW
    add_font.argtypes = (wintypes.LPCWSTR, wintypes.DWORD, wintypes.LPVOID)
    add_font.restype = ctypes.c_int
    loaded_paths = []
    for filename in ("InterVariable.ttf", "JetBrainsMono.ttf"):
        path = os.path.join(font_directory, filename)
        if path not in _REGISTERED_FONT_PATHS and os.path.isfile(path):
            if add_font(path, 0x10, None):
                _REGISTERED_FONT_PATHS.add(path)
        if path in _REGISTERED_FONT_PATHS:
            loaded_paths.append(path)
    root._karvit_bundled_fonts = tuple(loaded_paths)


def _resolve_family(root, candidates):
    available = {family.casefold(): family for family in tkfont.families(root)}
    for candidate in candidates:
        match = available.get(candidate.casefold())
        if match:
            return match
        if candidate == "Segoe UI Variable":
            for variant in ("Segoe UI Variable Text", "Segoe UI Variable Display"):
                match = available.get(variant.casefold())
                if match:
                    return match
    return tkfont.nametofont("TkDefaultFont", root=root).actual("family")


def _font(family, token):
    spec = TYPOGRAPHY[token]
    weighted_family = _FONT_WEIGHT_FAMILIES.get((family, spec["weight"]))
    if weighted_family:
        return (weighted_family, -spec["size_px"], "normal")
    weight = "bold" if spec["weight"] >= 600 else "normal"
    return (family, -spec["size_px"], weight)


def font_for(root, token, family_kind="ui"):
    _load_bundled_fonts(root)
    family = _resolve_family(root, FONT_FALLBACKS[family_kind])
    return _font(family, token)


def configure_styles(root):
    _load_bundled_fonts(root)
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    ui_font = _resolve_family(root, FONT_FALLBACKS["ui"])
    mono_font = _resolve_family(root, FONT_FALLBACKS["mono"])
    symbol_font = _resolve_family(root, FONT_FALLBACKS["symbols"])
    global _FONT_WEIGHT_FAMILIES
    available_families = {family.casefold(): family for family in tkfont.families(root)}
    _FONT_WEIGHT_FAMILIES = {}
    for family in {ui_font, mono_font}:
        for weight, suffixes in ((500, (" Medium",)), (600, (" SemiBold", " Semibold", " Medium"))):
            for suffix in suffixes:
                variant = available_families.get(f"{family}{suffix}".casefold())
                if variant:
                    _FONT_WEIGHT_FAMILIES[(family, weight)] = variant
                    break

    style.configure("TFrame", background=COLORS["background"])
    style.configure("Sidebar.TFrame", background=COLORS["sidebar"])
    style.configure(
        "Card.TFrame",
        background=COLORS["surface"],
        bordercolor=COLORS["border"],
        borderwidth=1,
        relief="solid",
    )
    style.configure("Surface.TFrame", background=COLORS["surface"], bordercolor=COLORS["border"], borderwidth=1, relief="solid")
    style.configure("StatusBand.TFrame", background=COLORS["blue_soft"])
    style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text"], font=_font(ui_font, "body"))
    style.configure("Title.TLabel", font=_font(ui_font, "page_title"), foreground=COLORS["text"])
    style.configure("Heading.TLabel", font=_font(ui_font, "section_heading"), foreground=COLORS["text"])
    style.configure("Welcome.TLabel", font=_font(ui_font, "section_heading"), foreground=COLORS["text"])
    style.configure("Body.TLabel", font=_font(ui_font, "body"), foreground=COLORS["body"])
    style.configure("Small.TLabel", font=_font(ui_font, "supporting"), foreground=COLORS["muted"])
    style.configure("Brand.TLabel", background=COLORS["sidebar"], font=_font(ui_font, "card_title"), foreground=COLORS["text"])
    style.configure("SidebarSmall.TLabel", background=COLORS["sidebar"], font=_font(ui_font, "badge"), foreground=COLORS["muted"])
    style.configure("CardTitle.TLabel", background=COLORS["surface"], font=_font(ui_font, "card_title"), foreground=COLORS["text"])
    style.configure("CardBody.TLabel", background=COLORS["surface"], font=_font(ui_font, "body"), foreground=COLORS["body"])
    style.configure("CardSmall.TLabel", background=COLORS["surface"], font=_font(ui_font, "supporting"), foreground=COLORS["muted"])
    style.configure("CardHeading.TLabel", background=COLORS["surface"], font=_font(ui_font, "section_heading"), foreground=COLORS["text"])
    style.configure("Eyebrow.TLabel", font=_font(ui_font, "badge"), foreground=COLORS["muted"])
    style.configure("CardEyebrow.TLabel", background=COLORS["surface"], font=_font(ui_font, "badge"), foreground=COLORS["muted"])
    style.configure("Status.TLabel", font=_font(ui_font, "badge"), foreground=COLORS["success"])
    style.configure("Success.TLabel", foreground=COLORS["success"])
    style.configure("Warning.TLabel", foreground=COLORS["warning"])
    style.configure("Error.TLabel", foreground=COLORS["error"])
    style.configure("CardSuccess.TLabel", background=COLORS["surface"], foreground=COLORS["success"], font=_font(ui_font, "body"))
    style.configure("CardWarning.TLabel", background=COLORS["surface"], foreground=COLORS["warning"], font=_font(ui_font, "body"))
    style.configure("CardError.TLabel", background=COLORS["surface"], foreground=COLORS["error"], font=_font(ui_font, "body"))
    style.configure("StatusBand.TLabel", background=COLORS["blue_soft"], foreground=COLORS["body"], font=_font(ui_font, "body"))
    style.configure("StatusBandTitle.TLabel", background=COLORS["blue_soft"], foreground=COLORS["text"], font=_font(ui_font, "badge"))
    style.configure("LocalStatus.TLabel", background=COLORS["teal_soft"], foreground=COLORS["teal"], font=_font(ui_font, "badge"), padding=(10, 6))
    style.configure("FeatureIconBlue.TLabel", background=COLORS["blue_soft"], foreground=COLORS["blue"], font=_font(symbol_font, "feature_icon"), padding=(7, 3))
    style.configure("FeatureIconTeal.TLabel", background=COLORS["teal_soft"], foreground=COLORS["teal"], font=_font(symbol_font, "feature_icon"), padding=(7, 3))
    style.configure("CardMono.TLabel", background=COLORS["surface"], foreground=COLORS["text"], font=_font(mono_font, "monospace"))

    style.configure("TButton", font=_font(ui_font, "button"), padding=(12, 8), background=COLORS["surface"], foreground=COLORS["text"], bordercolor=COLORS["border"], borderwidth=1, relief="flat")
    style.map("TButton", background=[("disabled", COLORS["surface_alt"]), ("active", COLORS["surface_alt"])], foreground=[("disabled", COLORS["muted"]), ("active", COLORS["text"])])
    style.configure("Primary.TButton", font=_font(ui_font, "button"), background=COLORS["blue"], foreground="#FFFFFF", bordercolor=COLORS["blue"], borderwidth=0, relief="flat", padding=(14, 9))
    style.map("Primary.TButton", background=[("disabled", "#C9D6F3"), ("active", COLORS["blue_hover"])], foreground=[("disabled", "#FFFFFF")])
    style.configure("Secondary.TButton", font=_font(ui_font, "button"), background=COLORS["surface"], foreground=COLORS["blue"], bordercolor=COLORS["border"], borderwidth=1, relief="flat", padding=(12, 8))
    style.map("Secondary.TButton", background=[("active", COLORS["blue_soft"])])
    style.configure("Subtle.TButton", font=_font(ui_font, "button"), background=COLORS["background"], foreground=COLORS["muted"], borderwidth=0, relief="flat", padding=(10, 7))
    style.map("Subtle.TButton", background=[("active", COLORS["blue_soft"])], foreground=[("active", COLORS["blue"])])
    style.configure("Nav.TButton", anchor="w", font=_font(ui_font, "sidebar_nav"), padding=(12, 9), background=COLORS["sidebar"], foreground=COLORS["muted"], borderwidth=0, relief="flat")
    style.configure("Nav.TButton", focuscolor=COLORS["sidebar"], focusthickness=0)
    style.map("Nav.TButton", background=[("disabled", COLORS["sidebar"]), ("active", COLORS["surface_alt"])], foreground=[("disabled", COLORS["muted"]), ("active", COLORS["text"])])
    style.configure("NavActive.TButton", anchor="w", font=_font(ui_font, "sidebar_nav_active"), padding=(10, 9), background=COLORS["blue_soft"], foreground=COLORS["blue"], borderwidth=0, relief="flat", focuscolor=COLORS["blue_soft"], focusthickness=0)
    style.map("NavActive.TButton", background=[("active", COLORS["blue_soft"])], foreground=[("active", COLORS["blue"])])
    style.configure("NavItem.TFrame", background=COLORS["sidebar"])
    style.configure("NavItemHover.TFrame", background=COLORS["surface_alt"])
    style.configure("NavItemActive.TFrame", background=COLORS["blue_soft"])
    style.configure("NavIndicator.TFrame", background=COLORS["sidebar"])
    style.configure("NavIndicatorActive.TFrame", background=COLORS["blue"])
    style.configure("NavIcon.TLabel", background=COLORS["sidebar"], foreground=COLORS["muted"], font=_font(symbol_font, "nav_icon"))
    style.configure("NavIconHover.TLabel", background=COLORS["surface_alt"], foreground=COLORS["text"], font=_font(symbol_font, "nav_icon"))
    style.configure("NavIconActive.TLabel", background=COLORS["blue_soft"], foreground=COLORS["blue"], font=_font(symbol_font, "nav_icon"))
    style.configure("Field.TEntry", fieldbackground=COLORS["surface"], foreground=COLORS["text"], insertcolor=COLORS["text"], bordercolor=COLORS["border"], padding=(10, 8), font=_font(ui_font, "body"))
    style.configure("FieldMono.TEntry", fieldbackground=COLORS["surface"], foreground=COLORS["text"], insertcolor=COLORS["text"], bordercolor=COLORS["border"], padding=(10, 8), font=_font(mono_font, "monospace"))
    style.map("Field.TEntry", bordercolor=[("focus", COLORS["blue"])], fieldbackground=[("disabled", COLORS["surface_alt"])])
    style.configure("TCombobox", font=_font(ui_font, "body"), fieldbackground=COLORS["surface"], foreground=COLORS["text"], background=COLORS["surface"], arrowcolor=COLORS["muted"], bordercolor=COLORS["border"], padding=(8, 7))
    style.map("TCombobox", fieldbackground=[("readonly", COLORS["surface"])], selectbackground=[("readonly", COLORS["blue_soft"])], selectforeground=[("readonly", COLORS["text"])], bordercolor=[("focus", COLORS["blue"])])
    style.configure("TSeparator", background=COLORS["border"])
    return style


def make_card(parent, padding=20):
    return ttk.Frame(parent, style="Card.TFrame", padding=padding)