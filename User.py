import csv

class Usermanager:
    """
    Manages user accounts by loading, appending  and overwriting a CSV file.
    """
    import User

    def __init__(self):
        """
        Initialize the Usermanager with an empty dictionary.
        """
        self.accounts = {} # creates a blank dictionary of our users

    def load_users(self):
        """
        this function reads CSV file to get user information and save it to a dict
        and then sets the key = to the first and last name
        :return: dict of users with names as keys
        """
        with open('User Information.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)  # skip first row

            for row in reader:
                first_name = row[0].strip()
                last_name = row[1].strip()
                pin = row[2].strip()
                amount = row[3].strip() if len(row) > 3 else 500

                user = User(first_name, last_name, pin, amount)
                new_key =  user.get_name()
                account_info = {new_key : user}
                self.accounts.update(account_info)
        return self.accounts

    def new_user(self, user : User) -> bool:
        """
        Adds a new user to the system if they don't already exist.

        :param user: User object to add
        :return: True if added successfully, False if duplicate
        """
        key = user.get_name()
        if key in self.accounts:
            return False
        self.accounts[key] = user
        self.save_user(user)
        return True


    def save_user(self, user : User) -> None:
        """
        This function will append any new users to the CSV File.

        :param user: User object to add
        """
        with open('User Information.csv', 'a', newline='' ) as file:
            writer = csv.writer(file)
            first, last = user.get_name()
            writer.writerow([first, last, user.get_pin(), str(user.get_amount())])

    def save_all_users(self) -> None:
        """
        Rewrites the entire CSV with current account data.
        Use this to update (deposit/withdraw).
        """
        with open('User Information.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['First Name', 'Last Name', 'PIN', 'Amount'])  # header
            for user in self.accounts.values():
                first, last = user.get_name()
                writer.writerow([first, last, user.get_pin(), str(user.get_amount())])

class User:
    """
    This is the information of a single user.
    """
    def __init__(self, first_name: str, last_name: str, pin:str, amount:str = '500'):
        """
        Initialize a new user object and sets base amount to 500
        the minimum requirements to open a new account

        :param first_name: User's first name
        :param last_name: User's last name
        :param pin: User's PIN code
        :param amount: Starting balance (as a string, converted to int)
        """

        self.__first_name = first_name.strip().lower()
        self.__last_name = last_name.strip().lower()
        self.__pin = pin.strip()
        self.__amount = int(amount)


    def get_name(self) ->tuple[str,str]:
        """
        gets user first name and last name

        :return: Tuple of usernames
        """
        return self.__first_name,self.__last_name

    def get_pin(self) -> str:
        """
        gets user's pin

        :return: string of pin
        """
        return self.__pin

    def get_amount(self) -> int:
        """
        gets user's balance

        :return: int of balance
        """
        return self.__amount

    def deposit(self, amount: int) -> None :
        """
        Adds money to user's balance
        :param amount:  amount to deposit
        """
        if amount > 0:
            self.__amount += amount

    def withdraw(self, amount: int) -> bool:
        """
        subtracts money from the user's balance.

        :param amount: Amount to withdraw
        :return: True if successful, False if insufficient funds
        """
        if 0 < amount <= int(self.__amount):
            self.__amount -= amount
            return True
        return False
