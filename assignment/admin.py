def read_lines_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        return []

# Utility function to write lines to a file
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
    print('5. Fleet Management')
    print('6. Reports')

    file_mapping = {
        1: 'order_ids.txt',
        2: 'ongoingorder.txt',
        3: 'completedorder.txt',
        4: 'driver.txt',
        5: 'vehicle.txt',
        6: 'user.txt'
    }

    try:
        choice = int(input('Enter your choice: '))
        if choice in file_mapping:
            lines = read_lines_from_file(file_mapping[choice])
            if lines:
                for line in lines:
                    print(line.strip())
            else:
                print("No data found")
        else:
            print("Invalid choice")
    except ValueError:
        print("Please enter a valid number")

def vehicle_management_and_maintenance():
    pass

def manage_fuel_and_vehicle_consumption():
    pass

def driver_management():
    pass

def generate_reports():
    read_lines_from_file('user.txt')

    generate_trip_log_reports()

def generate_trip_log_reports():
    pass

def execute_admin_features():
    admin_dashboard()
    vehicle_management_and_maintenance()
    manage_fuel_and_vehicle_consumption()
    driver_management()
    generate_reports()

admin_dashboard()
# read_lines_from_file('driver.txt')