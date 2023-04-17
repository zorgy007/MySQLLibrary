class Book:
    def __init__(self, title: str, year: int, author: str):
        self.title = title
        self.year = year
        self.author = author

    def __str__(self):
        return f'{self.title}, {self.author}, {self.year}'

    def __repr__(self):
        return f'{self.title}, {self.author}, {self.year}'
