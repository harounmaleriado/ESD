import requests

def is_valid_user(user_id):
    response = requests.get(f'http://localhost:5000/user/{user_id}')  # Adjust URL as needed
    return response.status_code == 200
