"""
University of Toronto
Faculty of Information
Bachelor of Information
INF452: Information Design Studio V: Coding

Student Name: Caitlyn Hundey, Mary Zhao, Qing Zhang

Final Project

Purpose: This program allows the user to view a list of clubs at the 
University of Toronto, filter the clubs by campus and interests, view club 
details, view club events, and favourite clubs.

Date Created: 2024-11-13
Date Last Modified: 2024-12-05
"""

import tkinter as tk
from tkinter import ttk
from Start_View import *
from Club_View import ClubListView, ClubView
from List_View import *
from Calendar_View import *
from Favourites_View import *


class MainApp(tk.Tk):
    """
    Main application class for the UofT Club Finder.
    """

    def __init__(self):
        """
        Initialize the main application.
        """
        tk.Tk.__init__(self)

        self.title("UofT Club Finder")
        self.geometry("375x667")  # size of iPhone shrunken down to 1/3

        # Main container to hold all frames
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Configure grid layout (so all child frames can fit)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Set the style and theme
        style = ttk.Style()
        style.theme_use("clam")

        self.styling = ttk.Style()
        self.bg_color = "white"
        self.sec_color = "#A2CDF0"
        self.font = "Arial"
        self.sec_font = "Helvetica"

        # Configure styles
        self.styling.configure("Red.TButton", foreground="#720808")
        self.styling.configure(
            "Title.TLabel", font=(self.sec_font, 16, "bold")
        )
        self.styling.configure(
            "TButton",
            font=(self.font, 12),
            padding=(3, 2),
            relief="flat",
            background=self.sec_color,
        )
        self.styling.configure("TFrame", background=self.bg_color)
        self.styling.configure(
            "TLabel", background=self.bg_color, font=(self.font, 12)
        )

        # Frames dictionary to store the references for each page
        self.frames = {}

        # Initialize all the frames (views)
        for Page in (
            Start_View,
            CategoryView,
            ClubEventCalendar,
            Favourites_View,
            ClubListView,
            ClubView,
        ):
            frame = Page(self.container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial frame (you can set it to Start_View if desired)
        self.show_frame(Start_View)

        # Create navigation buttons at the bottom (only once)
        self.create_nav_buttons()

    def create_nav_buttons(self):
        """
        Create navigation buttons at the bottom of the main window.
        """
        # Frame to hold navigation buttons
        nav_frame = tk.Frame(self, bg=self.bg_color)
        nav_frame.pack(side="bottom", fill="x", expand=False)

        # Container frame to center the buttons
        button_container = tk.Frame(nav_frame, bg=self.bg_color)
        button_container.pack(expand=True, anchor="center")

        # Navigation buttons
        home_button = ttk.Button(
            button_container,
            width=5,
            text="Home",
            command=lambda: self.show_frame(Start_View),
        )
        home_button.pack(side="left", padx=5, pady=5)

        calendar_button = ttk.Button(
            button_container,
            width=7,
            text="Calendar",
            command=lambda: self.show_frame(ClubEventCalendar),
        )
        calendar_button.pack(side="left", padx=5, pady=5)

        club_list_button = ttk.Button(
            button_container,
            width=5,
            text="Clubs",
            command=lambda: self.show_frame(CategoryView),
        )
        club_list_button.pack(side="left", padx=5, pady=5)

        favourites_button = ttk.Button(
            button_container,
            width=9,
            text="Favourites",
            command=lambda: self.show_frame(Favourites_View),
        )
        favourites_button.pack(side="left", padx=5, pady=5)

    def show_frame(self, page):
        """
        Bring the specified frame to the front.

        :param page: The frame to show.
        """
        frame = self.frames[page]
        frame.tkraise()

        # Refresh favourites page if it is being shown
        if page == Favourites_View:
            frame.refresh_favorite_clubs()

    def refresh_category(self):
        """
        Refresh the CategoryView frame.
        """
        self.frames[CategoryView].destroy()
        frame = CategoryView(self.container, self)
        self.frames[CategoryView] = frame
        frame.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
