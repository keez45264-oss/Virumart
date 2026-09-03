"""
App factory for the Grocery Store Management System.
Creates and configures the Flask app.
"""
from flask import Flask, session


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change-this-in-production'
    app.config['DATABASE'] = 'database/grocery.db'

    # Register blueprints (route groups) here as they're built
    from app.routes.customer import customer_bp
    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(customer_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp)

    @app.context_processor
    def inject_cart_count():
        cart = session.get('cart', {})
        cart_count = sum(cart.values())
        return {'cart_count': cart_count}

    return app