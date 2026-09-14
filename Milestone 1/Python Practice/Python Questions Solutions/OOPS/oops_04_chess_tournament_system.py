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
