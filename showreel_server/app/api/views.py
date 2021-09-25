"""
Endpoints definition and routing
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('reels', __name__, url_prefix='/auth')

@bp.route("/test", methods=('GET', 'POST'))
def test():
    return "Hi"