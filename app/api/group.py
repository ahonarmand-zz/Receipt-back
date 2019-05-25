from app.api import bp
from flask import request, make_response, jsonify
from app.models import User, Group, Member
from app import db
from app.api.authorization import login_required
from flask_cors import cross_origin

@bp.route('/group', methods=['POST'])
@login_required
def create_group(user_id):
    print(f"{user_id} making post request to /group")

    post_data = request.get_json()

    group_name = post_data['group_name']

    print(group_name)

    
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
