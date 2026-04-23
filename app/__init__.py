from flask import Flask
from app.models import db
import os

def create_app(config=None):
    app = Flask(__name__)
    
    # 載入基本設定
    app.config['SECRET_KEY'] = 'dev_secret_key_mock'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化擴充套件
    db.init_app(app)
    
    # 為了能跑 analysis，暫時加入簡單的登入模擬或先初始化 LoginManager (需要之後在 auth 模組中完成 user_loader)
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # 註冊藍圖
    from app.routes.analysis import analysis_bp
    app.register_blueprint(analysis_bp, url_prefix='/analysis')

    # 基本路由，確認狀態
    @app.route('/health')
    def health():
        return "OK"
    
    # 建立 db tables
    with app.app_context():
        # 建立 instance 目錄
        os.makedirs(app.instance_path, exist_ok=True)
        db.create_all()
        
    return app
