---
layout: post
title: "Python Script Output Redirection"
description: Integrate Python scripts into the Unix philosophy
tags:
 - Python
 - Unix
image:
  path: /assets/img/posts/python-script-output-redirection/bash-shell.png
  alt: A screenshot showing a python script appended with `> output.log 2>&1` which saves all output to a file.
---

> "Write programs to handle text streams, because that is a universal interface."
>
> -- Doug McIlroy, the inventor of Unix pipes [(source)](http://www.catb.org/~esr/writings/taoup/html/ch01s06.html#:~:text=Write%20programs%20to%20handle%20text%20streams%2C%20because%20that%20is%20a%20universal%20interface.)

Today, for the Nth time I got stuck while trying to redirect a Python script's output to a file for later processing. So, after figuring it out again, I'm finally documenting my findings.

Let's explore the default behavior for how Python scripts output to `stdout` vs `stderr`, and thus how we can save that output to a file or pipe it to another program (i.e. following the [Unix Philosophy](http://www.catb.org/~esr/writings/taoup/html/ch01s06.html))

## Example Script

Here's a script that outputs a text using both the basic `print` command and the built-in `logging` module.

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

print("printed message")
logging.info("log message")
```
{: file='script.py' }

As expected, running the script outputs each line to a terminal.

```bash
$ python script.py
printed message
log message
```

## Python sends `print` output to `stdout`

Redirecting the scripts `stdout` only captures the `print` message, leaving the `log` messages in the terminal.

```bash
$ python script.py > stdout.log
log message

$ cat stdout.log
printed message
```

## Python sends `logging` output to `stderr`

Redirecting `stderr` does the reverse, capturing the `log` output and leaving the `print` messages in the terminal.

```bash
$ python script.py 2> stderr.log
printed message

$ cat stderr.log
log message
```

## How to redirect `print` and `logging` output to the same file

Both `stdout` and `stderr` can be redirected to the same file by _appending_ the command with `2>&1` (see [I/O redirection docs](https://tldp.org/LDP/abs/html/io-redirection.html#:~:text=2%3E%261%0A%20%20%20%20%20%20%23%20Redirects%20stderr%20to%20stdout.)). 

```bash
$ python script.py > output.log 2>&1

$ cat output.log
log message
printed message
```

> I'm not sure why the `print` output appears _after_ the `logging` output, when the script executes `print` _before_ `logging`. If you know why, please comment below!
{: .prompt-warning }

## Piping output to another command

Another key principle in Unix-land is that the output of one program can be the input to another program. Connecting one program's output to another program's input is done with the pipe character `|` and is sometimes called "piping".

We'll start by using a command called `grep` which filters its input to only output the lines which contain a certain string.

> In my shell, `grep` highlights the found string, which I will indicate here by adding \*stars\*
{: .prompt-info }


### Default Pipe Behavior

```bash
$ python script.py | grep message
log message
printed *message*
```

Notice that only the `print` message was highlighted. By default, the pipe only redirects `stdout`, so `grep` only processed the `print` output. The `logging` messages went to `stderr` and thus were still output to the terminal even though they weren't processed by `grep`.

### Piping `stdout` and `stderr`

To send all output to `grep` we can use the same `2>&1` syntax from before.

```bash
$ python script.py 2>&1 | grep message
log *message*
printed *message*
```

Now `grep` is processing every line.

### Piping only `stderr`
If you want `grep` to only process the `stderr` output (i.e. `log` outputs), we have to send the `stdout` somewhere else. On Linux we can choose `/dev/null` which is a text trashcan.

```bash
$ (python script.py 2>&1 1>/dev/null) | grep message 
log *message*
```

Notice that the `print` output was discarded, while everything else was processed by `grep`.