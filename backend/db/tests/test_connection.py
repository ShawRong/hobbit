# Test code for KeyManager
import unittest
from unittest.mock import patch, MagicMock
from key_manager import KeyManager  # Assuming the class is in key_manager.py
from mongodb import create_collection

class TestKeyManager(unittest.TestCase):
    def setUp(self):
        self.api_url = "http://mockapi.com"
        self.mongo_uri = "mongodb://localhost:27017"
        self.db_name = "test_db"
        self.collection_name = "test_collection"
        create_collection("test_db", "test_collection")
        self.key_manager = KeyManager(self.api_url, self.mongo_uri, self.db_name, self.collection_name)

    def tearDown(self):
        self.key_manager.close()  # Ensure MongoClient is closed after tests

    @patch('key_manager.requests.get')
    def test_get_user_balance_success(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"balance": 10})
        balance = self.key_manager.get_user_balance("test_address")
        self.assertEqual(balance, 10)

    @patch('key_manager.requests.get')
    def test_get_user_balance_failure(self, mock_get):
        mock_get.return_value = MagicMock(status_code=500)
        with self.assertRaises(Exception) as context:
            self.key_manager.get_user_balance("test_address")
        self.assertTrue("failed to get balance" in str(context.exception))

    def test_activate_key_insufficient_balance(self):
        with self.assertRaises(ValueError) as context:
            self.key_manager.activate_key("test_address")
        self.assertTrue("insufficient tokens to activate key" in str(context.exception))

    @patch.object(KeyManager, 'get_user_balance', return_value=10)
    def test_activate_key_success(self, mock_balance):
        self.key_manager.activate_key("test_address")
        self.assertTrue(self.key_manager.is_key_active("test_address"))

    def test_deactivate_key(self):
        self.key_manager.user_keys["test_address"] = True
        self.key_manager.deactivate_key("test_address")
        self.assertFalse(self.key_manager.is_key_active("test_address"))

if __name__ == '__main__':
    #unittest.main()
    create_collection('hobbit', 'test') 