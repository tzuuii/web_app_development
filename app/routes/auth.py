from flask import Blueprint, render_template, request, redirect, url_prefix, flash
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: 渲染註冊表單
    POST: 接收表單資料，檢驗重複信箱並建立新 User，若成功則導向至登入頁
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 渲染登入表單
    POST: 驗證帳密，呼叫 User.get_by_email 與 check_password，成功則 login_user() 帶往 dashbaord
    """
    pass

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """
    清空 session，登出使用者並重導向至系統首頁
    """
    pass
