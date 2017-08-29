# This file is responsible for saving and retrieving comments for a particular binary.
class Comments(object):
    def __init__(self, filename):
        self.comments = {}
        pass

    def add_comment(self, address, comment):
        self.comments[int(address)] = comment

    def get_comment(self, address):
        return self.comments.get(address)

_comments = {}

# Get an existing comments object or load it from a file.
def get_comments(filename):
    comments = _comments.get(filename, None)
    if comments is None:
        comments = Comments(filename)
        _comments[filename] = comments
    return comments
