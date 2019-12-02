class User:
    """A sample User class"""

    def __init__(self, first, last, id):
        self.first = first
        self.last = last
        self.id = id

    @property
    def email(self):
        return '{}.{}@code.berlin'.format(self.first.lower(), self.last.lower())

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def __repr__(self):
        return "User('{}', '{}', {})".format(self.first, self.last, self.id)