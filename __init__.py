import os

from flask import Flask, abort, jsonify, redirect, render_template, url_for

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', default='dev'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from .models import db, Ticket
    db.init_app(app)

    from sqlalchemy.orm import exc

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404


    @app.route('/')
    def index():
        return redirect(url_for('tickets'))


    @app.route('/tickets')
    def tickets():
        tickets = Ticket.query.all()
        return render_template('tickets_index.html', tickets=tickets)


    @app.route('/tickets/<int:ticket_id>')
    def tickets_show(ticket_id):
        try:
            ticket = Ticket.query.filter_by(id=ticket_id).one()
            return render_template('tickets_show.html', ticket=ticket)
        except exc.NoResultFound:
            abort(404)


    @app.route('/api/tickets')
    def api_tickets():
        tickets = [ticket.to_json() for ticket in Ticket.query.all()]
        return jsonify(tickets)


    @app.route('/api/tickets/<int:ticket_id>')
    def api_tickets_show(ticket_id):
        try:
            result = Ticket.query.filter_by(id=ticket_id).one().to_json()
            status = 200
        except exc.NoResultFound:
            result = {'error': 'Ticket not found'}
            status = 404

        return jsonify(result), status


    return app

