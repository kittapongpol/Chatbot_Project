import requests

url = "http://127.0.0.1:5000/ask"
data = {"faculty": "คณะวิศวกรรมศาสตร์"}
response = requests.post(url, json=data)
print(response.json())  # แสดงผลลัพธ์
