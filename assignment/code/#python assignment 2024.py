# Initial seed (set to any starting integer)
initial_seed = 1234

def main():
    seed = initial_seed  # Use a local seed variable
    while True:
        print("Select an option:")
        print("1. Orders")
        print("2. Ratings and Reviews")
        print("3. Exit")

        user_choice = int(input("Enter choice: "))

        if user_choice == 1:
            seed = order_management(seed)
        elif user_choice == 2:
            ratings_and_reviews()
        elif user_choice == 3:
            print("Exiting the system. BYE!")
            break
        else:
            print("Invalid choice. Please try again.")

def order_management(seed):
    while True:
        print("\nOrder Management - Select an option:")
        print("1. New Order")
        print("2. Cancel Order")
        print("3. Order Received")
        print("4. Reorder an Order")
        print("5. View Ongoing Orders")
        print("6. View Cancelled Orders")
        print("7. View Completed Orders")
        print("8. Back to Main Menu")

        choice = int(input("Enter choice: "))

        if choice == 1:
            seed = new_order(seed)
        elif choice == 2:
            input_cancel_order()
        elif choice == 3:
            input_received_order()
        elif choice == 4:
            seed = reorder_order(seed)
        elif choice == 5:
            view_ongoing_orders('ongoingorder.txt')
        elif choice == 6:
            view_cancelled_orders('cancelledorder.txt')
        elif choice == 7:
            view_completed_orders('completedorder.txt')
        elif choice == 8:
            break
        else:
            print("Invalid choice. Please try again.")
    return seed

def new_order(seed):
    item_name = input("Enter Item Name: ")
    volume_per_item = float(input("Volume per Item (cubic meters): "))
    weight_per_item = float(input("Weight per Item (kilograms): "))
    quantity = int(input("Quantity: "))
    ship_from = input("Shipping From Address: ")
    ship_to = input("Shipping To Address: ")
    sender_name = input("Sender Name: ")
    sender_phone = input("Sender Phone: ")
    recipient_name = input("Recipient Name: ")
    recipient_phone = input("Recipient Phone: ")
    purchase_date = input("Enter Purchase Date (YYYY-MM-DD): ")

    total_volume = volume_per_item * quantity
    total_weight = weight_per_item * quantity

    recommended_vehicle = choose_vehicle(total_volume, total_weight)
    print("Recommended Vehicle:", recommended_vehicle)

    payment_option = int(input("Choose a payment method:\n1. Credit/Debit Card\n2. UPI\n3. Mobile Wallet\n4. Cash On Delivery\n"))

    order_id, seed = generate_order_id(seed)
    print("Order successfully placed! Your Order ID:", order_id)

    save_to_ongoing_orders(order_id, item_name, quantity, ship_to, ship_from, sender_name, sender_phone, recipient_name, recipient_phone, recommended_vehicle, payment_option, "Ongoing", purchase_date)
    return seed

def choose_vehicle(total_volume, total_weight):
    if total_volume <= 0.027 and total_weight <= 10:
        return "Motorcycle"
    elif total_volume <= 0.125 and total_weight <= 40:
        return "Car"
    elif total_volume <= 2.04 and total_weight <= 500:
        return "Van"
    else:
        return "Lorry"

def view_ongoing_orders(file_path):
    try:
        with open(file_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("Error: The file was not found!")

def view_cancelled_orders(file_path):
    try:
        with open(file_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("Error: The file was not found!")

def view_completed_orders(file_path):
    try:
        with open(file_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("Error: The file was not found!")

def save_to_ongoing_orders(order_id, item_name, quantity, ship_to, ship_from, sender_name, sender_phone, recipient_name, recipient_phone, vehicle, payment_option, status, purchase_date):
    with open("ongoingorder.txt", 'a') as file:
        if file.tell() == 0:
            header = "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,RecipientName,RecipientPhone,Vehicle,PaymentOption,Status,PurchaseDate\n"
            file.write(header)
        
        entry = f"{order_id},{item_name},{quantity},{ship_to},{ship_from},{sender_name},{sender_phone},{recipient_name},{recipient_phone},{vehicle},{payment_option},{status},{purchase_date}\n"
        file.write(entry)

def input_cancel_order():
    order_id = input("Please enter the order ID you wish to cancel: ")
    cancel_date = input("Enter Cancellation Date (YYYY-MM-DD): ")
    cancel_order(order_id, cancel_date)

def cancel_order(order_id, cancel_date):
    with open("cancelledorder.txt", 'a') as file:
        if file.tell() == 0:
            header = "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,RecipientName,RecipientPhone,Vehicle,PaymentOption,Status,PurchaseDate,CancellationDate,ReviewStatus\n"
            file.write(header)
    
    try:
        with open("ongoingorder.txt", 'r') as file:
            ongoing_orders = file.readlines()

        with open("cancelledorder.txt", 'a') as cancelled_file:
            for order in ongoing_orders:
                if order_id in order:
                    # Change status to 'Cancelled' and review status to 'Tobereview' before saving
                    order_details = order.strip().split(',')
                    order_details[11] = "Cancelled"  # Status in column 12
                    order_details.append(cancel_date)  # Append cancellation date
                    order_details.append("Tobereview")  # Review status
                    cancelled_file.write(','.join(order_details) + '\n')
                    ongoing_orders.remove(order)
                    print("Order", order_id, "has been cancelled. Refund will be processed soon.")
                    break

        with open("ongoingorder.txt", 'w') as file:
            file.writelines(ongoing_orders)
    except FileNotFoundError:
        print("Error: The file was not found!")

def input_received_order():
    order_id = input("Please enter the order ID that you've collected: ")
    received_date = input("Enter Received Date (YYYY-MM-DD): ")
    order_received(order_id, received_date)

def order_received(order_id, received_date):
    with open("completedorder.txt", 'a') as file:
        if file.tell() == 0:
            header = "OrderID,ItemName,Quantity,ShipTo,ShipFrom,SenderName,SenderPhone,RecipientName,RecipientPhone,Vehicle,PaymentOption,Status,PurchaseDate,ReceivedDate,ReviewStatus\n"
            file.write(header)
    
    try:
        with open("ongoingorder.txt", 'r') as file:
            ongoing_orders = file.readlines()

        with open("completedorder.txt", 'a') as completed_file:
            for order in ongoing_orders:
                if order_id in order:
                    # Change status to 'Completed' and review status to 'Tobereview' before saving
                    order_details = order.strip().split(',')
                    order_details[11] = "Completed"  # Status in column 12
                    order_details.append(received_date)  # Append received date
                    order_details.append("Tobereview")  # Review status
                    completed_file.write(','.join(order_details) + '\n')
                    ongoing_orders.remove(order)
                    print("Order", order_id, "has been completed. Thanks for choosing us.")
                    break

        with open("ongoingorder.txt", 'w') as file:
            file.writelines(ongoing_orders)
    except FileNotFoundError:
        print("Error: The file was not found!")

def reorder_order(seed):
    order_id = input("Please enter the Order ID you wish to reorder: ")
    found_order = False
    order_details = None

    # Check cancelled orders first
    with open("cancelledorder.txt", 'r') as file:
        for line in file:
            if order_id in line:
                order_details = line.strip().split(',')
                found_order = True
                break

    # Check completed orders if not found in cancelled orders
    if not found_order:
        with open("completedorder.txt", 'r') as file:
            for line in file:
                if order_id in line:
                    order_details = line.strip().split(',')
                    found_order = True
                    break

    if found_order and order_details:
        item_name = order_details[1]
        quantity = int(order_details[2])
        ship_to = order_details[3]
        ship_from = order_details[4]
        sender_name = order_details[5]
        sender_phone = order_details[6]
        recipient_name = order_details[7]
        recipient_phone = order_details[8]
        vehicle = order_details[9]
        payment_option = int(order_details[10])

        # Prompt for a new purchase date
        purchase_date = input("Enter new Purchase Date for reorder (YYYY-MM-DD): ")

        new_order_id, seed = generate_order_id(seed)
        print("Reorder successfully placed! New Order ID:", new_order_id)
        save_to_ongoing_orders(new_order_id, item_name, quantity, ship_to, ship_from, sender_name, sender_phone, recipient_name, recipient_phone, vehicle, payment_option, "Ongoing", purchase_date)

    else:
        print("Order ID not found in cancelled or completed orders.")
    return seed

def generate_order_id(seed):
    # Read all existing order IDs from the file
    existing_ids = set()
    try:
        with open("order_ids.txt", 'r') as file:
            existing_ids = set(line.strip() for line in file)
    except FileNotFoundError:
        pass  # File doesn't exist yet, which is fine for the first run 

    while True:
        # Generate a new order ID
        seed = (seed * 48271) % 9999
        order_id = str(seed).zfill(4)  # Ensures ID is always 4 digits

        # Check if this order ID is already in use
        if order_id not in existing_ids:
            # Store the new order ID in the file for future reference
            with open("order_ids.txt", 'a') as file:
                file.write(order_id + '\n')
            return order_id, seed
        # If order_id exists, loop will retry with the next generated ID

def update_review_status(file_path, order_id):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        with open(file_path, 'w') as file:
            for line in lines:
                if order_id in line:
                    # Update review status to "Reviewed"
                    order_details = line.strip().split(',')
                    order_details[-1] = "Reviewed"
                    file.write(','.join(order_details) + '\n')
                else:
                    file.write(line)
    except FileNotFoundError:
        print("Error: The file was not found!")

def save_review(order_id, review_text, rating, stars):
    with open("reviewed.txt", 'a') as file:
        if file.tell() == 0:
            header = "OrderID,Review,Rating,Stars\n"
            file.write(header)

        entry = f"{order_id},{review_text},{rating},{stars}\n"
        file.write(entry)

def ratings_and_reviews():
    review_choice = int(input("Ratings & Reviews:\n1. To Be Reviewed\n2. Reviewed\nEnter choice: "))

    if review_choice == 1:
        input_to_be_reviewed()
    elif review_choice == 2:
        view_reviewed('reviewed.txt')
    else:
        print("Invalid choice.")

def input_to_be_reviewed():
    order_id = input("Enter the Order ID you want to review: ")
    found_order = False
    order_details = None
    file_path = None

    # Check cancelled orders first
    with open("cancelledorder.txt", 'r') as file:
        for line in file:
            if order_id in line:
                order_details = line.strip().split(',')
                if order_details[-1] == "Tobereview":  # Check if review status is "Tobereview"
                    found_order = True
                    file_path = "cancelledorder.txt"
                break

    # Check completed orders if not found in cancelled orders
    if not found_order:
        with open("completedorder.txt", 'r') as file:
            for line in file:
                if order_id in line:
                    order_details = line.strip().split(',')
                    if order_details[-1] == "Tobereview":  # Check if review status is "Tobereview"
                        found_order = True
                        file_path = "completedorder.txt"
                    break

    if found_order and order_details:
        # Collect user review and rating
        review_text = input("Enter your review: ")
        rating = float(input("Enter rating (1-5): "))
        stars = "*" * int(rating)

        # Write review to reviewed.txt
        save_review(order_id, review_text, rating, stars)

        # Update order status to "Reviewed" in the original file
        update_review_status(file_path, order_id)
        print("Thank you for your review!")
        print("Thank you for your review!")
    else:
        print("Order not found or has already been reviewed.")

def view_reviewed(file_path):
    try:
        with open(file_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("Error: The file was not found!")


main()
