# chatterbot

A simple AI to create random-ish sentences that almost make sense. This is AI principles without neural nets, support vector machines, SciKit Learn, etc.

Generate a Markov Chain from text. That is, for each word, store the words that follow it in the text along with how many times they follow it. This will be clear with an example.

`train_chatterbot("The cat chased the bird and the dog chased the cat. The end.")`

Will yield

```
{
    <Position.BEGIN_SENTENCE: 1>: {'the': 2},
    'the': {'cat': 2, 'bird': 1, 'dog': 1, 'end': 1},
    'cat': {'chased': 1, <Position.END_SENTENCE: 2>: 1},
    'chased': {'the': 2},
    'bird': {'and': 1},
    'and': {'the': 1},
    'dog': {'chased': 1},
    'end': {<Position.END_SENTENCE: 2>: 1}
}
```

To pick one example, the word "the" is followed twice in the training text by "cat" and once each by "bird", "dog", and "end".

To improve this just a bit, I added a "begin sentence" and "end sentence" tokens to the text. This will allow the AI to pick sensible words to start a sentence and for the sentence to eventually end.

## These are the kinds of sentences you can expect after training this with your favorite book:

* but I take him for a marshall's baton
* not make nevertheless it with a crazed old whales in particular about the first
* thou art of his firm thing
* a continuous chain of decanting
* all hands and peered down with an inch in the shock was on and through toil but to the last accounts
* now for hate’s sake and leaving that can’t spare boats touched there tied to establish himself and furnished with the very fat
* it was soon the following titles the light though placed the heaviest storage of that he looked like two bones now sheltered it was foremost
* have to madness and so that wounded he might often hears he was turned upon which otherwise distrusted but slightly marked through the fruits of them
* he had evinced by the miracle which is it
* not the business and seeing that under even then again
* but unlike the same way an uncommon elevation indeed he demanded but nothing to account no more curious story about moby dick moved on one

Check out `example.py` if you want to play with it.

## How could we make that better?

The results would be a lot clearer if we looked back *two* words. Instead of selecting from words that come after "the", we could select from words that come after "of the", "all the", "up the", or "over the". We could do even better looking back 3 words then 4 then 5. We could also improve by adding "begin paragraph", "end paragraph", "begin quote", "end chapter", etc. to our text-positon indicators.

The easy problem is coding this and parsing it fast enough. Again, that's the easy problem. The hard problem is finding enough data to train. Moby Dick contains about 22,000 unique single words. 12,000 (more than half) are always followed by a specific word. For instance, "reticule" is only used once, followed by "where"; "insomuch" is used twice, but both times followed by "that"; "restricted", "confined", and "referred" are each used at least three times, but always followed by "to".

Even when those word pairs don't feel restrictive, they are nevertheless points where the algorithm is deterministic, and as you examine longer groups of words to make predictions, more and more of *those* predictions will become deterministic. You will quickly end up back at "The cat chased the bird and the dog chased the cat. The end".

There are mitigations for this, but that's a story for another day. The point is that there *is* a limit, and it's not processor speed.

