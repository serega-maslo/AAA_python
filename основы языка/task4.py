import sys

def sol1(reviews):
    stars = {}
    for i in reviews:
        if i['id'] in stars:
            stars[i['id']]['sum'] += i['stars']
            stars[i['id']]['amount'] += 1
        else:
            stars[i['id']] = {'sum': i['stars'], 'amount': 1}
    return {key: item['sum'] / item['amount'] for key, item in stars.items()}

def sol2(reviews):
    stars = {}
    for i in reviews:
        if i['id'] in stars:
            stars[i['id']]['sum'] += i['stars']
            stars[i['id']]['amount'] += 1
        else:
            stars[i['id']] = {'sum': i['stars'], 'amount': 1}
    ans = {key: item['sum'] / item['amount'] for key, item in stars.items() if item['amount'] > 1}
    min_stars = 6
    min_product = -1
    for key, item in ans.items():
        if item < min_stars:
            min_product = key
            min_stars = item
    return min_product

def sol3(reviews):
    return sum(1 for i in reviews if i['stars'] in [1, 2])
    

def sol4(reviews):
    return sum(1 for i in reviews if i['stars'] in [1, 2]) / len(reviews)

if __name__ == "__main__":
    reviews = [
        {"id": 1, "product": "Чехол", "stars": 5},
        {"id": 1, "product": "Чехол", "stars": 3},
        {"id": 1, "product": "Чехол", "stars": 4},
        {"id": 2, "product": "Наушники", "stars": 2},
        {"id": 2, "product": "наушники", "stars": 2},
        {"id": 2, "product": "НАУШНИКИ", "stars": 5},
        {"id": 3, "product": "Планшет", "stars": 5},
        {"id": 4, "product": "Колонка", "stars": 4},
        {"id": 4, "product": "Колонка", "stars": 4},
        {"id": 5, "product": "Кабель", "stars": 1},
    ]
    print(sol1(reviews))
    print(sol2(reviews))
    print(sol3(reviews))
    print(sol4(reviews))
