"""Import functions into the package namespace.

:author: ShayHill
:created: 2024-03-28
"""

from chatterbot.main import generate_chatter, train_chatterbot

__all__ = ["train_chatterbot", "generate_chatter"]
