from app.api import bp
from flask import request, make_response, jsonify
from app.models import User, Group, Member, Group_Expense, Member_Expense_Share
from app import db
from app.api.authorization import login_required
from flask_cors import cross_origin
from decimal import *



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

def ratios_are_valid(email_to_share):
    shares = email_to_share.values()
    print(sum(shares))
    if sum(shares) != 100:
        return False
    return True

@bp.route('/group_expense/<group_expense_id>/shares', methods=['POST'])
@login_required
def update_expense_ratios(user_id, group_expense_id):
    post_data = request.get_json()
    print(post_data)
    group_id = post_data["group_id"]
    email_to_share = { r["email"]: Decimal(r["share"]) for r in post_data["ratios"]}

    groupMember = db.session.query(Group, Member).filter(Member.group_id == Group.id).filter(Group.id == group_id).filter(Member.user_id == user_id).first()
    if not groupMember:
        return make_response("user is not part of group"), 403

    if not ratios_are_valid(email_to_share):
        return make_response("shares don't add up to one hundred"), 422

    users_in_group = db.session.query(User).filter(User.email.in_(email_to_share.keys()))

    for u in users_in_group:
        print(u.email)
        print(u.id)

        mem_share = db.session\
            .query(Member_Expense_Share)\
            .filter(Member_Expense_Share.user_id == u.id)\
            .filter(Member_Expense_Share.group_expense_id == group_expense_id).first()

        if mem_share:
            db.session\
                .query(Member_Expense_Share)\
                .filter(Member_Expense_Share.user_id == u.id)\
                .filter(Member_Expense_Share.group_expense_id == group_expense_id)\
                .update({"share": email_to_share[u.email] })

        else:
            db.session.add(Member_Expense_Share(
                user_id = u.id,
                group_expense_id = group_expense_id,
                share =  email_to_share[u.email]
            ))

    db.session.commit()
    return make_response(jsonify({"success": True, "message": "expense ratios updated"})), 200