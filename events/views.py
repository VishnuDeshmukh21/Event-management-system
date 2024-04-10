import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import timedelta
from .models import Event
from .serializers import EventSerializer
import json
import time 
from django.http import HttpResponse


def calculate_distance(latitude1, longitude1, latitude2, longitude2):
    url = f"https://gg-backend-assignment.azurewebsites.net/api/Distance?code=IAKvV2EvJa6Z6dEIUqqd7yGAu7IZ8gaH-a0QO6btjRc1AzFu8Y3IcQ==&latitude1={latitude1}&longitude1={longitude1}&latitude2={latitude2}&longitude2={longitude2}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        return str(json_data['distance'])
    else:
        return f"Error: {response.status_code}"

def calculate_weather(city,date):
    url = f"https://gg-backend-assignment.azurewebsites.net/api/Weather?code=KfQnTWHJbg1giyB_Q9Ih3Xu3L9QOBDTuU5zwqVikZepCAzFut3rqsg==&city={city}&date={date}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        return str(json_data['weather'])




@api_view(['POST'])
def event_find(request):
    try:
        latitude_str = request.data.get('latitude', '')
        longitude_str = request.data.get('longitude', '')
        date_str = request.data.get('date', '')

        if not (latitude_str and longitude_str and date_str):
            return Response({'error': "Latitude, longitude, and date are required fields."}, status=status.HTTP_400_BAD_REQUEST)

        latitude = float(latitude_str)
        longitude = float(longitude_str)
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        end_date = date + timedelta(days=14)
        events = Event.objects.filter(date__range=[date, end_date]).order_by('date')

        response_data = []
        for event in events:
            distance = calculate_distance(latitude, longitude, event.latitude, event.longitude)
            weather = calculate_weather(event.city_name, event.date)
            event_data = {
                'event_name': event.event_name,
                'city_name': event.city_name,
                'date': str(event.date),
                'weather': weather,
                'distance_km': distance
            }
            response_data.append(event_data)

        page_size = 10
        total_events = len(response_data)
        total_pages = (total_events + page_size - 1) // page_size

        # Split response_data into pages
        paginated_data = []
        for i in range(total_pages):
            start_index = i * page_size
            end_index = min((i + 1) * page_size, total_events)
            page_data = {
                'events': response_data[start_index:end_index],
                'page': i + 1,
                'pageSize': page_size,
                'totalEvents': total_events,
                'totalPages': total_pages
            }
            paginated_data.append(page_data)

        return Response(paginated_data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



from rest_framework import status

@api_view(['POST'])
def event_add(request):
    # Extract data from the request
    event_name = request.data.get('event_name')
    city_name = request.data.get('city_name')
    date = request.data.get('date')
    time = request.data.get('time')
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    # Validate the request data
    if not all([event_name, city_name, date, time, latitude, longitude]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Additional validation (e.g., date format, latitude, longitude)
    # Add your validation logic here
    
    try:
        # Create the event
        Event.objects.create(
            event_name=event_name,
            city_name=city_name,
            date=date,
            time=time,
            latitude=latitude,
            longitude=longitude
        )
        return Response({'Success': True}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def hello(request):
    return HttpResponse("Hello")