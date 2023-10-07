"""Protobuf functions"""
from dataclasses import dataclass
from typing import List

import betterproto


@dataclass
class ScoreLeaderboardData(betterproto.Message):
    """full data"""
    quest_id: int = betterproto.uint64_field(1)
    score: int = betterproto.uint32_field(2)
    accountentries: List[
        "ScoreLeaderboardDataAccountEntries"
    ] = betterproto.message_field(3)
    matchentries: List["ScoreLeaderboardDataEntry"] = betterproto.message_field(5)
    leaderboard_name: str = betterproto.string_field(6)


@dataclass
class ScoreLeaderboardDataEntry(betterproto.Message):
    """data entry"""
    tag: int = betterproto.uint32_field(1)
    val: int = betterproto.uint32_field(2)


@dataclass
class ScoreLeaderboardDataAccountEntries(betterproto.Message):
    """account entry"""
    accountid: int = betterproto.uint32_field(1)
    entries: List["ScoreLeaderboardDataEntry"] = betterproto.message_field(2)
    