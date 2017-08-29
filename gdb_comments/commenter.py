# This file is responsible for saving and retrieving comments for a particular binary.
class Comments(object):
    def __init__(self, filename):
        self.comments = {}
        self.savefile = filename + '.comments'
        try:
            with open(self.savefile) as f:
                for line in f:
                    address, comment = line.split(' ', 1)
                    self.comments[int(address)] = comment.strip()
        except FileNotFoundError:
            pass
        print('Loaded %d comments' % len(self.comments))

    def add_comment(self, address, comment):
        comment = comment.strip()
        self.comments[int(address)] = comment
        with open(self.savefile, 'a+') as f:
            f.write('%s %s\n' % (address, comment))

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
