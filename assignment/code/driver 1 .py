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



def manage_routes():
    # Define Routes
    routes = [
        ("Route 1: Johor – Kuala Lumpur – Butterworth - Kedah – Perlis", 60), #60 = 1hour 
        ("Route 2: Johor – Kuala Lumpur – Terengganu – Kelantan", 60)
    ]

    # Calculate Turnaround Time
    def calculate_turnaround_time(route, travel_time):
        stopover_time = 60  # in minutes
        return travel_time + (stopover_time * 2)  # Assuming stopover at both ends

    # Example of calculating turnaround time for Route 1
    travel_time = 300  # Example travel time in minutes
    turnaround_time = calculate_turnaround_time(routes[0], travel_time)
    print("Turnaround Time for", routes[0][0], ":", turnaround_time, "minutes")

        # Function to simulate package arrival
    def package_arrived(route):
        print("Order arrived at", route[0])

    # Simulating package arrival for Route 1
    package_arrived(routes[0])

# Main Execution
manage_driver_profile()
manage_shipment()
manage_routes()


