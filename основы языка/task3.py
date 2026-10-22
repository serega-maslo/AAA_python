import sys

def sol1(orders):
    return_sum = 0
    for i in orders:
        if i['status'] == "returned":
            return_sum += i["amount"]
    return return_sum

def sol2(orders):
    return_people = set()
    for i in orders:
        if i['status'] == "returned":
            return_people.add(i['buyer'])
    return return_people

def sol3(orders):
    person_amount = {}
    for i in orders:
        if i['status'] == "delivered":
            if i['buyer'] in person_amount:
                person_amount[i['buyer']] += i['amount']
            else:
                person_amount[i['buyer']] = i['amount']
        else:
            if i['buyer'] not in person_amount:
                person_amount[i['buyer']] = 0
    return person_amount

def sol4(orders):
    len_delivered = 0
    amount_delivered = 0
    for i in orders:
        if i['status'] == "delivered":
            len_delivered += 1
            amount_delivered += i['amount']
    return amount_delivered / len_delivered


if __name__ == "__main__":
    orders = [
    {"id": 1, "buyer": "anya", "status": "delivered", "amount": 900},
    {"id": 2, "buyer": "boris", "status": "returned", "amount": 4_500},
    {"id": 3, "buyer": "anya", "status": "delivered", "amount": 1_500},
    {"id": 4, "buyer": "vera", "status": "delivered", "amount": 3_200},
    {"id": 5, "buyer": "boris", "status": "delivered", "amount": 700},
    {"id": 6, "buyer": "gleb", "status": "returned", "amount": 2_100},
]
    print(sol1(orders))
    print(sol2(orders))
    print(sol3(orders))
    print(sol4(orders))
