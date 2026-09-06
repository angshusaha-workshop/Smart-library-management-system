class Book:
    def __init__(self, book_id, title, author, category):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.available = True
        self.issued_to = None
        self.issue_date = None

    @property
    def availability(self):
        return self.available

    @availability.setter
    def availability(self, value):
        self.available = bool(value)

    def display_book(self):

        print("\n==============Book Details=============")

        print(f"Book ID: {self.book_id}")
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Category: {self.category}")
        print(f"Availability: {'Available' if self.availability else 'Not Available'}")

        if not self.availability:
            print(f"Issued To: {self.issued_to}")
            print(f"Issue Date: {self.issue_date}")

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "available": self.available,
            "issued_to": self.issued_to,
            "issue_date": self.issue_date
        }