import requests
from bs4 import BeautifulSoup
import json  # codehs does not need to install
import os  # codehs does not need to install
import datetime

# names for files
CLUBS_FILE = "clubs.json"
EVENTS_FILE = "events.json"
FILTERS_FILE = "filters.json"


class Event:
    """
    The Event class.

    Attributes:
    club: The name of the club hosting the event.
    date: The date of the event, formatted as DD MONTH, YYYY.
    original_url: The original url of the event, may not be working.
    title: The title of the event.
    description: The description of the event from the club page.
    """

    def __init__(
        self,
        club: str,
        date: datetime.datetime,
        original_url: str,
        title: str,
        description: str,
    ):
        """
        Constructor for the Event class."""
        self.__club = club
        self.__date = date
        self.__original_url = original_url
        self.__title = title
        self.__description = description

    # GETTERS BELOW vvvvvvvvvvvvvvvvvvvvvvvv

    def get_club(self):
        return self.__club

    def get_date(self):
        return self.__date

    def get_original_url(self):
        return self.__original_url

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def to_dict(self):
        """
        Converts to a dictionary. We need this to save the data to a file.
        The date is converted back to a string in the form DD MONTH, YYYY.

        :return: A dictionary of the Event object.
        """
        return {
            "club": self.get_club(),
            "date": self.get_date().strftime("%d %B, %Y"),
            "original_url": self.get_original_url(),
            "title": self.get_title(),
            "description": self.get_description(),
        }


class Club:
    """
    The Club class.

    Attributes:
    name: The full name of the club. May include the campus and/or short form.
    campus: The campus the club is located at.
    description: The description of the club.
    contacts: Any social media, email, or phone numbers on the website.
    categories: The categories the club falls under.
    events: A list of Event objects related to the club.
    original_url: The original url of the club.
    is_favourited: A boolean to check if the club is favourited.
    """

    def __init__(
        self,
        name: str,
        campus: str,
        description: str,
        contacts: list,
        categories: list,
        events: list,
        original_url: str,
        is_favourited: bool,
    ):
        """
        Constructor for the Club class.
        """
        self.__name = name
        self.__campus = campus
        self.__description = description
        self.__contacts = contacts
        self.__categories = categories
        self.__events = events
        self.__original_url = original_url
        self.__is_favourited = is_favourited

    # GETTERS BELOW vvvvvvvvvvvvvvvvvvvvvvvv

    def get_name(self) -> str:
        return self.__name

    def get_campus(self) -> str:
        return self.__campus

    def get_description(self) -> str:
        return self.__description

    def get_contacts(self) -> list:
        return self.__contacts

    def get_categories(self) -> list:
        return self.__categories

    def get_events(self) -> list:
        return self.__events

    def get_original_url(self) -> str:
        return self.__original_url

    def get_is_favourited(self) -> bool:
        return self.__is_favourited

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def to_dict(self) -> dict:
        """
        Converts to a dictionary. We need this to save the data to a file.
        Note that the events are converted to a dictionary as well.

        :return: A dictionary of the Club object.
        """
        return {
            "name": self.get_name(),
            "campus": self.get_campus(),
            "description": self.get_description(),
            "contacts": self.get_contacts(),
            "categories": self.get_categories(),
            "events": [event.to_dict() for event in self.get_events()],
            "original_url": self.get_original_url(),
            "is_favourited": self.get_is_favourited(),
        }

    def favourite(self):
        """
        Sets the favourite attribute to true and updates the database.
        """
        self.__is_favourited = True
        clubs = load_from_file(CLUBS_FILE)
        for club in clubs:
            if club["original_url"] == self.get_original_url():
                club["is_favourited"] = True
                break
        save_to_file(CLUBS_FILE, clubs)

    def unfavourite(self):
        """
        Sets the favourite attribute to false and updates the database.
        """
        self.__is_favourited = False
        clubs = load_from_file(CLUBS_FILE)
        for club in clubs:
            if club["original_url"] == self.get_original_url():
                club["is_favourited"] = False
                break
        save_to_file(CLUBS_FILE, clubs)


def fetch_page(url: str) -> BeautifulSoup:
    """
    Helper function to fetch the page from the url and parse it.
    If it runs into an error, it prints the error and returns None.

    :param url: The url to fetch.
    :return: The BeautifulSoup object.
    """
    try:
        # fetch the page
        response = requests.get(url)

        # return the parsed page
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        # print an error message and return none
        print(f"Error fetching {url}: {e}")
        return None


def get_club_urls() -> list:
    """
    Gets all the club urls from the SOP website.
    Note that on the SOP page, we have to scroll down to load more clubs.
    As we scroll, the page number changes in the url.

    As of November 2024:
    - There are 25 pages of clubs (1 to 25 inclusive).
    - The urls for the clubs are <a> tags with the class
      "flex-1 font-bold text-primary".

    :return: A list of all the club urls.
    """
    all_club_urls = []

    # 1 to 25 inclusive
    for i in range(1, 26):
        # get the page
        page_url = "https://sop.utoronto.ca/groups/?pg=" + str(i)
        soup = fetch_page(page_url)

        # if the page is fetched, get the urls
        if soup:
            # finds all <a> tags with the class "flex-1 font-bold text-primary"
            urls = soup.find_all(
                "a", class_="flex-1 font-bold text-primary", href=True
            )

            # if there is a href and it is not in the list, add it
            for a in urls:
                if a["href"] not in all_club_urls:
                    all_club_urls.append(a["href"])

    print(f"Found {len(all_club_urls)} links for club on SOP.")
    return all_club_urls


def get_club_info(url: str) -> tuple:
    """
    Gets the club information from the url.
    Each attribute is found by selecting the appropriate tag and class.
    Check the comments for details on how each property is found.

    :param url: The url of the club.
    :return: A tuple of Club and Event objects.
    """
    # if any element does not exist, return None for the club and events
    try:
        # fetch the page
        soup = fetch_page(url)

        # NAME and CAMPUS are in the SECOND h1 tag
        # there are some extra spaces and newlines, so we strip and split
        h1_tags = soup.find_all("h1")[1].text  # convert to string
        h1_tags = h1_tags.strip().split("\n")  # remove extra spaces and split
        h1_tags = [x.strip() for x in h1_tags if x.strip()]  # remove empty str
        name = h1_tags[0]  # name is the first element
        campus = h1_tags[-1]  # campus is the last element

        # DESCRIPTION is the first element in the pr-8 class
        # we strip the text to remove extra spaces
        description = soup.select(".pr-8")[0].get_text(strip=True)

        # CATEGORIES are in the <a> tags with the href containing
        # "areas_of_interest". We can use the arial-label attribute to get the
        # proper text.
        a_tags = soup.find_all("a", href=True)
        categories = [
            tag["arial-label"]
            for tag in a_tags
            if "/groups/?areas_of_interest=" in tag["href"]
        ]

        # CONTACTS are split between socials, mail, and tel
        # socials are in the div with the class "flex gap-4 mb-4" with hrefs
        # some clubs do not have socials
        socials = soup.find("div", class_="flex gap-4 mb-4")
        if socials:
            socials = [div["href"] for div in socials.find_all("a", href=True)]
        else:
            socials = []
        # mail are in the <a> tags with the href containing "mailto:"
        mail = [a["href"] for a in a_tags if "mailto:" in a["href"]]
        # tel are in the <a> tags with the href containing "tel:"
        tel = [a["href"] for a in a_tags if "tel:" in a["href"]]
        # we can combine all contacts into one list
        contacts = socials + mail + tel

        # IS_FAVOURITED is set to False by default
        # if the CLUBS_FILE exists, we check if the club is favourited or not
        is_favourited = False
        # check if the file exists
        if os.path.exists(CLUBS_FILE):
            # open the file and load the data
            clubs = load_from_file(CLUBS_FILE)
            # go through each club and check if the url matches
            for club in clubs:
                if club["original_url"] == url:
                    # set the is_favourited to the value in the file
                    is_favourited = club["is_favourited"]
                    break

        # EVENTS are in the <ul> tags with the class "mb-4 flex flex-col ga-4"
        # each events is an <li> tag
        events = []
        events_ul = soup.find_all("ul", class_="mb-4 flex flex-col ga-4")
        for li in events_ul:
            # the club name is the same as the name of the club
            club = name

            # the date is in the <div> tag with the aria-label attribute
            # we convert the date to a datetime object
            date = li.find("div")["aria-label"]
            date = datetime.datetime.strptime(date, "%d %B, %Y")

            # the link is in the <a> tag
            link = li.find("a")["href"]

            # the title is the text inside the <a> tag
            title = li.find("a").text

            # description is text in the <p> tage
            event_description = li.find("p").text

            # create a new Event object and append it to the list
            new_event = Event(club, date, link, title, event_description)
            events.append(new_event)

        # create a new Club object with the information
        new_club = Club(
            name,
            campus,
            description,
            contacts,
            categories,
            events,
            url,
            is_favourited,
        )

        return new_club, events
    except Exception as e:
        # print(f"Error fetching {url}: {e}")
        return None, None


def refresh_database() -> tuple:
    """
    Refreshes the database by scraping new data and saving it.

    :return: A tuple of lists of Club and Event objects.
    """
    clubs = []
    events = []

    # get all the club urls with the helper function
    all_club_urls = get_club_urls()

    # go through each url and get the club and events if they exist
    for url in all_club_urls:
        print(f"URL found: {url}")
        club, club_events = get_club_info(url)
        if club:
            clubs.append(club)
        if club_events:
            events.extend(club_events)

    # for testing purposes, we only get the first 30 clubs
    # for i in range(30):
    #     print(f"URL found: {all_club_urls[i]}")
    #     club, club_events = get_club_info(all_club_urls[i])
    #     if club:
    #         clubs.append(club)
    #     if club_events:
    #         events.extend(club_events)

    # rewrites the json files, converting the objects to dictionaries
    save_to_file(CLUBS_FILE, [club.to_dict() for club in clubs])
    save_to_file(EVENTS_FILE, [event.to_dict() for event in events])

    return clubs, events


def save_to_file(filename: str, data: list) -> None:
    """
    Saves the data to the file.

    :param filename: The name of the file.
    :param data: The data to save.
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)  # indent for pretty printing :)


def load_from_file(filename: str) -> list:
    """
    Loads the data from the file.

    :param filename: The name of the file.
    :return: The data from the file as a list.
    """
    # creates empty files if they don't exist
    if not os.path.exists(filename):
        save_to_file(filename, [])

    with open(filename, "r") as f:
        return json.load(f)


def check_files() -> bool:
    """
    Checks if the files exist. If they don't, creates them.

    :return: True if the files were created, False otherwise.
    """
    files_created = False

    # checks the CLUBS_FILE
    if not os.path.exists(CLUBS_FILE):
        save_to_file(CLUBS_FILE, [])
        files_created = True

    # checks the EVENTS_FILE
    if not os.path.exists(EVENTS_FILE):
        save_to_file(EVENTS_FILE, [])
        files_created = True

    return files_created


def get_all_categories(clubs: list) -> list:
    """
    Collects all unique categories from a list of Club objects.

    :param clubs: The list of Club objects.
    :return: A list of all unique categories.
    """
    # use a set first to get unique categories
    all_categories = set()

    # go through all the clubs and add the categories to the set
    for club in clubs:
        all_categories.update(club.get_categories())

    # convert it to a list and return
    return list(all_categories)


def filter_campus(clubs: list, campus: str) -> list:
    """
    Filters the clubs by campus (St George, UTM, UTSC).

    :param clubs: The list of Club objects.
    :param campus: The campus to filter by.
    :return: A list of Club objects that match the campus.
    """
    return [club for club in clubs if club.get_campus() == campus]


def filter_categories(clubs: list, categories: list) -> list:
    """
    Filters the clubs by categories. Note that it needs to match ALL the
    categories in the list

    :param clubs: The list of Club objects.
    :param categories: The list of categories to filter by.
    :return: A list of Club objects that match the categories.
    """
    return [
        club
        for club in clubs
        if all(category in club.get_categories() for category in categories)
    ]


def filter_is_favourited(clubs: list, option: bool) -> list:
    """
    Filters the clubs by is_favourited.

    :param clubs: The list of Club objects.
    :param is_favourited: The is_favourited status to filter by.
    :return: A list of Club objects that match the is_favourited status.
    """
    return [club for club in clubs if club.get_is_favourited() == option]


def filter_keywords(clubs: list, keywords: list) -> list:
    """
    Filters the clubs by keywords in name or description.

    :param clubs: The list of Club objects.
    :param keywords: The list of keywords to filter by.
    :return: A list of Club objects that match the keywords.
    """
    return [
        club
        for club in clubs
        if any(
            keyword.lower() in club.get_name().lower()
            or keyword.lower() in club.get_description().lower()
            for keyword in keywords
        )
    ]


def update_filters(campus: str, interests: list) -> None:
    """
    Adds filters for campus and interests to the filter file.

    :param campus: String for campus
    :param interests: The list of interests chosen.
    """
    if os.path.exists(FILTERS_FILE):
        with open(FILTERS_FILE, "r") as f:
            filters = json.load(f)
            if campus:  # campus was selected
                filters["campus"] = campus
            elif interests:
                filters["interests"] = interests

    save_to_file(FILTERS_FILE, filters)
