"""
University of Toronto
Faculty of Information
Bachelor of Information
INF452: Information Design Studio V: Coding

Student Name: Caitlyn Hundey, Mary Zhao, Qing Zhang

Final Project

Purpose: This program opens a pop-up window to select the campus for filtering 
clubs.

Date Created: 2024-11-13
Date Last Modified: 2024-12-05
"""

import tkinter as tk
from tkinter import ttk
import json
from Database import *
from List_View import *


class Filter_Campus_View(ttk.Frame):
    """
    A class to represent the filter campus view.
    """

    def __init__(self, parent, controller):
        """
        Initialize the Filter_Campus_View frame.

        :param parent: The parent widget.
        :param controller: The controller for managing frames.
        """
        ttk.Frame.__init__(self, parent)
        self.controller = controller

    def open_campus_popup(self):
        """
        Open a pop-up window to select the campus for filtering clubs.
        """
        popup = tk.Toplevel(self)
        popup.title("Select your campus")
        popup.geometry("300x400")
        popup.configure(bg="white")

        # Title label
        title = ttk.Label(
            popup,
            text="Select your campus",
            font=("Helvetica", 25, "bold"),
            wraplength=200,
        )
        title.pack(padx=10, pady=10)

        # Description label
        description = ttk.Label(
            popup,
            text="Choose a campus to filter out the clubs.",
            wraplength=200,
        )
        description.pack(padx=10, pady=10)

        # Campus selection buttons
        campuses = ["St George", "UTSC", "UTM"]
        for campus in campuses:
            campus_button = ttk.Button(
                popup,
                text=campus,
                command=lambda campus=campus: self.apply_campus(campus, popup),
            )
            campus_button.pack(padx=10, pady=10)

        # Add a "Skip" button
        skip_button = ttk.Button(
            popup,
            text="No Filters",
            command=lambda: self.apply_campus(None, popup),
        )
        skip_button.pack(padx=10, pady=10)

    def apply_campus(self, campus, popup):
        """
        Apply the selected campus filter and update the filters.json file.

        :param campus: The selected campus.
        :param popup: The pop-up window to close after selection.
        """
        popup.destroy()

        clubs = load_from_file(CLUBS_FILE)
        clubs = [Club(**club) for club in clubs]
        all_interests = get_all_categories(clubs)

        # Add the property campus with the campus as a list to the filters.json file
        filters = {"campus": campus, "interests": all_interests}
        with open("filters.json", "w") as f:
            json.dump(filters, f, indent=4)

        # Refresh the list view by closing and reopening the app
        self.controller.refresh_category()
