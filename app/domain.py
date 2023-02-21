import dataclasses
import re
from dataclasses import dataclass
from typing import Any, List, Dict


@dataclass
class ScrapedWebsite:
    website: str
    logo: Any
    phones: Any

    def __post_init__(self):
        """
        Post-initialization method that gets executed after the dataclass is initialized.
        This method sanitizes the phone numbers and retrieves the URL for the website's logo.
        """
        self.phones: List = self._sanitize_phone_numbers()
        self.logo: str = self._get_url_logo(self.logo, self.website)

    def _sanitize_phone_numbers(self) -> List:
        """
        Helper method that extracts phone numbers from the given input and returns a list of sanitized phone numbers.

        Returns:
            List: A list of sanitized phone numbers.
        """
        regex = re.compile(r"(\+?\d[\d\s]*\d|\(?\d+\)?[\d\s]*\d+|\d{4}[\s]*\d{4})")
        return [match.group() for tag in self.phones for match in [regex.search(tag["href"])] if match]

    @classmethod
    def _get_url_logo(cls, logos: Any, url: str) -> str:
        """
        Helper method that retrieves the URL for the website's logo from the given input.

        Args:
            logos (Any): The input logo data.
            url (str): The URL of the website.

        Returns:
            str: The URL for the website's logo.
        """
        for logo in logos:
            if "src" not in logo.attrs or logo["src"].startswith("data:"):
                continue
            if logo["src"].startswith("http"):
                return logo["src"]
            else:
                src_url = logo["src"].lstrip("/")
                logo_url = f"{url}{src_url}"
                return logo_url
        return ""

    def as_a_dict(self) -> Dict:
        """
        Returns the dataclass as a dictionary.

        Returns:
            Dict: The dataclass as a dictionary.
        """
        return dataclasses.asdict(self)
