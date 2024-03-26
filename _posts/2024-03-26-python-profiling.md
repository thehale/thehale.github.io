---
layout: post
title: How to Find Python Performance Problems
categories:
 - How-To Guides
 - Python
tags:
 - Software Engineering
 - Software Performance
 - Python
image:
  path: /assets/img/posts/python_profiling/sorting.profile.svg
  alt: A flame graph showing the performance of different parts of a Python program.
---

When a Python program is running too slowly, use a profiler to measure which parts of the code are hurting performance the most.

## Measure Code Performance with `cProfile`

Start by writing a [decorator](https://realpython.com/primer-on-python-decorators/) which will add profiling metrics to the decorated function:
```python
# Credit: https://stackoverflow.com/a/5376616/14765128
import cProfile  # Python's built-in profiling tool

def profile(output_file_path):
    def inner(func):
        def wrapper(*args, **kwargs):
            prof = cProfile.Profile()
            retval = prof.runcall(func, *args, **kwargs)
            prof.dump_stats(output_file_path)
            return retval
        return wrapper
    return inner
```

Then apply that decorator to the function which is running slowly.
```python
@profile("path/to/output.profile")
def my_slow_function():
    ...
```

Now, when you execute `my_slow_function` a performance profile will be saved to `"path/to/output.profile"`.

## Generate a Flame Graph of Profiling Metrics

Download the [flameprof](https://github.com/baverman/flameprof) tool
```bash
wget https://raw.githubusercontent.com/baverman/flameprof/master/flameprof.py -o flameprof.py
```

Create a flame graph.
```bash
python flameprof.py "path/to/output.profile" --width 1800 > "output.profile.svg"
```

<!-- **TIP**
I also like using the following script which lets me generate multiple flame graphs at once:

```bash
// graph.sh
for var in "$@"
do
    python flameprof.py "$var" --width 1800 > "$var".svg
done
```

```bash
graph.sh output1.profile output2.profile
``` -->

## Review the Flame Graph to Identify Performance Bottlenecks

Here's a sample [flame graph](https://www.brendangregg.com/flamegraphs.html) for a function which generates a list of 250 random integers, then sorts the list twice -- first with [bubble sort](https://github.com/TheAlgorithms/Python/blob/master/sorts/bubble_sort.py), then again with [merge sort](https://github.com/TheAlgorithms/Python/blob/master/sorts/merge_sort.py).

![A flame graph showing that bubble sort takes longer to run than merge sort](/assets/img/posts/python_profiling/sorting.profile.svg){: width="600" }
_A flame graph showing that bubble sort is slower than merge sort. [[Source Code]](/assets/code/python_profiling_sorting.py)_

**The top half of the flame graph helps you find which line(s) of code in your function are the slowest.** It roughly shows the function call stack over time. Longer bars indicate more time spent in the function call. Taller peaks indicate a deeper function call stack. A split peak indicates that the function called multiple other functions. 

In the example above, you can clearly see that `bubble_sort_iterative` took longer than `merge_sort`. You can also see that `merge_sort` called other functions while `bubble_sort_iterative` did not.

**The bottom half of the flame graph helps you find which functions contribute the most to the total runtime, even if they were invoked from different places.** Longer bars indicate more time spent in the function call. Deeper valleys indicate that the function was called deeper in the call stack. A split valley indicates that the function was called from multiple places. In the example above, you can see that `merge_sort` was called from two places -- `sort_a_random_list` and `merge_sort` itself -- while `merge` was only ever called from `merge_sort`. You can also see that more time was spent executing code in `merge` than in `merge_sort`.

You can also see even more detailed information by hovering over any bar in the flame graph. For example, hovering over the blue bar for `merge_sort` shows the following tooltip:
```
/jhale.dev/posts/python-profiling/sample.py:41:merge_sort 11.37% (305 1 0.0002682973988063135 0.0008462241322068796)
```

The first section shows where the function is located in your code `/path:line-number:function_name`.  In this case, the `merge_sort` function was found on line 41 of a file called `sample.py`

The percent indicates what percent of the total profiled runtime was spent in that function. In this case, recursive calls to `merge_sort` accounted for 11.37% of the total recorded runtime.

The parentheses show `(calls_total calls_primitive duration_excluding_subcalls duration_total)`. In this case, the `merge_sort` function was called 305 times, but only one of those calls was "primitive" (i.e. non-recursive). Excluding calls to sub-functions, `merge_sort` completed its work in 0.000268... seconds, compared to a total runtime of 0.000846... seconds when including calls to sub-functions (including recursive calls).

## Conclusion

Now you have a new tool for tracking down performance issues in your Python applications!

Use the comments below to share your experiences with improving the performance of Python programs!
