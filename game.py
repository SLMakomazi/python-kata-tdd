def decide(player, opponent):
    
    winning_moves = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }
    
    
    if player == opponent:
        return "Tie"
    
    if winning_moves[player] == opponent:
        return "Player Wins"
    
    return "Player Loses"