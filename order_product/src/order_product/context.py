from datetime import date


class OrdersPath(str):
    """
    Marker class for the orders path context.
    """


class CustomersPath(str):
    """
    Marker class for the customers path context.
    """


class OutputPath(str):
    """
    Marker class for the output path context.
    """


class RunDate(date):
    """
    Marker class for the run date context.
    """
