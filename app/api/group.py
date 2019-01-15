from app.api import bp
from flask import request, make_response, jsonify
from app.models import User, Group
from app import db
from app.api.authorization import login_required

@bp.route('/group', methods=['POST'])
@login_required
def create_group(user_id):
    print(f"{user_id} making post request to /group")

    post_data = request.get_json()

    print(post_data['name'])

    group = Group(name = post_data['name'])
    
    db.session.add(group)
    db.session.commit()

