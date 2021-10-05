from flask import render_template
from app import webapp


@webapp.route('/main', methods=['GET'])
# Display an HTML page with links
def main():
    return render_template("main.html")
