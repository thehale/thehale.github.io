# Companion file to https://jhale.dev/posts/python-profiling/

import cProfile  # Python's built-in profiling tool

def profile(output_file_path):
    # Credit: https://stackoverflow.com/a/5376616/14765128
    def inner(func):
        def wrapper(*args, **kwargs):
            prof = cProfile.Profile()
            retval = prof.runcall(func, *args, **kwargs)
            prof.dump_stats(output_file_path)
            return retval
        return wrapper
    return inner


######################
# Demonstration Code:

from random import randint

@profile("sorting.profile")
def sort_a_random_list():
    ints = [randint(0, 1000) for _ in range(250)]
    sorted_ints_bubble = bubble_sort_iterative([i for i in ints])
    sorted_ints_merged = merge_sort([i for i in ints])


def bubble_sort_iterative(collection: list) -> list:
    # https://github.com/TheAlgorithms/Python/blob/master/sorts/bubble_sort.py
    length = len(collection)
    for i in reversed(range(length)):
        swapped = False
        for j in range(i):
            if collection[j] > collection[j + 1]:
                swapped = True
                collection[j], collection[j + 1] = collection[j + 1], collection[j]
        if not swapped:
            break  # Stop iteration if the collection is sorted.
    return collection


def merge_sort(collection: list) -> list:
    # https://github.com/TheAlgorithms/Python/blob/master/sorts/merge_sort.py
    def merge(left: list, right: list) -> list:
        result = []
        while left and right:
            result.append(left.pop(0) if left[0] <= right[0] else right.pop(0))
        result.extend(left)
        result.extend(right)
        return result

    if len(collection) <= 1:
        return collection
    mid_index = len(collection) // 2
    return merge(merge_sort(collection[:mid_index]), merge_sort(collection[mid_index:]))


if __name__ == "__main__":
    sort_a_random_list()