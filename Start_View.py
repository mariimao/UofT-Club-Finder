"""
University of Toronto
Faculty of Information
Bachelor of Information
INF452: Information Design Studio V: Coding

Student Name: Caitlyn Hundey, Mary Zhao, Qing Zhang

Final Project

Purpose: This program shows the starting screen/homepage. Users can choose to
 refresh the database or skip the refresh and go to the list view.

Date Created: 2024-11-13
Date Last Modified: 2024-12-05
"""

from tkinter import ttk
from Database import *
from Club_View import *
from List_View import *
import time


class Start_View(ttk.Frame):
    """
    A class to represent the start view of the application.
    """

    def __init__(self, parent, controller):
        """
        Initialize the Start_View frame.

        :param parent: The parent widget.
        :param controller: The controller for managing frames.
        """
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Title label
        title = ttk.Label(
            self, text="The UofT Club Finder", style="Title.TLabel"
        )
        title.pack(padx=10, pady=10)

        clubs = []
        events = []

        # Check if the database files exist
        if check_files():
            # Refresh the database if files exist
            clubs, events = refresh_database()
        else:
            # Load clubs and events from files if they exist
            clubs = load_from_file(CLUBS_FILE)
            events = load_from_file(EVENTS_FILE)
            clubs = [Club(**club) for club in clubs]
            events = [Event(**event) for event in events]

        # Display the current status of the database
        status = ttk.Label(
            self,
            text="In your database, you currently have:",
            wraplength=200,
            width=30,
        )
        status.pack(padx=20, pady=10)
        num_clubs = ttk.Label(
            self,
            text=f"--- {len(clubs)} clubs ---",
            wraplength=200,
            width=30,
            style="Title.TLabel",
            anchor="center",
        )
        num_clubs.pack(padx=20, pady=10)
        num_events = ttk.Label(
            self,
            text=f"--- {len(events)} events ---",
            wraplength=200,
            width=30,
            style="Title.TLabel",
            anchor="center",
        )
        num_events.pack(padx=20, pady=10)

        # Ask the user if they want to refresh the database
        refresh_label = ttk.Label(
            self,
            text="Do you want to refresh the database? It may take up to 10 minutes.",
            wraplength=200,
            width=30,
        )
        refresh_label.pack(padx=20, pady=10)

        # Frame to hold the buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        # Yes button to refresh the database
        yes_button = ttk.Button(
            button_frame,
            text="Yes",
            command=lambda: self.refresh_database(
                clubs, events, status, num_clubs, num_events
            ),
            padding=(10, 5),
        )
        yes_button.pack(side="left", padx=5, pady=5)

        # No button to skip refreshing and go to the list view
        no_button = ttk.Button(
            button_frame,
            text="No",
            command=lambda: self.change_to_List_View(),
            padding=(10, 5),
        )
        no_button.pack(side="left", padx=5, pady=5)

    def refresh_database(self, clubs, events, status, num_clubs, num_events):
        """
        Refresh the database and update the UI.

        :param clubs: The list of clubs.
        :param events: The list of events.
        :param status: The status label to update.
        """
        # Change cursor to loading
        self.config(cursor="watch")
        self.update_idletasks()

        # Perform the refresh after a delay to simulate loading
        def update_database():
            nonlocal clubs, events

            # Simulate a refresh operation
            clubs, events = refresh_database()

            # Update the UI
            self.config(cursor="")  # Reset cursor
            status.config(
                text=f"UPDATE: In your database, you currently have:"
            )
            num_clubs.config(text=f"--- {len(clubs)} clubs ---")
            num_events.config(text=f"--- {len(events)} events ---")
            # self.change_to_List_View()

        # Schedule the database update after 1 second
        self.after(1000, update_database)

    def change_to_List_View(self):
        """
        Navigate to the CategoryView.
        """
        time.sleep(0.5)
        self.controller.show_frame(CategoryView)
