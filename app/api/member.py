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



@bp.route('/member/groups', methods=['GET'])
@login_required
def get_groups(user_id):

    query = db.session.query(Group, Member).filter(Group.id == Member.group_id).filter(Member.user_id == user_id)

    for r in query:
        print(r[0].name)
        print(r[1].group_id)
        print(r[1].user_id)
    return "ok"