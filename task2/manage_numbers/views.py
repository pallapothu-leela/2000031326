from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import requests

@require_GET
def get_numbers(request):
    urls = request.GET.getlist('url')

    if not urls:
        return JsonResponse({'error': 'No URLs provided'}, status=400)

    responses = []
    for url in urls:
        try:
            response = requests.get(url, timeout=0.5)
            if response.status_code == 200:
                data = response.json()
                if 'numbers' in data:
                    responses.append(set(data['numbers']))
        except requests.exceptions.Timeout:
            print(f'Timeout retrieving numbers from {url}')
        except Exception as e:
            print(f'Error retrieving numbers from {url}: {e}')

    merged_numbers = sorted(list(set().union(*responses)))
    return JsonResponse({'numbers': merged_numbers})
