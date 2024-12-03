def admin_dashboard():
    print('1. Overview of Shipments')
    print('2. Pending Shipments')
    print('3. Completed Shipments')
    print('4. Ongoing Deliveries')
    print('5. Driver Information')
    print('6. Fleet Management')
    print('7. Order Processing Status')
    print('8. Fuel & Vehicle Consumption Stats')
    print('9. Reports')

    choice = int(input('Enter your choice: '))

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

