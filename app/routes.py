from flask import render_template, flash, redirect, url_for
from app.forms import CreateUserForm, CreateTeamForm
from app import db
from app import app
from app.models import User, Team, Squad, Game

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/create_user', methods=['GET', 'POST'])
def register():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you created a user!')
        return redirect(url_for('register'))
    return render_template('create_user.html', title='Create User', form=form)

@app.route('/create_team', methods=['GET', 'POST'])
def create_team():
    form = CreateTeamForm()
    if form.validate_on_submit():
        team = Team(name=form.name.data, abbreviation=form.abbreviation.data, logo_link=form.logo_link.data)
        db.session.add(team)
        db.session.commit()
        flash('Congratulations, you created a team!')
        return redirect(url_for('create_team'))
    return render_template('create_team.html', title='Create Team', form=form)

@app.route('/create_squad', methods=['GET', 'POST'])
def create_squad():
    # First get all the users
    users = User.query.all()
    # Get all the teams
    teams = Team.query.all()
    # Then pass the users to the template
    return render_template('create_squad.html', title='Create Squad', teams=teams, users=users)