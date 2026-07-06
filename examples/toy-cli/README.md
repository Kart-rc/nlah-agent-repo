# Toy CLI: hello

A minimal command-line example that greets a person by name.

## Prerequisite

Python 3. That is the only setup requirement — the script uses just the
standard library, so a fresh checkout of this repository needs nothing
installed beyond a working `python3` on your PATH.

## Usage

Run from the repository root:

```
python3 examples/toy-cli/hello.py <name>
```

Worked example:

```
$ python3 examples/toy-cli/hello.py Ada
Hello, Ada!
```

Quote multi-word names so the shell passes them as one argument:

```
$ python3 examples/toy-cli/hello.py "Ada Lovelace"
Hello, Ada Lovelace!
```

## Missing name

Running with no name prints a usage message on stderr and exits with
status 2 (no traceback):

```
$ python3 examples/toy-cli/hello.py
usage: hello.py [-h] name
hello.py: error: the following arguments are required: name
```

## Verification

There is no shipped test file; these runnable acceptance commands are the
verification surface. Each should succeed (exit 0) when run from the
repository root:

```sh
# Greets the named person, exit 0
test "$(python3 examples/toy-cli/hello.py Ada)" = "Hello, Ada!"
test "$(python3 examples/toy-cli/hello.py Grace)" = "Hello, Grace!"

# Quoted multi-word name is one argument
test "$(python3 examples/toy-cli/hello.py "Ada Lovelace")" = "Hello, Ada Lovelace!"

# Missing name: nothing on stdout, exit status 2
test -z "$(python3 examples/toy-cli/hello.py 2>/dev/null)"
python3 examples/toy-cli/hello.py 2>/dev/null; test $? -eq 2
```
