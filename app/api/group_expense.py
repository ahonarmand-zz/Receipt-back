from app.api import bp
from flask import request, make_response, jsonify
from app.models import User, Group, Member, Group_Expense, Member_Expense_Share
from app import db
from app.api.authorization import login_required
from flask_cors import cross_origin



@bp.route('/group_expense', methods=['POST'])
@login_required
def create_expense(user_id):

    print("in group_expense")
    post_data = request.get_json()

    group_id = post_data["group_id"]
    expense_name = post_data["expense_name"]

    group = Group.query.filter_by(id = group_id).first()
    if not group:
        return jsonify({"success": False, "message": "group does not exist"}), 404
    x = Group_Expense(group_id = group_id, expense_name = expense_name)
    db.session.add(x)
    db.session.commit()

    return make_response(jsonify({"success": True, "message": "expense created successfully"})), 200



@bp.route('/group_expense/<group_expense_id>', methods=['GET'])
@login_required
def get_expense(user_id, group_expense_id):
    expsense = Group_Expense.query.filter_by(id = group_expense_id).first()

    return make_response(jsonify(expsense)), 200

    # group_id, expense_name, 

# @bp.route('/group_expense/<group_expense_id>/shares', methods=['POST'])
# @login_required
# def get_expense(user_id, group_expense_id):
#     group_id = post_data["group_id"]
#     expense_id = post_data["expense_id"]

#     groupMember = db.session.query(Group, Member).filter(Memeber.group_id == Group.id).filter(Group.id == group_id).filter(Member.user_id == user_id).first()
#     if not groupMember:
#         return make_response("user is not part of group"), 403

#     db.session \
#         .query(Group, Group_Expense, Member_Expense_Share) \
#         .filter(Group.id == group_id)\
#         .filter(Group.id == Group_Expense.group_id)\
#         .filter(Group_Expense.expense_id == Member_Expense_Share.group_expense_id)