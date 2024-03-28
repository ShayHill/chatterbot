
from pathlib import Path
from chatterbot import train_chatterbot, generate_chatter

training_file = Path(__file__, "../training_data/moby_dick.txt").resolve()

with training_file.open(encoding="utf-8") as f:
    training_text = f.read()

chain = train_chatterbot(training_text)
sentences = [generate_chatter(chain) for _ in range(10)]

for sentence in sentences:
    print(sentence + "\n\n")
