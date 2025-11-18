---
layout: post
title: "How to detect Unicode characters outside the Basic Multilingual Plane"
category:
 - How-To Guides
 - Python
tags:
 - Unicode
---

_TL;DR_
```python
def is_on_basic_multilingual_plane(char):
    return int(char.encode().hex(), 16) <= 0xFFFF
```

## Backstory

Recently, I was programmatically moving a few hundred thousand documents to a cloud service when my script caught an error about an invalid document name. Included in the error description was an esoteric "clarification" that this particular cloud service only supported filenames with characters in the "basic multilingual plane".

That error message led to a fun bit of research covering text encoding and bit manipulation in Python. Let's go!

## Unicode and its 17 planes

The term ["basic multilingual plane"](https://www.unicode.org/standard/principles.html#:~:text=basic%20multilingual%20plane) comes from the Unicode specification -- a widely adopted set of rules for representing text as binary. 

In short, Unicode organizes characters into 17 large groups called "planes". The first plane, plane 0, is more commonly referred to as the Basic Multilingual Plane because it contains all the most common characters used in languages across the world.

Notably, emojis are not in the Basic Multilingual Plane, rather they are largely located on the Supplementary Mulitlingual Plane. 

## Checking a string for characters outside the Basic Multilingual Plane

Going back to my document upload issues, it turned out that the failing documents had emojis in their filenames. Since emojis aren't on the Basic Multilingual Plane, the cloud service was rejecting the file for its name.

But, these documents still needed to be transferred, so I had to adjust my scripts to swap out emojis for some other acceptable character. Here's how I did that.

First, I turned my filename into a list of characters to consider individually.

```python
filename = "Hello 👋.txt"
chars = [c for c in filename]
# ['H', 'e', 'l', 'l', 'o', ' ', '👋', '.', 't', 'x', 't']
```

Then I encoded those characters to bytes which really makes the emoji stand out.

```python
char_bytes = [c.encode().hex() for c in chars]
# ['48', '65', '6c', '6c', '6f', '20', 'f09f918b', '2e', '74', '78', '74']
```

I then converted each character's bytes to its corresponding integer.

```python
char_ints = [int(c, 16) for c in char_bytes]
# [72, 101, 108, 108, 111, 32, 4036989323, 46, 116, 120, 116]
```

Since the Basic Multilingual Plane covers binary values up to `0xFFFF`, we can now filter out any character with a higher numeric value.

```python
char_ints_bmp = [c for c in char_ints if c <= 0xFFFF]
# [72, 101, 108, 108, 111, 32, 46, 116, 120, 116]
```

Then we can go in reverse to reconstruct the string without the emojis.

```python
char_bytes_bmp = [c.to_bytes() for c in char_ints_bmp]
chars_bmp = [c.decode() for c in char_bytes_bmp]
filename_bmp = "".join(chars_bmp)
# 'Hello .txt'
```

## Packaging it all up nicely

While the repeated list comprehensions were a helpful tool for figuring out the conversion, I wanted to transform the filename in a single pass. I also wanted more flexibility for how to handle characters outside the Basic Multilingual Plane.

So, I refactored towards a function that flags whether or not a character is on the Basic Multilingual Plane.

```python
def is_bmp(char):
    return int(char.encode().hex(), 16) <= 0xFFFF
```

Notice that the given character is encoded to binary and transformed to an integer before being compared to the largest code point on the Basic Multilingual Plane.

With this function, I could then write a single list comprehension, this time replacing the emoji with an underscore.

```python
filename = "Hello 👋.txt"
filename_bmp = "".join((c if is_bmp(c) else "_") for c in filename)
# 'Hello _.txt'
```

## Closing Thoughts

And that's it! A fun little adventure learning more about the precise nature of how text is stored/transmitted on computers.

Feel free to comment one of your stories dealing with text encoding!
