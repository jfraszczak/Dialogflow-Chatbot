import mysql.connector


class DataBaseHandler:
    def __init__(self):
        self.db = mysql.connector.connect(
          host="jfraszczak.mysql.pythonanywhere-services.com",
          user="jfraszczak",
          password="Bazka123",
          database="jfraszczak$SDS_Database"
        )

        self.cursor = self.db.cursor()

    def executeSelect(self, sql, val=None):
        if val is not None:
            self.cursor.execute(sql, val)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def commit(self, sql, val=None):
        if val is not None:
            self.cursor.execute(sql, val)
        else:
            self.cursor.execute(sql)
        self.db.commit()

    def getDialogStage(self):
        sql = "SELECT dialog_stage FROM DialogState WHERE id = 1"
        return self.executeSelect(sql)[0][0]

    def getCity(self):
        sql = "SELECT city FROM DialogState WHERE id = 1"
        return self.executeSelect(sql)[0][0]

    def getEvent(self):
        sql = "SELECT event FROM DialogState WHERE id = 1"
        return self.executeSelect(sql)[0][0]

    def getShow(self):
        sql = "SELECT show_name FROM DialogState WHERE id = 1"
        return self.executeSelect(sql)[0][0]

    def getDate(self):
        sql = "SELECT date_time FROM DialogState WHERE id = 1"
        return self.executeSelect(sql)[0][0]

    def getNumberOfTickets(self):
        sql = "SELECT number_of_tickets FROM DialogState WHERE id = 1"
        return self.executeSelect(sql)[0][0]

    def eventAvailable(self):
        city = self.getCity()
        event = self.getEvent()
        sql = "SELECT * FROM Events WHERE city = %s AND event = %s"
        val = (city, event)
        return len(self.executeSelect(sql, val)) > 0

    def getAvailableEvents(self):
        city = self.getCity()
        event = self.getEvent()
        sql = "SELECT shows, dates FROM Events WHERE city = %s AND event = %s"
        val = (city, event)
        return self.executeSelect(sql, val)

    def getAvailableCities(self):
        event = self.getEvent()
        sql = "SELECT DISTINCT city FROM Events WHERE event = %s"
        val = (event, )
        return self.executeSelect(sql, val)

    def showAvailable(self):
        city = self.getCity()
        event = self.getEvent()
        show = self.getShow()
        sql = "SELECT * FROM Events WHERE city = %s AND event = %s and shows = %s"
        val = (city, event, show)
        return len(self.executeSelect(sql, val)) > 0

    def getAvailableShows(self):
        city = self.getCity()
        event = self.getEvent()
        sql = "SELECT DISTINCT shows FROM Events WHERE city = %s AND event = %s"
        val = (city, event)
        return self.executeSelect(sql, val)

    def getAvailableDates(self):
        city = self.getCity()
        event = self.getEvent()
        show = self.getShow()
        sql = "SELECT dates FROM Events WHERE city = %s AND event = %s and shows = %s"
        val = (city, event, show)
        return self.executeSelect(sql, val)

    def dateAvailable(self):
        city = self.getCity()
        event = self.getEvent()
        show = self.getShow()
        date = self.getDate()
        sql = "SELECT * FROM Events WHERE city = %s AND event = %s and shows = %s and dates = %s"
        val = (city, event, show, date)
        return len(self.executeSelect(sql, val)) > 0

    def updateCity(self, city):
        sql = "UPDATE DialogState SET city = %s WHERE id = 1"
        val = (city,)
        self.commit(sql, val)

    def updateEvent(self, event):
        sql = "UPDATE DialogState SET event = %s WHERE id = 1"
        val = (event,)
        self.commit(sql, val)

    def updateShow(self, show):
        sql = "UPDATE DialogState SET show_name = %s WHERE id = 1"
        val = (show,)
        self.commit(sql, val)

    def updateDate(self, date):
        sql = "UPDATE DialogState SET date_time = %s WHERE id = 1"
        val = (date,)
        self.commit(sql, val)

    def updateNumberOfTickets(self, number_of_tickets):
        sql = "UPDATE DialogState SET number_of_tickets = %s WHERE id = 1"
        val = (number_of_tickets,)
        self.commit(sql, val)

    def incrementDialogStage(self):
        stage = self.getDialogStage()
        stage += 1
        sql = "UPDATE DialogState SET dialog_stage = %s WHERE id = 1"
        val = (stage,)
        self.commit(sql, val)

    def updateDialogStage(self, stage):
        sql = "UPDATE DialogState SET dialog_stage = %s WHERE id = 1"
        val = (stage,)
        self.commit(sql, val)

    def reset(self):
        sql = "UPDATE DialogState SET " \
              "city = %s, " \
              "event = %s, " \
              "show_name = %s, " \
              "date_time = %s, " \
              "number_of_tickets = %s, " \
              "dialog_stage = %s WHERE id = 1"
        val = (None, None, None, None, None, 0)
        self.commit(sql, val)