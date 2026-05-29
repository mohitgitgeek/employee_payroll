"""Employee Payroll Management System.

Originally a console program that pickled `Account` objects to a flat file, this
is now a full Flask web app backed by a SQLite database (via SQLAlchemy) with an
ML-powered "Insights" page that flags anomalous salary records using an
IsolationForest model.
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'payroll_secret_key')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'payroll.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path.replace('\\', '/')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    accNo = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    des = db.Column(db.String(120))   # designation
    add = db.Column(db.String(200))   # address
    ba = db.Column(db.Integer, default=0)   # basic
    da = db.Column(db.Integer, default=0)   # dearness allowance
    ta = db.Column(db.Integer, default=0)   # travelling allowance
    hra = db.Column(db.Integer, default=0)  # house rent allowance
    pf = db.Column(db.Integer, default=0)   # provident fund
    esi = db.Column(db.Integer, default=0)  # employee state insurance

    # Derived salary figures (kept as properties so they stay consistent).
    @property
    def gs(self):
        return (self.ba or 0) + (self.da or 0) + (self.ta or 0) + (self.hra or 0)

    @property
    def gd(self):
        return (self.pf or 0) + (self.esi or 0)

    @property
    def ns(self):
        return self.gs - self.gd


with app.app_context():
    db.create_all()


def _form_int(field, default=0):
    try:
        return int(request.form.get(field, default))
    except (TypeError, ValueError):
        return default


@app.route('/')
def index():
    count = Account.query.count()
    return render_template('index.html', count=count)


@app.route('/accounts')
def list_accounts():
    accounts = Account.query.order_by(Account.accNo).all()
    return render_template('list_accounts.html', accounts=accounts)


@app.route('/add', methods=['GET', 'POST'])
def add_account():
    if request.method == 'POST':
        accNo = _form_int('accNo')
        if Account.query.filter_by(accNo=accNo).first():
            flash('Account number already exists!', 'danger')
            return redirect(url_for('add_account'))
        account = Account(
            accNo=accNo,
            name=request.form.get('name', '').strip(),
            des=request.form.get('des', '').strip(),
            add=request.form.get('add', '').strip(),
            ba=_form_int('ba'), da=_form_int('da'), ta=_form_int('ta'),
            hra=_form_int('hra'), pf=_form_int('pf'), esi=_form_int('esi'),
        )
        db.session.add(account)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('list_accounts'))
    return render_template('add_account.html')


@app.route('/modify/<int:accNo>', methods=['GET', 'POST'])
def modify_account(accNo):
    account = Account.query.filter_by(accNo=accNo).first()
    if not account:
        flash('Account not found.', 'danger')
        return redirect(url_for('list_accounts'))
    if request.method == 'POST':
        account.name = request.form.get('name', '').strip()
        account.des = request.form.get('des', '').strip()
        account.add = request.form.get('add', '').strip()
        account.ba = _form_int('ba'); account.da = _form_int('da')
        account.ta = _form_int('ta'); account.hra = _form_int('hra')
        account.pf = _form_int('pf'); account.esi = _form_int('esi')
        db.session.commit()
        flash('Account modified.', 'success')
        return redirect(url_for('list_accounts'))
    return render_template('modify_account.html', account=account)


@app.route('/delete/<int:accNo>', methods=['POST', 'GET'])
def delete_account(accNo):
    account = Account.query.filter_by(accNo=accNo).first()
    if account:
        db.session.delete(account)
        db.session.commit()
        flash(f'Account {accNo} deleted.', 'info')
    return redirect(url_for('list_accounts'))


@app.route('/insights')
def insights():
    """ML insights: flag salary records that look anomalous using IsolationForest."""
    accounts = Account.query.order_by(Account.accNo).all()
    anomalies, summary, model_used = [], {}, False

    if accounts:
        net_salaries = [a.ns for a in accounts]
        summary = {
            'total': len(accounts),
            'avg_net': round(sum(net_salaries) / len(net_salaries), 2),
            'max_net': max(net_salaries),
            'min_net': min(net_salaries),
        }

    # IsolationForest needs a few samples to be meaningful.
    if len(accounts) >= 5:
        try:
            import numpy as np
            from sklearn.ensemble import IsolationForest
            X = np.array([[a.ba, a.da, a.ta, a.hra, a.pf, a.esi, a.ns] for a in accounts])
            clf = IsolationForest(contamination=0.2, random_state=42)
            preds = clf.fit_predict(X)            # -1 = anomaly, 1 = normal
            scores = clf.score_samples(X)
            for acc, p, s in zip(accounts, preds, scores):
                if p == -1:
                    anomalies.append({'acc': acc, 'score': round(float(s), 3)})
            model_used = True
        except Exception as e:
            app.logger.warning('IsolationForest unavailable: %s', e)

    return render_template('insights.html', accounts=accounts, anomalies=anomalies,
                           summary=summary, model_used=model_used)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=True)
