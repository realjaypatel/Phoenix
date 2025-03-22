import requests
response = requests.get('https://excel2api.vercel.app/api/1BSOoMb-j3ALwi56lgSW8x7q17iNGSbuq1gpi9vV_ZOQ')
print('fetched data2 :',response)

import requests

# response = requests.get('https://api.example.com/data')
# print(response.status_code)  # Print the status code of the response
print(response.json())   