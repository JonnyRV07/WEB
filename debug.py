import json

with open('db/db_sess.json', 'r', encoding='utf-8') as query:
    data = json.load(query)["database"]["users"]
    for user in data:
        if user["login"] == 'nihil' and user["password"] == '123qwe':
            print(user)
