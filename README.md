# GDB Comments

Have you ever been in the middle of groking some assembly when all of sudden you wanted to write down a little note so you'll quickly remember what's going on the next time? Well now you can!

![Assembly comments in pwndbg](/screenshots/comments.png?raw=true)

## Requirements

* GDB with pwndbg or PEDA

## Installation

    git clone https://github.com/supersam654/gdb-comments.git ~/.gdb-comments
    echo "source ~/.gdb-comments/gdb-comments.py" >> ~/.gdbinit

## Usage

    > comment Whatever you want to say and don't worry about escaping anything

Will add a comment to wherever your PC is pointing to. If there's already a comment there, it will get overwritten.

    > comment -c

Clear the comment on the current line.

    > comment -a 0x55555555463c $eax = 0xdeadbeef

Add the comment `$eax = 0xdeadbeef` to line `0x55555555463c`. You can also get fancy and add comments to places like `$rip+13`.

## Under the hood

Behind the scenes, this creates a file called `/path/to/exe.comments` so there will be a new file in whatever directory the binary is in. That file is very human-readable. It's just a bunch of addresses and comments. If an address has multiple comments, the last one gets displayed.

## TODO

* Add support for gef
* Better support for cores (better naming convention and easier way to comment around the file)
