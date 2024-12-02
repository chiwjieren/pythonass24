# Define file names
USER_FILE = "userdetails.txt"
ONGOING_ORDER_FILE = "ongoingorder.txt"
CANCELLED_ORDER_FILE = "cancelledorder.txt"
COMPLETED_ORDER_FILE = "completedorder.txt"
ORDER_ID_FILE = "order_ids.txt"
REVIEWS_FILE = "reviews.txt"  # New file to store reviews
TO_BE_REVIEWED_FILE = "tobereview.txt"
REVIEWED_FILE = "reviewed.txt"

# Utility function to read lines from a file
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

def main():
    userID = None
    while True:
        print("\nSelect an option:")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")

        try:
            main_choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if main_choice == 1:
            sign_up()
        elif main_choice == 2:
            userID = login()
            if userID:
                welcome(userID)
            else:
                print("Invalid login credentials. Try again.")
        elif main_choice == 3:
            print("Exiting the system. BYE!")
            break
        else:
            print("Invalid choice. Please try again.")

def sign_up():
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()
    user_id = generate_user_id()

    user_data = f"U{user_id:03},{username},{password}\n"
    header = "Username,UserID,Password\n"
    write_lines_to_file(USER_FILE, [user_data], header)

    print(f"User created successfully! Your User ID: U{user_id:03}")

def login():
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()

    users = read_lines_from_file(USER_FILE)
    if not users:
        print("No users found. Please sign up first.")
        return None

    for user in users[1:]:  # Skip header
        try:
            stored_user_id, stored_username, stored_password = user.strip().split(",")
            if stored_username == username and stored_password == password:
                print(f"Login successful! Welcome {username}")
                return stored_user_id
        except ValueError:
            # Handle lines that don't have enough fields
            continue
    return None

def generate_user_id():
    users = read_lines_from_file(USER_FILE)
    if not users:
        return 1  # First user
    return len(users)  # Since header is first line

def welcome(userID):
    while True:
        print("\nSelect an option:")
        print("1. Orders")
        print("2. Ratings and Reviews")
        print("3. Log Out")

        try:
            user_choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if user_choice == 1:
            order_management(userID)
        elif user_choice == 2:
            ratings_and_reviews(userID)
        elif user_choice == 3:
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def order_management(userID):
    while True:
        print("\nOrder Management - Select an option:")
        print("1. New Order")
        print("2. Cancel Order")
        print("3. Order Received")
        print("4. Reorder an Order")
        print("5. View Orders")
        print("6. Back to Main Menu")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

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
            print("Invalid choice. Please try again.")

def new_order(userID):
    locations = [
        "Johor", "Kuala Lumpur", "Butterworth", "Kedah", "Perlis", 
        "Terengganu", "Kelantan"
    ]
    # Collect order details
    item_name = input("Enter Item Name: ").strip()
    try:
        quantity = int(input("Quantity: "))
    except ValueError:
        print("Invalid input for quantity. Must be a number.")
        return
    ship_from = print("Shipping From: ")
    for i, location in enumerate(locations, 1):
        print(f"{i}. {location}")
    
    try:
        ship_from_choice = int(input("Enter your choice (1-7): "))
        if ship_from_choice < 1 or ship_from_choice > len(locations):
            print("Invalid choice. Please select a valid location.")
            return
        ship_from = locations[ship_from_choice - 1]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    ship_to = print("Shipping To: ")
    for i, location in enumerate(locations, 1):
        print(f"{i}. {location}")
    
    try:
        ship_to_choice = int(input("Enter your choice (1-7): "))
        if ship_to_choice < 1 or ship_to_choice > len(locations):
            print("Invalid choice. Please select a valid location.")
            return
        ship_to = locations[ship_to_choice - 1]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    sender_name = input("Sender Name: ").strip()
    sender_phone = input("Sender Phone: ").strip()
    recipient_name = input("Recipient Name: ").strip()
    recipient_phone = input("Recipient Phone: ").strip()
    purchase_date = input("Enter Purchase Date (YYYY-MM-DD): ").strip()

    # Let user select shipment size
    print("Choose Shipment Size:")
    print("1. Bulk Order (Fits in a car trunk)")
    print("2. Small Parcel (Fits in a van)")
    print("3. Special Cargo (Requires a truck)")
    shipment_size_choice = input("Enter your choice (1-3): ").strip()
    shipment_size = ""
    if shipment_size_choice == "1":
        shipment_size = "BulkOrder"
    elif shipment_size_choice == "2":
        shipment_size = "SmallParcel"
    elif shipment_size_choice == "3":
        shipment_size = "SpecialCargo"
    else:
        print("Invalid choice for shipment size.")
        return

    # Let user select vehicle type
    print("Choose Vehicle Type:")
    print("1. Specialized Carrier")
    print("2. Van")
    print("3. Truck")
    vehicle_choice_input = input("Enter your choice (1-3): ").strip()
    vehicle_choice = ""
    if vehicle_choice_input == "1":
        vehicle_choice = "Specialized Carrier"
    elif vehicle_choice_input == "2":
        vehicle_choice = "Van"
    elif vehicle_choice_input == "3":
        vehicle_choice = "Truck"
    else:
        print("Invalid choice for vehicle type.")
        return

    # Select payment option
    print("Choose Payment Method:")
    print("1. Credit/Debit Card")
    print("2. UPI")
    print("3. Mobile Wallet")
    print("4. Cash On Delivery")
    payment_choice = input("Enter your choice (1-4): ").strip()
    payment_option = ""
    if payment_choice == "1":
        payment_option = "Credit/Debit Card"
    elif payment_choice == "2":
        payment_option = "UPI"
    elif payment_choice == "3":
        payment_option = "Mobile Wallet"
    elif payment_choice == "4":
        payment_option = "Cash On Delivery"
    else:
        print("Invalid choice for payment method.")
        return

    # Generate order ID
    order_id = generate_order_id()
    print("Order successfully placed! Your Order ID:", order_id)

    # Save to ongoing orders
    order_data = f"{order_id},{item_name},{quantity},{ship_to},{ship_from},{sender_name},{sender_phone},{recipient_name},{recipient_phone},{shipment_size},{vehicle_choice},{payment_option},Pending,{purchase_date},{userID}\n"
    header = "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,RecipientName,RecipientPhone,Shipment_size,Vehicle_choice,PaymentOption,Status,PurchaseDate,UserID\n"
    write_lines_to_file(ONGOING_ORDER_FILE, [order_data], header)

def generate_order_id():
    orders = read_lines_from_file(ORDER_ID_FILE)
    existing_ids = set(line.strip() for line in orders)
    order_id = 1
    while True:
        new_order_id = f"ORD{order_id:03}"
        if new_order_id not in existing_ids:
            break
        order_id += 1
    # Save the new order ID
    write_lines_to_file(ORDER_ID_FILE, [f"{new_order_id}\n"])
    return new_order_id, order_id +1

def view_orders(userID):
    for file_name, status in [(ONGOING_ORDER_FILE, 'Ongoing'), (CANCELLED_ORDER_FILE, 'Cancelled'), (COMPLETED_ORDER_FILE, 'Completed')]:
        print(f"\n{status} Orders for User {userID}:")
        orders = read_lines_from_file(file_name)
        if not orders or len(orders) <=1:
            print(f"No {status.lower()} orders.")
            continue
        for order in orders[1:]:
            order_details = order.strip().split(',')
            if order_details[-1] == userID:
                print(order)

def cancel_order(userID):
    ongoing_orders = read_lines_from_file(ONGOING_ORDER_FILE)
    if not ongoing_orders or len(ongoing_orders) <= 1:
        print("No ongoing orders to mark as cancelled.")
        return

    user_orders = [order.strip().split(',') for order in ongoing_orders[1:] if order.strip().split(',')[-1] == userID]
    if not user_orders:
        print("No ongoing orders to mark as cancelled.")
        return

    print("\nOngoing Orders to Cancel:")
    for i, order in enumerate(user_orders, start=1):
        print(f"{i}. Order ID: {order[0]}, Item: {order[1]}, Quantity: {order[2]}, Status: {order[12]}")

    try:
        choice = int(input("Enter the order number to mark as cancelled or 0 to cancel: "))
    except ValueError:
        print("Invalid input.")
        return

    if choice == 0:
        return
    elif 1 <= choice <= len(user_orders):
        order_to_cancel = user_orders[choice - 1]
        # Strip whitespace and compare status case-insensitively
        if order_to_cancel[13].strip().lower() == 'pending':
            order_to_cancel[13] = 'Cancelled'
            cancelled_order_data = ','.join(order_to_cancel) + '\n'
            header = "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,RecipientName,RecipientPhone,Shipment_size,Vehicle_choice,PaymentOption,Status,PurchaseDate,UserID\n"
            write_lines_to_file(CANCELLED_ORDER_FILE, [cancelled_order_data], header)

            # Add order to tobereview file
            to_be_reviewed_data = ','.join(order_to_cancel) + '\n'
            write_lines_to_file(TO_BE_REVIEWED_FILE, [to_be_reviewed_data], header)
            
            # Update ongoing orders
            updated_orders = [
                order for order in ongoing_orders if order.strip().split(',')[0] != order_to_cancel[0]
            ]
            with open(ONGOING_ORDER_FILE, 'w') as file:
                file.writelines(updated_orders)

            print(f"Order {order_to_cancel[0]} has been marked as cancelled.")
        else:
            print(f"Order {order_to_cancel[0]} cannot be cancelled as it is not in 'Pending' status. Current status: {order_to_cancel[12]}")
    else:
        print("Invalid choice.")

def order_received(userID):
    ongoing_orders = read_lines_from_file(ONGOING_ORDER_FILE)
    if not ongoing_orders or len(ongoing_orders) <= 1:
        print("No ongoing orders to mark as completed.")
        return

    user_orders = [order.strip().split(',') for order in ongoing_orders[1:] if order.strip().split(',')[-1] == userID]
    if not user_orders:
        print("No ongoing orders to mark as completed.")
        return

    print("\nOngoing Orders to Mark as Completed:")
    for i, order in enumerate(user_orders, start=1):
        print(f"{i}. Order ID: {order[0]}, Item: {order[1]}, Quantity: {order[2]}")

    try:
        choice = int(input("Enter the order number to mark as completed or 0 to cancel: "))
    except ValueError:
        print("Invalid input.")
        return

    if choice == 0:
        return
    elif 1 <= choice <= len(user_orders):
        order_to_receive = user_orders[choice - 1]
        # Change status to Completed
        order_to_receive[13] = 'Completed'
        completed_order_data = ','.join(order_to_receive) + '\n'
        header = "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,RecipientName,RecipientPhone,Shipment_size,Vehicle_choice,PaymentOption,Status,PurchaseDate,UserID\n"
        write_lines_to_file(COMPLETED_ORDER_FILE, [completed_order_data], header)

        # Add order to tobereview file
        to_be_reviewed_data = ','.join(order_to_receive) + '\n'
        write_lines_to_file(TO_BE_REVIEWED_FILE, [to_be_reviewed_data], header)

        # Update ongoing orders
        updated_orders = [
            order for order in ongoing_orders if order.strip().split(',')[0] != order_to_receive[0]
        ]
        with open(ONGOING_ORDER_FILE, 'w') as file:
            file.writelines(updated_orders)

        print("Order marked as completed and added to reviews queue.")
    else:
        print("Invalid choice. Please try again.")


def update_order_in_file(file_path, order_id, updated_order):
    # Read all lines from the file
    lines = read_lines_from_file(file_path)
    if not lines:
        return

    # Replace the line corresponding to the order_id
    updated_lines = []
    for line in lines:
        order = line.strip().split(',')
        if order[0] == order_id:  # Match based on order ID
            updated_lines.append(updated_order)  # Replace with updated order
        else:
            updated_lines.append(line)  # Keep other orders unchanged

    # Rewrite the file with the updated lines
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)


def reorder_order(userID):
    completed_orders = read_lines_from_file(COMPLETED_ORDER_FILE)
    if not completed_orders or len(completed_orders) <=1:
        print("No completed orders to reorder.")
        return

    user_completed_orders = [order.strip().split(',') for order in completed_orders[1:] if order.strip().split(',')[-1] == userID]
    if not user_completed_orders:
        print("No completed orders to reorder.")
        return

    print("\nCompleted Orders:")
    for i, order in enumerate(user_completed_orders, start=1):
        print(f"{i}. Order ID: {order[0]}, Item: {order[1]}, Quantity: {order[2]}")

    try:
        choice = int(input("Enter the order number to reorder or 0 to cancel: "))
    except ValueError:
        print("Invalid input.")
        return

    if choice == 0:
        return
    elif 1 <= choice <= len(user_completed_orders):
        order_to_reorder = user_completed_orders[choice -1]
        # Proceed with the reorder by creating a new order with same item and quantity
        item_name = order_to_reorder[1]
        quantity = int(order_to_reorder[2])
        print("Proceeding to reorder...")
        # Collect remaining details for the new order
        ship_from = input("Shipping From Address: ").strip()
        ship_to = input("Shipping To Address: ").strip()
        sender_name = input("Sender Name: ").strip()
        sender_phone = input("Sender Phone: ").strip()
        recipient_name = input("Recipient Name: ").strip()
        recipient_phone = input("Recipient Phone: ").strip()
        purchase_date = input("Enter Purchase Date (YYYY-MM-DD): ").strip()

        # Let user select shipment size
        print("Choose Shipment Size:")
        print("1. Small (Fits in a car trunk)")
        print("2. Medium (Fits in a van)")
        print("3. Large (Requires a truck)")
        shipment_size_choice = input("Enter your choice (1-3): ").strip()
        shipment_size = ""
        if shipment_size_choice == "1":
            shipment_size = "Small"
        elif shipment_size_choice == "2":
            shipment_size = "Medium"
        elif shipment_size_choice == "3":
            shipment_size = "Large"
        else:
            print("Invalid choice for shipment size.")
            return

        # Let user select vehicle type
        print("Choose Vehicle Type:")
        print("1. Specialized Carrier")
        print("2. Van")
        print("3. Truck")
        vehicle_choice_input = input("Enter your choice (1-3): ").strip()
        vehicle_choice = ""
        if vehicle_choice_input == "1":
            vehicle_choice = "Specialized Carrier"
        elif vehicle_choice_input == "2":
            vehicle_choice = "Van"
        elif vehicle_choice_input == "3":
            vehicle_choice = "Truck"
        else:
            print("Invalid choice for vehicle type.")
            return

        # Select payment option
        print("Choose Payment Method:")
        print("1. Credit/Debit Card")
        print("2. UPI")
        print("3. Mobile Wallet")
        print("4. Cash On Delivery")
        payment_choice = input("Enter your choice (1-4): ").strip()
        payment_option = ""
        if payment_choice == "1":
            payment_option = "Credit/Debit Card"
        elif payment_choice == "2":
            payment_option = "UPI"
        elif payment_choice == "3":
            payment_option = "Mobile Wallet"
        elif payment_choice == "4":
            payment_option = "Cash On Delivery"
        else:
            print("Invalid choice for payment method.")
            return

        # Generate order ID
        order_id = generate_order_id()
        print("Order successfully placed! Your Order ID:", order_id)

        # Save to ongoing orders
        order_data = f"{order_id},{item_name},{quantity},{ship_to},{ship_from},{sender_name},{sender_phone},{recipient_name},{recipient_phone},{shipment_size},{vehicle_choice},{payment_option},Ongoing,{purchase_date},{userID}\n"
        header = "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,RecipientName,RecipientPhone,Shipment_size,Vehicle_choice,PaymentOption,Status,PurchaseDate,UserID\n"
        write_lines_to_file(ONGOING_ORDER_FILE, [order_data], header)
        print("Order successfully reordered!")

    else:
        print("Invalid choice.")

def view_orders(userID):
    for file_name, status in [(ONGOING_ORDER_FILE, 'Ongoing'), (CANCELLED_ORDER_FILE, 'Cancelled'), (COMPLETED_ORDER_FILE, 'Completed')]:
        print(f"\n{status} Orders for User {userID}:")
        orders = read_lines_from_file(file_name)
        if not orders or len(orders) <= 1:
            print(f"No {status.lower()} orders.")
            continue
        
        # Add header to the order details
        if status == 'Ongoing':
            header = "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,RecipientName,RecipientPhone,Shipment_size,Vehicle_choice,PaymentOption,Status,PurchaseDate,UserID\n"
        elif status == 'Cancelled':
            header = "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,RecipientName,RecipientPhone,Shipment_size,Vehicle_choice,PaymentOption,Status,PurchaseDate,UserID\n"
        elif status == 'Completed':
            header = "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,RecipientName,RecipientPhone,Shipment_size,Vehicle_choice,PaymentOption,Status,PurchaseDate,UserID\n"
        
        print(header.strip())  # Print header

        for order in orders[1:]:  # Skip header in the file
            order_details = order.strip().split(',')
            if order_details[-1] == userID:
                print(order)


def remove_order_from_file(file_path, order_id):
    orders = read_lines_from_file(file_path)
    if not orders:
        return
    with open(file_path, 'w') as file:
        for order in orders:
            try:
                current_order_id = order.strip().split(',')[0]
                if current_order_id != order_id:
                    file.write(order)
            except IndexError:
                continue  # Skip invalid lines

def ratings_and_reviews(userID):
    while True:
        print("\nRatings and Reviews - Select an option:")
        print("1. Leave a Review")
        print("2. View Reviews")
        print("3. Back to Main Menu")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            leave_review(userID)
        elif choice == 2:
            view_reviews(userID)
        elif choice == 3:
            break
        else:
            print("Invalid choice. Please try again.")

def leave_review(userID):
    to_be_reviewed = read_lines_from_file(TO_BE_REVIEWED_FILE)
    if not to_be_reviewed or len(to_be_reviewed) <= 1:
        print("No orders available for review.")
        return

    user_orders = [
        order.strip().split(',')
        for order in to_be_reviewed[1:]
        if order.strip().split(',')[-1] == userID
    ]
    if not user_orders:
        print("No orders available for review.")
        return

    print("\nOrders to Review:")
    for i, order in enumerate(user_orders, start=1):
        print(f"{i}. Order ID: {order[0]}, Item: {order[1]}, Status: {order[12]}")

    try:
        choice = int(input("Select an order to review (0 to cancel): "))
    except ValueError:
        print("Invalid input.")
        return

    if choice == 0:
        return
    elif 1 <= choice <= len(user_orders):
        order_to_review = user_orders[choice - 1]
        review = input("Enter your review: ").strip()
        rating = input("Enter your rating (1-5): ").strip()

        # Save review to reviewed file
        review_data = f"{order_to_review[0]},{order_to_review[1]},{review},{rating},{userID}\n"
        header = "OrderID,ItemName,Review,Rating,UserID\n"
        write_lines_to_file(REVIEWED_FILE, [review_data], header)

        # Remove order from tobereview file
        updated_orders = [
            order for order in to_be_reviewed if order.strip().split(',')[0] != order_to_review[0]
        ]
        with open(TO_BE_REVIEWED_FILE, 'w') as file:
            file.writelines(updated_orders)

        print("Review submitted successfully!")
    else:
        print("Invalid choice. Please try again.")

def view_reviews(userID):
    reviewed = read_lines_from_file(REVIEWED_FILE)
    if not reviewed or len(reviewed) <= 1:
        print("No reviews found.")
        return

    user_reviews = [
        review.strip().split(',')
        for review in reviewed[1:]
        if review.strip().split(',')[-1] == userID
    ]
    if not user_reviews:
        print("You have not submitted any reviews.")
        return

    print("\nYour Reviews:")
    for review in user_reviews:
        print(f"Order ID: {review[0]}, Item: {review[1]}, Review: {review[2]}, Rating: {review[3]}")


main()
