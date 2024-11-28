import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class ReservationSystem:
    
    def __init__(self, hotel_name="The Greensboro Hotel", numRooms=30, current_date=datetime(2024, 11, 26)):
        self.hotel_name = hotel_name
        self.date = current_date
        self.rooms = [set() for _ in range(numRooms)]
        
    def is_full(self):
        for room in self.rooms:
            if not room:
                return False
        return True
            
    def reserve_room(self, name, check_in_date, checkout_date):
        
        for i in range(len(self.rooms)):
            # TODO check for check-in, check-out date range
            if not self.rooms[i]:  # Find the first empty room
                self.rooms[i].add((name, check_in_date, checkout_date))
                return i + 1  # Return room number
        return Exception("No rooms available.") # TODO create custome NoRoomException
                
    def cancel_reservation(self, roomNumber, name, check_in_date, checkout_date):
        if (name, check_in_date, checkout_date) in self.rooms[roomNumber - 1]:
            self.rooms[roomNumber - 1].remove((name, check_in_date, checkout_date))
        else:
            raise Exception("Reservation not found.")
            
    def getRooms(self):
        return self.rooms


# GUI Implementation
class HotelReservationApp:
    def __init__(self, root, system):
        self.system = system
        self.root = root
        root.title("Greensboro Hotel Booking")
        root.geometry("450x500")
        
        # Header
        header = tk.Label(root, text="Welcome to Greensboro Hotel", font=("Arial", 14), bg="lightgray")
        header.pack(fill=tk.X)
        
        # Top Section (Input)
        self.top_section = tk.Frame(root, bg="#f0f0f0", height=200)
        self.top_section.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(self.top_section, text="Full Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = tk.Entry(self.top_section)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self.top_section, text="Check-In Date (MM/DD/YYYY):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.checkin_entry = tk.Entry(self.top_section)
        self.checkin_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(self.top_section, text="Check-Out Date (MM/DD/YYYY):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.checkout_entry = tk.Entry(self.top_section)
        self.checkout_entry.grid(row=2, column=1, padx=10, pady=5)
        
        self.check_button = tk.Button(self.top_section, text="Check Availability", command=self.check_availability)
        self.check_button.grid(row=3, column=1, pady=10)
        
        # Bottom Section (Initially Hidden)
        self.bottom_section = tk.Frame(root, bg="#d3d3d3", height=200)
        self.output_label = tk.Label(self.bottom_section, text="", font=("Arial", 12), wraplength=400)
        self.output_label.pack(pady=10)
        
        # Buttons for booking or canceling
        self.book_button = tk.Button(self.bottom_section, text="Book Reservation", command=self.book_reservation)
        self.cancel_button = tk.Button(self.bottom_section, text="Cancel", command=self.cancel_reservation)

        # Variables to store reservation info
        self.current_room = None
        self.current_name = None
        self.current_checkin = None
        self.current_checkout = None
    
    def check_availability(self):
        name = self.name_entry.get()
        checkin_date = self.checkin_entry.get()
        checkout_date = self.checkout_entry.get()
        
        if not name or not checkin_date or not checkout_date:
            messagebox.showerror("Input Error", "All fields are required!")
            return
        
        try:
            checkin_date_obj = datetime.strptime(checkin_date, "%m/%d/%Y")
            checkout_date_obj = datetime.strptime(checkout_date, "%m/%d/%Y")
        except ValueError:
            messagebox.showerror("Date Error", "Enter dates in MM/DD/YYYY format!")
            return
        
        if checkout_date_obj <= checkin_date_obj:
            messagebox.showerror("Date Error", "Check-out date must be after check-in date!")
            return
        
        try:
            room_number = self.system.reserve_room(name, checkin_date, checkout_date)
            self.current_room = room_number
            self.current_name = name
            self.current_checkin = checkin_date
            self.current_checkout = checkout_date
            
            # Update output section
            self.output_label.config(
                text=f"Room {room_number} is available!\n\nCheck-in Date: {checkin_date}\nCheck-out Date: {checkout_date}\nCustomer: {name}",
                fg="green"
            )
            self.book_button.pack(pady=5)
            self.cancel_button.pack(pady=5)
        except Exception:
            self.output_label.config(
                text="Unfortunately, there are no available rooms from check-in date to check-out date.",
                fg="red"
            )
        
        self.bottom_section.pack(fill=tk.BOTH, expand=True)

    def book_reservation(self):
        messagebox.showinfo("Success", f"Room {self.current_room} has been booked successfully!")
        self.reset_form()

    def cancel_reservation(self):
        if self.current_room:
            self.system.cancel_reservation(self.current_room, self.current_name, self.current_checkin, self.current_checkout)
        self.reset_form()
    
    def reset_form(self):
        self.name_entry.delete(0, tk.END)
        self.checkin_entry.delete(0, tk.END)
        self.checkout_entry.delete(0, tk.END)
        self.current_room = None
        self.current_name = None
        self.current_checkin = None
        self.current_checkout = None
        self.bottom_section.pack_forget()


if __name__ == "__main__":
    reservation_system = ReservationSystem(numRooms=5)
    root = tk.Tk()
    app = HotelReservationApp(root, reservation_system)
    root.mainloop()
