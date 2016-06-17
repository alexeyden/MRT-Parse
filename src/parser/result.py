

class Discount:
    def __init__(self, company, sale_date_from, sale_date_to, flight_date_from, flight_date_to, prices):
        self.company = company
        self.sale_date_from = sale_date_from
        self.sale_date_to = sale_date_to
        self.flight_date_from = flight_date_from
        self.flight_date_to = flight_date_to
        self.prices = prices


class Price:
    def __init__(self, source, dest, price):
        self.source = source
        self.dest = dest
        self.price = price


class Status:
    OK = 0
    WARNING = 1
    ERROR = 2

    def __init__(self, status, message = None):
        self.status = status
        self.message = message
