"""index"""

import json
from flask import Flask,request
from data import LeaderboardStats

app = Flask(__name__)

@app.route('/')
def main():
    """"main"""
    return 'This is my pointless new page'

@app.route('/api/leaderboard', methods=['GET'])
def fetch_leaderboard():
    """get leaderboard"""

    world_leaderboard_stats = json.dumps(LeaderboardStats.request_world())
    return(world_leaderboard_stats)

@app.route('/api/player', methods=['GET'])
def get_player():
    """"get single player"""
    name=request.args.get("name")
    player_stats = LeaderboardStats.request_player(name)
    return(player_stats)



if __name__ == '__main__':
    app.run(debug=True)
