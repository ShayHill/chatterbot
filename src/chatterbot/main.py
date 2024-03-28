from typing import TypeVar, TypeAlias
import enum
import random


class Position(enum.Enum):
    """Parts of a sentence that are not words."""

    BEGIN_SENTENCE = enum.auto()
    END_SENTENCE = enum.auto()



# {word: {possible_next_word: count, another_possible_next_word: count, ...}, ...}
_MarkovChain: TypeAlias = dict[str | Position, dict[str | Position, int]]


_T = TypeVar("_T")

def pick_next_node(choices: list[_T], ps: list[int], selection: int) -> _T:
    """A simplified version of np.random.choice just to save the dependency.

    :param choices: The choices to select from, representing the next node to move to.
    :param ps: how many times this node was moved to in the training text.
    :param selection: a random number used to select the next node. [0, sum(ps)]
    """
    accum = 0
    for choice, prob in zip(choices, ps):
        accum += prob
        if selection < accum:
            return choice
    msg = "CDF values do not sum to selection value."
    raise ValueError(msg)


def clean_word(word: str | Position) -> str | Position:
    """Cleans a word for use in a markov chain.

    This is simple, so we're ignoring capitalization and punctiation when selecting
    the next likely word.
    """
    if isinstance(word, Position):
        return word
    return word.lower().strip().strip(".,?!;:()[]{}\"'ΓÇ£ΓÇ¥ΓÇö")


def train_chatterbot(text: str) -> dict[str | Position, dict[str | Position, int]]:
    """Generate a markov chain from the given text."""
    chain: _MarkovChain = {}
    prev_word: str | Position = Position.BEGIN_SENTENCE

    def add_word(word: str | Position):
        nonlocal prev_word
        if prev_word is Position.END_SENTENCE:
            prev_word = Position.BEGIN_SENTENCE

        text_only = clean_word(word)
        prev_node = chain.setdefault(prev_word, {})
        prev_node[text_only] = prev_node.get(text_only, 0) + 1
        prev_word = text_only

    for word in text.split():
        add_word(word)
        if word.endswith((".", "!", "?")):
            add_word(Position.END_SENTENCE)

    return chain


def generate_chatter(chain: _MarkovChain) -> str:
    """Generate one sentence from a markov chain."""
    sentence: list[str] = []
    word: str | Position = Position.BEGIN_SENTENCE
    while word is not Position.END_SENTENCE:
        next_words = chain[word].keys()
        probabilities = chain[word].values()
        selection = random.randint(1, sum(probabilities)) - 1
        word = pick_next_node(list(next_words), list(probabilities), selection)
        if word is not Position.END_SENTENCE:
            assert isinstance(word, str)
            sentence.append(word)
    return " ".join(sentence)
