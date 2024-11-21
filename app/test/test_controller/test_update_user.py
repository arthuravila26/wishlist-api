from unittest import TestCase
from unittest.mock import MagicMock, patch

from app.controllers.users_controller import update_user
from app.models import User
from app.utils.exceptions import EmailAlreadyExists


class TestUserFunctions(TestCase):

    @patch("app.controllers.users_controller.get_user_by_email")
    @patch("app.controllers.users_controller.get_user_by_id")
    @patch("app.controllers.users_controller.hash_password")
    @patch("app.controllers.users_controller.Session")
    def test_update_user(
        self,
        mock_session,
        mock_hash_password,
        mock_get_user_by_id,
        mock_get_user_by_email,
    ):
        user_id = 1
        data = MagicMock()
        data.name = "Updated User"
        data.email = "updateduser@test.com"
        data.password = "newpassword"

        mock_get_user_by_email.return_value = None
        mock_user = MagicMock(spec=User)
        mock_user.name = "Old User"
        mock_user.email = "olduser@example.com"
        mock_user.password = "oldpassword"
        mock_get_user_by_id.return_value = mock_user
        mock_hash_password.return_value = "newpassword"
        mock_session.return_value.commit.return_value = None
        mock_session.return_value.refresh.return_value = None

        updated_user = update_user(
            session=mock_session.return_value, user_id=user_id, data=data
        )

        self.assertEqual(updated_user.name, "Updated User")
        self.assertEqual(updated_user.email, "updateduser@test.com")

        mock_hash_password.assert_called_once_with(data.password)
        mock_session.return_value.commit.assert_called_once()

    @patch("app.controllers.users_controller.get_user_by_email")
    @patch("app.controllers.users_controller.get_user_by_id")
    def test_update_user_email_exists(
        self, mock_get_user_by_id, mock_get_user_by_email
    ):
        user_id = 1
        data = MagicMock()
        data.name = "Updated User"
        data.email = "existingemail@example.com"
        data.password = "newpassword"

        mock_existing_user = MagicMock(spec=User)
        mock_existing_user.id = 2
        mock_get_user_by_email.return_value = mock_existing_user
        mock_user = MagicMock(spec=User)
        mock_user.name = "Old User"
        mock_user.email = "olduser@example.com"
        mock_user.password = "oldpassword"
        mock_get_user_by_id.return_value = mock_user

        with self.assertRaises(EmailAlreadyExists):
            update_user(
                session=mock_get_user_by_id.return_value, user_id=user_id, data=data
            )

        mock_get_user_by_email.assert_called_once_with(
            mock_get_user_by_id.return_value, data.email
        )
