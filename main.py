import flet as ft
import re
from html import escape


class Layout(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.bb_blockquote_re = re.compile(r"\[quote\](?P<line_content>.+?)\[/quote\]", flags=re.IGNORECASE + re.DOTALL)
        self.bb_italics_re = re.compile(r"\[i\](?P<line_content>.+?)\[/i\]", flags=re.IGNORECASE + re.DOTALL)
        self.bb_bold_re = re.compile(r"\[b\](?P<line_content>.+?)\[/b\]", flags=re.IGNORECASE + re.DOTALL)
        self.html_italics_re = re.compile(r"<em>(?P<line_content>.+?)</em>")
        self.html_bold_re = re.compile(r"<strong>(?P<line_content>.+?)</strong>")
        self.html_tag_re = re.compile(r"<[^>]+?>")
        self.html_doublelinebreak_re = re.compile(r"\n\s*\n")

    def build(self) -> ft.Column:
        self.input_textfield = ft.TextField(
            label="BBCode",
            multiline=True,
            on_change=self.sync_text,
            expand=True,
            text_size=14,
            content_padding=ft.padding.only(),
        )
        self.display_text = ft.Text(
            selectable=True,
            expand=True,
            size=14,
        )
        self.scroll_to_top_button = ft.ElevatedButton(
            text="Scroll To Top",
            on_click=self.scroll_to_top,
        )

        self.column =  ft.Column(
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
                ),
                self.scroll_to_top_button,
            ],
        )
        return self.column

    def sync_text(self, e) -> None:
        content: str = e.data
        num_lines: int = len([i for i in content.split("\n") if i.strip()]) / 2
        if len(self.html_doublelinebreak_re.findall(content)) > num_lines: # If there are more than 50% of the content-containing lines double-spaced, then use double-spaced.
            self.display_text.value = self.double_spaced(e.data)
        else:
            self.display_text.value = self.single_spaced(e.data)
        self.scroll_to_top()
        self.update()

    def basic_html_convert(self, content: str) -> str:
        content = escape(content)
        content = self.bb_blockquote_re.sub(r"<blockquote>\n\n\g<line_content>\n\n</blockquote>\n\n", content)
        content = self.bb_italics_re.sub(r"<em>\g<line_content></em>", content)
        return self.bb_bold_re.sub(r"<strong>\g<line_content></strong>", content)

    def single_spaced(self, content: str) -> str:
        content = self.basic_html_convert(content)
        html_content: str = ""
        in_italics: bool = False
        in_bold: bool = False
        for line in content.split("\n"):            
            line = line.strip()
            if not line:
                line = "<br />"
                continue
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
            html_content += f"{line}\n"
        return html_content


    def double_spaced(self, content: str) -> str:
        content = self.basic_html_convert(content)
        html_content: str = ""
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
        return html_content

    def scroll_to_top(self, *_) -> None:
        self.page.scroll_to(offset=0, duration=1)
        self.update()


def main(page: ft.Page) -> None:
    page.title = "Convert BBCode to HTML"
    page.scroll = ft.ScrollMode.ALWAYS
    page.window_maximized = True
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    # Main Layout
    contents = Layout(page=page)
    page.add(contents)
    page.update()


ft.app(target=main)
