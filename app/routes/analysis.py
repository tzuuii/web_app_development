from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
import json

from app.models.answer import Answer
from app.utils.analysis_helper import calculate_weakness

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/')
@login_required
def index():
    """
    GET:
      - 自動將用戶過去的所有 Answer 撈出
      - 使用 utils/analysis_helper 分配知識點，統整優勢及弱項列表
      - 於畫面端提供雷達圖或條狀統計的數據
      - 渲染 analysis/index.html
    """
    try:
        answers = Answer.get_all_by_user(current_user.id)
        
        # 使用 helper 計算弱點
        weakness_data = calculate_weakness(answers)
        
        # 將資料轉為 JSON 格式片段，以便前端繪製圖表使用
        chart_data_json = json.dumps([
            {
                'topic': item['topic'],
                'accuracy': item['accuracy_percent']
            } for item in weakness_data
        ])
        
        return render_template(
            'analysis/index.html',
            weakness_data=weakness_data,
            chart_data_json=chart_data_json,
            total_answers=len(answers)
        )
    except Exception as e:
        flash(f"載入分析資料時發生錯誤：{str(e)}", "danger")
        return render_template('analysis/index.html', weakness_data=[], chart_data_json="[]", total_answers=0)
