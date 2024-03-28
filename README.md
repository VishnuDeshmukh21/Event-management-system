# Event-management-system


# event_find:

Method: POST
Functionality: This endpoint is used to find events based on the provided latitude, longitude, and date. It returns details about events happening within 14 days from the specified date, including their distances from the provided coordinates and weather forecasts for the event locations. It utilizes concurrent execution to improve performance by calculating distance and weather for each event concurrently.
Parameters:
latitude: Latitude of the location (float)
longitude: Longitude of the location (float)
date: Date in the format 'YYYY-MM-DD'
Returns:
JSON response containing event details including distances and weather forecasts.



# event_add:

Method: POST
Functionality: This endpoint is used to add a new event to the system. It requires details such as event name, city name, date, time, latitude, and longitude. It performs basic validation on the provided data and creates a new event if the data is valid.
Parameters:
event_name: Name of the event (string)
city_name: Name of the city where the event is happening (string)
date: Date of the event in the format 'YYYY-MM-DD'
time: Time of the event (string)
latitude: Latitude of the event location (float)
longitude: Longitude of the event location (float)
Returns:
JSON response indicating success or failure of the operation.