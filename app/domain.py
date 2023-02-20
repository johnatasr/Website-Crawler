import dataclasses
from dataclasses import dataclass, field
from typing import List


@dataclass
class ScrapedWebsite:

    website: str
    logo: str
    phones: List
    regex_pattern: object

    def __post_init__(self):
        self.phones = [self._sanitize_phone_number(number) for number in self.phones]

    def set_regex_compile(self, regex_pattern):
        self.regex_pattern = regex_pattern

    def _sanitize_phone_number(self, number) -> str:
        replacement_text = "PHONE_NUMBER_REMOVED"
        return self.regex_pattern.sub(replacement_text, number)

    def as_a_dict(self):
        return dataclasses.asdict(self)

