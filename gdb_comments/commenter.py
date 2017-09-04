import json

import gdb

from gdb_comments import utils

# Represents a single comment in memory. Also contains methods to be serialized
# and deserialized.
class Comment(object):
    def __init__(self, objfile, index, relative_address, text):
        self.objfile = objfile
        self.index = index
        self.relative_address = relative_address
        self.address = self._calculate_address()
        self.text = text.strip()

    def _calculate_address(self):
        return _relative_to_absolute(self.objfile, self.index, self.relative_address)

    def serialize(self):
        return json.dumps([self.objfile, self.index, self.relative_address, self.text])

    @classmethod
    def from_absolute_address(cls, address, text):
        objfile, index, relative_address = _absolute_to_relative(address)
        return Comment(objfile, index, relative_address, text)

    @classmethod
    def from_serialized_string(cls, serialized_string):
        # Note that `self.serialize` dumps the arguments in the same order as
        # the initializer expects them.
        return Comment(*json.loads(serialized_string))


# This file is responsible for saving and retrieving comments for a particular binary.
class Comments(object):
    def __init__(self, filename):
        self.comments = {}
        self.savefile = filename + '.comments'
        try:
            with open(self.savefile) as f:
                for line in f:
                    comment = Comment.from_serialized_string(line)
                    self.comments[comment.address] = comment
        except FileNotFoundError:
            pass

    def add_comment(self, address, text):
        address = int(address)
        comment = Comment.from_absolute_address(address, text)
        self.comments[address] = comment
        with open(self.savefile, 'a+') as f:
            f.write(comment.serialize() + '\n')

    def get_comment(self, address):
        comment = self.comments.get(address)
        if comment:
            return comment.text
        else:
            return None

_comments = {}

# PERF: Combine ranges with common endpoints.
# PERF: Search this list via binary search (assume it's sorted).
# PERF: Don't generate mappings every time.
def _absolute_to_relative(absolute_address):
    mappings = utils.get_mappings()
    for region, objfile_data in mappings.items():
        if absolute_address in region:
            relative_address = absolute_address - region.start
            objfile, index = objfile_data
            return objfile, index, relative_address
    return None, None, None

def _relative_to_absolute(objfile, index, relative_address):
    mappings = utils.get_mappings()
    for region, objfile_data in mappings.items():
        if (objfile, index) == objfile_data:
            return region.start + relative_address
    return None

# Get an existing comments object or load it from a file.
def get_comments(filename):
    comments = _comments.get(filename, None)
    if comments is None:
        comments = Comments(filename)
        _comments[filename] = comments
    return comments

# PERF: Only reload comments if ASLR is on.
def reload_comments(event):
    global _comments
    _comments = {}

# Clear comments when the program is run again to handle ASLR (if enabled).
gdb.events.exited.connect(reload_comments)
