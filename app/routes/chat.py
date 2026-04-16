from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/')
@login_required
def index():
    """
    GET: 開啟獨立對話框版面，加載過往的 ChatLog
    渲染 chat/index.html 
    """
    pass

@chat_bp.route('/ask', methods=['POST'])
@login_required
def ask():
    """
    POST (AJAX/Fetch 前端互動 API):
      - 接收帶有提問內容的 JSON Payload
      - 儲存 User 的歷史紀錄進資料庫
      - 交替給 ai_helper 尋求特定回答，並同時把回復也存為紀錄
      - 最後吐出包含 { "answer": "..." } 等結構的 JSON 體供頁面即時更新
    """
    pass
