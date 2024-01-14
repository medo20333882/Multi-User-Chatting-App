import unittest
from unittest.mock import MagicMock, patch
from db import DB
from roomdb import ChatroomsDB

class TestDB(unittest.TestCase):

    def setUp(self):
        self.db = DB()

    @patch('db.DB.is_account_exist')
    def test_is_account_exist(self, mock_is_account_exist):
        mock_is_account_exist.return_value = True
        self.assertTrue(self.db.is_account_exist('existing_user'))

    @patch('db.DB.register')
    def test_register_user(self, mock_register):
        self.db.register('new_user', 'password123')
        mock_register.assert_called_with('new_user', 'password123')

    @patch('db.DB.user_login')
    @patch('db.DB.user_logout')
    def test_user_login_logout(self, mock_user_logout, mock_user_login):
        self.db.user_login('test_user', '127.0.0.1', '8000', '8001')
        self.db.user_logout('test_user')

        mock_user_login.assert_called_with('test_user', '127.0.0.1', '8000', '8001')
        mock_user_logout.assert_called_with('test_user')

    @patch('db.DB.get_online_users')
    def test_get_online_users(self, mock_get_online_users):
        expected_users = ['user1', 'user2']
        mock_get_online_users.return_value = expected_users

        users = self.db.get_online_users()
        self.assertEqual(users, expected_users)

class TestChatroomsDB(unittest.TestCase):

    def setUp(self):
        self.chatrooms_db = ChatroomsDB()

    @patch('roomdb.ChatroomsDB.create_room')
    def test_create_room(self, mock_create_room):
        mock_create_room.return_value = None
        self.assertIsNone(self.chatrooms_db.create_room('Test Room'))

    @patch('roomdb.ChatroomsDB.join_room')
    @patch('roomdb.ChatroomsDB.user_leave_room')
    def test_join_and_leave_room(self, mock_user_leave_room, mock_join_room):
        self.chatrooms_db.join_room(1, 'test_user')
        self.chatrooms_db.user_leave_room(1, 'test_user')

        mock_join_room.assert_called_with(1, 'test_user')
        mock_user_leave_room.assert_called_with(1, 'test_user')

    @patch('roomdb.ChatroomsDB.get_users_in_room')
    def test_get_users_in_room(self, mock_get_users_in_room):
        expected_users = ['user1', 'user2']
        mock_get_users_in_room.return_value = expected_users

        users = self.chatrooms_db.get_users_in_room(1)
        self.assertEqual(users, expected_users)

    @patch('roomdb.ChatroomsDB.get_available_rooms')
    def test_get_available_rooms(self, mock_get_available_rooms):
        expected_rooms = [{'Room_id': 1, 'Room_Name': 'Test Room'}]
        mock_get_available_rooms.return_value = expected_rooms

        rooms = self.chatrooms_db.get_available_rooms()
        self.assertEqual(rooms, expected_rooms)

# Add more test classes for PeerServer, PeerClient, ClientThread, UDPServer as needed

if __name__ == '__main__':
    unittest.main()
