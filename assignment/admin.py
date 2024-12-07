def read_lines_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def write_lines_to_file(file_path, lines, header=None):
    file_exists = False
    try:
        with open(file_path, 'r') as file:
            first_char = file.read(1)
            if first_char:
                file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(file_path, 'a') as file:
        if not file_exists and header:
            file.write(header)
        file.writelines(lines)

def admin_dashboard():
    print('1. Overview of Shipments')
    print('2. Pending Shipments')
    print('3. Completed Shipments')
    print('4. Driver Information')
    print('5. Fuel & Consumption')
    print('6. Fleet Management')
    print('7. Reports')
    print('8. Exit')

    function_mapping = {
        1: overview_of_shipments,
        2: pending_shipments,
        3: completed_shipments,
        4: driver_management,
        5: manage_fuel_and_vehicle_consumption,
        6: vehicle_management_and_maintenance,
        7: generate_reports,
        8: exit
    }

    try:
        choice = int(input('Enter your choice: '))
        function_mapping[choice]()
    except ValueError:
        print("Please enter a valid number")

def overview_of_shipments():
    print("\n=== Overview of All Shipments ===")
    content = read_lines_from_file('order_ids.txt')
    if content:
        print("Order ID")
        print("-" * 50)
        for line in content:  
            try:
                data = line.strip().split(',')
                if len(data) >= 4:
                    print(f"{data[0]:8} | {data[1]:8} | {data[2]:9} | {data[3]}")
                else:
                    print(f"{line.strip()}")
            except Exception as e:
                print(f"Error processing line: {line.strip()}")
    else:
        print("No shipment data available")
        print("Note: Checking file at 'order_ids.txt'")

def pending_shipments():
    print("\n=== Pending Shipments ===")
    content = read_lines_from_file('ongoingorder.txt')
    if content:
        print("Order ID | Quantity | ShipFrom | ShipTo | Vehicle")
        print("-" * 45)
        for line in content[1:]:  
            data = line.strip().split(',')
            if len(data) >= 4:
                print(f"{data[0]:8} | {data[1]:6} | {data[2]:12} | {data[3]}")
    else:
        print("No pending shipments found")

def completed_shipments():
    print("\n=== Completed Shipments ===")
    content = read_lines_from_file('completedorder.txt')
    if content:
        print("Order ID | Driver | Delivery Date | Rating")
        print("-" * 45)
        for line in content[1:]:  
            data = line.strip().split(',')
            if len(data) >= 4:
                print(f"{data[0]:8} | {data[1]:6} | {data[2]:12} | {data[3]}")
    else:
        print("No completed shipments found")

def vehicle_management_and_maintenance():
    print("\n=== Vehicle Management & Maintenance ===")
    print("1. View Vehicle Status")
    print("2. View Maintenance Alerts")
    print("3. Back to Main Menu")

    try:
        choice = int(input("\nEnter your choice (1-3): "))
        
        if choice == 1:
            vehicles = read_lines_from_file('vehicle.txt')
            if vehicles:
                print("\n=== Vehicle Status ===")
                print("Vehicle ID | Maintenance | Performance | Fuel | Location")
                print("-" * 60)
                for vehicle in vehicles[1:]:  
                    v = vehicle.strip().split(',')
                    print(f"{v[0]:10} | {v[1]:11} | {v[2]:11} | {v[3]:4}% | {v[5]}")
            else:
                print("\nNo vehicle data found")

        elif choice == 2:
            vehicles = read_lines_from_file('vehicle.txt')
            if vehicles:
                print("\n=== Maintenance Alerts ===")
                alerts_found = False
                for vehicle in vehicles[1:]: 
                    v = vehicle.strip().split(',')
                    if v[1] == "Needs Maintenance" or int(v[3].strip('%')) < 50:
                        alerts_found = True
                        print(f"ALERT: {v[0]} needs attention:")
                        if v[1] == "Needs Maintenance":
                            print(f"- Maintenance Status: {v[1]}")
                        if int(v[3].strip('%')) < 50:
                            print(f"- Low Fuel Level: {v[3]}")
                        print()
                
                if not alerts_found:
                    print("No maintenance alerts at this time")
            else:
                print("\nNo vehicle data found")

        elif choice == 3:
            return
        else:
            print("Invalid choice")
            
    except ValueError:
        print("Invalid input. Please enter a number.")

def manage_fuel_and_vehicle_consumption():
    print("\n=== Fuel & Vehicle Consumption Management ===")
    print("1. View Fuel Levels")
    print("2. Track Consumption Patterns") 
    print("3. Vehicle Utilization Report")
    print("4. Back to Main Menu")

    try:
        choice = int(input("\nEnter your choice (1-4): "))
        
        if choice == 1:
            vehicles = read_lines_from_file('vehicle.txt')
            if vehicles:
                print("\n=== Current Fuel Levels ===")
                print("Vehicle ID | Fuel Level | Status")
                print("-" * 40)
                for vehicle in vehicles[1:]:
                    v = vehicle.strip().split(',')
                    fuel_level = int(v[3].strip('%'))
                    status = "LOW" if fuel_level < 50 else "OK"
                    print(f"{v[0]:10} | {v[3]:10} | {status}")
            else:
                print("\nNo vehicle data found")

        elif choice == 2:
            vehicles = read_lines_from_file('vehicle.txt')
            if vehicles:
                print("\n=== Consumption Analysis ===")
                low_fuel = sum(1 for v in vehicles[1:] if int(v.strip().split(',')[3].strip('%')) < 50)
                total = len(vehicles) - 1  # Exclude header
                print(f"Total Vehicles: {total}")
                print(f"Vehicles with Low Fuel: {low_fuel}")
                print(f"Fuel Efficiency Rate: {((total-low_fuel)/total)*100:.1f}%")
            else:
                print("\nNo vehicle data found")

        elif choice == 3:
            vehicles = read_lines_from_file('vehicle.txt')
            if vehicles:
                print("\n=== Vehicle Utilization Report ===")
                print("Vehicle ID | Performance | Fuel Level | Location")
                print("-" * 55)
                for vehicle in vehicles[1:]:
                    v = vehicle.strip().split(',')
                    print(f"{v[0]:10} | {v[2]:11} | {v[3]:10} | {v[5]}")
            else:
                print("\nNo vehicle data found")

        elif choice == 4:
            return
        else:
            print("Invalid choice")
            
    except ValueError:
        print("Invalid input. Please enter a number.")

def driver_management():
    print("\n=== Driver Management System ===")
    print("1. View All Drivers")
    print("2. View Active Deliveries")
    print("3. View Driver Locations")
    print("4. View Driver Health Reports")
    print("5. Back to Main Menu")

    try:
        choice = int(input("\nEnter your choice (1-5): "))
        
        if choice == 1:
            drivers = read_lines_from_file('driver.txt')
            if drivers:
                print("\n=== All Drivers ===")
                print("Driver ID | Name          | Route   | Status")
                print("-" * 50)
                for driver in drivers[1:]:
                    d = driver.strip().split(',')
                    print(f"{d[0]:9} | {d[1]:13} | {d[2]:7} | {d[5]}")
            else:
                print("\nNo driver data found")

        elif choice == 2:
            drivers = read_lines_from_file('driver.txt')
            if drivers:
                print("\n=== Active Deliveries ===")
                print("Driver ID | Name          | Consignment | Weight  | Status")
                print("-" * 60)
                for driver in drivers[1:]:
                    d = driver.strip().split(',')
                    if d[5] in ["In Progress", "Pending"]:
                        print(f"{d[0]:9} | {d[1]:13} | {d[3]:11} | {d[4]:7} | {d[5]}")
            else:
                print("\nNo driver data found")

        elif choice == 3:
            drivers = read_lines_from_file('driver.txt')
            vehicles = read_lines_from_file('vehicle.txt')
            if drivers and vehicles:
                print("\n=== Driver Locations ===")
                print("Driver ID | Name          | Location")
                print("-" * 45)
            
                vehicle_locations = {v.split(',')[4]: v.split(',')[5] 
                                  for v in vehicles[1:]}
                
                for driver in drivers[1:]:
                    d = driver.strip().split(',')
                    location = vehicle_locations.get(d[0], "Unknown")
                    print(f"{d[0]:9} | {d[1]:13} | {location}")
            else:
                print("\nNo data found")

        elif choice == 4:
            drivers = read_lines_from_file('driver.txt')
            if drivers:
                print("\n=== Driver Health Reports ===")
                print("Driver ID | Name          | Health Status")
                print("-" * 45)
                for driver in drivers[1:]:
                    d = driver.strip().split(',')
                    print(f"{d[0]:9} | {d[1]:13} | {d[6]}")
            else:
                print("\nNo driver data found")

        elif choice == 5:
            return
        else:
            print("Invalid choice")
            
    except ValueError:
        print("Invalid input. Please enter a number.")

def generate_reports():
    print("\n=== Generate Reports ===")
    print("1. Performance Metrics")
    print("2. Trip Log Reports")
    print("3. Back to Main Menu")

    try:
        choice = int(input("\nEnter your choice (1-3): "))
        
        if choice == 1:
            vehicles = read_lines_from_file('vehicle.txt')
            drivers = read_lines_from_file('driver.txt')
            
            if vehicles and drivers:
                print("\n=== Performance Metrics Report ===")
                
                total_vehicles = len(vehicles) - 1
                vehicles_needing_maintenance = sum(1 for v in vehicles[1:] 
                    if v.strip().split(',')[1] == "Needs Maintenance")
                
                total_drivers = len(drivers) - 1
                active_deliveries = sum(1 for d in drivers[1:] 
                    if d.strip().split(',')[5] in ["In Progress", "Pending"])
                completed_deliveries = sum(1 for d in drivers[1:] 
                    if d.strip().split(',')[5] == "Delivered")
                
                print("\nFleet Metrics:")
                print(f"Total Vehicles: {total_vehicles}")
                print(f"Vehicles Needing Maintenance: {vehicles_needing_maintenance}")
                print(f"Fleet Operational Rate: {((total_vehicles-vehicles_needing_maintenance)/total_vehicles)*100:.1f}%")
                
                print("\nDelivery Metrics:")
                print(f"Total Drivers: {total_drivers}")
                print(f"Active Deliveries: {active_deliveries}")
                print(f"Completed Deliveries: {completed_deliveries}")
                print(f"Delivery Success Rate: {(completed_deliveries/(completed_deliveries+active_deliveries))*100:.1f}%")
            else:
                print("\nInsufficient data for report generation")

        elif choice == 2:
            generate_trip_log_reports()

        elif choice == 3:
            return
        else:
            print("Invalid choice")
            
    except ValueError:
        print("Invalid input. Please enter a number.")

def generate_trip_log_reports():
    print("\n=== Trip Log Reports ===")
    drivers = read_lines_from_file('driver.txt')
    vehicles = read_lines_from_file('vehicle.txt')
    
    if drivers and vehicles:
        print("\nDetailed Trip Logs:")
        print("-" * 80)
        
        # Create vehicle lookup for locations
        vehicle_locations = {v.split(',')[4]: v.split(',')[5] 
                           for v in vehicles[1:]}
        
        for driver in drivers[1:]:
            d = driver.strip().split(',')
            location = vehicle_locations.get(d[0], "Unknown")
            
            print(f"Driver: {d[1]} (ID: {d[0]})")
            print(f"Route: {d[2]}")
            print(f"Current Location: {location}")
            print(f"Consignment: {d[3]} ({d[4]} kg)")
            print(f"Delivery Status: {d[5]}")
            print("-" * 80)
            
        total_weight = sum(float(d.strip().split(',')[4]) for d in drivers[1:])
        total_deliveries = len(drivers) - 1
        print("\nSummary Statistics:")
        print(f"Total Deliveries: {total_deliveries}")
        print(f"Total Weight Handled: {total_weight:.2f} kg")
        print(f"Average Weight per Delivery: {total_weight/total_deliveries:.2f} kg")
    else:
        print("\nNo data available for trip log generation")

def execute_admin_features():
    admin_dashboard()

if __name__ == "__main__":
    execute_admin_features()