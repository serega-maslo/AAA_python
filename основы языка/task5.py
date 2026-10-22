import sys

def sol1(city1, city2):
    return list(set(city1) & set(city2))

def sol2(city1, city2):
    return list(set(city1) - set(city2))

def sol3(city1, city2):
    return list(set(city2) - set(city1))

def sol4(city1, city2):
    return len(set(city1) | set(city2))


if __name__ == "__main__":
    moscow = {201, 202, 203, 204}
    kazan = {203, 204, 205, 206}
    print(sol1(moscow, kazan))
    print(sol2(moscow, kazan))
    print(sol3(moscow, kazan))
    print(sol4(moscow, kazan))
