import unittest
from src.database.database_manager import DatabaseManager

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(':memory:')
    
    def test_add_period(self):
        self.assertTrue(self.db.add_period('2024-01-01'))
        self.assertEqual(len(self.db.get_all_periods()), 1)
    
    def test_cycle_calculation(self):
        self.db.add_period('2024-01-01')
        self.db.add_period('2024-01-28')
        stats = self.db.get_cycle_stats()
        self.assertEqual(stats[0], 27)

if __name__ == '__main__':
    unittest.main()