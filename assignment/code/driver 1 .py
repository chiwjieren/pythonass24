from datetime import datetime, timedelta
# driver profile 
def manage_driver_profile():
    # Collect Driver Profile Data
    name = input("Enter driver's name: ")

    # Validate contact info to accept only numbers
    while True:
        contact_info = input("Enter driver's contact info (numbers only): ")
        if contact_info.isdigit():
            break
        else:
            print("Invalid input. Please enter numbers only.")

    # Collect address
    address = input("Enter driver's address: ")

    # Validate availability status to accept only YES or NO
    while True:
        availability_status = input("Enter driver's availability status (YES or NO): ").strip().upper()
        if availability_status in ["YES", "NO"]:
            break
        else:
            print("Invalid input. Please enter YES or NO.")

    # Validate health report to accept only GOOD or BAD
    while True:
        health_report = input("Enter driver's health report (GOOD or BAD): ").strip().upper()
        if health_report in ["GOOD", "BAD"]:
            break
        else:
            print("Invalid input. Please enter GOOD or BAD.")

    # Validate driving license to accept only date format (YYYY-MM-DD)
    while True:
        driving_license = input("Enter driver's driving license (YYYY-MM-DD): ")
        try:
            # Attempt to parse the date
            license_date = datetime.strptime(driving_license, "%Y-%m-%d")
            # Check if the license is expired or valid
            current_date = datetime.now()
            if current_date - license_date <= timedelta(days=3*365):  # Within 3 years
                license_status = "VALID"
            else:
                license_status = "EXPIRED"
            break
        except ValueError:
            print("Invalid format. Please enter a valid date in the format YYYY-MM-DD.")

    # Open a text file to store the driver profile
    with open("driver.txt", "a") as file:
        header = "Name,ContactInfo,Address,AvailabilityStatus,DrivingLicenseStatus,HealthReport\n"
        file.write(header)
        # Write data to the file
        file.write(f"{name},{contact_info},{address},{availability_status},{license_status},{health_report}\n")

    print("Driver profile has been saved.")

# Call the function to manage driver profile
manage_driver_profile()



#Shipment 
def manage_shipment():
    # Collect Shipment Details
    # take info from JR : OrderID, package_size , vehicle, 
    # take info from YY : time duration, route details 
with open('yourfile.txt', 'r') as file:
    for line in file:
        row = line.strip().split(',')
        specific_data = row[1]  
        print(specific_data)
        
    
 # Open a text file to store the driver profile
    with open("ShipmentDetail.txt", "a") as file:
        header = "OrderID,Package_Size,Vehicle,Route Details,Time Duration,\n"
        file.write(header)
        # Write data to the file
        file.write(f"{OrderID}{package_size},{vehicle},{route_details},{time_duration}\n")


    print("Shipment details have been saved.")

# Call the function to manage shipment
manage_shipment()


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
# Assuming these functions exist
# manage_driver_profile()
# manage_shipment()
manage_routes()
