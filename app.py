from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Static, Footer, Header
from utils import Tools
from rich.console import Group


class DomainChecker(App):
    CSS_PATH = "utils/styles.tcss"
    BINDINGS = [
        ("ctrl+c", "quit", "Close"),
        ("ctrl+r", "clear", "Clear"),
        ("shift+enter", "submit_response", "Submit"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.processed_domains = set()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Enter domains separated by comma...", id="input-field")
        yield VerticalScroll(Static(id="results"), id="results-container")
        yield Footer(id="footer")

    def action_submit_response(self):
        message = self.query_one(Input)
        self.lookup_word(message.value)
        self.query_one("#input-field", Input).value = ""

    def action_clear(self):
        self.query_one("#results", Static).update("")
        self.query_one("#input-field", Input).value = ""
        self.processed_domains.clear()

    def lookup_word(self, input_str: str) -> None:
        if input_str:
            domains = [d.strip() for d in input_str.split(",")]
            new_tables = []
            for domain in domains:
                if domain not in self.processed_domains:
                    self.processed_domains.add(domain)
                    new_tables.append(Tools.print_line(domain))

            if new_tables:
                results_widget = self.query_one("#results", Static)
                current_content = results_widget.renderable
                updated_content = Group(
                    *([current_content] if current_content else []) + new_tables
                )
                results_widget.update(updated_content)
        else:
            self.action_clear()


if __name__ == "__main__":
    app = DomainChecker()
    app.run()
