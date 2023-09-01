import os

from flask import Blueprint, redirect, url_for, session, render_template
from backend.db_interface import load_quotes_for_email

# Configuration for Google OAuth
GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']  # Secret key for JWT

pages_handlers_bp = Blueprint('pages', __name__)


@pages_handlers_bp.route('/page_logout')
def page_logout():
    """Display the logout screen."""
    return render_template('page_logout.html')


@pages_handlers_bp.route('/page_homepage')
def page_homepage():
    if 'email' in session:
        return "Hi from homepage"
    else:
        return redirect(url_for('page_forbidden'))


@pages_handlers_bp.route('/page_handcrafting')
def page_create_quote():
    if 'email' in session:
        return render_template('page_handcrafting.html', email=session['email'],
                               active_menu='page_create_quote')
    else:
        return redirect(url_for('page_forbidden'))


@pages_handlers_bp.route('/page_gen_ai')
def page_gen_ai():
    if 'email' in session:
        return render_template('page_gen_ai.html', email=session['email'],
                               active_menu='page_gen_ai')
    else:
        return redirect(url_for('page_forbidden'))


@pages_handlers_bp.route('/page_my_quotes')
def page_my_quotes():
    print(session)
    if 'email' in session:
        user_quotes = load_quotes_for_email(session['email'])
        print("User quotes:", user_quotes)
        return render_template('page_my_quotes.html', email=session['email'], quotes=user_quotes,
                               active_menu='page_my_quotes')
    else:
        return redirect(url_for('page_forbidden'))


@pages_handlers_bp.route('/page_forbidden')
def page_forbidden():
    return render_template('forbidden_screen.html')
