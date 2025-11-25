from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskapp.auth import login_required
from flaskapp.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    messages = db.execute(
        'SELECT m.id, content, created, author_id, username'
        ' FROM message m JOIN user u ON m.author_id = u.id'
        ' ORDER BY created ASC'
    ).fetchall()
    return render_template('blog/index.html', messages=messages)

@bp.route('/send', methods=('POST',))
@login_required
def send_message():
    content = request.form.get('content', '').strip()
    
    if content:
        db = get_db()
        db.execute(
            'INSERT INTO message (content, author_id)'
            ' VALUES (?, ?)',
            (content, g.user['id'])
        )
        db.commit()
    
    return redirect(url_for('blog.index'))

def get_message(id, check_author=True):
    message = get_db().execute(
        'SELECT m.id, content, created, author_id, username'
        ' FROM message m JOIN user u ON m.author_id = u.id'
        ' WHERE m.id = ?',
        (id,)
    ).fetchone()

    if message is None:
        abort(404, f"Message id {id} doesn't exist.")

    if check_author and message['author_id'] != g.user['id']:
        abort(403)

    return message

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete_message(id):
    get_message(id)
    db = get_db()
    db.execute('DELETE FROM message WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))