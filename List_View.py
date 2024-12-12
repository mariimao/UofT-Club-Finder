"""
University of Toronto
Faculty of Information
Bachelor of Information
INF452: Information Design Studio V: Coding

Student Name: Caitlyn Hundey, Mary Zhao, Qing Zhang

Final Project

Purpose: This program allows the user to view a list of clubs.

Date Created: 2024-11-13
Date Last Modified: 2024-12-05
"""

from tkinter import *
import json
from Database import *
from tkinter import ttk
from Filter_Campus_View import *


# Load data and receive all club categories
load_clubs = load_from_file("clubs.json")
# Convert dictionaries to Club and Event objects
all_clubs = [Club(**club) for club in load_clubs]


#### adjusted to work with filters ######
# Load filters from the filters.json file
def load_filters():
    """
    Load filters from the filters.json file.

    :return: A dictionary containing the filters.
    """
    if os.path.exists("filters.json"):
        with open("filters.json", "r") as f:
            return json.load(f)
    else:
        with open("filters.json", "w") as f:
            json.dump({"campus": None, "interests": []}, f)
    return {"campus": None, "interests": []}


filters = load_filters()


# Filter clubs based on campus and interests
def filter_clubs(clubs, filters):
    """
    Filter clubs based on the selected campus and interests.

    :param clubs: The list of all clubs.
    :param filters: The filters to apply.
    :return: A list of filtered clubs.
    """
    filtered_clubs = clubs
    if filters["campus"]:
        filtered_clubs = [
            club
            for club in filtered_clubs
            if club.get_campus() == filters["campus"]
        ]
    if filters["interests"]:
        filtered_clubs = [
            club
            for club in filtered_clubs
            if any(
                interest in club.get_categories()
                for interest in filters["interests"]
            )
        ]
    return filtered_clubs


filtered_clubs = filter_clubs(all_clubs, filters)
categories = get_all_categories(filtered_clubs)


# The main page
class CategoryView(ttk.Frame):
    """
    A class to represent the category view.
    """

    def __init__(self, parent, controller):
        """
        Initialize the CategoryView frame.

        :param parent: The parent widget.
        :param controller: The controller for managing frames.
        """
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.configure(style="TFrame")  # Set the background to white

        # Variables
        buttons_per_row = 2
        button_width = 14  # Width of each button
        padding = 10  # Padding between buttons

        # Configure grid layout for the main frame
        self.grid_rowconfigure(0, weight=0)  # Title
        self.grid_rowconfigure(2, weight=1)  # Scrollable content
        self.grid_columnconfigure(0, weight=1)  # Left margin
        self.grid_columnconfigure(1, weight=1)  # Content
        self.grid_columnconfigure(2, weight=0)  # Scrollbar

        # Title label
        label = ttk.Label(self, text="Browse Categories", style="Title.TLabel")
        label.grid(row=0, column=0, columnspan=3, pady=10)

        # Add a button for filter
        filter_campus = Filter_Campus_View(self, controller)
        filter_campus_button = Button(
            self,
            text="Filter by Campus",
            command=lambda: filter_campus.open_campus_popup(),
        )
        filter_campus_button.grid(
            row=1, column=1, columnspan=2, pady=20, padx=20
        )

        # Scrollable frame setup using Canvas
        canvas = Canvas(self, bg="white")
        canvas.grid(row=2, column=1, sticky="ns")

        # Make a scrollable frame
        scrollable_frame = ttk.Frame(canvas, style="TFrame")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Add a scrollbar
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=2, column=2, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Makes the scroll bar move
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        # Make scrollable frame columns distribute space evenly
        for i in range(buttons_per_row):
            scrollable_frame.grid_columnconfigure(i, weight=0)

        # Make dynamic buttons for each category
        for i, category in enumerate(categories):
            row = i // buttons_per_row  # Determine the row number
            column = i % buttons_per_row  # Determine the column number
            button = Button(
                scrollable_frame,
                text=category,
                bg="lightblue",
                fg="black",
                width=button_width,
                height=5,
                wraplength=120,
                command=lambda c=category: self.change_to_ClubListView(c),
            )
            button.grid(row=row, column=column, padx=padding, pady=padding)

    def change_to_ClubListView(self, category):
        """
        Navigate to the ClubListView and pass the selected category.

        :param category: The selected category.
        """
        from Club_View import (
            ClubListView,
        )  # Lazy way of importing, but ensures no circle error

        if self.controller:
            club_list_view = self.controller.frames[ClubListView]
            clubs_in_category = update_club_list(category)
            club_list_view.club_list(category, clubs_in_category)
            self.controller.show_frame(ClubListView)

    def filter_by_campus(self, controller):
        """
        Open the campus filter pop-up.

        :param controller: The controller for managing frames.
        """
        filter_campus = Filter_Campus_View(self, controller)
        filter_campus.open_campus_popup()


def update_club_list(category):
    """
    Add the clubs to the selected category.

    :param category: The selected category.
    :return: A list of club names in the selected category.
    """
    filters = load_filters()
    filtered_clubs = filter_clubs(all_clubs, filters)
    categories = get_all_categories(filtered_clubs)

    # Filter clubs that belong to the selected category
    filtered_club_names = [
        club.get_name()
        for club in filtered_clubs
        if category in club.get_categories()
    ]
    return filtered_club_names
