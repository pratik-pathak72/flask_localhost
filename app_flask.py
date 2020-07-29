from flask import Flask, Response, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import json
import os

file_path = os.path.abspath(os.getcwd())+r'\nba.db'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
db = SQLAlchemy(app)


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    points = db.Column(db.Integer)
    team_id = db.Column(db.String, db.ForeignKey('teams.id'))

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    state = db.Column(db.String)
    players = db.relationship('Player', backref='team')


def both_tables():
    player_team_all = db.session.query(Player).join(Team).all()
    data_all=[]
    final_data=[]
    for player_team in player_team_all:
        task_1={}
        data = {"id": player_team.id,
                        "name": player_team.name,
                        "points": player_team.points,
                        "team": player_team.team.name,
                        "team_id": player_team.team.id,
                        "state": player_team.team.state}
        data_all.append(data)
        result = json.dumps(data_all,indent=4, sort_keys=True)
        response = Response(result, content_type='application/json')
    return response

@app.route('/', methods=['GET'])
def nba_all_id():
    return both_tables()



@app.route('/player/<id_n>', methods=['GET'])
def nba_player_id(id_n):
    player_team_all = db.session.query(Player).join(Team).all()
    data_all=[]
    final_data=[]
    for player_team in player_team_all:
        if player_team.id == int(id_n):
            data = {"id": player_team.id,
                        "name": player_team.name,
                        "points": player_team.points,
                        "team": player_team.team.name,
                        "team_id": player_team.team.id,
                        "state": player_team.team.state}
            result = json.dumps(data,indent=4, sort_keys=True)
            result_lds = json.loads(result)
            return result_lds

@app.route('/team/<team_id>', methods=['GET'])
def nba_team_id(team_id):
    player_team_byteam_id = db.session.query(Player).join(Team).filter(Team.id==team_id).all()
    data_all=[]
    final_data=[]
    for player_state in player_team_byteam_id:
        if player_state.team.id == team_id:
            data = {"id": player_state.id,
                        "name": player_state.name,
                        "points": player_state.points,
                        "team": player_state.team.name,
                        "team_id": player_state.team.id,
                        "state": player_state.team.state}
            data_all.append(data)
            result = json.dumps(data_all,indent=4, sort_keys=True)
            response = Response(result, content_type='application/json')
    return response

@app.route('/state/<state_abbrev>', methods=['GET'])
def nba_state_id(state_abbrev):
    player_team_bystate = db.session.query(Player).join(Team).filter(Team.state==state_abbrev).all()
    data_all=[]
    final_data=[]
    for player_state in player_team_bystate:
        data = {"id": player_state.id,
                        "name": player_state.name,
                        "points": player_state.points,
                        "team": player_state.team.name,
                        "team_id": player_state.team.id,
                        "state": player_state.team.state}
        data_all.append(data)
        result = json.dumps(data_all,indent=4, sort_keys=True)
        response = Response(result, content_type='application/json')
    return response

if __name__ == "__main__":
    app.run(debug = True)
