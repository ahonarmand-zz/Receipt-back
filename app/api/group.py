from app.api import bp
from flask import request, make_response, jsonify
from app.models import User, Group, Member, Group_Expense
from app import db
from app.api.authorization import login_required

@bp.route('/group', methods=['POST'])
@login_required
def create_group(user_id):
    print(f"{user_id} making post request to /group")

    post_data = request.get_json()

    group_name = post_data['group_name']

    print(group_name)

    #TODO: there is no need for group to have unique name
    group = Group.query.filter_by(name = group_name).first()
    if group:
        return make_response(jsonify({"success": False, "message": "group already exists. Try a different name"})), 409


    # TODO: add the member in a transaction
    group = Group(name = group_name)
    db.session.add(group)
    db.session.commit()

    group = group.query.filter_by(name = group_name).first()

    member = Member(user_id, group.id, False)

    db.session.add(member)
    db.session.commit()

    return make_response(jsonify({"success": True, "message": "group created successfully"})), 200


@bp.route('/group/<group_id>/members', methods=['GET'])
@login_required
def get_members(user_id, group_id):
    print(f'user_id: {user_id}')
    print(f'group_id: {group_id}')
    query = \
        db.session.query(Group, Member, User) \
        .filter(Group.id == Member.group_id) \
        .filter(Group.id == group_id) \
        .filter(Member.user_id == User.id)

    response = [{"id": q[2].id, "name": q[2].name, "email": q[2].email} for q in query]

    return make_response(jsonify(response)), 200

@bp.route('/group/<group_id>/expenses', methods=['GET'])
@login_required
def get_expenses(user_id, group_id):
    results = db.session.query(Group, Group_Expense).filter(Group.id == Group_Expense.group_id).filter(Group.id == group_id).all()

    response = [r[1].serialize for r in results]
    print(response)
    return make_response(jsonify(response)), 200