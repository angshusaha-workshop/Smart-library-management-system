from library import Library
from admin import Admin

library = Library()
admin = Admin("admin", "1234")


print("=" * 45)
print("Library Management System")
print("=" * 45)


def admin_login():
    print("\n===== Admin Login =====")

    username = input("Username: ")
    password = input("Password: ")

    if admin.login(username, password):
        print("\nLogin successful!")
        return True

    print("\nInvalid username or password.")
    return False


while True:

    print("\n===== Smart Library System =====")
    print("1. Admin Login")
    print("2. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        if admin_login():

            while True:

                print("\n===== Admin Panel =====")
                print("1. Add Book")
                print("2. View Books")
                print("3. Search Book")
                print("4. Update Book")
                print("5. Delete Book")
                print("6. Register Member")
                print("7. View All Members")
                print("8. Search Member")
                print("9. Update Member")
                print("10. Delete Member")
                print("11. Issue Book")
                print("12. Return Book")
                print("13. Transaction History")
                print("14. Member Borrowing History")
                print("15. Dashboard")
                print("16. Overdue Books")
                print("17. Smart Book Recommendation")
                print("18. Popularity Report")
                print("19. Activity Log")
                print("20. Logout")
                choice = input("Enter your choice: ")

                if choice == "1":

                    library.add_book()

                elif choice == "2":

                    library.view_books()

                elif choice == "3":

                    library.search_book()

                elif choice == "4":

                    library.update_book()

                elif choice == "5":

                    library.delete_book()

                elif choice == "6":

                    library.register_member()

                elif choice == "7":

                    library.view_members()

                elif choice == "8":

                    library.search_member()

                elif choice == "9":

                    library.update_member()

                elif choice == "10":

                    library.delete_member()

                elif choice == "11":

                    library.issue_book()

                elif choice == "12":

                    library.return_book()

                elif choice == "13":
                    library.view_transactions()

                elif choice == "14":
                    library.member_history()

                elif choice == "15":
                    library.dashboard()

                elif choice == "16":
                    library.overdue_books()

                elif choice == "17":

                    library.recommend_books()

                elif choice == "18":

                    library.popularity_report()

                elif choice == "19":

                    library.view_activity_log()

                elif choice == "20":

                    print("\nLogged out successfully.")
                    break

    elif choice == "2":

        print("\nThank you for using Smart Library System.")
        break

    else:

        print("Invalid choice.")