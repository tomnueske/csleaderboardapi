"""parse leaderboard data"""
from typing import NamedTuple

import requests
from .leaderboarddata import ScoreLeaderboardData

__all__ = ( 'LeaderboardStats','LEADERBOARD_API_REGIONS')

CS2_LEADERBOARD_API = 'https://api.steampowered.com/ICSGOServers_730/GetLeaderboardEntries/v1/' \
                      '?lbname=official_leaderboard_premier_season1'

LEADERBOARD_API_REGIONS = ('northamerica', 'southamerica', 'europe', 'asia',
                           'australia', 'china', 'africa')

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0"}

MINUTE = 60
HOUR = 60 * MINUTE

SLD = ScoreLeaderboardData()
MAPS = {1: 'ancient',
        2: 'nuke',
        3: 'overpass',
        4: 'vertigo',
        5: 'mirage',
        6: 'inferno',
        7: 'anubis'}

REGIONS = {1: 'NA',
           2: 'SA',
           3: 'EU',
           4: 'AS',
           5: 'AU',
           7: 'AF',
           9: 'CH'}



class LeaderboardStats(NamedTuple):
    """leaderboarddata"""
    rank: int
    rating: int
    name: str
    wins: int
    ties: int
    losses: int
    last_wins: dict[str, int]
    timestamp: int
    region: str


    @classmethod
    def from_json(cls, data):
        """detaildata"""
        rank = data['rank']

        rating = data['score'] >> 15

        name = data['name']

        detail_data = data['detailData']
        detail_data = detail_data[2:].rstrip('0')
        detail_data = SLD.parse(bytes.fromhex(detail_data))

        wins = 0
        ties = 0
        losses = 0
        last_wins = {map_name: 0 for map_name in MAPS.values()}
        timestamp = 0
        region = 0

        for entry in detail_data.matchentries:
            if entry.tag == 16:
                wins = entry.val
            elif entry.tag == 17:
                ties = entry.val
            elif entry.tag == 18:
                losses = entry.val
            elif entry.tag == 19:
                for map_id, map_name in MAPS.items():
                    last_wins[map_name] = ((entry.val << (4 * map_id)) & 0xF0000000) >> 4*7
            elif entry.tag == 20:
                timestamp = entry.val
            elif entry.tag == 21:
                region = REGIONS.get(entry.val, 'unknown')



        return cls(rank, rating, name, wins, ties, losses, last_wins, timestamp, region)


    @staticmethod
    def request_world():
        """get world data"""
        world_leaderboard_data = requests.get(CS2_LEADERBOARD_API, headers=HEADERS, timeout=15).json()
        world_leaderboard_data = world_leaderboard_data['result']['entries']
        #world_leaderboard_data = world_leaderboard_data[:10]

        return [LeaderboardStats.from_json(person)._asdict() for person in world_leaderboard_data]

    @staticmethod
    def request_regional(region: str):
        """get region data"""
        api_link = CS2_LEADERBOARD_API + f'_{region}'
        regional_leaderboard_data = requests.get(api_link, headers=HEADERS, timeout=15).json()
        regional_leaderboard_data = regional_leaderboard_data['result']['entries']
        #regional_leaderboard_data = regional_leaderboard_data[:10]

        return [LeaderboardStats.from_json(person)._asdict() for person in regional_leaderboard_data]

    @staticmethod
    def request_player(name: str):
        """get player data"""
        world_leaderboard_data = requests.get(CS2_LEADERBOARD_API, headers=HEADERS, timeout=15).json()
        world_leaderboard_data = world_leaderboard_data['result']['entries']

        for person in world_leaderboard_data :
        
            if name in person.values() :
                player_data = person
                return [LeaderboardStats.from_json(player_data)._asdict()]
        
        return ["Player not found"]

     
