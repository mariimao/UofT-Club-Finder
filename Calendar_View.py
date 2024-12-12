"""
University of Toronto
Faculty of Information
Bachelor of Information
INF452: Information Design Studio V: Coding

Student Name: Caitlyn Hundey, Mary Zhao, Qing Zhang

Final Project

Purpose: This program displays a club event calendar for the user to view 
events by month, search for events by keyword, and open event links.

Date Created: 2024-11-13
Date Last Modified: 2024-12-05
"""

from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
import json
import webbrowser


# Load data from JSON file
def loadFromFile(filename):
    """
    Load data from a JSON file.

    :param filename: The name of the file to load data from.
    :return: The loaded data as a list.
    """
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# Load event data from the saved JSON file
EVENTS_FILE = "events.json"
events = loadFromFile(EVENTS_FILE)


class ClubEventCalendar(ttk.Frame):
    """
    A class to represent the club event calendar.
    """

    def __init__(self, parent, controller=None):
        """
        Initialize the ClubEventCalendar frame.

        :param parent: The parent widget.
        :param controller: The controller for managing frames.
        """
        super().__init__(parent)
        self.controller = controller
        self.grid(row=0, column=0, sticky="nsew")

        # Use ttk to style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Applies it to all pages
        self.styling = ttk.Style()
        self.bg_color = "white"
        self.sec_color = "#A2CDF0"
        self.font = "Arial"
        self.sec_font = "Helvetica"

        self.styling.configure("Red.TButton", foreground="red")
        self.styling.configure(
            "Title.TLabel", font=(self.sec_font, 14, "bold")
        )

        # Buttons:
        self.styling.configure(
            "TButton",
            font=(self.font, 10),
            padding=(2, 2),
            relief="flat",
            background=self.sec_color,
        )

        # White background
        self.styling.configure("TFrame", background=self.bg_color)
        self.styling.configure(
            "TLabel", background=self.bg_color, font=(self.font, 10)
        )

        # Title Label
        self.titleLabel = ttk.Label(
            self, text="Club Event Calendar", style="Title.TLabel"
        )
        self.titleLabel.grid(row=0, column=0, columnspan=7, pady=(5, 10))

        # Navigation Frame
        self.navFrame = ttk.Frame(self, style="TFrame")
        self.navFrame.grid(row=1, column=0, columnspan=7, pady=5)

        self.prevButton = ttk.Button(
            self.navFrame,
            text="<< Previous",
            command=self.previousMonth,
            style="TButton",
        )
        self.prevButton.grid(row=0, column=0, padx=2)

        self.monthYearLabel = ttk.Label(
            self.navFrame, style="TLabel", font=(self.font, 12)
        )
        self.monthYearLabel.grid(row=0, column=1, padx=2)

        self.nextButton = ttk.Button(
            self.navFrame,
            text="Next >>",
            command=self.nextMonth,
            style="TButton",
        )
        self.nextButton.grid(row=0, column=2, padx=2)

        # Make it equal space
        self.navFrame.grid_columnconfigure(0, weight=1)
        self.navFrame.grid_columnconfigure(1, weight=1)
        self.navFrame.grid_columnconfigure(2, weight=1)

        # Current date tracking
        self.currentYear = datetime.now().year
        self.currentMonth = datetime.now().month

        # Calendar grid
        self.calendarFrame = ttk.Frame(self, style="TFrame")
        self.calendarFrame.grid(row=2, column=0, columnspan=7, pady=5)

        # Search bar
        self.searchFrame = ttk.Frame(self, style="TFrame")
        self.searchFrame.grid(row=3, column=0, columnspan=7, pady=5)

        self.searchLabel = ttk.Label(
            self.searchFrame, text="Search Events:", style="TLabel"
        )
        self.searchLabel.grid(row=0, column=0, padx=2)

        self.searchEntry = ttk.Entry(self.searchFrame, width=15)
        self.searchEntry.grid(row=0, column=1, padx=2)

        self.searchButton = ttk.Button(
            self.searchFrame,
            text="Search",
            command=self.searchEvents,
            style="TButton",
        )
        self.searchButton.grid(row=0, column=2, padx=2)

        # Search results display using Text widget
        self.searchResultsText = Text(
            self, wrap="word", height=7, width=40, font=(self.font, 10)
        )
        self.searchResultsText.grid(row=4, column=0, columnspan=7, pady=5)
        self.searchResultsText.config(state=DISABLED)

        # Load events
        self.allEvents = events

        # Display the calendar
        self.displayCalendar()

    def displayCalendar(self):
        """
        Display the calendar for the current month and year.
        """
        # Update the month/year label
        self.monthYearLabel.config(
            text=f"{datetime(self.currentYear, self.currentMonth, 1).strftime('%B %Y')}"
        )

        # Clear previous calendar
        for widget in self.calendarFrame.winfo_children():
            widget.destroy()

        # Determine the first day and number of days in the current month
        firstDay = datetime(self.currentYear, self.currentMonth, 1)
        firstWeekday = firstDay.weekday()  # Monday = 0, Sunday = 6
        daysInMonth = (
            firstDay.replace(month=self.currentMonth % 12 + 1, day=1)
            - timedelta(days=1)
        ).day

        # Add day labels
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days):
            lbl = ttk.Label(
                self.calendarFrame,
                text=day,
                style="TLabel",
                font=(self.font, 10, "bold"),
            )
            lbl.grid(row=0, column=col, padx=2, pady=2)

        # Add days of the month
        row = 1
        col = firstWeekday

        for day in range(1, daysInMonth + 1):
            dayDate = datetime(self.currentYear, self.currentMonth, day)
            formattedDate = dayDate.strftime("%d %B, %Y")

            # Day frame
            dayFrame = ttk.Frame(
                self.calendarFrame,
                relief="raised",
                borderwidth=1,
                style="TFrame",
            )
            dayFrame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            dayLabel = ttk.Label(
                dayFrame, text=str(day), style="TLabel", font=(self.font, 10)
            )
            dayLabel.pack(anchor="nw")

            # Events for the day
            for event in self.allEvents:
                if event.get("date") == formattedDate:
                    # When I use wraplength in button will cause black screen issue. So I changed it to Label to avoid that issue
                    eventLabel = ttk.Label(
                        dayFrame,
                        text=event.get("title", "No Title"),
                        style="TLabel",
                        wraplength=80,
                        cursor="hand2",
                        background=self.sec_color,
                    )
                    eventLabel.pack(anchor="w", pady=1)
                    # Can click to open URL
                    eventLabel.bind(
                        "<Button-1>",
                        lambda e, url=event.get(
                            "original_url"
                        ): self.openEventLink(url),
                    )

            # Move to next row after Sunday
            col += 1
            if col > 6:
                col = 0
                row += 1

    def previousMonth(self):
        """
        Navigate to the previous month.
        """
        self.currentMonth -= 1
        if self.currentMonth == 0:
            self.currentMonth = 12
            self.currentYear -= 1
        self.displayCalendar()

    def nextMonth(self):
        """
        Navigate to the next month.
        """
        self.currentMonth += 1
        if self.currentMonth == 13:
            self.currentMonth = 1
            self.currentYear += 1
        self.displayCalendar()

    def openEventLink(self, url):
        """
        Open the link for the selected event.

        :param url: The URL of the event to open.
        """
        if url:
            webbrowser.open(url)

    def searchEvents(self):
        """
        Search events by keyword.
        """
        keyword = self.searchEntry.get().lower().strip()
        self.searchResultsText.config(state=NORMAL)
        self.searchResultsText.delete(1.0, END)
        found = False

        for event in self.allEvents:
            if (
                keyword in event.get("title", "").lower()
                or keyword in event.get("description", "").lower()
                or keyword in event.get("club", "").lower()
            ):
                eventText = f"{event.get('title', 'No Title')} by {event.get('club', 'Unknown Club')} on {event.get('date', 'Unknown Date')}\n\n"
                self.searchResultsText.insert(END, eventText)
                found = True

        if not found:
            self.searchResultsText.insert(
                END, "No events found. Please try a different keyword.\n"
            )

        self.searchResultsText.config(state=DISABLED)
