import flet as ft
import re
from html import escape


class Layout(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.bb_blockquote_re = re.compile(r"\[quote\](?P<line_content>.+?)\[/quote\]", flags=re.IGNORECASE + re.DOTALL)
        self.bb_italics_re = re.compile(r"\[i\](?P<line_content>.+?)\[/i\]", flags=re.IGNORECASE + re.DOTALL)
        self.bb_bold_re = re.compile(r"\[b\](?P<line_content>.+?)\[/b\]", flags=re.IGNORECASE + re.DOTALL)
        self.html_italics_re = re.compile(r"<em>(?P<line_content>.+?)</em>")
        self.html_bold_re = re.compile(r"<strong>(?P<line_content>.+?)</strong>")
        self.html_tag_re = re.compile(r"<[^>]+?>")
        self.html_doublelinebreak_re = re.compile(r"\n\s*\n")

    def build(self) -> ft.Column:
        self.input_textfield = ft.TextField(
            multiline=True,
            on_change=self.sync_text,
            expand=True,
            text_size=14,
            # border=ft.InputBorder.NONE,
            content_padding=ft.padding.only(),
        )
        self.display_text = ft.Text(
            selectable=True,
            expand=True,
            size=14,
        )

        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        self.input_textfield,
                        self.display_text,
                    ]
                )
            ],
        )

    def sync_text(self, e) -> None:
        content: str = e.data
        html_content: str = ""
        content = escape(content)
        content = self.bb_blockquote_re.sub(r"<blockquote>\n\n\g<line_content>\n\n</blockquote>\n\n", content)
        content = self.bb_italics_re.sub(r"<em>\g<line_content></em>", content)
        content = self.bb_bold_re.sub(r"<strong>\g<line_content></strong>", content)
        in_italics: bool = False
        in_bold: bool = False
        for line in self.html_doublelinebreak_re.split(content):
            line = line.strip()
            if in_italics:
                line = f"<em>{line}"
            if "<em>" in self.html_italics_re.sub(r"\g<line_content>", line):
                in_italics = True
                line = f"{line}</em>"
            else:
                in_italics = False
            if in_bold:
                line = f"<strong>{line}"
            if "<strong>" in self.html_bold_re.sub(r"\g<line_content>", line):
                in_bold = True
                line = f"{line}</strong>"
            else:
                in_bold = False
            if "[hr]" == line:
                line = "<hr />"
            elif "<blockquote>" == line or "</blockquote>" == line:
                pass
            else:
                line = f"<p>{line}</p>"
            line = line.replace("\n", "<br />")

            html_content += f"{line}\n"
        self.display_text.value = html_content
        self.update()


def main(page: ft.Page) -> None:
    page.title = "Convert BBCode to HTML"
    page.scroll = ft.ScrollMode.ALWAYS
    page.window_maximized = True
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    # Main Layout
    contents = Layout()
    page.add(contents)
    page.update()


ft.app(target=main)
