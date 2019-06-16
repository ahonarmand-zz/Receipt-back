from app import app, db
from app.models import User, Debt, Group, Member, Group_Expense, Member_Expense_Share
# The from app import app statement imports the app variable that is a member of the app package. If you find this confusing, you can rename either the package or the variable to something else.

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Debt': Debt, 'Group': Group, 'Member': Member, 'Group_Expense': Group_Expense, 'Member_Expense_Share': Member_Expense_Share}