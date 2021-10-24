from RestfulAPI.models.users import Users
from RestfulAPI.service.insfrastructure.user_repo import UsersPG


class AccountService:

    def __init__(self):
        self.user_pg = UsersPG()

    @staticmethod
    def is_valid_account(username, password):
        user = Users.query.filter_by(username=username).first_or_404()
        if user:
            if user.check_password(password):
                return user
        return

    @staticmethod
    def get_user(username):
        user = Users.query.filter_by(username=username).first_or_404()
        return user

    def store_account(self, account_username, account_email, password):
        account = Users(username=account_username, email=account_email)
        account.set_password(password)
        self.user_pg.store_account(account)
