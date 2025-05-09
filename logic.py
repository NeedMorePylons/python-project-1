from PyQt6.QtWidgets import *
from gui import *
from User import  *



class Logic(QMainWindow, Ui_MainWindow):
    """
    Handles logic for ATM interface
    """
    def __init__(self):
        """
        Initialize the main window, set up UI elements,
        connect buttons to functions, and load existing users.
        """
        super().__init__()
        self.setupUi(self)

        self.button_login.clicked.connect(lambda : self.login())
        self.button_newuser.clicked.connect(lambda : self.add_user())
        self.button_amount_enter.clicked.connect(lambda : self.enter())
        self.button_exit.clicked.connect(lambda : self.close_window())

        self.manager = Usermanager()
        self.manager.load_users()

        self.post_login_elements(False)


    def post_login_elements(self, visible):
        """
        Show or hide UI elements that should only appear after login.

        Args: visible (bool): Whether the post-login widgets should be visible.
        """
        self.radioButton_withdraw.setVisible(visible)
        self.radioButton_deposit.setVisible(visible)
        self.label_5.setVisible(visible)
        self.button_amount_enter.setVisible(visible)
        self.label_acount_balance.setVisible(visible)
        self.entrybox_amount.setVisible(visible)
        self.label_acount_balance_error.setVisible(visible)


    def login(self):
        """
        This will check that the information is correct when
        someone tries to log in
        shows balance if successful or error if login fails

        """
        first_name = self.entrybox_user_firstname.text().strip().lower()
        last_name = self.entrybox_user_lastname.text().strip().lower()
        pin = self.entrybox_user_pin.text().strip().lower()

        key = (first_name, last_name) # Uses first and last names to verify pin
        accounts = self.manager.accounts

        if key in accounts and accounts[key].get_pin() == pin:
            self.current_user = accounts[key]
            self.label_acount_balance.setText(f"Balance: ${self.current_user.get_amount()}")
            self.lable_welcome_message_.setText("Welcome!")
            self.lable_login_error.setText("")
            self.post_login_elements(True)
        else:
            self.lable_login_error.setText("Invalid login. Please try again.")
            self.lable_welcome_message_.setText("")
            self.post_login_elements(False)



    def add_user(self):
        """
        Register a new user with a first name, last name, and PIN.
        Shows a success message if created, or an error if
        user already exists or fields are empty.
        """
        first_name = self.entrybox_user_firstname.text().strip().lower()
        last_name = self.entrybox_user_lastname.text().strip().lower()
        pin = self.entrybox_user_pin.text().strip().lower()

        if not (first_name and last_name and pin):
            self.lable_login_error.setText("All fields must be filled.")
            return

        new_user = User(first_name, last_name, pin)
        success = self.manager.new_user(new_user)

        if success:
            self.lable_welcome_message_.setText("User added successfully!")
            self.lable_login_error.setText("")
        else:
            self.lable_login_error.setText("User already exists.")


    def enter(self):
        """
        Handles deposits or withdrawals based on the radio button selected
        validates transaction and updates UI
        """
        transaction_amount_text = self.entrybox_amount.toPlainText().strip()
        if not transaction_amount_text.isdigit():
            self.label_acount_balance_error.setText("Please enter a valid number")
            return

        transaction_amount = int(transaction_amount_text)
        if self.radioButton_withdraw.isChecked():
            if transaction_amount >self.current_user.get_amount():
                self.label_acount_balance_error.setText("Insufficient funds")

            success = self.current_user.withdraw(transaction_amount)
            if success:
                self.manager.save_all_users()
                self.label_acount_balance.setText(f"Balance: ${self.current_user.get_amount()}")
                self.label_acount_balance_error.setText("Withdrawal successful.")
            else:
                self.label_acount_balance_error.setText("Insufficient funds")


        elif self.radioButton_deposit.isChecked():
            self.current_user.deposit(transaction_amount)
            self.manager.save_all_users()
            self.label_acount_balance.setText(f"Balance: ${self.current_user.get_amount()}")
            self.label_acount_balance_error.setText("Deposit successful.")


        else:
            self.label_acount_balance_error.setText("Select Deposit or Withdraw.")


        self.label_acount_balance.setText(f"Balance: ${self.current_user.get_amount()}")


    def close_window(self):
        """
        Close the application window.
        """
        self.close()