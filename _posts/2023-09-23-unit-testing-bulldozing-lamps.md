---
layout: post
title: "Unit Tests: How to Fix a Lamp Without Bulldozing Your Hometown"
tags:
 - Debugging
 - Unit Testing
 - Software Engineering
 - Testing
image:
  path: /assets/img/posts/unit_testing_bulldozing_lamps/ram_destruction_square.jpg
  alt: Attempting to fix a small function by rerunning a large program is like fixing a lamp by bulldozing and rebuilding an entire city.
---


## A Short Story of Debugging Desperation

In *97 Things Every Programmer Should Know*, [Thomas Guest](https://www.linkedin.com/in/thomasguest) recounts a moment when he had identified a problematic piece of code in a large application, but had lost hours in recompilation time trying to experiment with the erring edge case.

At wit's end, he went to his co-worker, Hoppy, who "had a reputation as the local expert on programming issues." But Hoppy's help was not what Thomas expected.

Surprisingly, the programmer extraordinaire first admitted "he wasn't sure" about the problem. Then, instead of referencing documentation, Hoppy copied the failing function into a separate file to make a brand new program which took its inputs via the command line. After a few minutes of rapid experimentation, Hoppy and Thomas had their answer!

## By Small Programs are Great Insights Brought to Pass

Why was Hoppy's little program so much more effective at identifying the error than running the code in its full context?

Consider the amount of work required to execute a large program. Each run acquires acres of memory, spends significant effort framing the land with countless data structures, and constructs numerous communication highways -- just to burn everything down when the program exits. That is a massively wasteful amount of effort when trying evaluate a tiny, lamp-sized function.

By pulling the faulty function into a separate program, Hoppy was doing the digital equivalent of swapping out light bulbs.

[Creating a small progam](https://stackoverflow.com/help/minimal-reproducible-example) provides [insights into the workings of a larger program.](https://ericlippert.com/2014/03/05/how-to-debug-small-programs/#:~:text=these%20techniques%20then%20scale%20up%20to%20finding%20bugs%20in%20non-trivial%20programs.) In a recent pair programming session, a coworker showed me a large list of Python objects which would specify some complex database constraints. He asked if putting the constant at the bottom of the file would cause an error. Initially unsure, I wrote the following small program:

```python
class Apple:
    types = APPLE_TYPES
    
APPLE_TYPES = ["gala", "granny smith"]
```
{: file='fruit.py' }

Within 30 seconds of the question, we received our answer: `NameError: name 'APPLE_TYPES' is not defined`. 

Interestingly, because the program is so short, we identified a different approach within a minute which permits the constant at the end of the file.

```python
class Apple:
    types: list
    
    def __init__(self):
        types = APPLE_TYPES
    
APPLE_TYPES = ["gala", "granny smith"]
```
{: file='fruit.py' }

These small programs, written in less than two minutes,  reveal a big insight about the Python language: assignments to class variables resolve at the time of class *definition*, while assignments in an `__init__` method resolve at the time of class *instantiation*.

## Unit Tests are Small Programs which Yield Big Insights

This "small programs" approach is productively applied to unit testing. After all, a unit test is fundamentally a small program which evaluates a piece of a larger program.

Consider the following toy unit test in Python:

```python
from math import log2

def test_logarithms_work():
    assert log2(4) == 2
```

This test automates the same successful approach from Thomas's story with Hoppy. The function of interest, `log2`, is selected out of the [dozens of functions in Python's `math` module](https://docs.python.org/3/library/math.html?highlight=math#module-math) and efficiently evaluated in isolation.

When each unique insight gained from a program is recorded as a unique unit test, the test suite gains the additional benefit of becoming an executable specification for the program -- capable of continuously verifying its proper functionality.

## Keep Unit Tests Small. Avoid Omniscient Mocks

Some parts of large programs depend on complex infrastructure, which can make them hard to test in isolation. Examples include code which interacts with a remote server over the internet or invoking the command line of another program. Such parts of a program are like our small house lamp which depends on the electrical grid for its power.

Testing the edges of our system is often facilitated by mocks -- stand-in implementations of the dependency -- akin to a portable power supply in our lamp metaphor. Such mocks can be immensely helpful. Patching out network responses, for example, can de-couple tests from a flaky/slow third-party API, drastically reducing both test durations and failure rates.

However, one pitfall to avoid when unit testing is an anti-pattern I will call "omniscient mocking"

Omniscient mocking is characterized by the use of mocks which know too much about the intricacies of the implementation of the functionality under test. The use of such mocks makes a test suite more brittle and impedes improvements to the software.

Imagine testing a lightbulb by smashing it open to replace the filament. Not only does your test ruin the lightbulb, it excludes other valid implementations like LED and neon lights.

As a code example, the earlier test for `math.log2` makes a clear assertion about the relationship between its parameters and output. In contrast, an omniscient mock might patch out the [`loghelper` function](https://github.com/python/cpython/blob/74c72a2fc73941394839bd912c4814398b461446/Modules/mathmodule.c#L2219) from the C library which [implements `math.log2`](https://github.com/python/cpython/blob/74c72a2fc73941394839bd912c4814398b461446/Modules/mathmodule.c#L2302) -- only to break when [`loghelper`'s function signature changed last year](https://github.com/python/cpython/commit/5a80e8580e2eb9eac4035d81439ed51523fcc4d2).

In short, mocks are wonderful for patching out dependencies at the edges of your system, but they become more problematic the more they know about your code's implementation.

## Final Thoughts

Modern software systems are phenomenally complex. Compared to the mere 266 bits sufficient to count [all the atoms in the observable universe](https://www.thoughtco.com/number-of-atoms-in-the-universe-603795), the megabytes (and sometimes gigabytes) of memory used by modern programs encompass an unfathomably large state space. It is thanks to the well designed abstractions provided by modern programming languages that our programs are even remotely comprehensible.

As whole programs continue to grow more complex, we need effective tools and techniques to understand the interactions of their constituent parts. Unit tests are one such tool for both facilitating and documenting that learning process.

So, next time you find yourself repeatedly bulldozing your RAM, consider writing a small, lamp-sized program instead.

<!--
Proof: 266 bits are sufficient to count the 10**80 atoms in the observable universe.

$ python
>>> (2**266) // (10**80)
1

OR
$ python
>>> import math
>>> math.log2(10**80)
265.754247590989
-->

------

*CREDITS: The cover image of a wrecking ball and house lamp was AI generated using the Bing Image Creator powered by DALL-E. Except where quoted, the text of the article is entirely original writing by Joseph Hale.*