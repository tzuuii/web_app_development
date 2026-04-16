from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    """
    GET: 學習儀表板首頁
    撈取統計數據：總筆記數量、累積測驗次數、總平均答對率等。
    亦可列出最新動作的回顧列表，並渲染 dashboard/index.html 主版面
    """
    pass
