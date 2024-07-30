from ticket import Ticket


class Basket:
    def __init__(self):
        self.__tickets = []
        self.__mode = "0"

    def add_ticket(self, ticket: Ticket):
        if Basket.__checking_type(ticket):
            if ticket not in self.__tickets:
                self.__tickets.append(ticket)
            else:
                print("Pozycja którą próbujesz dodać znajduje się już w koszyku!")

    def remove_ticket(self, index: int):
        if self.len_tickets:
            if index <= len(self.__tickets):
                self.__tickets.pop(index - 1)
                print(f"Usunięto z koszyka pozycję nr {index}")
            else:
                raise IndexError("Indeks przekracza zakres listy!")
        else:
            print("Koszyk jest pusty!")

    def go_to_payment(self):
        print("Podsumowanie zamówienia")
        print(self.__str__())
        receivable = 0.0
        for ticket in self.__tickets:
            receivable += ticket.price
        print(f"Należność {receivable:.2f}")

    @staticmethod
    def __checking_type(ticket: Ticket) -> bool | TypeError:
        if isinstance(ticket, Ticket):
            return True
        else:
            return TypeError("Parametr nie jest typu Ticket!")

    @property
    def mode(self) -> str:
        return self.__mode

    @mode.setter
    def mode(self, value: str):
        self.__mode = value

    @property
    def len_tickets(self) -> int:
        return len(self.__tickets)

    def __str__(self):
        if self.__tickets:
            counter = 1
            repr_obj_str = ""
            for ticket in self.__tickets:
                repr_obj_str += f"{counter}: {str(ticket)}"
                counter += 1
            return repr_obj_str
        else:
            return "Twój koszyk jest pusty!"
