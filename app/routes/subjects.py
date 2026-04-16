from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

subjects_bp = Blueprint('subjects', __name__)

@subjects_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """
    GET: 列出該使用者的所有科目
    POST: 建立新的學習科目，將表單的名稱、顏色存入 DB 後重新導向回科目列表
    """
    pass

@subjects_bp.route('/<int:subject_id>')
@login_required
def detail(subject_id):
    """
    GET: 顯示特定科目的詳細資訊，包含旗下全部筆記與各測驗紀錄
    - 需檢查該使用者是否擁有存取此科目的權限
    - 渲染 subjects/detail.html
    """
    pass
