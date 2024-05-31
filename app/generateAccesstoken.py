import requests
from django.http import JsonResponse

def get_access_token(request):
    consumer_key =''
    consumer_secrete =''
    access_token_url =''
    headers = {'content-type':'application/json'}
    auth = (consumer_key, consumer_secrete)

    try:
        response = requests.get(access_token_url, headers=headers,auth=auth)
        response.raise_for_status()
        result = response.json()
        access_token=result['access_token']
        return JsonResponse({'access_token':access_token})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)})