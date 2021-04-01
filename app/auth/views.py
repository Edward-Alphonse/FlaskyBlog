from flask import render_template, redirect, request, url_for, flash, Response
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..email import send_email
# from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
#     PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
import json
from ..models import Authentication, User
import time
from ..network import ResponseModel

registerStatusMap = {
    0: "成功",
    1: "用户名或密码为空",
    2: "用户名已注册"
}

loginStatusMap = {
    0: "成功",
    1: "用户名为空",
    2: "密码为空",
    3: "用户名未注册",
    4: "用户名或密码错误",
}

changePassworStatusMap = {
    0: "成功",
    1: "用户名为空",
    2: "旧密码为空",
    3: "新密码为空",
    4: "与当前密码相同",
}


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    email = request.json["email"]
    password = request.json.get("password", "")

    if not email or len(email) == 0:
        result = ResponseModel(1, loginStatusMap[1])
        return Response(result.jsonSerialize(), mimetype='application/json')

    if len(password) == 0:
        result = ResponseModel(2, loginStatusMap[2])
        return Response(result.jsonSerialize(), mimetype='application/json')


    authentication = Authentication.query.filter_by(email=email).first()
    if not authentication:
        result = ResponseModel(3, loginStatusMap[3])
        return Response(result.jsonSerialize(), mimetype='application/json')

    if authentication.email != email or authentication.password != password:
        result = ResponseModel(4, loginStatusMap[4])
        return Response(result.jsonSerialize(), mimetype='application/json')

    result = ResponseModel(0, loginStatusMap[0])
    return Response(result.jsonSerialize(), mimetype='application/json')
    # if isFinded == 0:
    #     result = ResponseModel(1, registerStatusMap[1])
    #     return Response(result.jsonSerialize(), mimetype='application/json')

    # result = {
    #     "status": "success"
    # }
    # # 1. 生成uid
    # # 2. 写数据库
    # #     uid，email，password，createtime
    # print ("------login", result)
    # return Response(json.dumps(result), mimetype='application/json')


@auth.route('/logout', methods=['POST'])
# @login_required
def logout():
    result = ResponseModel(0, "成功")
    return Response(result.jsonSerialize(), mimetype='application/json')
    #
    # logout_user()
    # flash('You have been logged out.')
    # return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    email = request.json["email"]
    password = request.json.get("password", "")
    hasRegistered = Authentication.query.filter_by(email=email).count()
    print(hasRegistered)
    if not email or len(password) == 0:
        result = ResponseModel(1, registerStatusMap[1])
        print(result.jsonSerialize())
        response = Response(result.jsonSerialize(), mimetype='application/json')
        return response

    if hasRegistered != 0:
        result = ResponseModel(2, registerStatusMap[2])
        respose = Response(result.jsonSerialize(), mimetype='application/json')
        return respose


    #1.生成uid、创建时间,写入登录表
    #2. 生成默认用户信息
    id = 123
    createTime = int(round(time.time() * 1000))
    authentication = Authentication(id=id, email=email, password=password)
    authentication.createTime = createTime

    user = User()
    user.id = id

    db.session.add(authentication)
    db.session.add(user)
    db.session.commit()
    result = ResponseModel(0, registerStatusMap[0])
    response = Response(result.jsonSerialize(), mimetype='application/json')
    return response


    # res = User.query.filter_by(name='hzc').first
    # if res:
    #     jsonMap = {
    #         'status': 'fail'
    #     }
    #     response = Response(json.dumps(jsonMap), mimetype='application/json')
    #     return response
    #
    # user = User(id=123, name="hzc", avatar="", description="")

    # authentication = Authentication(id=user.id, email=request.json["email"], password=request.json["password"])
    # print(user)
    # print(authentication)
    # result = {
    #     'status': 'success'
    # }
    # db.session.add(user)
    # db.session.add(authentication)
    # db.session.commit()
    # response = Response(json.dumps(result),mimetype='application/json')
    # return response


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/change_password', methods=['GET', 'POST'])
# @login_required
def change_password():
    email = request.json["email"]
    oldPassword = request.json.get("old_password", "")
    newPassword = request.json.get("new_password", "")
    if not email or len(email) ==0:
        result = ResponseModel(1, changePassworStatusMap[1])
        return Response(result.jsonSerialize(), mimetype='application/json')

    if len(oldPassword) == 0:
        result = ResponseModel(2, changePassworStatusMap[2])
        return Response(result.jsonSerialize(), mimetype='application/json')

    if len(newPassword) == 0:
        result = ResponseModel(3, changePassworStatusMap[3])
        return Response(result.jsonSerialize(), mimetype='application/json')

    if newPassword == oldPassword:
        result = ResponseModel(4, changePassworStatusMap[4])
        return Response(result.jsonSerialize(), mimetype='application/json')

    authentication = Authentication.query.filter_by(email=email, password=oldPassword).first()
    authentication.password = newPassword
    db.session.commit()
    result = ResponseModel(0, changePassworStatusMap[0])
    return Response(result.jsonSerialize(), mimetype='application/json')
    # form = ChangePasswordForm()
    # if form.validate_on_submit():
    #     if current_user.verify_password(form.old_password.data):
    #         current_user.password = form.password.data
    #         db.session.add(current_user)
    #         db.session.commit()
    #         flash('Your password has been updated.')
    #         return redirect(url_for('main.index'))
    #     else:
    #         flash('Invalid password.')
    # return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token)
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
