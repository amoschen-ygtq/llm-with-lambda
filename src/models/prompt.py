from dataclasses import dataclass
from enum import StrEnum
from typing import List


class MessageType(StrEnum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


@dataclass
class Message:
    type: MessageType
    content: str


@dataclass
class Prompt:
    version: str
    messages: List[Message]
