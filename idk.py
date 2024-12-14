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

# Pricing constants
BASE_PRICE = 50
PRICE_PER_UNIT = 10
VEHICLE_PRICES = {
    "Specialized Carrier": 100,
    "Van": 150,
    "Truck": 200
}
SHIPMENT_SIZE_PRICES = {
    "BulkOrder": 50,
    "SmallParcel": 100,
    "SpecialCargo": 150
}

# Add these constants at the top with other constants
STOPOVER_TIME = 30  # minutes
SAFETY_CHECK_TIME = 30  # minutes
TURNOVER_TIME = 60  # minutes

# Utility functions for file operations
def load_data(filename):
    try:
        with open(filename, 'r') as file:
            lines = [line.strip().split(',') for line in file if line.strip()]
            # Skip header if it exists
            if lines and (lines[0][0] == 'DriverID' or lines[0][0] == 'OrderID' or 
                         lines[0][0] == 'Username' or lines[0][0] == 'UserID'):
                return lines[1:]
            return lines
    except:
        return []

def save_data(filename, data, header=None):
    with open(filename, 'w') as file:
        if header:
            file.write(header)
        for item in data:
            file.write(','.join(item) + '\n')

def get_next_id(prefix, current_ids):
    if not current_ids:
        return f"{prefix}001"
    last_id = max(int(id[len(prefix):]) for id in current_ids)
    return f"{prefix}{str(last_id + 1).zfill(3)}"

# UI utility functions
def print_header(text):
    width = 50
    print("\n" + "=" * width)
    print(f"{text:^{width}}")
    print("=" * width)

def print_menu(title, options):
    width = 50
    print("\n╔" + "═" * (width-2) + "╗")
    print(f"║{title:^{width-2}}║")
    print("╠" + "═" * (width-2) + "╣")
    for num, option in enumerate(options, 1):
        print(f"║ {num}. {option:<{width-4}}║")
    print("╚" + "═" * (width-2) + "╝") 

# Additional UI utility functions
def print_info(text):
    print(f"\n>>> {text}")

def print_error(text):
    print(f"\n!!! {text}")

def print_success(text):
    print(f"\n✓ {text}")

def print_divider():
    print("\n" + "─" * 50)

def print_order_details(order):
    width = 60
    print("\n┌" + "─" * (width-2) + "┐")
    print(f"│ Order ID: {order[0]:<{width-13}}│")
    print(f"│ Item: {order[1]:<{width-9}}│")
    print(f"│ Quantity: {order[2]:<{width-12}}│")
    print(f"│ Status: {order[12]:<{width-11}}│")
    print("└" + "─" * (width-2) + "┘")

def calculate_order_price(quantity, vehicle_type, shipment_size):
    total_price = BASE_PRICE
    total_price += quantity * PRICE_PER_UNIT
    total_price += VEHICLE_PRICES.get(vehicle_type, 0)
    total_price += SHIPMENT_SIZE_PRICES.get(shipment_size, 0)
    return total_price

# Main menu and system selection
def main_menu():
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
        
        # Select route based on source and destination
        print("\nSelect Route:")
        print("1. Route 1: Johor → KL → Butterworth → Kedah → Perlis")
        print("2. Route 2: Johor → KL → Terengganu → Kelantan")
        
        route_choice = input("\nEnter route number (1-2): ")
        if route_choice not in ['1', '2']:
            print_error("Invalid route selection!")
            return
        
        route = "Route 1" if route_choice == '1' else "Route 2"
        
        # Update order with assigned driver, route, and change status
        for i, order in enumerate(orders):
            if order[0] == selected_order[0]:
                order.extend([selected_driver[0], route])  # Add DriverID and Route
                order[12] = 'assigned'  # Update status to 'assigned'
                orders[i] = order
                break
        
        # Update driver status
        for i, driver in enumerate(drivers):
            if driver[0] == selected_driver[0]:
                driver[7] = "assigned"  # Update status
                drivers[i] = driver
                break
        
        # Save updates
        save_data(ONGOING_ORDER_FILE, orders,
                 "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                 "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                 "Status,PurchaseDate,UserID,Price,DriverID,Route\n")
        
        save_data(DRIVER_FILE, drivers,
                 "DriverID,Username,Password,Name,Contact,Address,LicenseNo,Status\n")
        
        print_success(f"Order {selected_order[0]} assigned to Driver {selected_driver[0]} on {route}")
        
    except ValueError:
        print_error("Invalid input!")

def assign_order_to_driver():
    print_header("Assign Order to Driver")
    
    # Load data
    ongoing_orders = load_data(ONGOING_ORDER_FILE)
    drivers = load_data(DRIVER_FILE)
    
    # Filter orders that are not yet assigned
    unassigned_orders = [order for order in ongoing_orders if len(order) < 17 or not order[16]]
    
    if not unassigned_orders:
        print_info("No unassigned orders available!")
        return
    
    # Display unassigned orders
    print("\nUnassigned Orders:")
    for i, order in enumerate(unassigned_orders, 1):
        print(f"\n{i}. Order Details:")
        print(f"   Order ID: {order[0]}")
        print(f"   From: {order[4]} To: {order[3]}")
        print(f"   Item: {order[1]} (Quantity: {order[2]})")
        print(f"   Status: {order[12]}")
        print("-" * 50)
    
    try:
        order_choice = int(input("\nSelect order to assign (0 to cancel): "))
        if order_choice == 0:
            return
        if not (1 <= order_choice <= len(unassigned_orders)):
            print_error("Invalid order selection!")
            return
        
        selected_order = unassigned_orders[order_choice - 1]
        
        # Display available drivers
        print("\nAvailable Drivers:")
        for i, driver in enumerate(drivers, 1):
            print(f"{i}. {driver[3]} (ID: {driver[0]})")
        
        driver_choice = int(input("\nSelect driver to assign (0 to cancel): "))
        if driver_choice == 0:
            return
        if not (1 <= driver_choice <= len(drivers)):
            print_error("Invalid driver selection!")
            return
        
        selected_driver = drivers[driver_choice - 1]
        
        # Assign driver to order
        for i, order in enumerate(ongoing_orders):
            if order[0] == selected_order[0]:
                order[16] = selected_driver[0]  # Assign driver ID
                ongoing_orders[i] = order
                break
        
        # Save updated orders
        save_data(ONGOING_ORDER_FILE, ongoing_orders,
                 "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                 "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                 "Status,PurchaseDate,UserID,Price,DriverID,Route\n")
        
        print_success(f"Order {selected_order[0]} assigned to driver {selected_driver[3]} successfully!")
        
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
    username = input("Username: ")
    password = input("Password: ")
    name = input("Full Name: ")
    contact = input("Contact Number: ")
    address = input("Address: ")
    license_no = input("License Number: ")
    
    drivers = load_data(DRIVER_FILE)
    
    if any(driver[1] == username for driver in drivers):
        print_error("Username already exists!")
        return
    
    driver_ids = [driver[0] for driver in drivers]
    driver_id = get_next_id('D', driver_ids)
    
    new_driver = [driver_id, username, password, name, contact, address, license_no, "available"]
    drivers.append(new_driver)
    save_data(DRIVER_FILE, drivers, "DriverID,Username,Password,Name,Contact,Address,LicenseNo,Status\n")
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
            drivers[i] = driver
            save_data(DRIVER_FILE, drivers, "DriverID,Username,Password,Name,Contact,Address,LicenseNo,Status\n")
            print_success("Profile updated successfully!")
            return
    print_error("Driver not found!")

def view_driver_orders(username):
    orders = load_data(ONGOING_ORDER_FILE)
    drivers = load_data(DRIVER_FILE)
    
    # Get driver ID
    driver_id = None
    for driver in drivers:
        if driver[1] == username:
            driver_id = driver[0]
            break
    
    if not driver_id:
        print_error("Driver not found!")
        return
    
    print_header("My Assigned Orders")
    found = False
    
    for order in orders:
        if len(order) >= 17 and order[16] == driver_id:  # Check if order has DriverID field
            found = True
            print("\nOrder Details:")
            print(f"Order ID: {order[0]}")
            print(f"From: {order[4]} To: {order[3]}")
            print(f"Item: {order[1]} (Quantity: {order[2]})")
            print(f"Vehicle Type: {order[10]}")
            print(f"Route: {order[17]}")
            print(f"Status: {order[12]}")
            print("-" * 50)
    
    if not found:
        print_info("No orders assigned!")

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
        if len(order) >= 17 and order[16] == driver_id and order[12] in ['assigned', 'Pending', 'Ongoing']
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
        print(f"   Route: {order[17]}")
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
        if current_status in ['assigned', 'Pending']:
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
    print(f"• Stopover time at each hub: {STOPOVER_TIME} minutes")
    print(f"• Safety checks and refueling: {SAFETY_CHECK_TIME} minutes")
    print(f"• Turnover time at destination: {TURNOVER_TIME} minutes")
    
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
    print("├" + "─" * (width-2) + "┤")
    print(f"│ Review: {review[2]:<{width-11}}│")
    print(f"│ Rating: {'⭐' * int(review[3]):<{width-11}}│")
    print("└" + "─" * (width-2) + "┘")

# Customer functions
def customer_signup():
    print_header("Customer Registration")
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()
    
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
    print_error("Invalid credentials!")
    return None

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
    item_name = input("Enter Item Name: ").strip()
    try:
        quantity = int(input("Quantity: "))
    except ValueError:
        print_error("Invalid input for quantity. Must be a number.")
        return

    print_location_menu(locations)
    try:
        ship_from_choice = int(input("\nEnter shipping from location (1-7): "))
        if ship_from_choice < 1 or ship_from_choice > len(locations):
            print_error("Invalid choice. Please select a valid location.")
            return
        ship_from = locations[ship_from_choice - 1]
    except ValueError:
        print_error("Invalid input. Please enter a number.")
        return

    print_location_menu(locations)
    try:
        ship_to_choice = int(input("\nEnter shipping to location (1-7): "))
        if ship_to_choice < 1 or ship_to_choice > len(locations):
            print_error("Invalid choice. Please select a valid location.")
            return
        ship_to = locations[ship_to_choice - 1]
    except ValueError:
        print_error("Invalid input. Please enter a number.")
        return

    print_divider()
    sender_name = input("Sender Name: ").strip()
    sender_phone = input("Sender Phone: ").strip()
    recipient_name = input("Recipient Name: ").strip()
    recipient_phone = input("Recipient Phone: ").strip()

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
    
    # Filter orders by user ID
    user_orders = {
        'Ongoing': [order for order in ongoing if order[-2] == userID and order[12] in ['Pending', 'Ongoing']],
        'Completed': [order for order in completed if order[-2] == userID],
        'Cancelled': [order for order in cancelled if order[-2] == userID]
    }
    
    if not any(user_orders.values()):
        print_info("No orders found!")
        return
    
    # Display orders by status with tracking information
    for status, orders in user_orders.items():
        if orders:
            print(f"\n{status} Orders:")
            for order in orders:
                print("\n" + "─" * 50)
                print(f"Order ID: {order[0]}")
                print(f"Item: {order[1]} (Quantity: {order[2]})")
                print(f"From: {order[4]} To: {order[3]}")
                print(f"Status: {order[12]}")
                
                # Show tracking status based on order status
                if status == 'Ongoing':
                    if order[12] == 'Pending':
                        print("Tracking: 📦 Order confirmed, waiting for pickup")
                    elif order[12] == 'Ongoing':
                        print("Tracking: 🚚 In transit to destination")
                elif status == 'Completed':
                    print("Tracking: ✅ Order completed")
                elif status == 'Cancelled':
                    print("Tracking: ❌ Order cancelled")
                
                print(f"Order Date: {order[13]}")
                print(f"Price: RM{order[15]}")
                
                if len(order) >= 17 and order[16]:  # If driver is assigned
                    driver_name = next((d[3] for d in load_data(DRIVER_FILE) if d[0] == order[16]), "Unassigned")
                    print(f"Driver: {driver_name}")
    
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
        if order[-2] == userID and order[12] == 'Delivered'
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
    # Get both completed and cancelled orders
    completed_orders = load_data(COMPLETED_ORDER_FILE)
    cancelled_orders = load_data(CANCELLED_ORDER_FILE)
    
    all_reorderable_orders = []
    
    # Process completed orders
    if completed_orders:
        completed = [order for order in completed_orders if order[-2] == userID]
        all_reorderable_orders.extend(completed)

    # Process cancelled orders
    if cancelled_orders:
        cancelled = [order for order in cancelled_orders if order[-2] == userID]
        all_reorderable_orders.extend(cancelled)

    if not all_reorderable_orders:
        print_info("No orders available to reorder!")
        return

    print_header("Orders Available to Reorder")
    for i, order in enumerate(all_reorderable_orders, 1):
        print_order_details(order)
        print_divider()

    try:
        choice = int(input("Select order number to reorder (0 to go back): "))
        if choice == 0:
            return
        if 1 <= choice <= len(all_reorderable_orders):
            order_to_reorder = all_reorderable_orders[choice - 1]
            
            # Automatically set new date to current date
            new_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Validate that new date is after original order date
            try:
                old_date_obj = datetime.datetime.strptime(order_to_reorder[13], "%Y-%m-%d")
                new_date_obj = datetime.datetime.strptime(new_date, "%Y-%m-%d")
                
                if new_date_obj.date() <= old_date_obj.date():
                    print_error(f"Cannot reorder on the same day as the original order ({order_to_reorder[13]})!")
                    return
                    
            except ValueError:
                # If original date was invalid, continue with current date
                pass
            
            # Generate new order ID
            orders = load_data(ORDER_ID_FILE)
            order_ids = [order[0] for order in orders]
            new_order_id = get_next_id('ORD', order_ids)
            
            # Create new order with same details but new ID, date and Pending status
            new_order = order_to_reorder.copy()
            new_order[0] = new_order_id
            new_order[12] = 'Pending'
            new_order[13] = new_date
            
            # Recalculate price
            price = calculate_order_price(
                int(new_order[2]),  # quantity
                new_order[10],      # vehicle_type
                new_order[9]        # shipment_size
            )
            new_order[15] = str(price)
            
            # Show price and confirm
            print_info(f"Total Order Price: RM {price}")
            confirm = input("Confirm reorder? (y/n): ").lower()
            if confirm != 'y':
                print_info("Reorder cancelled.")
                return
            
            # Save to ongoing orders
            ongoing_orders = load_data(ONGOING_ORDER_FILE)
            ongoing_orders.append(new_order)
            save_data(ONGOING_ORDER_FILE, ongoing_orders,
                     "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                     "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                     "Status,PurchaseDate,UserID,Price\n")
            
            # Save order ID
            with open(ORDER_ID_FILE, 'a') as file:
                file.write(f"{new_order_id}\n")
            
            print_success(f"Order reordered successfully! New Order ID: {new_order_id}")
        else:
            print_error("Invalid choice!")
    except ValueError:
        print_error("Invalid input!")

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
    # Get both completed and cancelled orders that can be reviewed
    to_be_reviewed = load_data(TO_BE_REVIEWED_FILE)
    completed_orders = load_data(COMPLETED_ORDER_FILE)
    cancelled_orders = load_data(CANCELLED_ORDER_FILE)
    
    # Combine orders that can be reviewed
    reviewable_orders = []
    
    # Add orders from to_be_reviewed
    reviewable_orders.extend([order for order in to_be_reviewed if order[-2] == userID])
    
    # Add completed orders that haven't been reviewed yet
    reviews = load_data(REVIEWS_FILE)
    reviewed_order_ids = [review[0] for review in reviews]
    
    # Add completed orders that haven't been reviewed
    for order in completed_orders:
        if order[-2] == userID and order[0] not in reviewed_order_ids:
            reviewable_orders.append(order)
    
    # Add cancelled orders that haven't been reviewed
    for order in cancelled_orders:
        if order[-2] == userID and order[0] not in reviewed_order_ids:
            reviewable_orders.append(order)
    
    if not reviewable_orders:
        print_info("No orders available for review!")
        return

    print_header("Orders Available for Review")
    for i, order in enumerate(reviewable_orders, 1):
        print(f"\n{i}. Order Details:")
        print(f"   Order ID: {order[0]}")
        print(f"   Item: {order[1]}")
        print(f"   Status: {order[12]}")
        print(f"   Date: {order[13]}")
        print("-" * 50)

    try:
        choice = int(input("Select order to review (0 to go back): "))
        if choice == 0:
            return
        if 1 <= choice <= len(reviewable_orders):
            order_to_review = reviewable_orders[choice - 1]
            
            # Get review details
            print_divider()
            review = input("Enter your review: ").strip()
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
            review_data = [
                order_to_review[0],  # Order ID
                order_to_review[1],  # Item name
                review,              # Review text
                str(rating),         # Rating
                userID,              # User ID
                review_date         # Review date
            ]
            
            # Add to reviews file
            reviews = load_data(REVIEWS_FILE)
            reviews.append(review_data)
            save_data(REVIEWS_FILE, reviews, "OrderID,ItemName,Review,Rating,UserID,ReviewDate\n")
            
            # Remove from to_be_reviewed if it's there
            if order_to_review in to_be_reviewed:
                updated_to_review = [
                    order for order in to_be_reviewed 
                    if order[0] != order_to_review[0]
                ]
                save_data(TO_BE_REVIEWED_FILE, updated_to_review,
                         "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,"
                         "RecipientName,RecipientPhone,ShipmentSize,VehicleType,Payment,"
                         "Status,PurchaseDate,UserID,Price\n")
            
            print_success("Review submitted successfully!")
        else:
            print_error("Invalid choice!")
    except ValueError:
        print_error("Invalid input!")

def view_reviews(userID):
    print_header(f"Reviews for User {userID}")
    reviews = load_data(REVIEWS_FILE)
    user_reviews = [review for review in reviews if review[-1] == userID]
    
    if not user_reviews:
        print_info("No reviews found!")
        return

    for review in user_reviews:
        print_review_details(review)
        print_divider()

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
    print_header("Fuel & Vehicle Consumption")
    
    # Sample fuel consumption data (in future, this could be loaded from a file)
    fuel_data = {
        "Specialized Carrier": {"consumption": 8, "price": 2.05},  # L/100km
        "Van": {"consumption": 12, "price": 2.05},
        "Truck": {"consumption": 20, "price": 2.05}
    }
    
    # Calculate consumption for active routes
    orders = load_data(ONGOING_ORDER_FILE)
    active_orders = [order for order in orders if order[12].lower() in ['ongoing', 'at hub']]
    
    route_distances = {
        "Route 1": 850,  # km (Johor-KL-Butterworth-Kedah-Perlis)
        "Route 2": 780   # km (Johor-KL-Terengganu-Kelantan)
    }
    
    total_fuel_cost = 0
    print("\nActive Routes Fuel Consumption:")
    
    for order in active_orders:
        if len(order) >= 18:  # Check if order has route information
            vehicle_type = order[10]
            route = order[17]
            
            if vehicle_type in fuel_data and route in route_distances:
                distance = route_distances[route]
                consumption = fuel_data[vehicle_type]["consumption"]
                price = fuel_data[vehicle_type]["price"]
                
                fuel_needed = (distance * consumption) / 100  # L
                cost = fuel_needed * price
                total_fuel_cost += cost
                
                print(f"\nOrder {order[0]}:")
                print(f"Vehicle: {vehicle_type}")
                print(f"Route: {route} ({distance}km)")
                print(f"Estimated Fuel Needed: {fuel_needed:.2f}L")
                print(f"Estimated Cost: RM{cost:.2f}")
    
    print_divider()
    print(f"Total Estimated Fuel Cost: RM{total_fuel_cost:.2f}")
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
    print("\nSpecialized Carriers:")
    print("Total: 5 | Available: 3 | In Use: 1 | Maintenance: 1")
    print("\nVans:")
    print("Total: 8 | Available: 5 | In Use: 2 | Maintenance: 1")
    print("\nTrucks:")
    print("Total: 6 | Available: 4 | In Use: 1 | Maintenance: 1")
    print_divider()
    input("Press Enter to continue...")

def schedule_maintenance():
    print_header("Schedule Maintenance")
    print_info("This feature will be implemented in future updates.")
    input("Press Enter to continue...")

def view_maintenance_history():
    print_header("Maintenance History")
    print_info("This feature will be implemented in future updates.")
    input("Press Enter to continue...")

def update_vehicle_status():
    print_header("Update Vehicle Status")
    print_info("This feature will be implemented in future updates.")
    input("Press Enter to continue...")

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
        report_date = input("Enter date to report (YYYY-MM-DD) or press Enter for today: ").strip()
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
    
    # Filter orders for today
    today_ongoing = [order for order in ongoing if order[13] == report_date]
    today_completed = [order for order in completed if order[13] == report_date]
    today_cancelled = [order for order in cancelled if order[13] == report_date]
    
    print(f"\nReport for {report_date}")
    print_divider()
    print(f"New Orders: {len(today_ongoing)}")
    print(f"Completed Orders: {len(today_completed)}")
    print(f"Cancelled Orders: {len(today_cancelled)}")
    
    if today_ongoing:
        print("\nNew Orders Details:")
        for order in today_ongoing:
            print_order_details(order)
    
    print_divider()
    input("Press Enter to continue...")

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
    
    # Get all reviews
    reviews = load_data(REVIEWS_FILE)
    
    if not reviews:
        print_info("No reviews found!")
        return
    
    # Calculate average rating
    total_rating = sum(float(review[3]) for review in reviews)
    avg_rating = total_rating / len(reviews)
    
    # Count ratings
    rating_counts = {str(i): 0 for i in range(1, 6)}
    for review in reviews:
        rating_counts[review[3]] += 1
    
    print(f"\nTotal Reviews: {len(reviews)}")
    print(f"Average Rating: {avg_rating:.1f} ⭐")
    
    print("\nRating Distribution:")
    for rating, count in rating_counts.items():
        percentage = (count / len(reviews)) * 100
        print(f"{rating} ⭐: {count} ({percentage:.1f}%)")
    
    print("\nRecent Reviews:")
    for review in reviews[-5:]:  # Show last 5 reviews
        print_review_details(review)
    
    print_divider()
    input("Press Enter to continue...")

main_menu()