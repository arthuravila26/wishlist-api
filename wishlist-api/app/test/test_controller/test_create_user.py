from unittest import TestCase
from unittest.mock import MagicMock, patch

from app.controllers.users_controller import create_user
from app.utils.exceptions import EmailAlreadyExists


class TestCreateUser(TestCase):
    @patch("app.controllers.users_controller.hash_password")
    @patch("app.controllers.users_controller.get_user_by_email")
    def test_create_user(self, mock_get_user_by_email, mock_hash_password):
        mock_get_user_by_email.return_value = None
        mock_hash_password.return_value = "password"

        create_user_data = MagicMock(
            name="Test User", email="test@test.com", password="123456"
        )
        session_mock = MagicMock()

        user = create_user(session=session_mock, create_user=create_user_data)

        mock_hash_password.assert_called_once_with(create_user_data.password)

        session_mock.add.assert_called_once()
        session_mock.commit.assert_called_once()
        session_mock.refresh.assert_called_once_with(user)

        self.assertEqual(user.name, create_user_data.name)
        self.assertEqual(user.email, create_user_data.email)
        self.assertEqual(user.password, "password")

    @patch("app.controllers.users_controller.get_user_by_email")
    def test_create_user_email_already_exists(self, mock_get_user_by_email):
        mock_session = MagicMock()
        mock_get_user_by_email.return_value = MagicMock()

        create_user_data = MagicMock()
        create_user_data.email = "test@test.com"

        with self.assertRaises(EmailAlreadyExists):
            create_user(mock_session, create_user_data)

        mock_get_user_by_email.assert_called_once_with(
            mock_session, create_user_data.email
        )
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()
