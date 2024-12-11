from datetime import datetime, timedelta
import os

def manage_driver_profile():
    # Function to update profile if the name already exists
    def update_driver_profile(file_name, name, new_data):
        updated = False
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                lines = file.readlines()
            
            # Rewrite the file with updated data if name matches
            with open(file_name, "w") as file:
                for line in lines:
                    if line.startswith(name + ","):
                        file.write(new_data)  # Write updated data
                        updated = True
                    else:
                        file.write(line)  # Keep existing data unchanged
        
        return updated

    # Collect driver details
    while True:
        name = input("Enter driver's name: ")
        if name.isalpha():
            break
        else:
            print("Invalid input. Please enter letters only.")
    
    while True:
        contact_info = input("Enter driver's contact info: ")
        if contact_info.isdigit():
            break
        else:
            print("Invalid input. Please enter numbers only.")
    
    address = input("Enter driver's address: ")
    
    while True:
        availability_status = input("Enter driver's availability status (YES or NO): ").strip().upper()
        if availability_status in ["YES", "NO"]:
            break
        else:
            print("Invalid input. Please enter YES or NO.")
    
    while True:
        health_report = input("Enter driver's health report (GOOD or BAD): ").strip().upper()
        if health_report in ["GOOD", "BAD"]:
            break
        else:
            print("Invalid input. Please enter GOOD or BAD.")
    
    while True:
        driving_license = input("Enter driver's driving license (YYYY-MM-DD): ")
        try:
            license_date = datetime.strptime(driving_license, "%Y-%m-%d")
            current_date = datetime.now()
            if current_date - license_date <= timedelta(days=3 * 365):  # Within 3 years
                license_status = "VALID"
            else:
                license_status = "EXPIRED"
            break
        except ValueError:
            print("Invalid format. Please enter a valid date in the format YYYY-MM-DD.")
    
    # File to save driver data
    file_name = "driver.txt"
    new_driver_data = f"{name},{contact_info},{address},{availability_status},{license_status},{health_report}\n"
    
    # Check if profile exists and update if necessary
    updated = update_driver_profile(file_name, name, new_driver_data)
    
    if not updated:
        # If not updated, create file if necessary and add new profile
        if not os.path.exists(file_name):
            with open(file_name, "w") as file:
                header = "Name,ContactInfo,Address,AvailabilityStatus,DrivingLicenseStatus,HealthReport\n"
                file.write(header)
        with open(file_name, "a") as file:
            file.write(new_driver_data)
        print("New profile is saved.")
    else:
        print(f"{name}'s profile is updated.")


#Shipment 
def manage_shipment():
    # Collect Shipment Details
    # take info from JR : OrderID, package_size , vehicle, 
    # take  info from YY : time duration, route details 
    with open('jr.txt', 'r') as infile:
        with open('outputfile.txt', 'w') as outfile:
            for line in infile:
                row = line.strip().split(',')
                
                OrderID = row[0]  # Adjust the index as needed
                Package_size = row[0]
                Vehicle = row[0]

    
                outfile.write(f"{OrderID},{Package_size},{Vehicle}\n") 
                
    with open('yy.txt', 'r') as infile:
        with open('outputfile.txt', 'w') as outfile:
            for line in infile:
                row = line.strip().split(',')
                
                Time_duration = row[0]  # Adjust the index as needed
                Route_details = row[0]
                

    
                outfile.write(f"{Time_duration},{Route_details}\n")        
    
 # Open a text file to store the driver profile
    with open("ShipmentDetail.txt", "a") as file:
        header = "OrderID,Package_Size,Vehicle,Route Details,Time Duration,\n"
        file.write(header)
        # Write data to the file
        file.write(f"{OrderID}{Package_size},{Vehicle},{Time_duration},{Route_details}\n")  


    print("Shipment details have been saved.")

# Call the function to manage shipment


def manage_route():
    # Define routes with distances between stops (in km) and stopover times (in hours)
    def calculate_travel_time(distances, average_speed):
        """Calculate total travel time between all stops (one way)."""
        return sum(distances) / average_speed

    def calculate_segment_time(distances, average_speed, start_index, end_index):
        """Calculate travel time for a specific segment of the route."""
        return sum(distances[start_index:end_index]) / average_speed

    def calculate_turnaround_time(distances, stopover_time, average_speed):
        """Calculate total turnaround time for the round trip."""
        one_way_travel_time = calculate_travel_time(distances, average_speed)
        total_stopover_time = stopover_time * (len(distances) + 1)  # Stop at each hub except the starting point
        return (one_way_travel_time * 2) + total_stopover_time

    def update_parcel_status(file_path, status):
        """Update the parcel status in a text file."""
        with open(file_path, "a") as file:
            file.write(f"{status}\n")

    def simulate_route(stops, distances, file_path, start, destination):
        """Simulate the route and update parcel status upon arrival at each stop."""
        if start not in stops or destination not in stops:
            print("Invalid start or destination location.")
            return

        start_index = stops.index(start)
        destination_index = stops.index(destination)

        if start_index > destination_index:
            print("Invalid route: Destination must come after the start point.")
            return

        print(f"Parcel picked up from {start}. Status updated to 'on going'.")
        update_parcel_status(file_path, f"Parcel picked up from {start}. Status: On going")

        for i in range(start_index, destination_index + 1):
            stop = stops[i]
            print(f"Parcel has arrived at {stop}.")
            update_parcel_status(file_path, f"Arrived at {stop}.")
            if stop == destination:
                print(f"Destination {destination} reached. Status updated to 'delivered'.")
                update_parcel_status(file_path, f"Destination {destination} reached. Status: Delivered.")
                break
            if i < destination_index:
                print(f"Traveling to next destination: {stops[i + 1]}...")

        # Calculate travel time for the segment and format it
        travel_time = calculate_segment_time(distances, route1_average_speed, start_index, destination_index)
        hours = int(travel_time)
        minutes = int((travel_time - hours) * 60)
        print(f"Time needed to arrive at {destination}: {hours} hours and {minutes} minutes")
        update_parcel_status(file_path, f"Total travel time to {destination}: {hours} hours and {minutes} minutes.")

    # Route 1 details
    route1_stops = ["Johor", "Kuala Lumpur", "Butterworth", "Kedah", "Perlis"]
    route1_distances = [281, 349, 86, 88]  # Distances between consecutive stops
    route1_stopover_time = 1  # in hours
    route1_average_speed = 80  # in km/h

    # Route 2 details
    route2_stops = ["Johor", "Kuala Lumpur", "Terengganu", "Kelantan"]
    route2_distances = [281, 417, 324]  # Distances between consecutive stops
    route2_stopover_time = 1  # in hours
    route2_average_speed = 80  # in km/h

    # File to update parcel status
    status_file = "parcel_status.txt"

    # Input start and destination from user
    start = input("Enter your departure location: ")
    destination = input("Enter your destination: ")

    # Determine which route to simulate
    if start in route1_stops and destination in route1_stops:
        print("\nSimulating Route 1:")
        simulate_route(route1_stops, route1_distances, status_file, start, destination)
    elif start in route2_stops and destination in route2_stops:
        print("\nSimulating Route 2:")
        simulate_route(route2_stops, route2_distances, status_file, start, destination)
    else:
        print(f"The route from {start} to {destination} is not valid on any predefined routes.")



# Main Execution
#manage_driver_profile()
#manage_shipment()
#manage_route()




