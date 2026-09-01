class Member:
    def __init__(self, member_id, name, email):
        self.member_id = member_id
        self.name = name
        self.email = email

    def display_member(self):
        print(f"Member ID: {self.member_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email
        }