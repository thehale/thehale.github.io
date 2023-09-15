# How Writing Unit Tests Prevents Bulldozing Homes

## A Story of Debugging Desperation

In *97 Things Every Programmer Should Know*, [Thomas Guest](https://www.linkedin.com/in/thomasguest) recounts a moment of debugging desperation.

He had identified a problematic piece of code in a large application, but had lost hours in recompilation time trying to experiment with the erring edge case.

At wit's end, he went to his co-worker, Hoppy, who "had a reputation as the local expert on programming issues." But Hoppy's help was not what Thomas expected.

First, Hoppy admited "he wasn't sure" about the problem. Then, instead of referencing documentation, he copied the failing function into a separate file to make a brand new program which took its inputs via the command line. After a few minutes of rapid experimentation, Hoppy and Thomas had their answer!

## By Small Programs are Great Insights Brought to Pass

Why was Hoppy's little program so much more effective at identifying the error than running the code in its full context? Because attempting to debug a small function by re-running a large program is like bulldozing and repeatedly rebuilding an entire house to fix a lone lamp that won't turn on. By pulling the faulty function into a separate program for evaluation, Hoppy was doing the digital equivalent of simply testing the lamp with a new lightbulb.

<!--
Seriously, think about how a program discards memory when it exits only to ask for it all again when it restarts -- it's like you are razing a chunk of RAM Real Estate just to rebuild what was already there.
-->

[Creating a small progam](https://stackoverflow.com/help/minimal-reproducible-example) provides [insights into the workings of a larger program.](https://ericlippert.com/2014/03/05/how-to-debug-small-programs/#:~:text=these%20techniques%20then%20scale%20up%20to%20finding%20bugs%20in%20non-trivial%20programs.) For example, while pair programming recently a coworker showed me a large constant which was to be used to specify some complex database constraints. He asked if putting the constant at the bottom of the file would cause an error. To find out for sure, I quickly wrote a small program.

```python
# fruit.py

class Apple:
    types = APPLE_TYPES
    
APPLE_TYPES = ["gala", "granny smith"]
```

Running this program immediately gave us an negative answer in the form of `NameError: name 'APPLE_TYPES' is not defined`. Interestingly, because the program is so short, we quickly identified a different approach which did allow the constant at the end of the file.

```python
# fruit.py

class Apple:
    types: list
    
    def __init__(self):
        types = APPLE_TYPES
    
APPLE_TYPES = ["gala", "granny smith"]
```

These small programs reveal a big insight about the Python language: assignments to class variables resolve at the time of class *definition*, while assignments in an `__init__` method resolve at the time of class *instantiation*.

## Unit Tests are Small Programs which Yield Big Insights

This perspective can also be applied to unit testing. After all, a unit test is simply a small program which evaluates a piece of a larger program.

Consider the following unit test in Python:

```python
from math import log2

def test_logarithms_work():
    assert log2(4) == 2
```

This test automates the same successful approach from Thomas's story with Hoppy. The function of interest, `log2`, is selected out of the [dozens of functions in Python's `math` module](https://docs.python.org/3/library/math.html?highlight=math#module-math) and efficiently evaluated in isolation.

When each unique insight gained from a program is recorded as a unique unit test, the test suite gains the additional benefit of becoming an executable specification for the program -- capable of continuously verifying its proper functionality.

## Beware of Omniscient Mocking in Unit Tests

One pitfall to avoid when unit testing is an anti-pattern I will call "omniscient mocking".

<!-- TODO continue writing here... -->
Many unit testing tools offer the ability to replace...

We test a lightbulb by applying a charge to its positive and negative contacts -- its public interface. We don't break open the lightbulb to see if the contacts work with a fake wire.

We isolate the lightbulb from its normal, large surrounding systems, but we don't break it apart.

We don't mock out [`loghelper`](https://github.com/python/cpython/blob/74c72a2fc73941394839bd912c4814398b461446/Modules/mathmodule.c#L2219) from the [`log2` implementation](https://github.com/python/cpython/blob/74c72a2fc73941394839bd912c4814398b461446/Modules/mathmodule.c#L2302)



<!-- Modern software systems are phenomenally complex. To illustrate, compare the mere 266 bits needed to count [all the atoms in the observable universe](https://www.thoughtco.com/number-of-atoms-in-the-universe-603795) with the multiple megabytes (and sometimes gigabytes) of memory used by modern programs. Without the abstractions provided by modern programming languages, the possible state space of our programs would be impossibly complex to reason about. -->





<!--
Proof:

$ python
>>> (2**266) // (10**80)
1

OR
$ python
>>> import math
>>> math.log2(10**80)
265.754247590989
-->
