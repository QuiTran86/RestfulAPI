from RestfulAPI.models.users import Users
from RestfulAPI.service.insfrastructure.user_repo import UsersPG


class AccountService:

    def __init__(self):
        self.user_pg = UsersPG()

    def store_account(self, account_username, account_email, password):
        account = Users(username=account_username, email=account_email)
        account.set_password(password)
        self.user_pg.store_account(account)

