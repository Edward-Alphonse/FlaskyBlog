from . import profile
from flask import render_template, redirect, request, url_for, flash, Response
from flask_login import login_user, logout_user, login_required, \
    current_user
from ..models import User
from ..network import ResponseModel

profileStatusMap = {
    0: "success",
    1: "用户不存在"
}

@profile.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@profile.route('/main', methods = ['GET'])
def profile():
    uid = request.args.get("uid", "")
    user = User.query.filter_by(id = uid).first()
    if not user:
        result = ResponseModel(1, profileStatusMap[1])
        return Response(result.jsonSerialize(), mimetype='application/json')
    result = ResponseModel(0, profileStatusMap[0], {
        "uid": user.id,
        "name": "water",
        "description": "二次元，业余摄影，前端打杂人员，略微代码洁癖",
        "avatar": "---"
    })
    return Response(result.jsonSerialize(), mimetype='application/json')