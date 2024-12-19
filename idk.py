# File paths
import datetime
DRIVER_FILE = "drivers.txt"
USER_FILE = "userdetails.txt"
ONGOING_ORDER_FILE = "ongoingorder.txt"
CANCELLED_ORDER_FILE = "cancelledorder.txt"
COMPLETED_ORDER_FILE = "completedorder.txt"
ORDER_ID_FILE = "order_ids.txt"
REVIEWS_FILE = "reviews.txt"
TO_BE_REVIEWED_FILE = "tobereview.txt"
REVIEWED_FILE = "reviewed.txt"
VEHICLE_FILE = "vehicles.txt"
MAINTENANCE_FILE = "maintenance.txt"
FUEL_LOG_FILE = "fuel_logs.txt"
FUEL_RATES_FILE = "fuel_rates.txt"
ROUTE_DISTANCES_FILE = "route_distances.txt"

# Add these constants at the top with other constants
STOPOVER_TIME = 30  # minutes
SAFETY_CHECK_TIME = 30  # minutes
TURNOVER_TIME = 60  # minutes

# Utility functions for file operations
def load_data(filename):
    try:
        with open(filename, 'r') as file:
            lines = [line.strip().split(',') for line in file if line.strip()]
            if not lines:  # If file is empty
                return []
            # Skip header if it exists
            if lines and (lines[0][0] == 'DriverID' or lines[0][0] == 'OrderID' or 
                         lines[0][0] == 'Username' or lines[0][0] == 'UserID' or
                         lines[0][0] == 'VehicleID' or lines[0][0] == 'VehicleType' or
                         lines[0][0] == 'RouteName'):
                return lines[1:]
            return lines
    except FileNotFoundError:
        # Create the file with appropriate header
        initialize_system_files()
        return []
    except Exception as e:
        print_error(f"Error loading data from {filename}: {e}")
        return []

def save_data(filename, data, header=None):
    with open(filename, 'w') as file:
        if header:
            file.write(header)
        for item in data:
            file.write(','.join(item) + '\n')

def get_next_id(prefix, current_ids=None):
    """Get next ID considering all order files"""
    if prefix == 'ORD':  # Special handling for order IDs
        # Load orders from all order-related files
        ongoing_orders = load_data(ONGOING_ORDER_FILE)
        completed_orders = load_data(COMPLETED_ORDER_FILE)
        cancelled_orders = load_data(CANCELLED_ORDER_FILE)
        
        # Combine all order IDs
        all_order_ids = []
        all_order_ids.extend(order[0] for order in ongoing_orders)
        all_order_ids.extend(order[0] for order in completed_orders)
        all_order_ids.extend(order[0] for order in cancelled_orders)
        
        if not all_order_ids:
            return f"{prefix}001"
            
        # Extract numbers from order IDs and find the maximum
        max_num = max(int(order_id[3:]) for order_id in all_order_ids)
        return f"{prefix}{str(max_num + 1).zfill(3)}"
    else:
        # Original logic for other ID types
        if not current_ids:
            return f"{prefix}001"
        last_id = max(int(id[len(prefix):]) for id in current_ids)
        return f"{prefix}{str(last_id + 1).zfill(3)}"

# UI utility functions
def print_header(text):
    """Print a consistent header with a title"""
    width = 50
    print("\n" + "=" * width)
    print(f"{text:^{width}}")
    print("=" * width)

def print_menu(title, options):
    """Print a consistent menu with options"""
    width = 50
    print("\n+" + "-" * (width-2) + "+")
    print(f"| {title:<{width-3}}|")
    print("+" + "-" * (width-2) + "+")
    for i, option in enumerate(options, 1):
        print(f"| {i}. {option:<{width-5}}|")
    print("+" + "-" * (width-2) + "+")

def print_info(text):
    """Print information messages consistently"""
    print(f"\n| > {text}")

def print_error(text):
    """Print error messages consistently"""
    print(f"\n| ! {text}")

def print_success(text):
    """Print success messages consistently"""
    print(f"\n| * {text}")

def print_divider():
    """Print a consistent divider line"""
    print("\n" + "─" * 50)

def print_order_details(order):
    """Print order details in a consistent format"""
    width = 50
    print("\n+" + "-" * (width-2) + "+")
    print(f"| Order ID: {order[0]:<{width-13}}|")
    print(f"| Item: {order[1]:<{width-9}}|")
    print(f"| Quantity: {order[2]:<{width-12}}|")
    print(f"| Status: {order[12]:<{width-11}}|")
    print("+" + "-" * (width-2) + "+")

def print_review_details(review):
    """Print review details in a consistent format"""
    width = 50
    print("\n+" + "-" * (width-2) + "+")
    print(f"| Order ID: {review[0]:<{width-13}}|")
    print(f"| Item: {review[1]:<{width-9}}|")
    print(f"| Rating: {'*' * int(review[3]):<{width-11}}|")
    print(f"| Review: {review[2]:<{width-11}}|")
    print(f"| Date: {review[5]:<{width-9}}|")
    print("+" + "-" * (width-2) + "+")

class PricingCalculator:
    def __init__(self):
        # Base pricing configuration
        self.base_price = 50
        self.price_per_unit = 10
        
        # Vehicle type pricing
        self.vehicle_prices = {
            "Specialized Carrier": 100,
            "Van": 150,
            "Truck": 200
        }
        
        # Shipment size pricing
        self.shipment_size_prices = {
            "BulkOrder": 50,
            "SmallParcel": 100,
            "SpecialCargo": 150
        }
    
    def calculate_vehicle_price(self, vehicle_type):
        """Calculate price based on vehicle type"""
        return self.vehicle_prices.get(vehicle_type, 0)
    
    def calculate_shipment_price(self, shipment_size):
        """Calculate price based on shipment size"""
        return self.shipment_size_prices.get(shipment_size, 0)
    
    def calculate_quantity_price(self, quantity):
        """Calculate price based on quantity"""
        return quantity * self.price_per_unit
    
    def calculate_total_price(self, quantity, vehicle_type, shipment_size):
        """Calculate total price for an order"""
        total = self.base_price
        total += self.calculate_quantity_price(quantity)
        total += self.calculate_vehicle_price(vehicle_type)
        total += self.calculate_shipment_price(shipment_size)
        return total

# Create a global instance of the pricing calculator
pricing_calculator = PricingCalculator()

def calculate_order_price(quantity, vehicle_type, shipment_size):
    """Calculate the total price for an order using the pricing calculator"""
    return pricing_calculator.calculate_total_price(quantity, vehicle_type, shipment_size)

# Main menu and system selection
def main_menu():
    # Initialize system files
    initialize_system_files()
    
    while True:
        print_header("LOGISTICS MANAGEMENT SYSTEM")
        options = ["Driver Access", "Customer Access", "Admin Access", "Exit"]
        print_menu("Main Menu", options)
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == '1':
            driver_system()
        elif choice == '2':
            customer_system()
        elif choice == '3':
            admin_login()
        elif choice == '4':
            print_info("Thank you for using the system!")
            break
        else:
            print_error("Invalid choice!")

def admin_login():
    print_header("Admin Login")
    username = input("Admin Username: ")
    password = input("Admin Password: ")
    
    # Simple admin authentication (you might want to make this more secure)
    if username == "admin" and password == "admin123":
        print_success("Admin login successful!")
        admin_system()
    else:
        print_error("Invalid admin credentials!")

def admin_system():
    while True:
        print_header("Admin Dashboard")
        options = [
            "Overview of Shipments",
            "Pending Shipments",
            "Completed Shipments",
            "Driver Information",
            "Assign Orders to Drivers",
            "Fuel & Consumption",
            "Fleet Management",
            "Reports",
            "Logout"
        ]
        print_menu("Admin Options", options)

        try:
            choice = int(input("\nEnter choice (1-9): "))
            if choice == 1:
                overview_of_shipments()
            elif choice == 2:
                pending_shipments()
            elif choice == 3:
                completed_shipments()
            elif choice == 4:
                driver_management()
            elif choice == 5:
                assign_orders_to_drivers()
            elif choice == 6:
                manage_fuel_and_vehicle_consumption()
            elif choice == 7:
                vehicle_management_and_maintenance()
            elif choice == 8:
                generate_reports()
            elif choice == 9:
                print_success("Logged out from admin system")
                break
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input. Please enter a number.")

def assign_orders_to_drivers():
    print_header("Assign Orders to Drivers")
    
    # Get pending orders
    orders = load_data(ONGOING_ORDER_FILE)
    pending_orders = [order for order in orders if order[12].lower() == 'pending']
    
    if not pending_orders:
        print_info("No pending orders to assign!")
        return
    
    # Get available drivers
    drivers = load_data(DRIVER_FILE)
    available_drivers = [driver for driver in drivers if driver[7].lower() == 'available']
    
    if not available_drivers:
        print_info("No available drivers!")
        return
    
    # Show pending orders
    print("\nPending Orders:")
    for i, order in enumerate(pending_orders, 1):
        print(f"\n{i}. Order Details:")
        print(f"   Order ID: {order[0]}")
        print(f"   From: {order[4]} To: {order[3]}")
        print(f"   Item: {order[1]} (Quantity: {order[2]})")
        print(f"   Vehicle Type: {order[10]}")
        print("-" * 50)
    
    # Select order
    try:
        order_choice = int(input("\nSelect order to assign (0 to cancel): "))
        if order_choice == 0:
            return
        if not (1 <= order_choice <= len(pending_orders)):
            print_error("Invalid order selection!")
            return
        
        selected_order = pending_orders[order_choice - 1]
        
        # Show available drivers
        print("\nAvailable Drivers:")
        for i, driver in enumerate(available_drivers, 1):
            print(f"{i}. Driver ID: {driver[0]}, Name: {driver[3]}")
        
        # Select driver
        driver_choice = int(input("\nSelect driver to assign (0 to cancel): "))
        if driver_choice == 0:
            return
        if not (1 <= driver_choice <= len(available_drivers)):
            print_error("Invalid driver selection!")
            return
        
        selected_driver = available_drivers[driver_choice - 1]

        # Simplified route selection
        print("\nAvailable Routes:")
        print("1. Route 1")
        print("2. Route 2")
        
        route_choice = int(input("\nSelect route to assign (1-2): "))
        if route_choice not in [1, 2]:
            print_error("Invalid route selection! Please select 1 or 2.")
            return
        
        selected_route = f"Route {route_choice}"  # Assign simplified route
        
        # Ensure the order list is long enough
        while len(selected_order) < 18:  # Ensure it has at least 18 elements
            selected_order.append('')  # Extend the list if necessary
        
        # Update order with assigned driver, route, and change status
        selected_order[16] = selected_driver[0]  # Assign DriverID
        selected_order[12] = 'Assigned'  # Update status to 'Assigned'
        selected_order[17] = selected_route  # Assign the selected route
        
        # Update the original orders list with the modified order
        orders[orders.index(selected_order)] = selected_order
        
        # Save updates
        save_data(ONGOING_ORDER_FILE, orders,
                 "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                 "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                 "Status,PurchaseDate,UserID,Price,DriverID,Route\n")
        
        print_success(f"Order {selected_order[0]} assigned to Driver {selected_driver[0]} on {selected_route}")
        
    except ValueError:
        print_error("Invalid input! Please enter a number.")

def update_order_status(username):
    print_header("Update Order Status")
    
    # Load driver data
    drivers = load_data(DRIVER_FILE)
    
    # Get driver's ID
    driver_id = next((driver[0] for driver in drivers if driver[1] == username), None)
    
    if not driver_id:
        print_error("Driver not found!")
        return
    
    # Get orders assigned to this driver
    orders = load_data(ONGOING_ORDER_FILE)
    assigned_orders = [
        order for order in orders 
        if len(order) >= 17 and order[16] == driver_id and order[12] in ['Assigned', 'Ongoing', 'Delivered']
    ]
    
    if not assigned_orders:
        print_info("No orders to update!")
        return
    
    # Display assigned orders
    print("\nYour Assigned Orders:")
    for i, order in enumerate(assigned_orders, 1):
        print(f"\n{i}. Order Details:")
        print(f"   Order ID: {order[0]}")
        print(f"   From: {order[4]} To: {order[3]}")
        print(f"   Item: {order[1]} (Quantity: {order[2]})")
        print(f"   Current Status: {order[12]}")
        # Check if the route index exists
        if len(order) > 17:
            print(f"   Route: {order[17]}")
        else:
            print("   Route: Not specified")
        print("-" * 50)
    
    try:
        choice = int(input("\nSelect order to update (0 to cancel): "))
        if choice == 0:
            return
        if not (1 <= choice <= len(assigned_orders)):
            print_error("Invalid order selection!")
            return
        
        selected_order = assigned_orders[choice - 1]
        current_status = selected_order[12]
        
        # Simplified status options based on current status
        if current_status == 'Assigned':
            new_status = 'Ongoing'
            print_info("Starting delivery journey...")
        elif current_status == 'Ongoing':
            new_status = 'Delivered'
            print_info("Marking as delivered...")
        else:
            print_error("Invalid order status for update!")
            return
            
        # Update the status
        for i, order in enumerate(orders):
            if order[0] == selected_order[0]:
                order[12] = new_status
                orders[i] = order
                break
        
        # Save the updated orders
        save_data(ONGOING_ORDER_FILE, orders,
                 "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                 "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                 "Status,PurchaseDate,UserID,Price,DriverID,Route\n")
        
        print_success(f"Status updated to {new_status} successfully!")
            
    except ValueError:
        print_error("Invalid input!")

def confirm_order_receipt(username):
    print_header("Confirm Order Receipt")
    
    # Load user data
    users = load_data(USER_FILE)
    
    # Get user's ID
    user_id = next((user[0] for user in users if user[1] == username), None)
    
    if not user_id:
        print_error("User not found!")
        return
    
    # Load orders
    orders = load_data(ONGOING_ORDER_FILE)
    
    # Filter orders for this user
    delivered_orders = [
        order for order in orders 
        if len(order) >= 17 and order[14] == user_id and order[12] == 'Delivered'
    ]
    
    if not delivered_orders:
        print_info("No delivered orders to confirm!")
        return
    
    # Display delivered orders
    for i, order in enumerate(delivered_orders, 1):
        print(f"\n{i}. Order Details:")
        print(f"   Order ID: {order[0]}")
        print(f"   From: {order[4]} To: {order[3]}")
        print(f"   Item: {order[1]} (Quantity: {order[2]})")
        print(f"   Status: {order[12]}")
        print("-" * 50)
    
    try:
        choice = int(input("\nSelect order to confirm receipt (0 to cancel): "))
        if choice == 0:
            return
        if not (1 <= choice <= len(delivered_orders)):
            print_error("Invalid order selection!")
            return
        
        selected_order = delivered_orders[choice - 1]
        
        # Move order to completed
        for i, order in enumerate(orders):
            if order[0] == selected_order[0]:
                order[12] = 'Completed'
                orders[i] = order
                break
        
        # Save the updated orders
        save_data(ONGOING_ORDER_FILE, orders,
                 "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                 "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                 "Status,PurchaseDate,UserID,Price,DriverID,Route\n")
        
        # Optionally, move the order to a completed orders file
        completed_orders = load_data(COMPLETED_ORDER_FILE)
        completed_orders.append(selected_order)
        save_data(COMPLETED_ORDER_FILE, completed_orders,
                 "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                 "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                 "Status,PurchaseDate,UserID,Price,DriverID,Route\n")
        
        print_success(f"Order {selected_order[0]} confirmed as received and moved to completed orders.")
        
    except ValueError:
        print_error("Invalid input!")

# Driver-related functions
def driver_system():
    while True:
        print_header("Driver Management System")
        options = ["Login", "Sign Up", "Back to Main Menu"]
        print_menu("Driver Options", options)
        
        choice = input("\nEnter choice (1-3): ")
        
        if choice == '1':
            username = driver_login()
            if username:
                driver_menu(username)
        elif choice == '2':
            driver_signup()
        elif choice == '3':
            break
        else:
            print_error("Invalid choice!")

def driver_login():
    print_header("Driver Login")
    username = input("Username: ")
    password = input("Password: ")
    
    drivers = load_data(DRIVER_FILE)
    for driver in drivers:
        if driver[1] == username and driver[2] == password:
            print_success(f"Login successful! Welcome Driver {driver[0]}")
            return username
    print_error("Invalid credentials!")
    return None

def driver_signup():
    print_header("Driver Registration")
    
    username = get_validated_input(
        "Enter Username",
        validate_username,
        "Username must be at least 5 characters long and contain only letters and numbers",
        "(min 5 characters, letters and numbers only)"
    )
    
    password = get_validated_input(
        "Enter Password",
        validate_password,
        "Password must be at least 8 characters and contain at least one letter and one number",
        "(min 8 chars, include numbers and letters)"
    )
    
    name = get_validated_input(
        "Enter Full Name",
        validate_name,
        "Name must contain only letters and spaces"
    )
    
    contact = get_validated_input(
        "Enter Contact Number",
        validate_phone_number,
        "Phone number must be in format: XXX-XXXXXXXX",
        "(format: XXX-XXXXXXXX)"
    )
    
    address = get_str_input("Enter Address: ")
    
    license_no = get_validated_input(
        "Enter License Number",
        validate_license_number,
        "License number must be in format: LXXXX (L=letter, X=number)",
        "(format: LXXXX)"
    )

    drivers = load_data(DRIVER_FILE)
    
    if any(driver[1] == username for driver in drivers):
        print_error("Username already exists!")
        return
    
    driver_ids = [driver[0] for driver in drivers]
    driver_id = get_next_id('D', driver_ids)
    
    new_driver = [
        driver_id, username, password, name, contact, 
        address, license_no, "available", "good"
    ]
    drivers.append(new_driver)
    save_data(DRIVER_FILE, drivers, 
             "DriverID,Username,Password,Name,Contact,Address,LicenseNo,Status,HealthReport\n")
    print_success(f"Registration successful! Your Driver ID is: {driver_id}")

def driver_menu(username):
    while True:
        print_header(f"Driver Menu - {username}")
        options = [
            "Update Profile",
            "View Assigned Orders",
            "Update Order Status",
            "View Routes",
            "Logout"
        ]
        print_menu("Driver Options", options)
        
        choice = input("\nEnter choice (1-5): ")
        
        if choice == '1':
            update_driver_profile(username)
        elif choice == '2':
            view_driver_orders(username)
        elif choice == '3':
            update_order_status(username)
        elif choice == '4':
            view_routes()
        elif choice == '5':
            print_success("Logged out successfully!")
            break
        else:
            print_error("Invalid choice!")

def update_driver_profile(username):
    drivers = load_data(DRIVER_FILE)
    for i, driver in enumerate(drivers):
        if driver[1] == username:
            print_header("Update Profile")
            driver[3] = input(f"Full Name (current: {driver[3]}): ") or driver[3]
            driver[4] = input(f"Contact (current: {driver[4]}): ") or driver[4]
            driver[5] = input(f"Address (current: {driver[5]}): ") or driver[5]
            driver[6] = input(f"License Number (current: {driver[6]}): ") or driver[6]
            
            # Update health report
            health_report = input(f"Health Report (current: {driver[8]}): ") or driver[8].lower()
            while health_report not in ["good", "bad"]:
                print_error("Invalid input! Please enter 'Good' or 'Bad'.")
                health_report = input("Health Report (Good/Bad): ").strip().lower()
            driver[8] = health_report
            
            drivers[i] = driver
            save_data(DRIVER_FILE, drivers, "DriverID,Username,Password,Name,Contact,Address,LicenseNo,Status,HealthReport\n")
            print_success("Profile updated successfully!")
            return
    print_error("Driver not found!")

def view_driver_orders(username):
    print_header("My Assigned Orders")
    
    # Load driver data
    drivers = load_data(DRIVER_FILE)
    
    # Get driver's ID
    driver_id = next((driver[0] for driver in drivers if driver[1] == username), None)
    
    if not driver_id:
        print_error("Driver not found!")
        return
    
    # Load orders
    orders = load_data(ONGOING_ORDER_FILE)
    
    # Filter orders for this driver
    driver_orders = [
        order for order in orders 
        if len(order) >= 17 and order[16] == driver_id and order[12] in ['Assigned', 'Ongoing', 'Delivered']
    ]
    
    if not driver_orders:
        print_info("No assigned orders found!")
        return
    
    # Display driver orders
    for order in driver_orders:
        print("\nOrder Details:")
        print(f"Order ID: {order[0]}")
        print(f"From: {order[4]} To: {order[3]}")
        print(f"Item: {order[1]} (Quantity: {order[2]})")
        print(f"Vehicle Type: {order[10]}")
        # Check if the route index exists
        if len(order) > 17:
            print(f"Route: {order[17]}")
        else:
            print("Route: Not specified")
        print(f"Status: {order[12]}")
        print("-" * 50)
    
    input("Press Enter to continue...")

def view_routes():
    print_header("Route Information")
    
    print("\nRoute Details:")
    print("1. Route 1: Johor → KL → Butterworth → Kedah → Perlis")
    print("   - Two round trips per day")
    print("   - Total distance: 850 km")
    
    print("\n2. Route 2: Johor → KL → Terengganu → Kelantan")
    print("   - One round trip per day")
    print("   - Total distance: 780 km")
    
    print("\nTime Requirements:")
    print(f"- Stopover time at each hub: {STOPOVER_TIME} minutes")
    print(f"- Safety checks and refueling: {SAFETY_CHECK_TIME} minutes")
    print(f"- Turnover time at destination: {TURNOVER_TIME} minutes")
    
    print("\nEstimated Journey Times:")
    print("Route 1:")
    print("  Johor → KL: 4 hours")
    print("  KL → Butterworth: 4 hours")
    print("  Butterworth → Kedah: 1 hour")
    print("  Kedah → Perlis: 1 hour")
    
    print("\nRoute 2:")
    print("  Johor → KL: 4 hours")
    print("  KL → Terengganu: 4 hours")
    print("  Terengganu → Kelantan: 2 hours")
    
    calculate_route_times()

def calculate_route_times():
    # Convert times to hours for calculations
    stopover = STOPOVER_TIME / 60
    safety_check = SAFETY_CHECK_TIME / 60
    turnover = TURNOVER_TIME / 60
    
    # Route 1 calculations
    route1_driving = 10  # 4 + 4 + 1 + 1 hours
    route1_stops = 3 * stopover  # 3 intermediate stops
    route1_total = (
        (route1_driving * 2) +  # Round trip driving
        (route1_stops * 2) +    # Stops both ways
        turnover +              # Destination turnover
        safety_check           # Safety checks
    )
    
    # Route 2 calculations
    route2_driving = 10  # 4 + 4 + 2 hours
    route2_stops = 2 * stopover  # 2 intermediate stops
    route2_total = (
        (route2_driving * 2) +  # Round trip driving
        (route2_stops * 2) +    # Stops both ways
        turnover +              # Destination turnover
        safety_check           # Safety checks
    )
    
    print("\nTotal Round Trip Times (including all stops):")
    print(f"Route 1: {route1_total:.1f} hours")
    print(f"Route 2: {route2_total:.1f} hours")

# Customer-related functions
def customer_system():
    while True:
        print_header("Customer System")
        options = ["Sign Up", "Login", "Back to Main Menu"]
        print_menu("Customer Options", options)
        
        try:
            choice = int(input("\nEnter choice: "))
            if choice == 1:
                customer_signup()
            elif choice == 2:
                userID = customer_login()
                if userID:
                    customer_welcome(userID)
            elif choice == 3:
                break
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input. Please enter a number.")

# Add all the remaining customer-related functions here...
# (The rest of the customer functions from your combined_logistics_system.py)

# Add these additional UI utility functions
def print_location_menu(locations):
    width = 50
    print("\n┌" + "─" * (width-2) + "┐")
    print("│" + "Available Locations".center(width-2) + "│")
    print("├" + "─" * (width-2) + "┤")
    for i, location in enumerate(locations, 1):
        print(f"│ {i}. {location:<{width-4}}│")
    print("└" + "─" * (width-2) + "┘")

def print_shipment_menu():
    width = 50
    print("\n┌" + "─" * (width-2) + "┐")
    print("│" + "Shipment Size Options".center(width-2) + "│")
    print("├" + "─" * (width-2) + "┤")
    print("│ 1. Bulk Order (Fits in a car trunk)".ljust(width-1) + "│")
    print("│ 2. Small Parcel (Fits in a van)".ljust(width-1) + "│")
    print("│ 3. Special Cargo (Requires a truck)".ljust(width-1) + "│")
    print("└" + "─" * (width-2) + "┘")

def print_vehicle_menu():
    width = 50
    print("\n┌" + "─" * (width-2) + "┐")
    print("│" + "Vehicle Type Options".center(width-2) + "│")
    print("├" + "─" * (width-2) + "┤")
    print("│ 1. Specialized Carrier".ljust(width-1) + "│")
    print("│ 2. Van".ljust(width-1) + "│")
    print("│ 3. Truck".ljust(width-1) + "│")
    print("└" + "─" * (width-2) + "┘")

def print_payment_menu():
    width = 50
    print("\n┌" + "─" * (width-2) + "┐")
    print("│" + "Payment Method Options".center(width-2) + "│")
    print("├" + "─" * (width-2) + "┤")
    print("│ 1. Credit/Debit Card".ljust(width-1) + "│")
    print("│ 2. UPI".ljust(width-1) + "│")
    print("│ 3. Mobile Wallet".ljust(width-1) + "│")
    print("│ 4. Cash On Delivery".ljust(width-1) + "│")
    print("└" + "─" * (width-2) + "┘")

def print_order_details_extended(order):
    width = 60
    print("\n┌" + "─" * (width-2) + "┐")
    print(f"│ Order ID: {order[0]:<{width-13}}│")
    print(f"│ Item: {order[1]:<{width-9}}│")
    print(f"│ Quantity: {order[2]:<{width-12}}│")
    print(f"│ Ship To: {order[3]:<{width-12}}│")
    print(f"│ Ship From: {order[4]:<{width-13}}│")
    print(f"│ Sender: {order[5]:<{width-11}}│")
    print(f"│ Sender Phone: {order[6]:<{width-16}}│")
    print(f"│ Recipient: {order[7]:<{width-13}}│")
    print(f"│ Recipient Phone: {order[8]:<{width-19}}│")
    print(f"│ Shipment Size: {order[9]:<{width-16}}│")
    print(f"│ Vehicle Type: {order[10]:<{width-16}}│")
    print(f"│ Payment Method: {order[11]:<{width-18}}│")
    print(f"│ Status: {order[12]:<{width-11}}│")
    print(f"│ Purchase Date: {order[13]:<{width-17}}│")
    print(f"│ Price: RM {order[15]:<{width-12}}│")
    print("└" + "─" * (width-2) + "┘")

def print_review_details(review):
    width = 50
    print("\n┌" + "─" * (width-2) + "┐")
    print(f"│ Order ID: {review[0]:<{width-13}}│")
    print(f"│ Item: {review[1]:<{width-9}}│")
    print(f"│ Rating: {'*' * int(review[3]):<{width-11}}│")
    print(f"│ Review: {review[2]:<{width-11}}│")
    print(f"│ Date: {review[5]:<{width-9}}│")
    print("└" + "─" * (width-2) + "┘")

# Customer functions
def customer_signup():
    print_header("Customer Registration")
    
    username = get_validated_input(
        "Enter Username",
        validate_username,
        "Username must be at least 5 characters long and contain only letters and numbers",
        "(min 5 characters, letters and numbers only)"
    )
    
    password = get_validated_input(
        "Enter Password",
        validate_password,
        "Password must be at least 8 characters and contain at least one letter and one number",
        "(min 8 chars, include numbers and letters)"
    )
    
    users = load_data(USER_FILE)
    user_ids = [user[0] for user in users]
    user_id = get_next_id('U', user_ids)
    
    user_data = [user_id, username, password]
    users.append(user_data)
    save_data(USER_FILE, users, "UserID,Username,Password\n")
    print_success(f"User created successfully! Your User ID: {user_id}")

def customer_login():
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()

    users = load_data(USER_FILE)
    for user in users:
        if user[1] == username and user[2] == password:
            print_success(f"Login successful! Welcome {username}")
            return user[0]

def customer_welcome(userID):
    while True:
        print_header(f"Welcome User {userID}")
        options = ["Orders", "Ratings and Reviews", "Log Out"]
        print_menu("User Menu", options)

        try:
            choice = int(input("\nEnter choice: "))
            if choice == 1:
                order_management(userID)
            elif choice == 2:
                ratings_and_reviews(userID)
            elif choice == 3:
                print_info("Logging out...")
                break
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input!")

def order_management(userID):
    while True:
        print_header("Order Management")
        options = [
            "New Order",
            "Cancel Order",
            "Order Received",
            "Reorder an Order",
            "View Orders",
            "Back to Main Menu"
        ]
        print_menu("Order Options", options)

        try:
            choice = int(input("\nEnter choice: "))
            if choice == 1:
                new_order(userID)
            elif choice == 2:
                cancel_order(userID)
            elif choice == 3:
                order_received(userID)
            elif choice == 4:
                reorder_order(userID)
            elif choice == 5:
                view_orders(userID)
            elif choice == 6:
                break
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input!")

def new_order(userID):
    print_header("New Order")
    locations = [
        "Johor", "Kuala Lumpur", "Butterworth", "Kedah", "Perlis", 
        "Terengganu", "Kelantan"
    ]
    
    print_divider()
    item_name = get_str_input("Enter Item Name: ")
    quantity = get_int_input("Enter Quantity: ", min_val=1)

    print_location_menu(locations)
    ship_from_choice = get_int_input("Enter shipping from location (1-7): ", min_val=1, max_val=7)
    ship_from = locations[ship_from_choice - 1]

    print_location_menu(locations)
    ship_to_choice = get_int_input("Enter shipping to location (1-7): ", min_val=1, max_val=7)
    ship_to = locations[ship_to_choice - 1]

    print_divider()
    sender_name = get_validated_input(
        "Enter Sender Name",
        validate_name,
        "Name must contain only letters and spaces"
    )
    
    sender_phone = get_validated_input(
        "Enter Sender Phone",
        validate_phone_number,
        "Phone number must be in format: XXX-XXXXXXXX",
        "(format: XXX-XXXXXXXX)"
    )
    
    recipient_name = get_validated_input(
        "Enter Recipient Name",
        validate_name,
        "Name must contain only letters and spaces"
    )
    
    recipient_phone = get_validated_input(
        "Enter Recipient Phone",
        validate_phone_number,
        "Phone number must be in format: XXX-XXXXXXXX",
        "(format: XXX-XXXXXXXX)"
    )

    print_shipment_menu()
    shipment_size_choice = input("\nEnter your choice (1-3): ").strip()
    shipment_size = {
        "1": "BulkOrder",
        "2": "SmallParcel",
        "3": "SpecialCargo"
    }.get(shipment_size_choice)
    
    if not shipment_size:
        print_error("Invalid choice for shipment size.")
        return

    print_vehicle_menu()
    vehicle_choice = input("\nEnter your choice (1-3): ").strip()
    vehicle_type = {
        "1": "Specialized Carrier",
        "2": "Van",
        "3": "Truck"
    }.get(vehicle_choice)
    
    if not vehicle_type:
        print_error("Invalid choice for vehicle type.")
        return

    print_payment_menu()
    payment_choice = input("\nEnter your choice (1-4): ").strip()
    payment_option = {
        "1": "Credit/Debit Card",
        "2": "UPI",
        "3": "Mobile Wallet",
        "4": "Cash On Delivery"
    }.get(payment_choice)
    
    if not payment_option:
        print_error("Invalid choice for payment method.")
        return

    # Automatically set purchase date to current date
    purchase_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Calculate order price
    price = calculate_order_price(quantity, vehicle_type, shipment_size)
    
    # Show price to user and confirm
    print_info(f"Total Order Price: RM {price}")
    confirm = input("Confirm order? (y/n): ").lower()
    if confirm != 'y':
        print_info("Order cancelled.")
        return

    # Generate order ID
    orders = load_data(ORDER_ID_FILE)
    order_ids = [order[0] for order in orders]
    order_id = get_next_id('ORD', order_ids)

    # Create order data
    order_data = [
        order_id, item_name, str(quantity), ship_to, ship_from,
        sender_name, sender_phone, recipient_name, recipient_phone,
        shipment_size, vehicle_type, payment_option, "Pending",
        purchase_date, userID, str(price)
    ]

    # Save to ongoing orders
    orders = load_data(ONGOING_ORDER_FILE)
    orders.append(order_data)
    save_data(ONGOING_ORDER_FILE, orders, 
              "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
              "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
              "Status,PurchaseDate,UserID,Price\n")
    
    # Save order ID
    with open(ORDER_ID_FILE, 'a') as file:
        file.write(f"{order_id}\n")
    
    print_success(f"Order successfully placed! Your Order ID: {order_id}")

def view_orders(userID):
    print_header("View Orders")
    
    # Load all orders for this user
    ongoing = load_data(ONGOING_ORDER_FILE)
    completed = load_data(COMPLETED_ORDER_FILE)
    cancelled = load_data(CANCELLED_ORDER_FILE)
    
    # Filter orders by user ID (index 14 is UserID)
    user_orders = {
        'Ongoing': [order for order in ongoing if order[14] == userID and order[12] in ['Pending', 'Assigned', 'Ongoing', 'Delivered']],
        'Completed': [order for order in completed if order[14] == userID],
        'Cancelled': [order for order in cancelled if order[14] == userID]
    }
    
    if not any(user_orders.values()):
        print_info("No orders found!")
        return
    
    # Display orders by status with tracking information
    for status, orders in user_orders.items():
        if orders:
            print(f"\n{status} Orders:")
            for order in orders:
                print("\n" + "-" * 50)
                print(f"Order ID: {order[0]}")
                print(f"Item: {order[1]} (Quantity: {order[2]})")
                print(f"From: {order[4]} To: {order[3]}")
                print(f"Status: {order[12]}")
                # Show tracking status based on order status
                if order[12] == 'Pending':
                    print("Tracking: Order confirmed, waiting for pickup")
                elif order[12] == 'Assigned':
                    print("Tracking: Driver assigned, preparing for pickup")
                elif order[12] == 'Ongoing':
                    print("Tracking: In transit to destination")
                elif order[12] == 'Delivered':
                    print("Tracking: Package delivered")
                elif order[12] == 'Completed':
                    print("Tracking: Order completed")
                elif order[12] == 'Cancelled':
                    print("Tracking: Order cancelled")
                
                print(f"Order Date: {order[13]}")
                print(f"Price: RM{order[15]}")
                
                if len(order) >= 17 and order[16]:  # If driver is assigned
                    driver_name = next((d[3] for d in load_data(DRIVER_FILE) if d[0] == order[16]), "Unassigned")
    
    print_divider()
    input("Press Enter to continue...")

def cancel_order(userID):
    orders = load_data(ONGOING_ORDER_FILE)
    user_orders = [order for order in orders if order[-2] == userID and order[12].lower() == 'pending']
    if not user_orders:
        print_info("No orders available to cancel!")
        return

    print_header("Orders Available to Cancel")
    for i, order in enumerate(user_orders, 1):
        print_order_details(order)
        print_divider()

    try:
        choice = int(input("Select order number to cancel (0 to go back): "))
        if choice == 0:
            return
        if 1 <= choice <= len(user_orders):
            order_to_cancel = user_orders[choice - 1]
            
            # Use current date for cancellation
            cancellation_date = datetime.datetime.now().strftime("%Y-%m-%d")
            order_to_cancel[13] = cancellation_date
            
            # Update status to Cancelled
            order_to_cancel[12] = 'Cancelled'
            
            # Move to cancelled orders
            cancelled_orders = load_data(CANCELLED_ORDER_FILE)
            cancelled_orders.append(order_to_cancel)
            save_data(CANCELLED_ORDER_FILE, cancelled_orders,
                     "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                     "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                     "Status,PurchaseDate,UserID,Price\n")
            
            # Remove from ongoing orders
            orders = [order for order in orders if order[0] != order_to_cancel[0]]
            save_data(ONGOING_ORDER_FILE, orders,
                     "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                     "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                     "Status,PurchaseDate,UserID,Price\n")
            
            print_success("Order cancelled successfully!")
        else:
            print_error("Invalid choice!")
    except ValueError:
        print_error("Invalid input!")

def order_received(userID):
    print_header("Mark Order as Received")
    
    # Get ongoing orders that are delivered and ready to be completed
    ongoing_orders = load_data(ONGOING_ORDER_FILE)
    completable_orders = [
        order for order in ongoing_orders 
        if order[14] == userID and order[12] == 'Delivered'
    ]
    
    if not completable_orders:
        print_info("No orders available to mark as received!")
        print_info("Note: Only delivered orders can be marked as received.")
        return
    
    print("\nOrders Available to Mark as Received:")
    for i, order in enumerate(completable_orders, 1):
        print(f"\n{i}. Order Details:")
        print(f"   Order ID: {order[0]}")
        print(f"   Item: {order[1]} (Quantity: {order[2]})")
        print(f"   From: {order[4]} To: {order[3]}")
        print(f"   Status: {order[12]}")
        print(f"   Driver: {next((d[3] for d in load_data(DRIVER_FILE) if d[0] == order[16]), 'Unknown')}")
        print("-" * 50)
    
    try:
        choice = int(input("\nSelect order to mark as received (0 to cancel): "))
        if choice == 0:
            return
        
        if 1 <= choice <= len(completable_orders):
            order_to_complete = completable_orders[choice - 1]
            
            # Update status to Completed
            order_to_complete[12] = 'Completed'
            
            # Move to completed orders
            completed_orders = load_data(COMPLETED_ORDER_FILE)
            completed_orders.append(order_to_complete)
            save_data(COMPLETED_ORDER_FILE, completed_orders,
                     "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                     "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                     "Status,PurchaseDate,UserID,Price,DriverID\n")
            
            # Remove from ongoing orders
            updated_ongoing = [
                order for order in ongoing_orders 
                if order[0] != order_to_complete[0]
            ]
            save_data(ONGOING_ORDER_FILE, updated_ongoing,
                     "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                     "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                     "Status,PurchaseDate,UserID,Price,DriverID,Route\n")
            
            # Add to to-be-reviewed
            to_be_reviewed = load_data(TO_BE_REVIEWED_FILE)
            to_be_reviewed.append(order_to_complete)
            save_data(TO_BE_REVIEWED_FILE, to_be_reviewed,
                     "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                     "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                     "Status,PurchaseDate,UserID,Price,DriverID\n")
            
            print_success("Order marked as received successfully!")
            print_info("You can now leave a review for this order.")
        else:
            print_error("Invalid choice!")
    except ValueError:
        print_error("Invalid input!")

def reorder_order(userID):
    print_header("Reorder Order")
    
    # Load orders
    completed_orders = load_data(COMPLETED_ORDER_FILE)
    cancelled_orders = load_data(CANCELLED_ORDER_FILE)
    
    # Filter orders for this user
    user_completed_orders = [
        order for order in completed_orders 
        if len(order) >= 15 and order[14] == userID
    ]
    
    user_cancelled_orders = [
        order for order in cancelled_orders 
        if len(order) >= 15 and order[14] == userID
    ]
    
    # Combine completed and cancelled orders
    user_orders = user_completed_orders + user_cancelled_orders
    
    if not user_orders:
        print_info("No completed or cancelled orders found!")
        return
    
    # Display user orders
    print("\nOrders available for reorder:")
    for i, order in enumerate(user_orders, 1):
        print(f"\n{i}. Order Details:")
        print(f"   Order ID: {order[0]}")
        print(f"   From: {order[4]} To: {order[3]}")
        print(f"   Item: {order[1]} (Quantity: {order[2]})")
        print(f"   Status: {'Completed' if order in user_completed_orders else 'Cancelled'}")
        print("-" * 50)
    
    try:
        choice = int(input("\nSelect order to reorder (0 to cancel): "))
        if choice == 0:
            return
        if not (1 <= choice <= len(user_orders)):
            print_error("Invalid order selection!")
            return
            
        selected_order = user_orders[choice - 1]
        
        # Get existing order IDs to generate new ID
        existing_orders = load_data(ONGOING_ORDER_FILE)
        order_ids = [order[0] for order in existing_orders]
        new_order_id = get_next_id('ORD', order_ids)
        
        # Create new order based on selected order, but without driver info
        new_order = selected_order[:16]  # Only copy up to the price field
        new_order[0] = new_order_id      # Set new order ID
        new_order[12] = 'Pending'        # Set status to Pending
        new_order[13] = datetime.datetime.now().strftime("%Y-%m-%d")  # Update date
        
        # Add the new order to ongoing orders
        existing_orders.append(new_order)
        save_data(ONGOING_ORDER_FILE, existing_orders,
                 "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                 "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                 "Status,PurchaseDate,UserID,Price\n")
        
        print_success(f"Order {new_order_id} has been successfully created!")
        
    except ValueError:
        print_error("Invalid input! Please enter a number.")

def ratings_and_reviews(userID):
    while True:
        print_header("Ratings and Reviews")
        options = ["Leave a Review", "View Reviews", "Back to Main Menu"]
        print_menu("Review Options", options)

        try:
            choice = int(input("\nEnter choice: "))
            if choice == 1:
                leave_review(userID)
            elif choice == 2:
                view_reviews(userID)
            elif choice == 3:
                break
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input!")

def leave_review(userID):
    # Get orders that can be reviewed
    to_be_reviewed = load_data(TO_BE_REVIEWED_FILE)
    completed_orders = load_data(COMPLETED_ORDER_FILE)
    cancelled_orders = load_data(CANCELLED_ORDER_FILE)  # Add cancelled orders
    reviews = load_data(REVIEWS_FILE)
    
    # Get IDs of orders already reviewed
    reviewed_order_ids = {review[0] for review in reviews}  # Using set for faster lookup
    
    # Create a set to track added order IDs to prevent duplicates
    added_order_ids = set()
    reviewable_orders = []
    
    # Add orders from to_be_reviewed if not already reviewed
    for order in to_be_reviewed:
        if (order[14] == userID and 
            order[0] not in reviewed_order_ids and 
            order[0] not in added_order_ids):
            reviewable_orders.append(order)
            added_order_ids.add(order[0])
    
    # Add completed orders that haven't been reviewed
    for order in completed_orders:
        if (order[14] == userID and 
            order[0] not in reviewed_order_ids and 
            order[0] not in added_order_ids):
            reviewable_orders.append(order)
            added_order_ids.add(order[0])
    
    # Add cancelled orders that haven't been reviewed
    for order in cancelled_orders:
        if (order[14] == userID and 
            order[0] not in reviewed_order_ids and 
            order[0] not in added_order_ids):
            reviewable_orders.append(order)
            added_order_ids.add(order[0])
    
    if not reviewable_orders:
        print_info("No orders available for review!")
        return

    print_header("Orders Available for Review")
    for i, order in enumerate(reviewable_orders, 1):
        print(f"\n{i}. Order Details:")
        print(f"   Order ID: {order[0]}")
        print(f"   Item: {order[1]} (Quantity: {order[2]})")
        print(f"   Status: {order[12]}")
        print(f"   Date: {order[13]}")
        print("-" * 50)

    try:
        choice = int(input("\nSelect order to review (0 to cancel): "))
        if choice == 0:
            return
        if not (1 <= choice <= len(reviewable_orders)):
            print_error("Invalid order selection!")
            return
            
        order_to_review = reviewable_orders[choice - 1]
        
        # Get review details
        print_divider()
        review_text = input("Enter your review: ").strip()
        while True:
            try:
                rating = int(input("Enter rating (1-5 stars): "))
                if 1 <= rating <= 5:
                    break
                print_error("Rating must be between 1 and 5!")
            except ValueError:
                print_error("Invalid input! Please enter a number.")
        
        # Use current date for review
        review_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Create review record
        review_data = [
            order_to_review[0],  # Order ID
            order_to_review[1],  # Item name
            review_text,         # Review text
            str(rating),         # Rating
            userID,              # User ID
            review_date          # Review date
        ]
        
        # Add to reviews file
        reviews = load_data(REVIEWS_FILE)
        reviews.append(review_data)
        save_data(REVIEWS_FILE, reviews, 
                 "OrderID,ItemName,Review,Rating,UserID,ReviewDate\n")
        
        # Remove from to_be_reviewed if it's there
        if order_to_review in to_be_reviewed:
            updated_to_review = [
                order for order in to_be_reviewed 
                if order[0] != order_to_review[0]
            ]
            save_data(TO_BE_REVIEWED_FILE, updated_to_review,
                     "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                     "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                     "Status,PurchaseDate,UserID,Price,DriverID\n")
        
        print_success("Review submitted successfully!")
        
    except ValueError:
        print_error("Invalid input!")

def view_reviews(userID):
    print_header(f"Reviews for User {userID}")
    reviews = load_data(REVIEWS_FILE)
    user_reviews = [review for review in reviews if review[4] == userID]
    
    if not user_reviews:
        print_info("No reviews found!")
        return
    
    for review in user_reviews:
        width = 50
        print("\n+" + "-" * (width-2) + "+")
        print(f"| Order ID: {review[0]:<{width-13}}|")
        print(f"| Item: {review[1]:<{width-9}}|")
        print(f"| Rating: {'*' * int(review[3]):<{width-11}}|")
        print(f"| Review: {review[2]:<{width-11}}|")
        print(f"| Date: {review[5]:<{width-9}}|")
        print("+" + "-" * (width-2) + "+")
    
    print_divider()
    input("Press Enter to continue...")

# Add this utility function if not already present
def validate_date(date_str, allow_future=False):
    """
    Validates date string format and logic.
    Returns tuple (is_valid, formatted_date, error_message)
    """
    try:
        # Parse the date string
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        
        # Check if date is in the future when not allowed
        if not allow_future and date_obj.date() > datetime.datetime.now().date():
            return False, None, "Date cannot be in the future!"
        
        # Return formatted date string
        return True, date_obj.strftime("%Y-%m-%d"), None
    except ValueError:
        return False, None, "Invalid date format! Use YYYY-MM-DD"

def overview_of_shipments():
    print_header("Overview of Shipments")
    
    # Load all orders from different files
    ongoing = load_data(ONGOING_ORDER_FILE)
    completed = load_data(COMPLETED_ORDER_FILE)
    cancelled = load_data(CANCELLED_ORDER_FILE)
    
    # Calculate statistics
    total_orders = len(ongoing) + len(completed) + len(cancelled)
    pending_orders = len([order for order in ongoing if order[12].lower() == 'pending'])
    in_transit = len([order for order in ongoing if order[12].lower() in ['ongoing', 'at hub']])
    delivered = len([order for order in ongoing if order[12].lower() == 'delivered'])
    
    # Display statistics
    print("\nOrder Statistics:")
    print(f"Total Orders: {total_orders}")
    print(f"Pending Orders: {pending_orders}")
    print(f"In Transit: {in_transit}")
    print(f"Delivered: {delivered}")
    print(f"Completed: {len(completed)}")
    print(f"Cancelled: {len(cancelled)}")
    
    print_divider()
    input("Press Enter to continue...")

def pending_shipments():
    print_header("Pending Shipments")
    
    ongoing = load_data(ONGOING_ORDER_FILE)
    pending = [order for order in ongoing if order[12].lower() == 'pending']
    
    if not pending:
        print_info("No pending shipments found!")
        return
    
    for order in pending:
        print_order_details_extended(order)
    
    print_divider()
    input("Press Enter to continue...")

def completed_shipments():
    print_header("Completed Shipments")
    
    completed = load_data(COMPLETED_ORDER_FILE)
    
    if not completed:
        print_info("No completed shipments found!")
        return
    
    for order in completed:
        print_order_details_extended(order)
    
    print_divider()
    input("Press Enter to continue...")

def driver_management():
    while True:
        print_header("Driver Management")
        options = [
            "View All Drivers",
            "View Available Drivers",
            "View Assigned Drivers",
            "Update Driver Status",
            "Remove Driver",
            "Back"
        ]
        print_menu("Driver Management Options", options)
        
        try:
            choice = int(input("\nEnter choice (1-6): "))
            if choice == 1:
                view_all_drivers()
            elif choice == 2:
                view_available_drivers()
            elif choice == 3:
                view_assigned_drivers()
            elif choice == 4:
                update_driver_status()
            elif choice == 5:
                remove_driver()
            elif choice == 6:
                break
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input!")

def view_all_drivers():
    drivers = load_data(DRIVER_FILE)
    print_header("All Drivers")
    
    if not drivers:
        print_info("No drivers found!")
        return
    
    for driver in drivers:
        print_driver_details(driver)
    
    print_divider()
    input("Press Enter to continue...")

def print_driver_details(driver):
    width = 50
    print("\n┌" + "─" * (width-2) + "┐")
    print(f"│ Driver ID: {driver[0]:<{width-13}}│")
    print(f"│ Name: {driver[3]:<{width-9}}│")
    print(f"│ Contact: {driver[4]:<{width-12}}│")
    print(f"│ Status: {driver[7]:<{width-11}}│")
    print("└" + "─" * (width-2) + "┘")

def view_available_drivers():
    drivers = load_data(DRIVER_FILE)
    available = [driver for driver in drivers if driver[7].lower() == 'available']
    
    print_header("Available Drivers")
    
    if not available:
        print_info("No available drivers found!")
        return
    
    for driver in available:
        print_driver_details(driver)
    
    print_divider()
    input("Press Enter to continue...")

def view_assigned_drivers():
    drivers = load_data(DRIVER_FILE)
    assigned = [driver for driver in drivers if driver[7].lower() == 'assigned']
    
    print_header("Assigned Drivers")
    
    if not assigned:
        print_info("No assigned drivers found!")
        return
    
    for driver in assigned:
        print_driver_details(driver)
        # Show current assignment
        orders = load_data(ONGOING_ORDER_FILE)
        for order in orders:
            if len(order) >= 17 and order[16] == driver[0]:
                print(f"Current Assignment: Order {order[0]}")
                print(f"Route: {order[17]}")
                break
    
    print_divider()
    input("Press Enter to continue...")

def update_driver_status():
    drivers = load_data(DRIVER_FILE)
    
    print_header("Update Driver Status")
    driver_id = input("Enter Driver ID: ").strip()
    
    for i, driver in enumerate(drivers):
        if driver[0] == driver_id:
            print(f"Current status: {driver[7]}")
            print("\nAvailable statuses:")
            print("1. Available")
            print("2. Assigned")
            print("3. On Leave")
            
            try:
                status_choice = input("\nEnter choice (1-3): ")
                new_status = {
                    '1': 'available',
                    '2': 'assigned',
                    '3': 'on leave'
                }.get(status_choice)
                
                if new_status:
                    driver[7] = new_status
                    drivers[i] = driver
                    save_data(DRIVER_FILE, drivers,
                             "DriverID,Username,Password,Name,Contact,Address,LicenseNo,Status\n")
                    print_success(f"Status updated to {new_status}")
                    return
                else:
                    print_error("Invalid choice!")
            except ValueError:
                print_error("Invalid input!")
            return
    
    print_error("Driver not found!")

def remove_driver():
    drivers = load_data(DRIVER_FILE)
    
    print_header("Remove Driver")
    driver_id = input("Enter Driver ID: ").strip()
    
    # Check if driver has any ongoing assignments
    orders = load_data(ONGOING_ORDER_FILE)
    for order in orders:
        if len(order) >= 17 and order[16] == driver_id:
            print_error("Cannot remove driver with ongoing assignments!")
            return
    
    # Remove driver
    updated_drivers = [driver for driver in drivers if driver[0] != driver_id]
    
    if len(updated_drivers) == len(drivers):
        print_error("Driver not found!")
        return
    
    save_data(DRIVER_FILE, updated_drivers,
             "DriverID,Username,Password,Name,Contact,Address,LicenseNo,Status\n")
    print_success("Driver removed successfully!")

def manage_fuel_and_vehicle_consumption():
    while True:
        print_header("Fuel & Vehicle Consumption Management")
        options = [
            "View Completed Orders Fuel Analysis",
            "View Fuel Consumption History",
            "Update Fuel Rates",
            "View Route Analysis",
            "Back"
        ]
        print_menu("Fuel Management Options", options)
        
        try:
            choice = int(input("\nEnter choice (1-5): "))
            if choice == 1:
                view_completed_orders_fuel_analysis()
            elif choice == 2:
                view_fuel_consumption_history()
            elif choice == 3:
                update_fuel_rates()
            elif choice == 4:
                view_route_analysis()
            elif choice == 5:
                break
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input!")

def view_completed_orders_fuel_analysis():
    print_header("Fuel Consumption Analysis")
    
    # Load necessary data
    completed_orders = load_data(COMPLETED_ORDER_FILE)
    fuel_logs = load_data(FUEL_LOG_FILE)
    
    # Get set of already logged order IDs
    logged_orders = {log[0] for log in fuel_logs}
    
    # Get completed orders from last 30 days that haven't been logged yet
    recent_completed = [
        order for order in completed_orders 
        if (datetime.datetime.now() - datetime.datetime.strptime(order[13], "%Y-%m-%d")).days <= 30
        and len(order) >= 18  # Ensure order has route information
        and order[0] not in logged_orders  # Only include orders not already logged
    ]
    
    fuel_rates = load_fuel_rates()
    route_distances = load_route_distances()
    current_fuel_price = 2.05  # RM per liter
    
    if not recent_completed:
        print_info("No new completed orders to analyze!")
        return
    
    total_fuel = 0
    total_cost = 0
    
    print("\nCompleted Orders Analysis (Last 30 days):")
    
    # Group orders by vehicle type
    vehicle_orders = {}
    for order in recent_completed:
        vehicle_type = order[10]
        if vehicle_type not in vehicle_orders:
            vehicle_orders[vehicle_type] = []
        vehicle_orders[vehicle_type].append(order)
    
    # Display analysis by vehicle type
    for vehicle_type, orders in vehicle_orders.items():
        print(f"\n{vehicle_type}:")
        vehicle_fuel = 0
        vehicle_cost = 0
        
        for order in orders:
            route = order[17]
            if route in route_distances and vehicle_type in fuel_rates:
                distance = route_distances[route]
                consumption_rate = fuel_rates[vehicle_type]
                
                # Calculate fuel used for this trip
                fuel_used = (distance * consumption_rate) / 100  # L
                cost = fuel_used * current_fuel_price
                
                vehicle_fuel += fuel_used
                vehicle_cost += cost
                total_fuel += fuel_used
                total_cost += cost
                
                print(f"\nOrder {order[0]}:")
                print(f"Route: {route} ({distance}km)")
                print(f"Fuel Used: {fuel_used:.2f}L")
                print(f"Cost: RM{cost:.2f}")
                print(f"Completion Date: {order[13]}")
                
                # Log fuel consumption only if not already logged
                if order[0] not in logged_orders:
                    log_fuel_consumption(order[0], vehicle_type, distance, fuel_used, cost)
        
        print(f"\nTotal for {vehicle_type}:")
        print(f"Orders: {len(orders)}")
        print(f"Fuel Used: {vehicle_fuel:.2f}L")
        print(f"Cost: RM{vehicle_cost:.2f}")
        print("-" * 50)
    
    print("\nOverall Summary:")
    print(f"Total New Orders Analyzed: {len(recent_completed)}")
    print(f"Total Fuel Used: {total_fuel:.2f}L")
    print(f"Total Cost: RM{total_cost:.2f}")
    print(f"Average Fuel per Order: {(total_fuel/len(recent_completed)):.2f}L")
    print(f"Average Cost per Order: RM{(total_cost/len(recent_completed)):.2f}")
    
    print_divider()
    input("Press Enter to continue...")

def log_fuel_consumption(order_id, vehicle_type, distance, fuel_used, cost):
    """Log fuel consumption details to file"""
    fuel_logs = load_data(FUEL_LOG_FILE)
    
    log_entry = [
        order_id,
        vehicle_type,
        str(distance),
        f"{fuel_used:.2f}",
        f"{cost:.2f}",
        datetime.datetime.now().strftime("%Y-%m-%d")
    ]
    
    fuel_logs.append(log_entry)
    save_data(FUEL_LOG_FILE, fuel_logs,
             "OrderID,VehicleType,Distance,FuelUsed,Cost,Date\n")

def view_fuel_consumption_history():
    print_header("Fuel Consumption History")
    
    fuel_logs = load_data(FUEL_LOG_FILE)
    if not fuel_logs:
        print_info("No fuel consumption history found!")
        return
    
    # Sort logs by date (newest first)
    fuel_logs.sort(key=lambda x: x[5], reverse=True)
    
    # Calculate totals
    total_distance = sum(float(log[2]) for log in fuel_logs)
    total_fuel = sum(float(log[3]) for log in fuel_logs)
    total_cost = sum(float(log[4]) for log in fuel_logs)
    
    print("\nRecent Consumption Records:")
    for log in fuel_logs[:10]:  # Show last 10 records
        print(f"\nOrder: {log[0]}")
        print(f"Vehicle: {log[1]}")
        print(f"Distance: {log[2]}km")
        print(f"Fuel Used: {log[3]}L")
        print(f"Cost: RM{log[4]}")
        print(f"Date: {log[5]}")
        print("-" * 50)
    
    print("\nOverall Statistics:")
    print(f"Total Distance Covered: {total_distance:.2f}km")
    print(f"Total Fuel Used: {total_fuel:.2f}L")
    print(f"Total Cost: RM{total_cost:.2f}")
    print(f"Average Consumption: {(total_fuel/total_distance*100):.2f}L/100km")
    
    print_divider()
    input("Press Enter to continue...")

def update_fuel_rates():
    print_header("Update Fuel Rates")
    
    fuel_rates = load_fuel_rates()
    
    print("\nCurrent Fuel Rates (L/100km):")
    for vehicle, rate in fuel_rates.items():
        print(f"{vehicle}: {rate:.1f}")
    
    print("\nSelect vehicle type to update:")
    vehicle_types = list(fuel_rates.keys())
    for i, v_type in enumerate(vehicle_types, 1):
        print(f"{i}. {v_type}")
    
    try:
        choice = int(input("\nEnter choice (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(vehicle_types):
            vehicle_type = vehicle_types[choice - 1]
            new_rate = float(input(f"Enter new rate for {vehicle_type} (L/100km): "))
            if new_rate <= 0:
                print_error("Rate must be greater than 0!")
                return
            
            fuel_rates[vehicle_type] = new_rate
            save_fuel_rates(fuel_rates)
            print_success("Fuel rate updated successfully!")
        else:
            print_error("Invalid choice!")
    except ValueError:
        print_error("Invalid input! Please enter a number.")

def view_route_analysis():
    print_header("Route Analysis")
    
    route_distances = load_route_distances()
    fuel_rates = load_fuel_rates()
    current_fuel_price = 2.05  # RM per liter
    
    print("\nRoute Analysis:")
    for route, distance in route_distances.items():
        print(f"\n{route} ({distance}km):")
        print("Estimated Consumption by Vehicle Type:")
        for vehicle, rate in fuel_rates.items():
            fuel_needed = (distance * rate) / 100
            cost = fuel_needed * current_fuel_price
            print(f"{vehicle}:")
            print(f"  Fuel Needed: {fuel_needed:.2f}L")
            print(f"  Estimated Cost: RM{cost:.2f}")
    
    print_divider()
    input("Press Enter to continue...")

def vehicle_management_and_maintenance():
    while True:
        print_header("Fleet Management")
        options = [
            "View Vehicle Status",
            "Schedule Maintenance",
            "View Maintenance History",
            "Update Vehicle Status",
            "Back"
        ]
        print_menu("Fleet Management Options", options)
        
        try:
            choice = int(input("\nEnter choice (1-5): "))
            if choice == 1:
                view_vehicle_status()
            elif choice == 2:
                schedule_maintenance()
            elif choice == 3:
                view_maintenance_history()
            elif choice == 4:
                update_vehicle_status()
            elif choice == 5:
                break
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input!")

def view_vehicle_status():
    print_header("Vehicle Status")
    
    # Load vehicles and ongoing orders
    vehicles = load_data(VEHICLE_FILE)
    ongoing_orders = load_data(ONGOING_ORDER_FILE)
    maintenance = load_data(MAINTENANCE_FILE)
    
    # Group vehicles by type
    vehicle_types = {"Specialized Carrier": [], "Van": [], "Truck": []}
    
    for vehicle in vehicles:
        v_type = vehicle[1]  # Assuming format: [VehicleID, Type, Status, LastMaintenance]
        if v_type in vehicle_types:
            vehicle_types[v_type].append(vehicle)
    
    # Display status for each vehicle type
    for v_type, v_list in vehicle_types.items():
        total = len(v_list)
        in_use = sum(1 for v in v_list if v[2].lower() == 'in use')
        maintenance = sum(1 for v in v_list if v[2].lower() == 'maintenance')
        available = total - in_use - maintenance
        
        print(f"\n{v_type}:")
        print(f"Total: {total} | Available: {available} | In Use: {in_use} | Maintenance: {maintenance}")
    
    print_divider()
    input("Press Enter to continue...")

def schedule_maintenance():
    print_header("Schedule Maintenance")
    
    # Load vehicles
    vehicles = load_data(VEHICLE_FILE)
    
    # Show available vehicles
    print("\nAvailable Vehicles:")
    available_vehicles = [v for v in vehicles if v[2].lower() != 'maintenance']
    
    for i, vehicle in enumerate(available_vehicles, 1):
        print(f"{i}. Vehicle ID: {vehicle[0]}")
        print(f"   Type: {vehicle[1]}")
        print(f"   Status: {vehicle[2]}")
        print(f"   Last Maintenance: {vehicle[3]}")
        print("-" * 50)
    
    try:
        choice = int(input("\nSelect vehicle for maintenance (0 to cancel): "))
        if choice == 0:
            return
        if not (1 <= choice <= len(available_vehicles)):
            print_error("Invalid selection!")
            return
        
        selected_vehicle = available_vehicles[choice - 1]
        maintenance_date = input("Enter maintenance date (YYYY-MM-DD): ")
        
        # Validate date
        is_valid, formatted_date, error = validate_date(maintenance_date, allow_future=True)
        if not is_valid:
            print_error(error)
            return
        
        # Create maintenance record
        maintenance = load_data(MAINTENANCE_FILE)
        maintenance_record = [
            selected_vehicle[0],    # VehicleID
            formatted_date,         # Scheduled Date
            "Scheduled",           # Status
            "Routine maintenance"  # Description
        ]
        maintenance.append(maintenance_record)
        
        # Update vehicle status
        for i, vehicle in enumerate(vehicles):
            if vehicle[0] == selected_vehicle[0]:
                vehicle[2] = "Maintenance"
                vehicles[i] = vehicle
                break
        
        # Save updates
        save_data(MAINTENANCE_FILE, maintenance,
                 "VehicleID,Date,Status,Description\n")
        save_data(VEHICLE_FILE, vehicles,
                 "VehicleID,Type,Status,LastMaintenance\n")
        
        print_success("Maintenance scheduled successfully!")
        
    except ValueError:
        print_error("Invalid input!")

def view_maintenance_history():
    print_header("Maintenance History")
    
    maintenance = load_data(MAINTENANCE_FILE)
    vehicles = load_data(VEHICLE_FILE)
    
    if not maintenance:
        print_info("No maintenance history found!")
        return
    
    # Group maintenance records by vehicle
    for vehicle in vehicles:
        vehicle_maintenance = [m for m in maintenance if m[0] == vehicle[0]]
        if vehicle_maintenance:
            print(f"\nVehicle ID: {vehicle[0]} ({vehicle[1]})")
            for record in vehicle_maintenance:
                print(f"Date: {record[1]}")
                print(f"Status: {record[2]}")
                print(f"Description: {record[3]}")
                print("-" * 50)
    
    print_divider()
    input("Press Enter to continue...")

def update_vehicle_status():
    print_header("Update Vehicle Status")
    
    # Load vehicles
    vehicles = load_data(VEHICLE_FILE)
    
    # Show all vehicles
    for i, vehicle in enumerate(vehicles, 1):
        print(f"\n{i}. Vehicle Details:")
        print(f"   ID: {vehicle[0]}")
        print(f"   Type: {vehicle[1]}")
        print(f"   Current Status: {vehicle[2]}")
        print("-" * 50)
    
    try:
        choice = int(input("\nSelect vehicle to update (0 to cancel): "))
        if choice == 0:
            return
        if not (1 <= choice <= len(vehicles)):
            print_error("Invalid selection!")
            return
        
        print("\nAvailable Statuses:")
        print("1. Available")
        print("2. In Use")
        print("3. Maintenance")
        
        status_choice = input("\nSelect new status (1-3): ")
        new_status = {
            '1': 'Available',
            '2': 'In Use',
            '3': 'Maintenance'
        }.get(status_choice)
        
        if not new_status:
            print_error("Invalid status choice!")
            return
        
        # Update vehicle status
        vehicles[choice - 1][2] = new_status
        
        # Save updates
        save_data(VEHICLE_FILE, vehicles,
                 "VehicleID,Type,Status,LastMaintenance\n")
        
        print_success("Vehicle status updated successfully!")
        
    except ValueError:
        print_error("Invalid input!")

def generate_reports():
    while True:
        print_header("Generate Reports")
        options = [
            "Daily Orders Report",
            "Revenue Report",
            "Driver Performance Report",
            "Customer Feedback Report",
            "Back"
        ]
        print_menu("Report Options", options)
        
        try:
            choice = int(input("\nEnter choice (1-5): "))
            if choice == 1:
                generate_daily_orders_report()
            elif choice == 2:
                generate_revenue_report()
            elif choice == 3:
                generate_driver_performance_report()
            elif choice == 4:
                generate_customer_feedback_report()
            elif choice == 5:
                break
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input!")

def generate_daily_orders_report():
    print_header("Daily Orders Report")
    
    while True:
        report_date = input("\n│ Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not report_date:
            report_date = datetime.datetime.now().strftime("%Y-%m-%d")
            break
        
        is_valid, formatted_date, error = validate_date(report_date)
        if is_valid:
            report_date = formatted_date
            break
        print_error(error)
    
    # Get all orders
    ongoing = load_data(ONGOING_ORDER_FILE)
    completed = load_data(COMPLETED_ORDER_FILE)
    cancelled = load_data(CANCELLED_ORDER_FILE)
    
    # Filter orders for the specified date
    today_ongoing = [order for order in ongoing if order[13] == report_date]
    today_completed = [order for order in completed if order[13] == report_date]
    today_cancelled = [order for order in cancelled if order[13] == report_date]
    
    width = 50
    print("\n┌" + "─" * (width-2) + "┐")
    print(f"│ Report for {report_date:<{width-13}}│")
    print("├" + "─" * (width-2) + "┤")
    print(f"│ New Orders: {len(today_ongoing):<{width-15}}│")
    print(f"│ Completed Orders: {len(today_completed):<{width-21}}│")
    print(f"│ Cancelled Orders: {len(today_cancelled):<{width-20}}│")
    print(f"│ Total Orders: {len(today_ongoing) + len(today_completed) + len(today_cancelled):<{width-16}}│")
    print("└" + "─" * (width-2) + "┘")
    
    input("\n│ Press Enter to continue...")

def generate_revenue_report():
    print_header("Revenue Report")
    
    # Get date range
    while True:
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        is_valid, formatted_date, error = validate_date(start_date)
        if is_valid:
            start_date = formatted_date
            break
        print_error(error)
    
    while True:
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        is_valid, formatted_date, error = validate_date(end_date)
        if is_valid:
            end_date_obj = datetime.datetime.strptime(formatted_date, "%Y-%m-%d")
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            if end_date_obj < start_date_obj:
                print_error("End date must be after start date!")
                continue
            end_date = formatted_date
            break
        print_error(error)
    
    # Get completed orders within date range
    completed = load_data(COMPLETED_ORDER_FILE)
    filtered_orders = [
        order for order in completed 
        if start_date <= order[13] <= end_date
    ]
    
    # Calculate total revenue
    total_revenue = sum(float(order[15]) for order in filtered_orders)
    
    # Calculate revenue by vehicle type
    revenue_by_vehicle = {}
    for order in filtered_orders:
        vehicle_type = order[10]
        price = float(order[15])
        revenue_by_vehicle[vehicle_type] = revenue_by_vehicle.get(vehicle_type, 0) + price
    
    print(f"\nRevenue Report ({start_date} to {end_date})")
    print(f"Total Revenue: RM{total_revenue:.2f}")
    print("\nRevenue by Vehicle Type:")
    for vehicle, revenue in revenue_by_vehicle.items():
        print(f"{vehicle}: RM{revenue:.2f}")
    
    print_divider()
    input("Press Enter to continue...")

def generate_driver_performance_report():
    print_header("Driver Performance Report")
    
    # Load driver data
    drivers = load_data(DRIVER_FILE)
    
    # Get date range
    while True:
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        is_valid, formatted_date, error = validate_date(start_date)
        if is_valid:
            start_date = formatted_date
            break
        print_error(error)
    
    while True:
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        is_valid, formatted_date, error = validate_date(end_date)
        if is_valid:
            end_date_obj = datetime.datetime.strptime(formatted_date, "%Y-%m-%d")
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            if end_date_obj < start_date_obj:
                print_error("End date must be after start date!")
                continue
            end_date = formatted_date
            break
        print_error(error)
    
    # Get completed orders within date range
    completed = load_data(COMPLETED_ORDER_FILE)
    filtered_orders = [
        order for order in completed 
        if start_date <= order[13] <= end_date
    ]
    
    # Calculate statistics per driver
    driver_stats = {}
    for order in filtered_orders:
        if len(order) >= 17:  # Check if order has driver information
            driver_id = order[16]
            if driver_id not in driver_stats:
                driver_stats[driver_id] = {"completed": 0, "revenue": 0}
            driver_stats[driver_id]["completed"] += 1
            driver_stats[driver_id]["revenue"] += float(order[15])
    
    # Print report
    for driver_id, stats in driver_stats.items():
        # Get driver name
        driver_name = next((driver[3] for driver in drivers if driver[0] == driver_id), "Unknown")
        
        print(f"\nDriver: {driver_name} ({driver_id})")
        print(f"Completed Orders: {stats['completed']}")
        print(f"Total Revenue Generated: RM{stats['revenue']:.2f}")
        print(f"Average Revenue per Order: RM{(stats['revenue']/stats['completed']):.2f}")
        print_divider()
    
    input("Press Enter to continue...")

def generate_customer_feedback_report():
    print_header("Customer Feedback Report")
    
    reviews = load_data(REVIEWS_FILE)
    if not reviews:
        print_info("No reviews found!")
        return
    
    # Calculate average rating
    total_rating = sum(int(review[3]) for review in reviews)
    avg_rating = total_rating / len(reviews)
    
    print("\nOverall Statistics:")
    print(f"Total Reviews: {len(reviews)}")
    print(f"Average Rating: {avg_rating:.1f} (*{'*' * int(avg_rating)})")
    
    # Group reviews by rating
    reviews_by_rating = {}
    for i in range(5, 0, -1):
        reviews_by_rating[i] = [review for review in reviews if int(review[3]) == i]
    
    print("\nReviews by Rating:")
    for rating, rating_reviews in reviews_by_rating.items():
        if rating_reviews:
            print(f"\nRating {rating} {'*' * rating} ({len(rating_reviews)} reviews):")
            for review in rating_reviews[:3]:  # Show only 3 most recent reviews per rating
                print(f"\nOrder: {review[0]}")
                print(f"Item: {review[1]}")
                print(f"Review: {review[2]}")
                print(f"Date: {review[5]}")
                print("-" * 50)
    
    print_divider()
    input("Press Enter to continue...")

def view_user_orders(username):
    print_header("My Orders")
    
    # Load user data
    users = load_data(USER_FILE)
    
    # Get user's ID
    user_id = next((user[0] for user in users if user[1] == username), None)
    
    if not user_id:
        print_error("User not found!")
        return
    
    # Load orders
    orders = load_data(ONGOING_ORDER_FILE)
    
    # Debug: Print all orders to verify data
    print("Debug: All Orders Loaded")
    for order in orders:
        print(order)
    
    # Filter orders for this user
    user_orders = [
        order for order in orders 
        if len(order) >= 17 and order[14] == user_id and order[12] in ['Pending', 'Assigned', 'Ongoing', 'Cancelled', 'Completed']
    ]
    
    # Debug: Print filtered orders
    print("Debug: Filtered User Orders")
    for order in user_orders:
        print(order)
    
    if not user_orders:
        print_info("No orders found!")
        return
    
    # Display user orders
    for order in user_orders:
        print("\nOrder Details:")
        print(f"Order ID: {order[0]}")
        print(f"From: {order[4]} To: {order[3]}")
        print(f"Item: {order[1]} (Quantity: {order[2]})")
        print(f"Vehicle Type: {order[10]}")
        print(f"Status: {order[12]}")
        # Check if the route index exists
        if len(order) > 17:
            print(f"Route: {order[17]}")
        else:
            print("Route: Not specified")
        print("-" * 50)
    
    input("Press Enter to continue...")

# Add this function to fetch user data by ID
def get_user_data_by_id(user_id):
    """Fetch user data based on user ID."""
    users = load_data(USER_FILE)
    for user in users:
        if user[0].strip() == user_id.strip():
            return user
    print_error("User not found!")
    return None

# Add these functions for fuel management
def load_fuel_rates():
    """Load fuel rates from file or create with defaults if not exists"""
    try:
        rates = load_data(FUEL_RATES_FILE)
        if not rates:
            raise FileNotFoundError
        return {rate[0]: float(rate[1]) for rate in rates}
    except FileNotFoundError:
        # Default rates in L/100km
        default_rates = {
            "Specialized Carrier": 8.5,
            "Van": 12.0,
            "Truck": 20.0
        }
        # Save default rates
        save_fuel_rates(default_rates)
        return default_rates

def save_fuel_rates(rates):
    """Save fuel rates to file"""
    data = [[vehicle, str(rate)] for vehicle, rate in rates.items()]
    save_data(FUEL_RATES_FILE, data, "VehicleType,ConsumptionRate\n")

def load_route_distances():
    """Load route distances from file or create with defaults if not exists"""
    try:
        distances = load_data(ROUTE_DISTANCES_FILE)
        if not distances:
            raise FileNotFoundError
        return {route[0]: int(route[1]) for route in distances}
    except FileNotFoundError:
        # Default distances in km
        default_distances = {
            "Route 1": 850,  # Johor-KL-Butterworth-Kedah-Perlis
            "Route 2": 780   # Johor-KL-Terengganu-Kelantan
        }
        # Save default distances
        save_route_distances(default_distances)
        return default_distances

def save_route_distances(distances):
    """Save route distances to file"""
    data = [[route, str(dist)] for route, dist in distances.items()]
    save_data(ROUTE_DISTANCES_FILE, data, "RouteName,Distance\n")

def initialize_system_files():
    """Initialize all required system files with headers if they don't exist"""
    file_headers = {
        VEHICLE_FILE: "VehicleID,Type,Status,LastMaintenance\n",
        MAINTENANCE_FILE: "VehicleID,Date,Status,Description\n",
        FUEL_LOG_FILE: "OrderID,VehicleType,Distance,FuelUsed,Cost,Date\n",
        FUEL_RATES_FILE: "VehicleType,ConsumptionRate\n",
        ROUTE_DISTANCES_FILE: "RouteName,Distance\n"
    }
    
    # Initialize each file if it doesn't exist or is empty
    for filename, header in file_headers.items():
        try:
            # Check if file exists and has content
            try:
                with open(filename, 'r') as file:
                    content = file.read().strip()
                    if not content:  # File is empty
                        raise FileNotFoundError  # Treat empty file as non-existent
            except FileNotFoundError:
                # Create or overwrite the file with header and default content
                with open(filename, 'w') as file:
                    file.write(header)
                    if filename == VEHICLE_FILE:
                        # Add 6 vehicles of each type
                        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                        
                        # Add Specialized Carriers
                        for i in range(1, 7):
                            file.write(f"SC{str(i).zfill(2)},Specialized Carrier,Available,{current_date}\n")
                        
                        # Add Vans
                        for i in range(1, 7):
                            file.write(f"VN{str(i).zfill(2)},Van,Available,{current_date}\n")
                        
                        # Add Trucks
                        for i in range(1, 7):
                            file.write(f"TR{str(i).zfill(2)},Truck,Available,{current_date}\n")
                    elif filename == FUEL_RATES_FILE:
                        # Add default fuel rates
                        file.write("Specialized Carrier,8.5\n")
                        file.write("Van,12.0\n")
                        file.write("Truck,20.0\n")
                    elif filename == ROUTE_DISTANCES_FILE:
                        # Add default routes
                        file.write("Route 1,850\n")
                        file.write("Route 2,780\n")
        except Exception as e:
            print_error(f"Error initializing {filename}: {e}")

def get_int_input(prompt, error_message="Invalid input! Please enter a number."):
    """Get an integer input from the user with validation."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print_error(error_message)

def get_str_input(prompt, error_message="Invalid input! Please enter a valid string."):
    """Get a string input from the user with validation."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print_error(error_message)

def get_enum_input(prompt, valid_options, error_message="Invalid input!"):
    """Get an enumerated input from the user with validation."""
    while True:
        value = input(prompt).strip().lower()
        if value in valid_options:
            return value
        print_error(error_message)

# Add these validation functions at the beginning of the file, after the imports

def validate_phone_number(phone):
    """Validate phone number format: XXX-XXXXXXX"""
    import re
    pattern = r'^\d{3}-\d{7}$'
    return bool(re.match(pattern, phone))

def validate_name(name):
    """Validate name format: only letters and spaces allowed"""
    return bool(name.strip() and all(c.isalpha() or c.isspace() for c in name))

def validate_username(username):
    """Validate username format: letters, numbers, minimum 5 characters"""
    return bool(username.strip() and len(username) >= 5 and username.isalnum())

def validate_password(password):
    """Validate password format: minimum 8 characters, at least one number and one letter"""
    return bool(
        len(password) >= 8 and 
        any(c.isdigit() for c in password) and 
        any(c.isalpha() for c in password)
    )

def validate_license_number(license_no):
    """Validate license number format: LXXXX (L=letter, X=number)"""
    import re
    pattern = r'^[A-Z]\d{4}$'
    return bool(re.match(pattern, license_no))

def get_validated_input(prompt, validator, error_message, format_hint=""):
    """Generic function to get validated input"""
    while True:
        value = input(f"{prompt}{' ' + format_hint if format_hint else ''}: ").strip()
        if validator(value):
            return value
        print_error(f"{error_message}")

# Update these existing input functions
def get_str_input(prompt, error_message="Invalid input! Please enter a valid string."):
    """Get a non-empty string input"""
    while True:
        value = input(prompt).strip()
        if value and all(c.isalpha() or c.isspace() for c in value):
            return value
        print_error(error_message)

def get_int_input(prompt, min_val=None, max_val=None):
    """Get integer input within optional range"""
    while True:
        try:
            value = int(input(prompt))
            if (min_val is None or value >= min_val) and (max_val is None or value <= max_val):
                return value
            range_str = f"between {min_val} and {max_val}" if min_val is not None and max_val is not None else \
                       f"greater than {min_val}" if min_val is not None else \
                       f"less than {max_val}"
            print_error(f"Please enter a number {range_str}.")
        except ValueError:
            print_error("Invalid input! Please enter a number.")

def get_float_input(prompt, min_val=None, max_val=None):
    """Get float input within optional range"""
    while True:
        try:
            value = float(input(prompt))
            if (min_val is None or value >= min_val) and (max_val is None or value <= max_val):
                return value
            range_str = f"between {min_val} and {max_val}" if min_val is not None and max_val is not None else \
                       f"greater than {min_val}" if min_val is not None else \
                       f"less than {max_val}"
            print_error(f"Please enter a number {range_str}.")
        except ValueError:
            print_error("Invalid input! Please enter a number.")

main_menu()
