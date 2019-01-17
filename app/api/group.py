from app.api import bp
from flask import request, make_response, jsonify
from app.models import User, Group, Member
from app import db
from app.api.authorization import login_required

@bp.route('/group', methods=['POST'])
@login_required
def create_group(user_id):
    print(f"{user_id} making post request to /group")

    post_data = request.get_json()

    print(post_data['name'])

    group = Group(name = post_data['name'])
    # TODO: add the member in a transaction

    print(1)

    db.session.add(group)
    print(2)
    db.session.commit()
    print(3)

    group = group.query.filter_by(name = post_data['name']).first()

    print(4)

    member = Member(user_id, group.id, False)

    print(5)
    db.session.add(member)
    print(6)
    db.session.commit()

    return "group created"
