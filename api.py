from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = '../Impostor/src/Impostor.Server/gamestats.db'

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv
## ig redundant
@app.route('/gamestats', methods=['GET'])
def get_gamestats():
    gamestats = query_db('SELECT * FROM GameStats')
    result = []
    for gs in gamestats:
        players = query_db('SELECT * FROM PlayerStats WHERE GameCode = ?', [gs['GameCode']])
        result.append({
            'GameCode': gs['GameCode'],
            'EmergencyMeetingsCalled': gs['EmergencyMeetingsCalled'],
            'ReportedBodyMeetingsCalled': gs['ReportedBodyMeetingsCalled'],
            'AlivePlayers': gs['AlivePlayers'],
            'KilledPlayers': gs['KilledPlayers'],
            'GameOverReason': gs['GameOverReason'],
            'Players': [{'PlayerName': p['PlayerName'], 'VentsEntered': p['VentsEntered'], 'TasksCompleted': p['TasksCompleted'], 'Kills': p['Kills'], 'IsAlive': p['IsAlive']} for p in players]
        })
    return jsonify(result)

@app.route('/playerstats', methods=['GET'])
def get_playerstats():
    playerstats = query_db('SELECT * FROM PlayerStats')
    result = []
    for ps in playerstats:
        result.append({
            'PlayerName': ps['PlayerName'],
            'VentsEntered': ps['VentsEntered'],
            'TasksCompleted': ps['TasksCompleted'],
            'Kills': ps['Kills'],
            'IsAlive': ps['IsAlive'],
            'GameCode': ps['GameCode']
        })
    return jsonify(result)
##redundant
@app.route('/playerstatus', methods=['GET'])
def get_playerstatus():
    playerstatus = query_db('SELECT * FROM PlayerStatuses')
    result = []
    for ps in playerstatus:
        result.append({
            'PlayerName': ps['PlayerName'],
            'IsActive': ps['IsActive']
        })
    return jsonify(result)

@app.route('/activeplayers', methods=['GET'])
def get_active_players():
    active_players = query_db('SELECT * FROM PlayerStatuses WHERE IsActive = 1')
    result = [{'PlayerName': ap['PlayerName'], 'IsActive': ap['IsActive']} for ap in active_players]
    return jsonify(result)

@app.route('/gamestats/<game_code>', methods=['GET'])
def get_game_by_code(game_code):
    gs = query_db('SELECT * FROM GameStats WHERE GameCode = ?', [game_code], one=True)
    if gs:
        players = query_db('SELECT * FROM PlayerStats WHERE GameCode = ?', [gs['GameCode']])
        result = {
            'GameCode': gs['GameCode'],
            'EmergencyMeetingsCalled': gs['EmergencyMeetingsCalled'],
            'ReportedBodyMeetingsCalled': gs['ReportedBodyMeetingsCalled'],
            'AlivePlayers': gs['AlivePlayers'],
            'KilledPlayers': gs['KilledPlayers'],
            'GameOverReason': gs['GameOverReason'],
            'Players': [{'PlayerName': p['PlayerName'], 'VentsEntered': p['VentsEntered'], 'TasksCompleted': p['TasksCompleted'], 'Kills': p['Kills'], 'IsAlive': p['IsAlive']} for p in players]
        }
        return jsonify(result)
    else:
        return jsonify({"error": "Game not found"}), 404    
    
@app.route('/playerstats/<player_name>', methods=['GET'])
def get_player_by_name(player_name):
    ps = query_db('SELECT * FROM PlayerStats WHERE PlayerName = ?', [player_name], one=True)
    if ps:
        result = {
            'PlayerName': ps['PlayerName'],
            'VentsEntered': ps['VentsEntered'],
            'TasksCompleted': ps['TasksCompleted'],
            'Kills': ps['Kills'],
            'IsAlive': ps['IsAlive'],
            'GameCode': ps['GameCode']
        }
        return jsonify(result)
    else:
        return jsonify({"error": "Player not found"}), 404    

if __name__ == '__main__':
    app.run(debug=True)
