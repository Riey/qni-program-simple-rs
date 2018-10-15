import ctypes
from ctypes import cdll, c_void_p, c_float, c_int, c_uint, c_char_p, c_uint16, c_ubyte, c_uint32, c_int32, c_size_t, byref, POINTER

TEXT_ALIGN_LEFT = 0
TEXT_ALIGN_RIGHT = 1
TEXT_ALIGN_CENTER = 2

FONT_STYLE_REGULAR = 0,
FONT_STYLE_ITALIC = 1,
FONT_STYLE_BOLD = 2,
FONT_STYLE_UNDERLINE = 4

QNI_ENTRY_CALLBACK = ctypes.CFUNCTYPE(None, c_void_p)


class QniEndError(Exception):
    pass


class QniBinding():
    def __init__(self, path: str):
        self.lib = cdll.LoadLibrary(path)

        self.lib.qni_init_program.argtypes = []
        self.lib.qni_init_program.restype = None

        self.lib.qni_hub_new.argtypes = [QNI_ENTRY_CALLBACK]
        self.lib.qni_hub_new.restype = c_void_p
        self.lib.qni_hub_exit.argtypes = [c_void_p]
        self.lib.qni_hub_delete.argtypes = [c_void_p]

        c_byte_p = c_char_p  # POINTER(c_ubyte)

        self.lib.qni_print.argtypes = [c_void_p, c_byte_p, c_size_t]
        self.lib.qni_print_line.argtypes = [c_void_p, c_byte_p, c_size_t]
        self.lib.qni_new_line.argtypes = [c_void_p]
        self.lib.qni_delete_line.argtypes = [c_void_p, c_uint32]
        self.lib.qni_set_font.argtypes = [
            c_void_p, c_byte_p, c_size_t, c_float, c_uint32]
        self.lib.qni_set_text_align.argtypes = [c_void_p, c_uint32]
        self.lib.qni_set_text_color.argtypes = [c_void_p, c_uint32]
        self.lib.qni_set_back_color.argtypes = [c_void_p, c_uint32]
        self.lib.qni_set_highlight_color.argtypes = [c_void_p, c_uint32]

        self.lib.qni_wait_int.argtypes = [c_void_p, POINTER(c_int32)]
        self.lib.qni_wait_int.restype = c_int32

        self.lib.qni_start_program.argtypes = [
            c_void_p, c_byte_p, c_size_t]

        self.lib.qni_start_program.restype = c_int32

    def init_program(self):
        self.lib.qni_init_program()

    def hub_new(self, entry: QNI_ENTRY_CALLBACK):
        return self.lib.qni_hub_new(entry)

    def hub_exit(self, hub: c_void_p):
        self.lib.qni_hub_exit(hub)

    def hub_delete(self, hub: c_void_p):
        self.lib.qni_hub_delete(hub)

    def wait_int(self, ctx: c_void_p):
        ret = c_int32()

        if self.lib.qni_wait_int(ctx, byref(ret)) is -1:
            raise QniEndError()

        return ret.value

    def print(self, ctx: c_void_p, text: str):
        text = text.encode('utf-8')
        if self.lib.qni_print(ctx, text, len(text)) is -1:
            raise QniEndError()

    def print_line(self, ctx: c_void_p, text: str):
        text = text.encode('utf-8')
        if self.lib.qni_print_line(
                ctx, text, len(text)) is -1:
            raise QniEndError()

    def new_line(self, ctx: c_void_p):
        if self.lib.qni_new_line(ctx) is -1:
            raise QniEndError()

    def delete_line(self, ctx: c_void_p, count: int):
        if self.lib.qni_delete_line(ctx, count) is -1:
            raise QniEndError()

    def set_font(self, ctx: c_void_p, font_family: str, font_size: float, font_style: int):
        font_family = font_family.encode('utf-8')
        if self.lib.qni_set_font(ctx, font_family, len(
                font_family), font_size, font_style) is -1:
            raise QniEndError()

    def set_text_align(self, ctx: c_void_p, align: int):
        if self.lib.qni_set_text_align(ctx, align) is -1:
            raise QniEndError()

    def set_text_color(self, ctx: c_void_p, color: int):
        if self.lib.qni_set_text_color(ctx, color) is -1:
            raise QniEndError()

    def set_back_color(self, ctx: c_void_p, color: int):
        if self.lib.qni_set_back_color(ctx, color) is -1:
            raise QniEndError()

    def set_highlight_color(self, ctx: c_void_p, color: int):
        if self.lib.qni_set_highlight_color(ctx, color) is -1:
            raise QniEndError()

    def connector_ws_start(self, hub: c_void_p, host: str):
        host = host.encode('utf-8')
        return self.lib.qni_start_program(hub, host, len(host))
