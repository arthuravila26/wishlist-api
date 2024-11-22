from unittest import TestCase
from unittest.mock import MagicMock, patch

from app.controllers.users_controller import (
    add_item_to_user_wishlist,
    delete_item_from_user_wishlist,
)
from app.models import User
from app.utils.exceptions import ItemDuplicatedInWishList, ProductNotFound


class TestWishlistFunctions(TestCase):

    @patch("app.controllers.users_controller.get_user_by_id")
    @patch("app.controllers.users_controller.send_request_to_get_product")
    @patch("app.controllers.users_controller.Session")
    def test_add_item_to_user_wishlist(
        self, mock_session, mock_send_request, mock_get_user_by_id
    ):
        user_id = 1
        product_id = 10
        product_data = {
            "id": product_id,
            "name": "Product 10",
            "price": 100.99,
            "image": "image.jpg",
            "brand": "brand1",
            "reviewScore": 4.5,
        }

        mock_user = MagicMock(spec=User)
        mock_user.wishlist = []
        mock_get_user_by_id.return_value = mock_user
        mock_send_request.return_value = product_data
        mock_session.return_value.commit.return_value = None

        add_item_to_user_wishlist(
            session=mock_session.return_value, user_id=user_id, product_id=product_id
        )

        self.assertIn(product_data, mock_user.wishlist)

        mock_session.return_value.commit.assert_called_once()

    @patch("app.controllers.users_controller.get_user_by_id")
    @patch("app.controllers.users_controller.send_request_to_get_product")
    def test_add_item_to_user_wishlist_duplicate(
        self, mock_send_request, mock_get_user_by_id
    ):
        user_id = 1
        product_id = 10
        product_data = {
            "ID": product_id,
            "price": 100.99,
            "image": "image",
            "brand": "test brand2",
            "title": "test title2",
            "reviewScore": 4.9,
        }

        mock_user = MagicMock()
        mock_user.wishlist = [{"ID": product_id, "name": "Product 10"}]
        mock_get_user_by_id.return_value = mock_user
        mock_send_request.return_value = product_data

        with self.assertRaises(ItemDuplicatedInWishList):
            add_item_to_user_wishlist(
                session=MagicMock(),
                user_id=user_id,
                product_id=product_id,
            )

        mock_user.session.commit.assert_not_called()

    @patch("app.controllers.users_controller.get_user_by_id")
    @patch("app.controllers.users_controller.send_request_to_get_product")
    def test_delete_item_from_user_wishlist(
        self, mock_send_request, mock_get_user_by_id
    ):
        user_id = 1
        product_id = 10
        product_data = {"id": product_id, "name": "Product 10"}

        mock_user = MagicMock(spec=User)
        mock_user.wishlist = [{"id": 11, "name": "Product 11"}]
        mock_get_user_by_id.return_value = mock_user

        mock_send_request.return_value = product_data

        with self.assertRaises(ProductNotFound):
            try:
                delete_item_from_user_wishlist(
                    session=None, user_id=user_id, product_id=product_id
                )
            except StopIteration:
                raise ProductNotFound()

    @patch("app.controllers.users_controller.get_user_by_id")
    @patch("app.controllers.users_controller.send_request_to_get_product")
    def test_delete_item_from_user_wishlist_not_found(
        self, mock_send_request, mock_get_user_by_id
    ):
        user_id = 1
        product_id = 10
        product_data = {"id": product_id, "name": "Product 10"}

        mock_user = MagicMock(spec=User)
        mock_user.wishlist = []  # Wishlist vazia
        mock_get_user_by_id.return_value = mock_user
        mock_send_request.return_value = product_data

        with self.assertRaises(StopIteration):
            delete_item_from_user_wishlist(
                session=None, user_id=user_id, product_id=product_id
            )
