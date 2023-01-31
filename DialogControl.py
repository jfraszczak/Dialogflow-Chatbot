from DataBaseHandler import DataBaseHandler
from intents import intents

context_id = "projects/eventio-wrlo/agent/sessions/8585a0a9-7949-ea1b-a10d-74b6ef61d44b/contexts/__system_counters__"


class DialogControl:
    def __init__(self, request):
        self.db_handler = DataBaseHandler()

        self.intent = request.get('queryResult').get('intent').get('displayName')
        self.parameters = {}
        for context in request.get('queryResult').get('outputContexts'):
            if context['name'] == context_id:
                self.parameters = context.get('parameters')

        self.textResponse = ""

    def handleIncomingParameters(self):
        if 'geo-city' in self.parameters:
            city = self.parameters['geo-city']
            if city != "":
                self.db_handler.updateCity(city)
        if 'event' in self.parameters:
            event = self.parameters['event']
            if event != "":
                self.db_handler.updateEvent(event)
        if 'music-artist' in self.parameters:
            show = self.parameters['music-artist']
            if show != "":
                self.db_handler.updateShow(show)
        if 'date' in self.parameters:
            date = str(self.parameters['date'])[:10]
            if date != "":
                self.db_handler.updateDate(date)
        if 'number-integer' in self.parameters:
            number_of_tickets = int(self.parameters['number-integer'])
            if number_of_tickets != "":
                self.db_handler.updateNumberOfTickets(number_of_tickets)

    def handleChooseCityAndEvent(self):
        city = self.db_handler.getCity()
        event = self.db_handler.getEvent()

        if city is None and event is None:
            self.textResponse = "Please specify city and type of the event"
            return

        if event is None:
            self.textResponse = "Please specify type of the event"
            return

        if city is None:
            self.textResponse = "Please specify the city. Following locations are available:"
            cities = self.db_handler.getAvailableCities()
            for city in cities:
                self.textResponse += city[0] + ", "
            return

        if self.db_handler.eventAvailable():
            self.textResponse = "Following events are available: "
            events = self.db_handler.getAvailableEvents()
            for show, date in events:
                self.textResponse += show + ": " + date + ", "
            self.textResponse += "Which show are you interested in?"
            return
        self.textResponse = "Unfortunately there is no {} in {}. " \
                            "Maybe try with different city? Following locations are available:".\
                            format(self.db_handler.getEvent(), self.db_handler.getCity())
        cities = self.db_handler.getAvailableCities()
        for city in cities:
            self.textResponse += city[0] + ", "

    def handleChooseAvailableShow(self):
        show = self.db_handler.getShow()
        if show is None:
            self.textResponse = "Please specify show which you would like to attend."
            return

        if self.db_handler.showAvailable():
            self.textResponse = "Following dates are available for {}: ".format(show)
            dates = self.db_handler.getAvailableDates()
            for date in dates:
                self.textResponse += str(date[0]) + ", "
            return

        self.textResponse = "Unfortunately there is no such show available. " \
                            "Maybe try with different one? Following shows are available:"
        shows = self.db_handler.getAvailableShows()
        for show in shows:
            self.textResponse += show[0] + ", "

    def handleChooseDate(self):
        date = self.db_handler.getDate()
        if date is None:
            self.textResponse = "Please specify date of the show"
            return

        if self.db_handler.dateAvailable():
            self.textResponse = "Event has been selected. Please specify number of tickets."
            return

        self.textResponse = "Unfortunately there is no such date available " \
                            "Only following ones are available:"
        dates = self.db_handler.getAvailableDates()
        for date in dates:
            self.textResponse += str(date[0]) + ", "

    def handleChooseNumberOfTickets(self):
        number_of_tickets = self.db_handler.getNumberOfTickets()
        if number_of_tickets is None:
            self.textResponse = "Please specify desired number of tickets"
            return

        if number_of_tickets <= 0:
            self.textResponse = "Number of tickets must be greater than 0"
            return

        if number_of_tickets > 10:
            self.textResponse = "Number of tickets can't exceed 10"
            return

        event = self.db_handler.getEvent()
        city = self.db_handler.getCity()
        show = self.db_handler.getShow()
        date = self.db_handler.getDate()
        if event == "Concert":
            self.textResponse = "Thank you. This is the summary of your order: " \
                                "{} tickets for {} of {} in {} on {}".\
                                format(number_of_tickets, event, show, city, date)
        else:
            self.textResponse = "Thank you. This is the summary of your order: " \
                                "{} tickets for {} {} in {} on {}".\
                                format(number_of_tickets, event, show, city, date)

    def handleCancel(self):
        self.textResponse = "The order has been cancelled. " \
                            "In order to start a new one please say Hello."

    def handleStartAgain(self):
        self.textResponse = "The order has been restarted, " \
                            "please specify location and type of event you would like to attend."

    def getResponse(self):
        return {'fulfillmentText': self.textResponse}

    def handleRequest(self):

        # Error Handling
        if intents[self.intent] < self.db_handler.getDialogStage():
            if not intents[self.intent] == 0:
                self.textResponse = "You have already provided these data."
                return

        # Error Handling
        if intents[self.intent] > self.db_handler.getDialogStage():
            if not ((intents[self.intent] == 2 and self.db_handler.getDialogStage() == 1)
                    or (intents[self.intent] == 3 and self.db_handler.getDialogStage() == 2)
                    or (intents[self.intent] == 4 and self.db_handler.getDialogStage() == 3)
                    or intents[self.intent] == 5
                    or intents[self.intent] == 6):
                self.textResponse = "You still haven't provided all the required information."
                return

        self.handleIncomingParameters()

        # Welcome
        if intents[self.intent] == 0:
            if self.db_handler.getDialogStage() == 0:
                self.textResponse = "Welcome to Eventio, do you want to make a booking for an event? " \
                                    "You will have to choose the location, the type of event you want to " \
                                    "visit and lastly the time and date for your visit."
                self.db_handler.incrementDialogStage()
            else:
                self.textResponse = "Hello, but we have already greeted each other. " \
                                    "Shall we continue with the order?"
            return

        # Choose City and Event
        if intents[self.intent] == 1:
            if self.db_handler.getDialogStage() == 1:
                self.handleChooseCityAndEvent()
                return

        # Choose Available Show
        if intents[self.intent] == 2:
            if self.db_handler.getDialogStage() == 1:
                self.db_handler.incrementDialogStage()

            if self.db_handler.getDialogStage() == 2:
                self.handleChooseAvailableShow()
                return

        # Choose Date
        if intents[self.intent] == 3:
            if self.db_handler.getDialogStage() == 2:
                self.db_handler.incrementDialogStage()

            if self.db_handler.getDialogStage() == 3:
                self.handleChooseDate()
                return

        # Choose Number of Tickets
        if intents[self.intent] == 4:
            if self.db_handler.getDialogStage() == 3:
                self.db_handler.incrementDialogStage()

            if self.db_handler.getDialogStage() == 4:
                self.handleChooseNumberOfTickets()
                return

        # Cancel
        if intents[self.intent] == 5:
            self.db_handler.reset()
            self.handleCancel()
            return

        # Start Again
        if intents[self.intent] == 6:
            self.db_handler.reset()
            self.db_handler.incrementDialogStage()
            self.handleStartAgain()
            return
        
