import json
import random
from datetime import datetime
from pathlib import Path
from book import Book
from member import Member


DATA_DIR = Path(__file__).resolve().parent


class Library:

    def __init__(self):
        self.books = []
        self.members = []

        self.load_books()
        self.load_members()



#=======================Book section=========================



    def add_book(self):
        print("\n===== Add New Book =====")

        book_id = input("Enter Book ID: ").strip()

        if book_id == "":
            print("Book ID cannot be empty.")
            return

        for book in self.books:
            if book.book_id == book_id:
                print("Book ID already exists. Please use a unique ID.")
                return
            
        title = input("Enter Book Title: ").strip()

        if title == "":
            print("Book title cannot be empty.")
            return
        
        author = input("Enter Author Name: ").strip()

        if author == "":
            print("Author name cannot be empty.")
            return
        
        category = input("Enter Book Category: ").strip()

        if category == "":
            print("Book category cannot be empty.")
            return

        book = Book(book_id, title, author, category)

        self.books.append(book)
        self.save_books()

        self.log_activity(
            f"Book {book.book_id} added"
        )

        print("\nBook added successfully!")

    def view_books(self):
        print("\n===== All Books =====")

        if len(self.books) == 0:
            print("No books available.")
            return

        for book in self.books:
            book.display_book()

    def search_book(self):
        print("\n===== Search Book =====")

        search_text = input(
            "Enter book title, author, or book ID: "
        ).strip().lower()

        if search_text == "":
            print("Search text cannot be empty.")
            return

        found = False

        for book in self.books:

            if (
                search_text in book.book_id.lower()
                or search_text in book.title.lower()
                or search_text in book.author.lower()
                or search_text in book.category.lower()
            ):
                book.display_book()
                found = True

        if not found:
            print("No matching book found.")
            

    def save_books(self):
        books_data = []

        for book in self.books:
            books_data.append(book.to_dict())

        with open(DATA_DIR / "database.json", "w") as file:
            json.dump(books_data, file, indent=4)

    def load_books(self):
        try:
            with open(DATA_DIR / "database.json", "r") as file:
                books_data = json.load(file)

            for data in books_data:
                book = Book(
                    data["book_id"],
                    data["title"],
                    data["author"],
                    data["category"]
                )

                book.available = data.get(
                    "available",
                    data.get("availability", True)
                )
                book.issued_to = data.get("issued_to", None)
                book.issue_date = data.get("issue_date", None)

                self.books.append(book)

        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []


    def update_book(self):
        print("\n===== Update Book =====")

        book_id = input("Enter Book ID to update: ").strip()

        selected_book = None

        for book in self.books:
            if book.book_id == book_id:
                selected_book = book
                break

        if selected_book is None:
            print("Book not found.")
            return

        print("\nLeave a field empty if you don't want to update it.")

        title = input("Enter new title: ").strip()
        author = input("Enter new author: ").strip()
        category = input("Enter new category: ").strip()

        if title:
            selected_book.title = title
        if author:
            selected_book.author = author
        if category:
            selected_book.category = category

        self.save_books()

        self.log_activity(
            f"Book {selected_book.book_id} updated"
        )

        print("\nBook updated successfully!")


    def delete_book(self):
        print("\n===== Delete Book =====")

        book_id = input("Enter Book ID to delete: ").strip()

        selected_book = None

        for book in self.books:
            if book.book_id == book_id:
                selected_book = book
                break

        if selected_book is None:
            print("Book not found.")
            return

        if not selected_book.available:
            print("This book is currently issued.")
            print("Return the book before deleting it.")
            return

        confirmation = input(
            "Are you sure you want to delete this book? (yes/no): "
        ).lower()

        if confirmation != "yes":
            print("Book deletion canceled.")
            return

        self.books.remove(selected_book)
        self.save_books()

        self.log_activity(
            f"Book {selected_book.book_id} deleted"
        )

        print("\nBook deleted successfully!")



#=========================Member section=========================



    def register_member(self):
        print("\n===== Register Member =====")

        member_id = input("Enter Member ID: ").strip()

        if member_id == "":
            print("Member ID cannot be empty.")
            return
        for member in self.members:
            if member.member_id == member_id:
                print("Member ID already exists.")
                return
            
        name = input("Enter Member Name: ").strip()

        if name == "":
            print("Member name cannot be empty.")
            return
        
        phone = input("Enter Phone Number: ").strip()

        if phone == "":
            print("Phone number cannot be empty.")
            return
        

        member = Member(member_id, name, phone)

        self.members.append(member)

        self.save_members()

        self.log_activity(
            f"Member {member.member_id} registered"
        )

        print("\nMember registered successfully!")

    def update_member(self):
        print("\n===== Update Member =====")
    
        member_id = input("Enter Member ID to update: ").strip()

        selected_member=None

        for member in self.members:
            if member.member_id == member_id:
                selected_member = member
                break

        if selected_member is None:
            print("Member not found.")
            return

        print("\nLeave a field empty if you don't want to update it.")

        name = input("Enter new name: ").strip()
        phone = input("Enter new phone number: ").strip()

        if name:
            selected_member.name = name
        if phone:
            selected_member.phone = phone

        self.save_members()

        self.log_activity(
            f"Member {selected_member.member_id} updated"
        )

        print("\nMember updated successfully!")

    def delete_member(self):
        print("\n===== Delete Member =====")

        member_id = input("Enter Member ID to delete: ").strip()

        selected_member = None

        for member in self.members:
            if member.member_id == member_id:
                selected_member = member
                break

        if selected_member is None:
            print("Member not found.")
            return

        for book in self.books:
            if book.issued_to == member_id:
                print("This member has issued books.")
                print("Return the books before deleting the member.")
                return

        confirmation = input(
            "Are you sure you want to delete this member? (yes/no): "
        ).lower()

        if confirmation != "yes":
            print("Member deletion canceled.")
            return

        self.members.remove(selected_member)
        self.save_members()
    
        self.log_activity(
            f"Member {selected_member.member_id} deleted"
        )

        print("\nMember deleted successfully!")

    def save_members(self):
        members_data = []

        for member in self.members:
            members_data.append(member.to_dict())

        with open(DATA_DIR / "members.json", "w") as file:
            json.dump(members_data, file, indent=4)

    def load_members(self):
        try:
            with open(DATA_DIR / "members.json", "r") as file:
                members_data = json.load(file)

            for data in members_data:
                member = Member(
                    data["member_id"],
                    data["name"],
                    data.get("phone", data.get("email", ""))
                )

                self.members.append(member)

        except (FileNotFoundError, json.JSONDecodeError):
            self.members = []

    def view_members(self):
        print("\n===== All Members =====")

        if len(self.members) == 0:
            print("No members registered.")
            return

        for member in self.members:
            member.display_member()

    def search_member(self):
        print("\n===== Search Member =====")

        search_text = input(
            "Enter member name or member ID: "
        ).strip().lower()

        if search_text == "":
            print("Search text cannot be empty.")
            return

        found = False

        for member in self.members:

            if (
                search_text in member.member_id.lower()
                or search_text in member.name.lower()
                or search_text in member.phone.lower()
            ):
                member.display_member()
                found = True

        if not found:
            print("No matching member found.")

    def issue_book(self):
        print("\n===== Issue Book =====")

        member_id = input("Enter Member ID: ").strip()
        book_id = input("Enter Book ID to issue: ").strip()

        if member_id == "":
            print("Member ID cannot be empty.")
            return
        if book_id == "":
            print("Book ID cannot be empty.")
            return

    
        selected_member = None

        for member in self.members:
            if member.member_id == member_id:
                selected_member = member
                break

        if selected_member is None:
            print("Member not found.")
            return

    
        selected_book = None

        for book in self.books:
            if book.book_id == book_id:
                selected_book = book
                break

        if selected_book is None:
            print("Book not found.")
            return

    
        if not selected_book.available:
            print("Book is currently not available for issue.")
            return

    
        selected_book.available = False
        selected_book.issued_to = member_id
        selected_book.issue_date = datetime.now().strftime("%Y-%m-%d")

        self.save_books()

        self.save_transaction(
            member_id,
            book_id,
            "Issued",
            fine=0
        )

        self.log_activity(
            f"Book {book_id} issued to member {member_id}"
        )

        print("\nBook issued successfully!")
        print(
            f"Member: {selected_member.name} "
            f"(ID: {selected_member.member_id})"
        )
        print(
            f"Book: {selected_book.title} "
            f"(ID: {selected_book.book_id})"
        )



#==========================Borrow section=========================



    def return_book(self):
        print("\n===== Return Book =====")

        book_id = input("Enter Book ID to return: ").strip()

        if book_id == "":
            print("Book ID cannot be empty.")
            return


        selected_book = None

        for book in self.books:
            if book.book_id == book_id:
                selected_book = book
                break

        if selected_book is None:
            print("Book not found.")
            return

        if selected_book.available:
            print("This book is not currently issued.")
            return

        member_id = selected_book.issued_to

        issue_date = datetime.strptime(
            selected_book.issue_date,
            "%Y-%m-%d"
        )

        return_date = datetime.now()

        days_kept = (return_date - issue_date).days

        allowed_days = 14
        fine_per_day = 5

        if days_kept > allowed_days:
            late_days = days_kept - allowed_days
            fine_amount = late_days * fine_per_day
        else:
            fine_amount = 0

    
        selected_book.available = True
        selected_book.issued_to = None
        selected_book.issue_date = None

        self.save_books()

        self.save_transaction(
            member_id,
            book_id,
            "Returned",
            fine_amount
        )

        self.log_activity(
            f"Book {book_id} returned by member {member_id}"
        )

        print("\nBook returned successfully!")
        print(
            f"Book: {selected_book.title} "
            f"(ID: {selected_book.book_id})"
        )
        print(f"Days Kept: {days_kept} days")
        print(f"Fine Amount: {fine_amount} Tk")

    def _load_transactions(self):
        try:
            with open(DATA_DIR / "transactions.json", "r") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_transaction(self,member_id,book_id,action,fine=0):

        if member_id is None or book_id is None:
            print("Member ID and Book ID cannot be empty.")
            return

        transactions = self._load_transactions()

        transaction = {
            "transaction_id": str(random.randint(100000, 999999)),
            "member_id": member_id,
            "book_id": book_id,
            "action": action,
            "fine": fine,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        transactions.append(transaction)

        with open(DATA_DIR / "transactions.json", "w") as file:
            json.dump(transactions, file,indent=4)

        print("\nTransaction saved successfully!")


    def view_transactions(self):
        print("\n===== All Transactions =====")

        try:
            with open(DATA_DIR / "transactions.json", "r") as file:
                transactions = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            print("No transactions found.")
            return

        if len(transactions) == 0:
            print("No transactions found.")
            return

        for transaction in transactions:
            print("\n------------------------")
            print(f"Transaction ID: {transaction['transaction_id']}")
            print(f"Member ID     : {transaction['member_id']}")
            print(f"Book ID       : {transaction['book_id']}")
            print(f"Action        : {transaction['action']}")
            print(f"Fine          : {transaction['fine']} Tk")
            print(f"Date          : {transaction['date']}")
           

    def member_history(self):
        print("\n===== Member Transaction History =====")

        member_id = input("Enter Member ID: ")

        member_found = False

        for member in self.members:
            if member.member_id == member_id:
                member_found = True
                break

        if not member_found:
            print("Member not found.")
            return

        try:
            with open(DATA_DIR / "transactions.json", "r") as file:
                transactions = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            print("No transactions found.")
            return

        found=False

        for transaction in transactions:
            
            if transaction["member_id"] == member_id:
                found=True
                print("\n------------------------")
                print(f"Transaction ID: {transaction['transaction_id']}")
                print(f"Book ID       : {transaction['book_id']}")
                print(f"Action        : {transaction['action']}")
                print(f"Fine          : {transaction['fine']} Tk")
                print(f"Date          : {transaction['date']}")

                found=True

        if not found:
            print("No transactions or borrowing history found for this member.")


    def recommend_books(self):
        print("\n===== Smart Book Recommendation =====")

        member_id = input("Enter Member ID: ").strip()

        selected_member = None

        for member in self.members:
            if member.member_id == member_id:
                selected_member = member
                break

        if selected_member is None:
            print("Member not found.")
            return

        try:
            with open(DATA_DIR / "transactions.json", "r") as file:
                transactions = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            print("No transaction history found.")
            return

        member_transactions = []

        for transaction in transactions:

            if transaction["member_id"] == member_id:
                member_transactions.append(transaction)

        if len(member_transactions) == 0:
            print("No borrowing history available.")
            return

        borrowed_book_ids = []

        for transaction in member_transactions:

            if transaction["action"] == "Issued":
                borrowed_book_ids.append(transaction["book_id"])

        if len(borrowed_book_ids) == 0:
            print("No borrowed books found.")
            return

        favorite_category = None
        favorite_author = None

        category_count = {}
        author_count = {}

        for book_id in borrowed_book_ids:

            for book in self.books:

                if book.book_id == book_id:

                    category = book.category
                    author = book.author

                    category_count[category] = (
                        category_count.get(category, 0) + 1
                    )

                    author_count[author] = (
                        author_count.get(author, 0) + 1
                    )

        if category_count:
            favorite_category = max(
                category_count,
                key=category_count.get
            )

        if author_count:
            favorite_author = max(
                author_count,
                key=author_count.get
            )

        recommendations = []

        for book in self.books:

            if not book.available:
                continue

            if book.book_id in borrowed_book_ids:
                continue

            score = 0

            if book.category == favorite_category:
                score += 50

            if book.author == favorite_author:
                score += 20

            issue_count = 0

            for transaction in transactions:

                if (
                    transaction["book_id"] == book.book_id
                    and transaction["action"] == "Issued"
                ):
                    issue_count += 1

            if issue_count >= 5:
                score += 20

            elif issue_count >= 2:
                score += 10

            else:
                score += 5

            recommendations.append((score, book))

        if len(recommendations) == 0:
            print("No suitable recommendations available.")
            return

        recommendations.sort(
            key=lambda item: item[0],
            reverse=True
        )

        print(f"\nMember: {selected_member.name}")
        print(f"Favorite Category: {favorite_category}")
        print(f"Favorite Author  : {favorite_author}")

        print("\n===== Recommended Books =====")

        count = 1

        for score, book in recommendations[:5]:

            print("\n----------------------------")
            print(f"Rank  : {count}")
            print(f"Book  : {book.title}")
            print(f"Author: {book.author}")
            print(f"Genre : {book.category}")
            print(f"Score : {score}/100")


            count += 1

    def popularity_report(self):
        print("\n===== Library Popularity Report =====")
        transactions = self._load_transactions()
        issued_transactions = [
            transaction for transaction in transactions
            if transaction.get("action") == "Issued"
        ]

        if not issued_transactions:
            print("No borrowing data available.")
            return

        book_count = {}
        member_count = {}
        author_count = {}
        category_count = {}

        for transaction in issued_transactions:
            book_id = transaction.get("book_id")
            member_id = transaction.get("member_id")
            book_count[book_id] = book_count.get(book_id, 0) + 1
            member_count[member_id] = member_count.get(member_id, 0) + 1

            book = next(
                (item for item in self.books if item.book_id == book_id),
                None
            )
            if book:
                author_count[book.author] = author_count.get(book.author, 0) + 1
                category_count[book.category] = category_count.get(book.category, 0) + 1

        most_borrowed_book_id = max(book_count, key=book_count.get)
        most_borrowed_book = next(
            (book for book in self.books if book.book_id == most_borrowed_book_id),
            None
        )
        print("\n===== Most Borrowed Book =====")
        print(f"Book     : {most_borrowed_book.title if most_borrowed_book else most_borrowed_book_id}")
        print(f"Borrowed : {book_count[most_borrowed_book_id]} times")

        if author_count:
            most_borrowed_author = max(author_count, key=author_count.get)
            print("\n===== Most Borrowed Author =====")
            print(f"Author   : {most_borrowed_author}")
            print(f"Borrowed : {author_count[most_borrowed_author]} times")

        if category_count:
            popular_category = max(category_count, key=category_count.get)
            print("\n===== Most Popular Category =====")
            print(f"Category : {popular_category}")
            print(f"Borrowed : {category_count[popular_category]} times")

        most_active_member_id = max(member_count, key=member_count.get)
        member = next(
            (item for item in self.members if item.member_id == most_active_member_id),
            None
        )
        print("\n===== Most Active Member =====")
        print(f"Member   : {member.name if member else 'Unknown'}")
        print(f"Borrowed : {member_count[most_active_member_id]} times")

    def overdue_books(self):
        print("\n===== Overdue Books =====")
        today = datetime.now()
        found = False

        for book in self.books:
            if book.available or not book.issue_date:
                continue

            issue_date = datetime.strptime(book.issue_date, "%Y-%m-%d")
            days_kept = (today - issue_date).days
            if days_kept <= 14:
                continue

            late_days = days_kept - 14
            print("\n------------------------")
            print(f"Book ID      : {book.book_id}")
            print(f"Book Title   : {book.title}")
            print(f"Issued To    : {book.issued_to}")
            print(f"Days Kept    : {days_kept} days")
            print(f"Late Days    : {late_days} days")
            print(f"Current Fine : {late_days * 5} Tk")
            found = True

        if not found:
            print("No overdue books found.")


#===============Dashboard====================



    def dashboard(self):
        print("\n" + "=" * 45)
        print("\n===== Library Dashboard =====")
        print("=" * 45)

        transactions = self._load_transactions()
        available_books = sum(book.available for book in self.books)
        issued_books = len(self.books) - available_books
        overdue_count = 0
        today = datetime.now()

        for book in self.books:
            if not book.available and book.issue_date:
                issue_date = datetime.strptime(book.issue_date, "%Y-%m-%d")
                if (today - issue_date).days > 14:
                    overdue_count += 1

        book_counts = {}
        category_counts = {}
        author_counts = {}
        for transaction in transactions:
            if transaction.get("action") != "Issued":
                continue
            book_id = transaction.get("book_id")
            book_counts[book_id] = book_counts.get(book_id, 0) + 1
            book = next((item for item in self.books if item.book_id == book_id), None)
            if book:
                category_counts[book.category] = category_counts.get(book.category, 0) + 1
                author_counts[book.author] = author_counts.get(book.author, 0) + 1

        most_borrowed_book = "N/A"
        if book_counts:
            book_id = max(book_counts, key=book_counts.get)
            book = next((item for item in self.books if item.book_id == book_id), None)
            most_borrowed_book = book.title if book else book_id

        popular_category = max(category_counts, key=category_counts.get) if category_counts else "N/A"
        popular_author = max(author_counts, key=author_counts.get) if author_counts else "N/A"
        total_fine = sum(transaction.get("fine", 0) for transaction in transactions)

        print(f"\nTotal Books          : {len(self.books)}")
        print(f"Available Books      : {available_books}")
        print(f"Issued Books         : {issued_books}")
        print(f"Total Members        : {len(self.members)}")
        print(f"Total Transactions   : {len(transactions)}")
        print("\n===== Library Insights =====")
        print(f"Most Borrowed Book   : {most_borrowed_book}")
        print(f"Popular Category     : {popular_category}")
        print(f"Popular Author       : {popular_author}")
        print(f"Overdue Books        : {overdue_count}")
        print(f"Total Fine Collected : {total_fine} Tk")
        print("=" * 45)


    def log_activity(self, message):
        log_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message
    }

        try:
            with open(DATA_DIR / "activity_log.json", "r") as file:
                logs = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            logs = []

        logs.append(log_entry)

        with open(DATA_DIR / "activity_log.json", "w") as file:
            json.dump(logs, file, indent=4)

    def view_activity_log(self):
        print("\n===== Activity Log =====")

        try:
            with open(DATA_DIR / "activity_log.json", "r") as file:
                activity_log = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            print("No activity log found.")
            return

        if len(activity_log) == 0:
            print("No activity log found.")
            return

        for log in activity_log:
            print("\n------------------------")
            print(f"Time   : {log['time']}")
            print(f"Message: {log['message']}")
