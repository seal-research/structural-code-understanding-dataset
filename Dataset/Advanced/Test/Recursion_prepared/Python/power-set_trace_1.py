from functools import reduce


def list_powerset(lst):
    result = [[]]
    for x in lst:
        result.extend([subset + [x] for subset in result])
    return result

def list_powerset2(lst):
    return reduce(lambda result, x: result + [subset + [x] for subset in result],
                  lst, [[]])

def powerset(s):
    return frozenset(map(frozenset, list_powerset(list(s))))

if __name__ == "__main__":
    print(powerset({1, 2, 3}))