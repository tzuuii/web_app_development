from flask import Blueprint, render_template
from flask_login import login_required, current_user

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/')
@login_required
def index():
    """
    GET:
      - 自動將用戶過去的所有 Answer 撈出
      - 使用 utils/analysis_helper 分配知識點，統整優勢及弱項列表
      - 於畫面端提供雷達圖或條狀統計
      - 同時附上複習方向之連結推薦
    """
    pass
