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
    package_weight = input("Enter package weight: ")
    special_requirements = input("Enter any special requirements: ")
    route_details = input("Enter route details: ")
    time_duration = input("Enter time duration: ")

    # Create a dictionary for the shipment details
    shipment_details = {
        "Package Weight": package_weight,
        "Special Requirements": special_requirements,
        "Route Details": route_details,
        "Time Duration": time_duration
    }

    # Define the CSV file name
    csv_file_name = "shipment_details.csv"

    # Write to the CSV file
    with open(csv_file_name, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=shipment_details.keys())

        # Write the header only if the file is empty
        if file.tell() == 0:
            writer.writeheader()  # Write header only if the file is empty

        # Write the shipment details to the CSV file
        writer.writerow(shipment_details)

    print("Shipment details have been saved to CSV.")

# Call the function to manage shipment
manage_shipment()



