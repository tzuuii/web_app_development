from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """
    GET: 展現上傳界面，允許用戶選擇科目及檔案格式
    POST: 
      - 接收並儲存 PDF/影像檔
      - 呼叫 utils 中 pdf_parser 擷取內文
      - 將內容傳遞給 ai_helper 產生摘要與重點條列
      - 將各種結果合併紀錄至 Note model 中
      - 成功後帶往詳細頁
    """
    pass

@notes_bp.route('/<int:note_id>', methods=['GET'])
@login_required
def detail(note_id):
    """
    GET: 呈現特定筆記的細節(原文、AI摘要、重點等)
    需要權限查核
    """
    pass

@notes_bp.route('/<int:note_id>/edit', methods=['GET'])
@login_required
def edit(note_id):
    """
    GET: 端出編輯界面讓用戶可針對 AI 生成之內容進行手工微調
    """
    pass

@notes_bp.route('/<int:note_id>/update', methods=['POST'])
@login_required
def update(note_id):
    """
    POST: 接收來自修改表單的內容，透過 ORM 回存變更
    """
    pass

@notes_bp.route('/<int:note_id>/delete', methods=['POST'])
@login_required
def delete(note_id):
    """
    POST: 移除選定筆記，結束後回歸至所屬科目畫面
    """
    pass
