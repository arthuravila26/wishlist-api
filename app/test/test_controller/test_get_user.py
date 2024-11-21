from unittest import TestCase
from unittest.mock import ANY, MagicMock, patch

from app.controllers.users_controller import (
    get_user_by_email,
    get_user_by_id,
    get_users,
)
from app.models import User
from app.utils.exceptions import UserNotFound


class TestUserFunctions(TestCase):
    @patch("app.controllers.users_controller.Session")
    def test_get_users(self, mock_session):
        mock_query = mock_session.return_value.query.return_value
        mock_query.all.return_value = [
            MockUser(id=1, name="User 1", email="user1@example.com"),
            MockUser(id=2, name="User 2", email="user2@example.com"),
        ]

        users = get_users(session=mock_session.return_value)

        mock_session.return_value.query.assert_called_once_with(User)
        mock_query.all.assert_called_once()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].name, "User 1")
        self.assertEqual(users[1].email, "user2@example.com")

    @patch("app.controllers.users_controller.Session")
    def test_get_user_by_id(self, mock_session):
        mock_user = MagicMock(spec=User)
        mock_user.name = "Test User"

        mock_session.return_value.query.return_value.filter.return_value.first.return_value = (
            mock_user
        )
        user = get_user_by_id(session=mock_session.return_value, user_id=1)

        self.assertEqual(user.name, "Test User")

    @patch("app.controllers.users_controller.Session")
    def test_get_user_by_id_not_found(self, mock_session):
        mock_session.return_value.query.return_value.filter.return_value.first.return_value = (
            None
        )

        with self.assertRaises(UserNotFound):
            get_user_by_id(session=mock_session.return_value, user_id=999)

    @patch("app.controllers.users_controller.Session")
    def test_get_user_by_email(self, mock_session):
        mock_query = mock_session.return_value.query.return_value
        mock_query.filter.return_value.first.return_value = MagicMock(
            id=1, name="Test User", email="test@example.com"
        )
        user = get_user_by_email(
            session=mock_session.return_value, email="test@example.com"
        )

        mock_session.return_value.query.assert_called_once_with(User)
        mock_query.filter.assert_called_once_with(ANY)
        mock_query.filter.return_value.first.assert_called_once()
        self.assertEqual(user.email, "test@example.com")

    @patch("app.controllers.users_controller.Session")
    def test_get_user_by_email_not_found(self, mock_session):
        mock_query = mock_session.return_value.query.return_value
        mock_query.filter.return_value.first.return_value = None

        user = get_user_by_email(
            session=mock_session.return_value, email="notfound@example.com"
        )

        self.assertIsNone(user)
        mock_query.filter.assert_called_once_with(ANY)
        mock_query.filter.return_value.first.assert_called_once()


class MockUser:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
