import unittest
from game import decide


class TestRockPaperScissors(unittest.TestCase):
    
    def test_rock_tie(self):
        self.assertEqual(decide("rock", "rock"), "Tie")
        
    def test_paper_tie(self):
        self.assertEqual(decide("paper" , "paper"), "Tie")
        
    def test_scissors_tie(self):
            self.assertEqual(decide("scissors", "scissors"), "Tie")
            
    def test_rock_beats_scissors(self):
                self.assertEqual(decide("rock", "scissors"), "Player Wins")
                
    def test_paper_beats_rock(self):
        self.assertEqual(decide("paper", "rock"), "Player Wins")
                    
    def test_scissors_beats_paper(self):
        self.assertEqual(decide("scissors", "paper"), "Player Wins")
        
    def test_paper_loses_scissors(self):
        self.assertEqual(decide("paper", "scissors"), "Player Loses")
                    
    def test_rock_loses_paper(self):
        self.assertEqual(decide("rock", "paper"), "Player Loses")
                        
    def test_scissors_loses_rock(self):
        self.assertEqual(decide("scissors", "rock"), "Player Loses")
        
    