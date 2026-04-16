from flask import Blueprint

def register_routes(app):
    """
    註冊所有的 Flask Blueprints 到主要的 app 實例中
    """
    from .auth import auth_bp
    from .dashboard import dashboard_bp
    from .subjects import subjects_bp
    from .notes import notes_bp
    from .quiz import quiz_bp
    from .analysis import analysis_bp
    from .chat import chat_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(subjects_bp, url_prefix='/subjects')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    app.register_blueprint(analysis_bp, url_prefix='/analysis')
    app.register_blueprint(chat_bp, url_prefix='/chat')
