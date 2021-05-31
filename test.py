import requests

BASE="http://127.0.0.1:5000/"

data = [
    {
        "likes":42, 
        "name":"socketio tutorial",
        "views":235,
    },
    {
        "likes":5009, 
        "name":"minecraft survival",
        "views":9001,
    },
    {
        "likes":10, 
        "name":"how to create a REST API",
        "views":8313,
    },
]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

# response = requests.put(
#     BASE + "video/1", 
#     {
#         "likes":10, 
#         "name":"how to create a REST API",
#         "views":8313,
#     })
# print(response.json())

input()
response = requests.delete(BASE + "video/1")
print(response)
