import requests

# Define the API endpoint
api_url = "http://127.0.0.1:8000/schedule"


# Example data for the request
request_data = {
    "algorithm": "sjf without preemption",
    "table": [
        {"Process_ID": 1, "Task": 1, "Arrival_Time": 0, "Burst_Time": 3, "Deadline": 7, "Period": 20},
        {"Process_ID": 2, "Task": 2, "Arrival_Time": 0, "Burst_Time": 2, "Deadline": 4, "Period": 5},
        {"Process_ID": 3, "Task": 3, "Arrival_Time": 0, "Burst_Time": 2, "Deadline": 9, "Period": 10}
    ]
}

# Make a POST request to the API
response = requests.post(api_url, json=request_data)

# Print the response
print(response.status_code)
print(response.json())
