#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from datetime import datetime
import pandas as pd

class TravelPlannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Planner")

        # Variables to store user inputs
        self.name_var = tk.StringVar()
        self.mobile_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.destination_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.theme_var = tk.StringVar()
        self.accommodation_var = tk.StringVar()
        self.transport_var = tk.StringVar()
        self.transport_expense_var = tk.StringVar()
        self.total_acc_var = tk.StringVar()
        self.distance_var = tk.StringVar()
        self.total_expense_var = tk.StringVar()

        # Personal details frame
        personal_frame = tk.LabelFrame(root, text="Personal Details")
        personal_frame.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(personal_frame, text="Name:").grid(row=0, column=0, sticky="w")
        tk.Entry(personal_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=3)

        tk.Label(personal_frame, text="Mobile Number:").grid(row=1, column=0, sticky="w")
        tk.Entry(personal_frame, textvariable=self.mobile_var).grid(row=1, column=1, padx=5, pady=3)

        tk.Label(personal_frame, text="Address:").grid(row=2, column=0, sticky="w")
        tk.Entry(personal_frame, textvariable=self.address_var).grid(row=2, column=1, padx=5, pady=3)

        tk.Label(personal_frame, text="Destination:").grid(row=3, column=0, sticky="w")
        tk.Entry(personal_frame, textvariable=self.destination_var).grid(row=3, column=1, padx=5, pady=3)

        tk.Button(personal_frame, text="Next", command=self.validate_personal_details).grid(row=4, columnspan=2, pady=10)

    def validate_personal_details(self):
        name = self.name_var.get().strip()
        mobile_number = self.mobile_var.get().strip()
        address = self.address_var.get().strip()
        destination = self.destination_var.get().strip()

        if not all([name, mobile_number, address, destination]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Proceed to next step
        self.show_spots_at_destination()

    def show_spots_at_destination(self):
        destination = self.destination_var.get()

        # Fetch spots data
        spots_dict = create_places_dict(destination)
        spots = spots_dict.get(destination, [])

        if not spots:
            messagebox.showinfo("Spots", f"No spots found for {destination}.")
        else:
            messagebox.showinfo("Spots", f"Spots at {destination}:\n\n" + "\n".join(spots))

        # Calculate distance
        distance = self.calculate_distance()

        # Update distance variable
        self.distance_var.set(f"Distance between your address and {destination}: {distance:.2f} kilometers")

        # Proceed to next step
        self.plan_travel_details()

    def calculate_distance(self):
        geolocator = Nominatim(user_agent="geo_distance_calculator")
        address = self.address_var.get()
        destination = self.destination_var.get()
        location1 = geolocator.geocode(address)
        location2 = geolocator.geocode(destination)

        if location1 is None or location2 is None:
            return 0

        distance = geodesic((location1.latitude, location1.longitude), (location2.latitude, location2.longitude)).kilometers
        return distance

    def plan_travel_details(self):
        travel_frame = tk.Toplevel(self.root)
        travel_frame.title("Travel Details")

        tk.Label(travel_frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
        tk.Entry(travel_frame, textvariable=self.start_date_var).grid(row=0, column=1, padx=5, pady=3)

        tk.Label(travel_frame, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="w")
        tk.Entry(travel_frame, textvariable=self.end_date_var).grid(row=1, column=1, padx=5, pady=3)

        tk.Label(travel_frame, text="Theme:").grid(row=2, column=0, sticky="w")
        tk.OptionMenu(travel_frame, self.theme_var, "Adventure", "Relaxation", "Cultural").grid(row=2, column=1, padx=5, pady=3)

        tk.Label(travel_frame, textvariable=self.distance_var).grid(row=3, columnspan=2, padx=5, pady=3)

        tk.Button(travel_frame, text="Next", command=self.validate_travel_details).grid(row=4, columnspan=2, pady=10)

    def validate_travel_details(self):
        start_date_str = self.start_date_var.get().strip()
        end_date_str = self.end_date_var.get().strip()
        selected_theme = self.theme_var.get()

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return

        if end_date < start_date:
            messagebox.showerror("Error", "End date must be after or equal to start date.")
            return

        # Proceed to next step
        self.plan_accommodation()

    def plan_accommodation(self):
        accommodation_frame = tk.Toplevel(self.root)
        accommodation_frame.title("Accommodation")

        tk.Label(accommodation_frame, text="Accommodation Type:").grid(row=0, column=0, sticky="w")
        tk.OptionMenu(accommodation_frame, self.accommodation_var, "Hotel", "Homeliving", "Other").grid(row=0, column=1, padx=5, pady=3)

        tk.Label(accommodation_frame, text="Number of Days:").grid(row=1, column=0, sticky="w")
        tk.Entry(accommodation_frame, textvariable=self.total_acc_var).grid(row=1, column=1, padx=5, pady=3)

        tk.Label(accommodation_frame, text="Accommodation Budget per Day:").grid(row=2, column=0, sticky="w")
        tk.Entry(accommodation_frame, textvariable=self.total_acc_var).grid(row=2, column=1, padx=5, pady=3)

        tk.Button(accommodation_frame, text="Next", command=self.plan_transport_details).grid(row=3, columnspan=2, pady=10)

    def plan_transport_details(self):
        transport_frame = tk.Toplevel(self.root)
        transport_frame.title("Transport Details")

        tk.Label(transport_frame, text="Transport Mode:").grid(row=0, column=0, sticky="w")
        tk.OptionMenu(transport_frame, self.transport_var, "Car", "Train", "Bus", "Other", command=self.calculate_car_expenses).grid(row=0, column=1, padx=5, pady=3)

        tk.Button(transport_frame, text="Next", command=self.calculate_total_expenses).grid(row=1, columnspan=2, pady=10)

    def calculate_car_expenses(self, mode):
        if mode == "Car":
            # Assuming expenses calculation for car mode here
            # You can add your calculation logic here
            self.transport_expense_var.set("1000")

    def calculate_total_expenses(self):
        accommodation_expense = float(self.total_acc_var.get()) if self.accommodation_var.get() in ["Hotel", "Homeliving"] else 0
        transport_expense = float(self.transport_expense_var.get())
        total_expense = accommodation_expense + transport_expense

        # Update total expense variable
        self.total_expense_var.set(f"Total Expenses: Rs. {total_expense:.2f}")

        # Display all details and total expenses
        self.display_trip_details()

    def display_trip_details(self):
        details = (
            f"Name: {self.name_var.get()}\n"
            f"Mobile Number: {self.mobile_var.get()}\n"
            f"Address: {self.address_var.get()}\n"
            f"Destination: {self.destination_var.get()}\n"
            f"Start Date: {self.start_date_var.get()}\n"
            f"End Date: {self.end_date_var.get()}\n"
            f"Total Distance: {self.distance_var.get()}\n"
            f"Theme: {self.theme_var.get()}\n"
            f"Accommodation Type: {self.accommodation_var.get()}\n"
            f"Transport Mode: {self.transport_var.get()}\n"
            f"Transport Expense: {self.transport_expense_var.get()}\n"
            f"Total Expenses: Rs. {self.total_expense_var.get()}"
        )

        messagebox.showinfo("Trip Details", details)

        # Ask for confirmation
        self.ask_confirmation()

    def ask_confirmation(self):
        confirmation = messagebox.askyesno("Confirmation", "Would you like to confirm the trip?")
        if confirmation:
            messagebox.showinfo("Confirmation", "Your trip has been confirmed. Enjoy your journey!")
        else:
            messagebox.showinfo("Confirmation", "Trip canceled. Have a great day!")
        self.root.destroy()

def create_places_dict(destination):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel("C:/Users/SAYALI/Downloads/seven.xlsx")

        # Filter the DataFrame to get only the rows where the destination matches user input
        destination_data = df[df['destination'] == destination]

        # Create a dictionary to store the data
        places_dict = {}

        # Iterate through the rows of filtered data and populate the dictionary
        for index, row in destination_data.iterrows():
            city = row['destination']
            spot = row['spots']
            if city not in places_dict:
                places_dict[city] = []
            places_dict[city].append(spot)

        return places_dict
    except FileNotFoundError:
        print("Error: File not found. Please make sure the file exists.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    root = tk.Tk()
    app = TravelPlannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# In[ ]:


from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from datetime import datetime
import pandas as pd

def get_valid_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            return date
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

def create_places_dict(destination):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel("C:/Users/SAYALI/Downloads/seven.xlsx")

        # Filter the DataFrame to get only the rows where the destination matches user input
        destination_data = df[df['destination'] == destination]

        # Create a dictionary to store the data
        places_dict = {}

        # Iterate through the rows of filtered data and populate the dictionary
        for index, row in destination_data.iterrows():
            city = row['destination']
            spot = row['spots']
            if city not in places_dict:
                places_dict[city] = []
            places_dict[city].append(spot)

        return places_dict
    except FileNotFoundError:
        print("Error: File not found. Please make sure the file exists.")
    except Exception as e:
        print(f"Error: {e}")

class TravelPlanner:
    def __init__(self):
        pass  

def main():
    print("-------TRAVEL WITH NO REGRETS-------")
    print("YOU ARE WARMLY WELCOMED TO UNIQUE TRAVEL PLANNER PLATFORM !!!\n")

    # Get user details
    name = input("Enter your name: ")
    mobile_number = input("Enter your mobile number: ")
    address = input("Enter your address: ")
    destination = input("Enter your desired destination: ")

    # Create a dictionary of spots for the destination
    spots_dict = create_places_dict(destination)
    if spots_dict:
        print("Spots at the destination:")
        for spot in spots_dict.get(destination, []):
            print("- ", spot)
    else:
        print("No spots found for the destination.")

    # Get geographical coordinates and calculate distance
    geolocator = Nominatim(user_agent="geo_distance_calculator")
    location1 = geolocator.geocode(address)
    location2 = geolocator.geocode(destination)

    # Check if geocoding was successful
    if location1 is None or location2 is None:
        print("Error: One or both of the provided addresses could not be geocoded.")
        return

    distance = geodesic((location1.latitude, location1.longitude), (location2.latitude, location2.longitude)).kilometers
    print(f"Distance between {address} and {destination}: {distance:.2f} kilometers")
    
    
    planner = TravelPlanner()

    while True:
        start_date = get_valid_date("Enter the start date (YYYY-MM-DD): ")
        end_date = get_valid_date("Enter the end date (YYYY-MM-DD): ")
        if end_date < start_date:
            print("End date must be after or equal to start date.")
        else:
            break

    print("\nChoose a Theme:")
    print("1. Adventure")
    print("2. Relaxation")
    print("3. Cultural")

    theme = int(input("Enter the Theme number: "))
    themes = {
        1: "Adventure",
        2: "Relaxation",
        3: "Cultural"
    }

    selected_theme = themes.get(theme, "Desirable")

    print(f"\nBE READY FOR AN {selected_theme.upper()} TRIP!")
    print(f"It's time to plan your {selected_theme.lower()} adventure...\n")

    # Plan accommodation
    print("\nIT'S TIME TO PLAN ACCOMMODATION !!!")
    print("Enter the type of Accommodation you will prefer:")
    print("1. Hotel")
    print("2. Homeliving")

    acc_choice = int(input("Your Choice is: "))
    accommodation_type = "Hotel" if acc_choice == 1 else "Homeliving" if acc_choice == 2 else "Other"

    if acc_choice in [1, 2]:
        print(f"\nYou have selected {accommodation_type}.")
        days = int(input("How many days will you like to take accommodation for: "))
        acc_price = float(input("Enter your accommodation budget per day: "))
        total_acc = days * acc_price
        print(f"TOTAL ACCOMMODATION COST WILL BE {total_acc:.2f}")

    # Plan travel details
    print("\nIT'S TIME TO PLAN TRAVEL DETAILS:")
    print("Select the Mode of Transport:")
    print("1. Car")
    print("2. Train")
    print("3. Bus")

    transport_choice = int(input("Your Choice is [1/2/3]: "))
    transport_modes = {1: "Car", 2: "Train", 3: "Bus"}
    transport_mode = transport_modes.get(transport_choice, "Other")
    
    
    if transport_choice == 1:
        print("\nMode of Transport is Car!!")
        distance = float(input("Enter distance from source to destination you entered (in km): "))
        fuel_consumption = distance * 0.5
        transport_expense = fuel_consumption * 104
        print(f"Fuel consumption will be {fuel_consumption:.2f} litres")
        print(f"Transport Expenditure will be Rs. {transport_expense:.2f}")
    elif transport_choice in [2, 3]:
        mode_name = "Train" if transport_choice == 2 else "Bus"
        print(f"\nMode of Transport is {mode_name}!!")
        transport_expense = float(input(f"Enter the price of {mode_name} tickets (in Rs): "))
    else:
        print("\nMode of Transport is Other!!")
        transport_expense = float(input("Enter the price of ticket: "))

    
    
      
    print("\nTRAVEL PLANNER")
    print("--------------------------------------------------------------")
    print(f"\nTransport Mode: {transport_mode}")
    print(f"Transport Expenditure: Rs. {transport_expense:.2f}")
    print(f"\nAccommodation Choice: {accommodation_type}")
    if acc_choice in [1, 2]:
        print(f"TOTAL ACCOMMODATION COST: Rs. {total_acc:.2f}")
    print("----------------------------------------------------------------")
    
    
    confirmation = input("Would you like to confirm the trip? (yes/no): ")
    if confirmation.lower() == "yes":
        print("Your trip has been confirmed. Enjoy your journey!")
    else:
        print("Trip canceled. Have a great day!")

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




