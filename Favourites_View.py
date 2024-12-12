"""
University of Toronto
Faculty of Information
Bachelor of Information
INF452: Information Design Studio V: Coding

Student Name: Caitlyn Hundey, Mary Zhao, Qing Zhang

Final Project

Purpose: This program lets the user view a list of their favourite clubs.

Date Created: 2024-11-13
Date Last Modified: 2024-12-05
"""

from tkinter import ttk, messagebox
from Database import *
from Start_View import *
from Club_View import ClubView


class Favourites_View(ttk.Frame):
    """
    A class to represent the favourites view.
    """

    def __init__(self, parent, controller):
        """
        Initialize the Favourites_View frame.

        :param parent: The parent widget.
        :param controller: The controller for managing frames.
        """
        super().__init__(parent)
        self.controller = controller

        # Display the favourite clubs
        self.display_favourites()

    def display_favourites(self):
        """
        Display the list of favourite clubs.
        """
        # Clear the current screen
        for widget in self.winfo_children():
            widget.destroy()

        # Title
        title = ttk.Label(self, text="Favourites", style="Title.TLabel")
        title.grid(row=0, column=0, columnspan=7, pady=10, padx=120)

        # Load and display favourite clubs
        clubs = load_from_file("clubs.json")
        clubs = [Club(**club) for club in clubs]

        # Filter favourite clubs
        favourite_clubs = [club for club in clubs if club.get_is_favourited()]

        # Display each favourite club
        for i, club in enumerate(favourite_clubs):
            club_label = ttk.Label(
                self,
                text=club.get_name(),
                wraplength=220,
                width=23,
                anchor="w",
            )
            club_label.grid(row=1 + i, column=0, padx=10, pady=5, sticky="w")

            # Button to view club details
            ttk.Button(
                self,
                text="View Club",
                width=9,
                command=lambda club=club: self.change_to_Club_View(club),
            ).grid(row=1 + i, column=1)

            # Button to remove from favourites
            favourite_style = ttk.Style()
            favourite_style.configure("DarkRed.TButton", foreground="#720808")
            toggle_favourite = ttk.Button(
                self,
                text="♥",
                width=2,
                style="DarkRed.TButton",
                command=lambda club=club: self.confirm_and_remove_favourite(
                    club
                ),
            )
            toggle_favourite.grid(row=1 + i, column=2)

        # Display message if no favourites
        if len(favourite_clubs) == 0:
            ttk.Label(
                self, text="No favourites yet. Check clubs to find some."
            ).grid(row=2, column=0, padx=10)

    def refresh_favorite_clubs(self):
        """
        Refresh the list of favourite clubs.
        """
        self.display_favourites()

    def confirm_and_remove_favourite(self, club):
        """
        Confirm and remove a club from favourites.

        :param club: The club to remove from favourites.
        """
        # Show a confirmation popup
        confirmed = messagebox.askyesno(
            "Confirm Removal",
            f"Are you sure you want to remove {club.get_name()} from favourites?",
        )
        if confirmed:
            club.unfavourite()  # Remove the club from favourites
            self.display_favourites()  # Refresh the screen

    def change_to_Club_View(self, club):
        """
        Navigate to the ClubView and display the selected club.

        :param club: The club to display.
        """
        club_view = self.controller.frames[ClubView]
        club_view.display_club(club)
        self.controller.show_frame(ClubView)
