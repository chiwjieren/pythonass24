from user import read_lines_from_file
from user import write_lines_to_file

def admin_dashboard():
    print('1. Overview of Shipments')
    print('2. Pending Shipments')
    print('3. Completed Shipments')
    print('4. Driver Information')
    print('5. Fleet Management')
    print('6. Fuel & Vehicle Consumption Stats')
    print('7. Reports')

    choice = int(input('Enter your choice: '))

    options = {
        1 : read_lines_from_file('order_ids.txt'),
        2 : read_lines_from_file('ongoingorder.txt'),
        3 : read_lines_from_file('completedorder.txt'),
        4 : read_lines_from_file('driver.txt'),
        5 : read_lines_from_file('vehicle.txt'),
        6 : read_lines_from_file('fuel.txt'),
        7 : read_lines_from_file('user.txt'),
    }

    if choice in options:
        print(options[choice])
    else:
        print('Invalid choice')

def vehicle_management_and_maintenance():
    print('1. Vehicle Status')
    print('2. Vehicle Maintenance History')
    print('3. Maintenance Alert')
    print('4. Schedule Maintenance')

def manage_fuel_and_vehicle_consumption():
    print('1. Fuel Level')
    print('2. Fuel Consumption Pattern')
    print('3. Utilization Rate')
    print('4. Low Fuel Alert')

def driver_management():
    print('1. Driver Status')
    print('2. Current Location')
    print('3. Ongoing Assignment')

def generate_reports():
    print('1. Inventory Turnover Ratio')
    print('2. Truck Turnaround Time')
    print('3. Average Transportation Cost')

    generate_trip_log_reports()

    def generate_trip_log_reports():
                print('1. Trip Log Reports')

def execute_admin_features():
    admin_dashboard()
    vehicle_management_and_maintenance()
    manage_fuel_and_vehicle_consumption()
    driver_management()
    generate_reports()

admin_dashboard()