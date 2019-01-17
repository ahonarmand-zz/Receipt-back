from app.api import bp
from flask import request, make_response, jsonify
from app.models import User, Group, Member
from app import db
from app.api.authorization import login_required

@bp.route('/member', methods=['POST'])
@login_required
def add_member(user_id):
    print(f"\n{user_id} making post request to /member\n")

    post_data = request.get_json()

    new_member_email = post_data['new_member_email']
    group_name = post_data['group_name']

    print(new_member_email)
    print(group_name)

    group = Group.query.filter_by(name = group_name).first()
    new_member_user = User.query.filter_by(email=new_member_email).first()

    print("adding " + new_member_email)

    member = Member(new_member_user.id, group.id, True)

    print("adding to db")    
    db.session.add(member)
    db.session.commit()
    return "member created"
