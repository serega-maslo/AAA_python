import sys

def sol1(queries):
    return len(queries)

def sol2(queries):
    ans = {}
    for i in queries:
        if i in ans:
            ans[i] += 1
        else:
            ans[i] = 1
    return ans

def sol3(queries):
    ans = {}
    best = -1
    best_result = -1
    for i in queries:
        if i in ans:
            ans[i] += 1
        else:
            ans[i] = 1
        if ans[i] > best_result:
            best_result = ans[i]
            best = i
    return best

def sol4(queries):
    ans = {}
    best = -1
    best_result = -1
    for i in queries:
        if i in ans:
            ans[i] += 1
        else:
            ans[i] = 1
        if ans[i] > best_result:
            best_result = ans[i]
            best = i
    return best_result / len(queries)

def sol5(queries):
    ans = {}
    ones = set(queries)
    for i in queries:
        if i in ans:
            if i in ones:
                ones.remove(i)
        else:
            ans[i] = 1
    return ones


if __name__ == "__main__":
    queries = [
    "чехол",
    "iphone",
    "чехол",
    "наушники",
    "iphone",
    "iphone",
    "кабель",
    "чехол",
    "iphone",
]
    print(sol1(queries))
    print(sol2(queries))
    print(sol3(queries))
    print(sol4(queries))
    print(sol5(queries))
