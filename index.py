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
    #print(world_leaderboard_stats)

@app.route('/api/player', methods=['GET'])
def get_player():
    """"get single player"""
    name=request.args.get("name")
    world_leaderboard_stats = LeaderboardStats.request_world()
    for person in world_leaderboard_stats :
        if name in person.values():
            #print(person)
            return(person)



if __name__ == '__main__':
    app.run(debug=True)
