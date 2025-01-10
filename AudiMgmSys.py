import datetime
import threading

# Sample data structures for two auditoriums with 10 seats each
auditorium_1 = {
    'A1': 'available', 'A2': 'available', 'A3': 'available',
    'B1': 'available', 'B2': 'available', 'B3': 'available',
    'C1': 'available', 'C2': 'available', 'C3': 'available',
    'D1': 'available'
}

auditorium_2 = {
    'A1': 'available', 'A2': 'available', 'A3': 'available',
    'B1': 'available', 'B2': 'available', 'B3': 'available',
    'C1': 'available', 'C2': 'available', 'C3': 'available',
    'D1': 'available'
}

# Dictionary to store booking details
booking_details = {
    'auditorium_1': {},
    'auditorium_2': {}
}

# Locks for concurrency control
lock_1 = threading.Lock()
lock_2 = threading.Lock()

# Function to display auditorium layout as a box
def display_auditorium(auditorium):
    rows = {}
    for seat, status in auditorium.items():
        row = seat[0]
        if row not in rows:
            rows[row] = []
        rows[row].append(f"{seat}: {status[0].upper()}")  # Use first letter of status (A for available, B for booked)
    
    for row, seats in rows.items():
        print(f"Row {row}: {' '.join(seats)}")
    print()

# Function to display booked seats
def display_booked_seats(auditorium):
    booked_seats = [seat for seat, status in auditorium.items() if status == 'booked']
    if booked_seats:
        print("Booked Seats: " + ", ".join(booked_seats))
    else:
        print("No seats are currently booked.")

# Function to select date and time
def select_date_time():
    date_str = input("Enter date (YYYY-MM-DD): ")
    time_str = input("Enter time (HH:MM): ")
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        time = datetime.datetime.strptime(time_str, "%H:%M").time()
        return date.date(), time
    except ValueError:
        print("Invalid date or time format.")
        return None, None

# Function to book seats with concurrency handling
def book_seats(auditorium, lock, booking_key):
    with lock:
        display_auditorium(auditorium)
        seats = input("Enter seats to book (comma-separated): ").split(',')
        all_available = all(auditorium.get(seat.strip()) == 'available' for seat in seats)
        
        if all_available:
            name = input("Enter your name: ")
            phone = input("Enter your phone number: ")
            email = input("Enter your email: ")
            for seat in seats:
                seat = seat.strip()
                auditorium[seat] = 'booked'
                booking_details[booking_key][seat] = {
                    'name': name,
                    'phone': phone,
                    'email': email,
                    'date': datetime.datetime.now().date(),
                    'time': datetime.datetime.now().time()
                }
            print(f"Booking successful for {name}!")
        else:
            print("Some seats are already booked. Please choose a different time or auditorium.")
        display_auditorium(auditorium)

# Function to see booking details
def see_booking_details(booking_key):
    if booking_details[booking_key]:
        for seat, details in booking_details[booking_key].items():
            print(f"Seat {seat}:")
            print(f"  Name: {details['name']}")
            print(f"  Phone: {details['phone']}")
            print(f"  Email: {details['email']}")
            print(f"  Date: {details['date']}")
            print(f"  Time: {details['time']}")
    else:
        print("No bookings found.")

# Main function to run the booking system
def main():
    while True:
        print("\n1. Display Auditorium\n2. Select Date and Time\n3. Book Seats\n4. Show Booked Seats\n5. See Booking Details\n6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            aud_choice = input("Select Auditorium (1 or 2): ")
            if aud_choice == '1':
                display_auditorium(auditorium_1)
            elif aud_choice == '2':
                display_auditorium(auditorium_2)
            else:
                print("Invalid auditorium choice.")
        elif choice == '2':
            date, time = select_date_time()
            if date and time:
                print(f"Selected Date: {date}, Time: {time}")
        elif choice == '3':
            aud_choice = input("Select Auditorium (1 or 2): ")
            if aud_choice == '1':
                book_seats(auditorium_1, lock_1, 'auditorium_1')
            elif aud_choice == '2':
                book_seats(auditorium_2, lock_2, 'auditorium_2')
            else:
                print("Invalid auditorium choice.")
        elif choice == '4':
            aud_choice = input("Select Auditorium (1 or 2): ")
            if aud_choice == '1':
                display_booked_seats(auditorium_1)
            elif aud_choice == '2':
                display_booked_seats(auditorium_2)
            else:
                print("Invalid auditorium choice.")
        elif choice == '5':
            aud_choice = input("Select Auditorium (1 or 2): ")
            if aud_choice == '1':
                see_booking_details('auditorium_1')
            elif aud_choice == '2':
                see_booking_details('auditorium_2')
            else:
                print("Invalid auditorium choice.")
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
