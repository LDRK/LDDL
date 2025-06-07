import requests

def obtener_productos():
    
    URL = 'https://fakestoreapi.com/products'

    response = requests.get(URL)

    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        
