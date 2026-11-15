"""
Chess Tournament Player Management System

Class: ChessTournamentSystem

Problem Statement:
A chess academy wants to manage players participating in a tournament.
Each player has a unique Player ID, player name, rating, and participation status.

Storage Structure:
Dictionary mapping player_id -> {"name": str, "rating": int, "status": "Active"}
Example:
{
    "P101": {
        "name": "Arjun",
        "rating": 1850,
        "status": "Active"
    }
}

State Initialization:
def __init__(self):
    self.players = {}

Methods Required:
1. add_player(self, player_id: str, name: str, rating: int) -> dict
   If player_id already exists, raise ValueError("Player already exists").
   Otherwise add player with name, rating, and status="Active". Return updated dictionary.
2. update_rating(self, player_id: str, new_rating: int) -> dict
   If player_id does not exist, raise KeyError("Player not found").
   Otherwise update rating and return updated dictionary.
3. get_player_details(self, player_id: str) -> dict
   If player_id does not exist, raise KeyError("Player not found").
   Otherwise return player details dict.
4. qualified_players(self, minimum_rating: int) -> list
   Return list of player IDs where rating >= minimum_rating.
"""


class ChessTournamentSystem:
    def __init__(self):
        self.players = {}

    def add_player(self, player_id: str, name: str, rating: int) -> dict:
        if player_id in self.players:
            raise ValueError("Player already exists")
        self.players[player_id] = {
            "name": name,
            "rating": rating,
            "status": "Active"
        }
        return self.players

    def update_rating(self, player_id: str, new_rating: int) -> dict:
        if player_id not in self.players:
            raise KeyError("Player not found")
        self.players[player_id]["rating"] = new_rating
        return self.players

    def get_player_details(self, player_id: str) -> dict:
        if player_id not in self.players:
            raise KeyError("Player not found")
        return self.players[player_id]

    def qualified_players(self, minimum_rating: int) -> list:
        return [
            player_id
            for player_id, data in self.players.items()
            if data["rating"] >= minimum_rating
        ]


if __name__ == "__main__":
    chess = ChessTournamentSystem()
    print("Add P101:", chess.add_player("P101", "Arjun", 1850))
    print("Add P102:", chess.add_player("P102", "Priya", 1750))
    print("Add P103:", chess.add_player("P103", "Rohan", 1920))
    print("Update Rating P101:", chess.update_rating("P101", 1900))
    print("Get Details P101:", chess.get_player_details("P101"))
    print("Qualified (>=1800):", chess.qualified_players(1800))
