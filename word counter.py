import re

class WordCounter:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, 'r')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def __iter__(self):
        return self

    def __next__(self):
        text = self.file.read()
        if not text:
            raise StopIteration

        text = re.sub(r'[^\w\s]', '', text.lower())
        words = text.split()
        return len(words)

with WordCounter('words.txt') as file:
    for word in file:
        print(word)
