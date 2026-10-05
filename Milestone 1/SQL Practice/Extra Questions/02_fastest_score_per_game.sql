-- ==============================================================================
-- Question 2: Fastest Score per Game (Tables: Games, Players, Scores)
-- ==============================================================================
-- Problem Statement:
--   An online gaming platform maintains match performance data for multiple
--   games. Each game has multiple players participating, and each player's score
--   is stored in the Scores table.
--
-- Requirements:
--   Generate a report that, for every recorded score, shows:
--     - The game name
--     - The player name
--     - The score
--     - The rank of that performance within the game, based on score (highest = rank 1)
--   - Only include results where status = 'Recorded'.
--   - Use ROW_NUMBER (not RANK), so that even if two players have the same score
--     in the same game, they still get different ranks.
--   - Apply ROW_NUMBER() ordered by score DESC and player_name ASC to break
--     ties consistently.
--
-- Required Output Columns:
--   game_name, player_name, score, rank_in_game
-- ==============================================================================

USE GAMING_PLATFORM_DB;

SELECT 
    g.game_name,
    p.player_name,
    s.score,
    ROW_NUMBER() OVER (
        PARTITION BY s.game_id 
        ORDER BY s.score DESC, p.player_name ASC
    ) AS rank_in_game
FROM Scores s
JOIN Games g 
    ON s.game_id = g.game_id
JOIN Players p 
    ON s.player_id = p.player_id
WHERE s.status = 'Recorded'
ORDER BY 
    g.game_name ASC, 
    rank_in_game ASC;
