from unittest import TestCase
from unittest.mock import MagicMock, patch

from app.controllers.users_controller import delete_user
from app.models import User
from app.utils.exceptions import UserNotFound


class TestUserFunctions(TestCase):

    @patch("app.controllers.users_controller.get_user_by_id")
    @patch("app.controllers.users_controller.Session")
    def test_delete_user(self, mock_session, mock_get_user_by_id):
        user_id = 1
        mock_user = MagicMock(spec=User)
        mock_user.name = "Test User"
        mock_user.id = user_id
        mock_get_user_by_id.return_value = mock_user
        mock_session.return_value.commit.return_value = None

        result = delete_user(session=mock_session.return_value, user_id=user_id)

        self.assertEqual(result, {"message": "User deleted successfully"})

        mock_session.return_value.delete.assert_called_once_with(mock_user)
        mock_session.return_value.commit.assert_called_once()

    @patch("app.controllers.users_controller.get_user_by_id")
    def test_delete_user_not_found(self, mock_get_user_by_id):
        user_id = 1
        mock_get_user_by_id.return_value = None

        with self.assertRaises(UserNotFound):
            delete_user(session=mock_get_user_by_id.return_value, user_id=user_id)

        mock_get_user_by_id.assert_called_once_with(
            mock_get_user_by_id.return_value, user_id
        )
