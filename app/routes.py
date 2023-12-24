from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import CreateUserForm, CreateTeamForm
from app import db
from app import app
from app.models import User, Team, Squad, Game, SquadName

@app.route('/')
@app.route('/index')
@app.route('/standings')
def standings():
    # get users, teams, squads, squad names, and games
    users = User.query.all()
    teams = Team.query.all()
    squads = Squad.query.all()
    games = Game.query.all()
    squad_names = SquadName.query.all()

    # use the squad get record method to get the squad records for each user
    # the record should be by user, not id
    squad_records = {}
    for squad in squads:
        squad_records[squad.id] = squad.get_record()
    
    print(squads)

    return render_template('standings.html', title='Standings', 
        users=users, teams=teams, squads=squads, games=games, squad_names=squad_names,
        squad_records=squad_records)

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
    if request.method == 'POST':
        # Handle the AJAX POST request
        data = request.json
        squads = data['squads']

        for squad_data in squads:
            squad = Squad(
                user_id=squad_data['user_id'],
                team_id=squad_data['team_id']
            )
            db.session.add(squad)
        
        db.session.commit()
        return redirect(url_for('index'))

    else:
        # Handle the GET request as before
        users = User.query.all()
        teams = Team.query.all()
        return render_template('create_squad.html', title='Create Squad', teams=teams, users=users)
    