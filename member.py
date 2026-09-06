class Member:
    def __init__(self, member_id, name, phone):
        self.member_id = member_id
        self.name = name
        self.phone = phone

    @property
    def email(self):
        return self.phone

    @email.setter
    def email(self, value):
        self.phone = value

    def display_member(self):
        print(f"Member ID: {self.member_id}")
        print(f"Name: {self.name}")
        print(f"Phone: {self.phone}")

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "phone": self.phone
        }