import random

def poolReducer(pool, percentage):
    """Takes a dictionary and integer (ex. 50 for 50%) as inputs. Alters the dictionary
    to be that percentage of its original size, and returns it. Eliminates the
    keys randomly. (ex. inputting 10 as percentage will return the dictionary to be 10%
    of its original size). Rounds down to remove an integer number of keys. Used to make
    data working with smaller, thus faster, while setting up the program"""

    lenPool = len(pool)
    percentage = 1 - (percentage * 0.01)
    numberToRemove = int(lenPool * percentage)
    for key in random.sample(pool.keys(), numberToRemove):
        del pool[key]
    return pool




