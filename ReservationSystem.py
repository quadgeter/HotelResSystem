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
            
    def reserve_room(self, name, check_in_date, checkout_date):
        for i in range(len(self.rooms)):
            
            # TODO naive logic
            # FIXME check if room is 
            if not self.rooms[i]:
                self.rooms[i].add((name, check_in_date, checkout_date))
                return i + 1
            
        return Exception
                
                
    def cancel_reservation(self, roomNumber, name, check_in_date, checkout_date):
        if (name, check_in_date, checkout_date) in self.rooms[roomNumber - 1]:
            self.rooms[roomNumber - 1].remove((name, check_in_date, checkout_date))
        else:
            raise Exception
            
        
    def findReservation(self, roomNumber, name):
        pass
    
    def getRooms(self):
        return self.rooms
    
    
if __name__ == "__main__":
    system = ReservationSystem(numRooms=5)
    print(system.getRooms())
    
    system.reserve_room("John", "11/20/2024", "11/24/2024")
    print(system.getRooms())
    
    system.cancel_reservation(1, "John", "11/20/2024", "11/24/2024")
    print(system.getRooms())
            
        
    