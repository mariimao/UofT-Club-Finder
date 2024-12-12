"""
University of Toronto
Faculty of Information
Bachelor of Information
INF452: Information Design Studio V: Coding

Student Name: Caitlyn Hundey, Mary Zhao, Qing Zhang

Final Project

Purpose: This program allows the user to view a list of clubs and see a more
detailed view of each club. The user can also favourite clubs.

Date Created: 2024-11-13
Date Last Modified: 2024-12-05
"""

from tkinter import *
import json
from Database import *
from List_View import all_clubs
from tkinter import ttk


class ClubListView(ttk.Frame):
    """
    A class to represent the list view of clubs.
    """

    def __init__(self, parent, controller):
        """
        Initialize the ClubListView frame.

        :param parent: The parent widget.
        :param controller: The controller for managing frames.
        """
        super().__init__(parent)
        self.controller = controller
        self.all_clubs = all_clubs

        self.configure(style="TFrame")  # Set the background to white

        # Configure grid rows and columns
        self.grid_rowconfigure(0, weight=0)  # Title row
        self.grid_rowconfigure(1, weight=0)  # Listbox row
        self.grid_rowconfigure(2, weight=0)  # Back button row
        self.grid_columnconfigure(0, weight=1)  # Single column

        # Title label
        self.label = Label(
            self,
            text="Club List",
            font=("Arial", 16),
            wraplength=250,
            bg="white",
        )
        self.label.grid(row=0, column=0, pady=5, sticky="n")

        # Placeholder for club list content
        self.club_listbox = Listbox(self, width=50, height=20)
        self.club_listbox.grid(
            row=1, column=0, padx=10, pady=10, sticky="nsew"
        )

        # Bind listbox selection to the handler
        self.club_listbox.bind("<<ListboxSelect>>", self.open_club_view)

        # Back button to return to CategoryView
        back_button = Button(
            self, text="<< Back", command=self.change_to_CategoryView
        )
        back_button.grid(row=2, column=0, pady=10)

    def change_to_CategoryView(self):
        """
        Navigate back to the CategoryView.
        """
        from List_View import (
            CategoryView,
        )  # Lazy way of importing, but ensures no circle error

        self.controller.show_frame(CategoryView)

    def club_list(self, category, list_of_clubs):
        """
        Populate the listbox with clubs in the selected category.

        :param category: The selected category.
        :param list_of_clubs: The list of clubs in the category.
        """
        self.label.config(
            text=f"Clubs in {category}"
        )  # Update the title to show the category
        self.club_listbox.delete(0, END)  # Clear previous entries

        # Insert each club name into the Listbox
        for name in list_of_clubs:
            self.club_listbox.insert(END, name)

    def open_club_view(self, event):
        """
        Open the detailed view for the selected club.

        :param event: The event that triggered the method.
        """
        # Get selected club name
        selected_index = self.club_listbox.curselection()
        if not selected_index:
            return
        selected_club_name = self.club_listbox.get(selected_index)

        # Find the selected club
        selected_club = next(
            (
                club
                for club in self.all_clubs
                if club.get_name() == selected_club_name
            ),
            None,
        )
        if selected_club:
            # Navigate to ClubView with the selected club
            club_view = self.controller.frames[ClubView]
            club_view.display_club(selected_club)
            self.controller.show_frame(ClubView)


class ClubView(ttk.Frame):
    """
    A class to represent the detailed view of a club.
    """

    def __init__(self, parent, controller):
        """
        Initialize the ClubView frame.

        :param parent: The parent widget.
        :param controller: The controller for managing frames.
        """
        super().__init__(parent)
        self.controller = controller

        self.configure(style="TFrame")  # Set the background to white

        # Configure the layout of the parent frame
        self.grid_rowconfigure(0, weight=1)  # Allow parent row to expand
        self.grid_columnconfigure(0, weight=1)  # Allow parent column to expand

        # Nested frame for club details
        nested_frame = ttk.Frame(self, style="TFrame")
        nested_frame.grid(row=0, column=0, sticky="nsew")
        nested_frame.grid_rowconfigure(0, weight=0)  # Club title row
        nested_frame.grid_rowconfigure(1, weight=0)  # Description title row
        nested_frame.grid_rowconfigure(2, weight=1)  # Description row
        nested_frame.grid_rowconfigure(3, weight=0)  # Location and Contact row
        nested_frame.grid_columnconfigure(0, weight=1)  # Content column
        nested_frame.grid_columnconfigure(
            1, weight=0
        )  # Heart/scrollbar column

        # Title for club information
        self.label = Label(
            nested_frame,
            text="Club Details",
            font=("Arial", 18),
            wraplength=250,
            bg="white",
        )
        self.label.grid(row=0, column=0, pady=(10, 5), sticky="n")

        # Add description title above the scrollable area
        description_label = Label(
            nested_frame,
            text="Description:",
            font=("Arial", 14),
            fg="blue",
            bg="white",
        )
        description_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Scrollable frame setup using Canvas for the description
        description_canvas = Canvas(
            nested_frame, height=200, bg="white"
        )  # Set height to restrict space
        description_canvas.grid(row=2, column=0, padx=5, pady=0, sticky="nsew")

        # Add a scrollbar for the canvas
        scrollbar = Scrollbar(
            nested_frame, orient="vertical", command=description_canvas.yview
        )
        scrollbar.grid(row=2, column=1, sticky="ns")
        description_canvas.configure(yscrollcommand=scrollbar.set)

        # Create a scrollable frame within the canvas
        description_frame = Frame(
            description_canvas, padx=5, pady=0, bg="white"
        )
        description_canvas.create_window(
            (0, 0), window=description_frame, anchor="nw"
        )

        # Club description
        self.club_info = Label(
            description_frame,
            text="",
            font=("Arial", 10),
            wraplength=270,
            bg="white",
            anchor="w",
            justify="left",
        )
        self.club_info.grid(row=0, column=0, pady=(10, 10), sticky="nw")

        # Makes the scroll bar move
        description_frame.bind(
            "<Configure>",
            lambda e: description_canvas.configure(
                scrollregion=description_canvas.bbox("all")
            ),
        )

        # Back button to return to ClubListView
        back_button = Button(
            nested_frame,
            text="<< Back",
            command=self.change_to_ClubListView,
            anchor="center",
        )
        back_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="n")

        # Location and Contact Frame Widgets
        loc_contact_frame = ttk.Frame(nested_frame, style="TFrame")
        loc_contact_frame.grid(
            row=3, column=0, columnspan=2, pady=(20, 10), sticky="nsew"
        )

        loc_contact_frame.grid_rowconfigure(0, weight=1)
        loc_contact_frame.grid_columnconfigure(0, weight=1)
        loc_contact_frame.grid_columnconfigure(1, weight=1)

        # Location information in a separate frame on the left
        location_frame = ttk.Frame(loc_contact_frame, style="TFrame")
        location_frame.grid(row=0, column=0, padx=5, sticky="nsew")
        self.location_label = Label(
            location_frame,
            text="Location⚑:",
            font=("Arial", 11),
            anchor="w",
            fg="blue",
            bg="white",
        )
        self.location_label.grid(row=0, column=0, pady=(5, 5), sticky="w")

        self.location_info = Label(
            location_frame,
            text="",
            font=("Arial", 10),
            wraplength=100,
            anchor="w",
            justify="left",
            bg="white",
        )
        self.location_info.grid(row=1, column=0, pady=(0, 10), sticky="w")

        # Contact information in a separate frame on the right
        contact_frame = ttk.Frame(loc_contact_frame, style="TFrame")
        contact_frame.grid(row=0, column=1, padx=5, sticky="nsew")

        self.contact_label = Label(
            contact_frame,
            text="Contact Information ☎:",
            font=("Arial", 11),
            anchor="w",
            fg="blue",
            bg="white",
        )
        self.contact_label.grid(row=0, column=0, pady=(5, 5), sticky="w")

        self.contact_info = Label(
            contact_frame,
            text="",
            font=("Arial", 10),
            wraplength=200,
            anchor="w",
            justify="left",
            bg="white",
        )
        self.contact_info.grid(row=1, column=0, pady=(0, 10), sticky="w")

        # Favourite button to add/remove from favourites
        self.favourite_button = Button(
            nested_frame,
            text="♡",
            font=("Arial", 14),
            command=self.toggle_favourite,
            bg=self.controller.sec_color,
        )
        self.favourite_button.grid(row=0, column=1, padx=10, sticky="e")

        # Store the current club
        self.current_club = None

    def display_club(self, club):
        """
        Display the selected club's information.

        :param club: The club object to display.
        """
        self.current_club = club
        self.label.config(text=f"{club.get_name()}")
        self.club_info.config(text=club.get_description())

        # Update location info
        self.location_info.config(text=f"Campus: {club.get_campus()}")

        # Update contact info with formatted list of contacts
        contacts = club.get_contacts()
        contact_str = (
            "\n".join(contacts)
            if contacts
            else "No contact information available."
        )
        self.contact_info.config(text=contact_str)

        # Update favourite button state
        if club.get_is_favourited():
            self.favourite_button.config(text="♥")
        else:
            self.favourite_button.config(text="♡")

    def toggle_favourite(self):
        """
        Toggle the favourite status of the current club.
        """
        if self.current_club:
            if self.current_club.get_is_favourited():
                self.current_club.unfavourite()
                self.favourite_button.config(text="♡", fg="#720808")
            else:
                self.current_club.favourite()
                self.favourite_button.config(text="♥", fg="#720808")

            # Save updated clubs.json file
            self.save_clubs_to_file()

    def save_clubs_to_file(self):
        """
        Helper function to save the updated clubs to the clubs.json file.
        """
        # Load all club objects from the file
        clubs = load_from_file(CLUBS_FILE)
        all_clubs = [Club(**club) for club in clubs]

        # Save the updated list of clubs to the file
        updated_clubs_data = [club.to_dict() for club in all_clubs]
        save_to_file(CLUBS_FILE, updated_clubs_data)

    def change_to_ClubListView(self):
        """
        Navigate back to the ClubListView.
        """
        self.controller.show_frame(ClubListView)
