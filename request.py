import requests

url = "http://localhost:8000/process-claim"
files = [
    ('files', ('Bill-2.pdf', open('D:\\Mediacal Insurence Claim\\Bill-2.pdf', 'rb'), 'application/pdf')),
    ('files', ('Discharge_summary2.pdf', open('D:\\Mediacal Insurence Claim\\Discharge_summary2.pdf', 'rb'), 'application/pdf')),
]

response = requests.post(url, files=files)
try:
    data= response.json()
    print(data)
except requests.exceptions.JSONDecodeError:
    print(response.text)
