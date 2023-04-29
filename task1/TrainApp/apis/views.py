from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

def get_access_token():
    client_id = "a5976733-4257-4246-849d-31b65342f669"
    client_secret = "vWLjZZAHQHWIGRYP"

    auth_url = 'http://104.211.219.98/train/auth'
    
    auth_data = {
        "companyName": "KL Trains",
        "clientID": client_id,
        "ownerName": "KL",
        "ownerEmail": "kl@abc.edu",
        "rollNo": "2000031326",
        "clientSecret": client_secret
    }
    auth_response = requests.post(auth_url, json=auth_data)

    return auth_response.json()['access_token']



def get_trains():
    access_token = get_access_token()
    trains_url = 'http://104.211.219.98/train/trains'
    headers = {'Authorization': f'Bearer {access_token}'}
    trains_response = requests.get(trains_url, headers=headers)

    trains = trains_response.json()
    return trains


def filter_trains(trains):
    filtered_trains = []
    for train in trains:
        departure_time = datetime.now().replace(hour=train['departureTime']['Hours'], minute=train['departureTime']['Minutes'], second=train['departureTime']['Seconds'])
        if departure_time > datetime.now() + timedelta(minutes=30):
            filtered_trains.append(train)

    return filtered_trains


def sort_trains(trains):
    sorted_trains = sorted(trains, key=lambda x: (x['price']['AC'], x['price']['sleeper'], -x['seatsAvailable']['AC'], -x['seatsAvailable']['sleeper'], (datetime.now() + timedelta(minutes=x['delayedBy'])).replace(hour=x['departureTime']['Hours'], minute=x['departureTime']['Minutes'], second=x['departureTime']['Seconds'])))
    return sorted_trains

@api_view(['GET'])
def get_train_schedule(request):
    trains = get_trains()

    filtered_trains = filter_trains(trains)
    sorted_trains = sort_trains(filtered_trains)

    return Response(sorted_trains)

@api_view(['GET'])
def get_train(request, pk):
    access_token = get_access_token()
    trains_url = f'http://104.211.219.98/train/trains/{pk}'
    headers = {'Authorization': f'Bearer {access_token}'}
    train = requests.get(trains_url, headers=headers).json()
    return Response(train)