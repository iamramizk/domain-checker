import re
import socket
from rich.table import Table
from rich import box
from urllib.parse import urlparse

from rich.console import Console

console = Console()


class Tools:
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Checks if a string is a valid URL"""

        # Regular expression for validating a URL
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"|^"  # or start of string for URLs without a scheme
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+"  # domain
            r"(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain extension
            r"localhost|"  # localhost
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # ipv4
            r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # ipv6
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)?$",  # optional path
            re.IGNORECASE,
        )

        return re.match(regex, url) is not None

    @staticmethod
    def get_short_url(url: str) -> str | None:
        """Gets the short url without full path or schema"""
        # Add scheme if missing
        if not urlparse(url).scheme:
            url = "https://" + url

        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith("www."):
            domain = domain[4:]
        return domain

    @staticmethod
    def is_domain_available(domain):
        """
        Checks if a domain is available by attempting to connect to it.
        Returns True if the domain is available, False otherwise.
        """
        try:
            # Try to connect to the domain on port 80 (HTTP)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # Set a timeout of 5 seconds
            sock.connect((domain, 80))
            sock.close()
            return False  # If we can connect, the domain is taken
        except socket.error:
            return True  # If we can't connect, the domain is available

    @staticmethod
    def print_line(domain: str) -> Table:
        if not Tools.is_valid_url(domain):
            status = "[bold wheat4]Invalid Domain[/bold wheat4]"
        else:
            domain = Tools.get_short_url(domain)
            status = (
                "[bold orange1]Available[/bold orange1]"
                if Tools.is_domain_available(domain)
                else "[bold orange4]Not Avaialble[/bold orange4]"
            )
        table = Table(
            show_header=False,
            box=box.SIMPLE,
        )
        table.add_column("domain", width=50)
        table.add_column("status")
        table.add_row(domain, status)
        # console.print(table)
        return table
