import requests

URL = 'http://127.0.0.1:5000'

#       Пользователи
response = requests.post(
    f"{URL}/user/",
    json={
        "email": "a1@b.c",
        "password": "ajdgouhiweuhr"
    }
)
print(response.status_code)
print(response.json())

response = requests.post(
    f"{URL}/login/",
    json={
        "email": "a1@b.c",
        "password": "ajdgouhiweuhr"
    }
)
print(response.status_code)
print(response.json())

headers = {
    "email": "a1@b.c",
    "token": response.json()['token']
}
# response = requests.get(f"{URL}/user/1", headers=headers)

#      Объявления
response = requests.post(
    f'{URL}/',
    headers=headers,
    json={"title": "some title",
          "description": "some desc"
          }
)

# response = requests.get(f'{URL}/1/')

# response = requests.get(f'{URL}/')

# response = requests.patch(
#     f'{URL}/2/',
#     headers=headers,
#     json={
#         "description": "new desc 1"
#     }
# )

# response = requests.delete(f'{URL}/2/', headers=headers)


print(response.status_code)
print(response.json())
