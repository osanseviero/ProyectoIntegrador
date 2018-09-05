from flask import render_template
from main import app

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.register_error_handler(404, page_not_found)
