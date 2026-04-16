from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    """
    GET: 提供表單讓使用者挑選欲做題的筆記、題數、及難度
    POST:
      - 向資料庫檢索所選筆記原文
      - 委由 AI 端 (ai_helper.generate_questions) 產生相應數量的考題
      - 將生成的題目建檔存回 Quiz 與 Question 資料表內
      - 測驗卷準備完畢後重導至 /quiz/<id> 開始挑戰
    """
    pass

@quiz_bp.route('/<int:quiz_id>', methods=['GET'])
@login_required
def take(quiz_id):
    """
    GET: 渲染答題介面，逐一列出現有題庫並搭配表單供送出
    需防範未授權或他人測卷的存取
    """
    pass

@quiz_bp.route('/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit(quiz_id):
    """
    POST: 
      - 取回用戶透過前端勾選出來的選項陣列
      - 將之與正確答案比對，生成對應之 Answer 操作存紀錄
      - 確認各題主題 (Topic) 並進行歸納或計算平均後寫入數據
      - 前往結果頁 /result
    """
    pass

@quiz_bp.route('/<int:quiz_id>/result', methods=['GET'])
@login_required
def result(quiz_id):
    """
    GET: 呈現此份測驗之對錯狀況、總分與 AI 詳細解說
    """
    pass
