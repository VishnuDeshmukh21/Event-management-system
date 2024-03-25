import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import timedelta
from .models import Event
from .serializers import EventSerializer
import json
import time  # Add this import statement

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
    

import time  # Add this import statement

# @api_view(['GET'])
# def event_find(request):
#     try:
#         start_time = time.time()  # Record start time

#         latitude = float(request.data.get('latitude'))
#         longitude = float(request.data.get('longitude'))
#         date_str = request.data.get('date')
        
#         # Parse the date from string
#         date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        
#         # Calculate the end date (14 days later)
#         end_date = date + timedelta(days=14)
        
#         # Get events occurring within the next 14 days from the specified date
#         events = Event.objects.filter(date__range=[date, end_date]).order_by('date')[:10]
        
#         # Serialize the events
#         serializer = EventSerializer(events, many=True)
        
#         # Calculate distance for each event and include it in the response
#         response_data = []
#         for event, event_data in zip(events, serializer.data):
#             distance = calculate_distance(latitude, longitude, event.latitude, event.longitude)
#             weather = calculate_weather(event.city_name,event.date)
#             event_data['distance'] = distance # Add distance to event data
#             event_data['weather'] = weather
#             response_data.append(event_data)
        
#         end_time = time.time()  # Record end time
#         execution_time = end_time - start_time  # Calculate execution time
#         print(f"Total execution time: {execution_time} seconds")

#         return Response({'eventDetails': response_data})
    
#     except Exception as e:
#         return Response({'error': str(e)}, status=400)




import concurrent.futures

@api_view(['GET'])
def event_find(request):
    try:
        start_time = time.time()  # Record start time

        latitude = float(request.data.get('latitude'))
        longitude = float(request.data.get('longitude'))
        date_str = request.data.get('date')
        
        # Parse the date from string
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Calculate the end date (14 days later)
        end_date = date + timedelta(days=14)
        
        # Get events occurring within the next 14 days from the specified date
        events = Event.objects.filter(date__range=[date, end_date]).order_by('date')[:10]
        
        # Serialize the events
        serializer = EventSerializer(events, many=True)
        
        # Function to calculate distance and weather concurrently
        def calculate_distance_and_weather(event):
            distance = calculate_distance(latitude, longitude, event.latitude, event.longitude)
            weather = calculate_weather(event.city_name, event.date)
            return {'distance': distance, 'weather': weather}
        
        # Concurrently execute calculate_distance_and_weather for each event
        with concurrent.futures.ThreadPoolExecutor() as executor:
            event_futures = [executor.submit(calculate_distance_and_weather, event) for event in events]
        
        # Get results from the futures
        response_data = []
        for future, event_data in zip(event_futures, serializer.data):
            result = future.result()
            event_data.update(result)  # Merge distance and weather data into event data
            response_data.append(event_data)
        
        end_time = time.time()  # Record end time
        execution_time = end_time - start_time  # Calculate execution time
        print(f"Total execution time: {execution_time} seconds")

        return Response({'eventDetails': response_data})
    
    except Exception as e:
        return Response({'error': str(e)}, status=400)



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