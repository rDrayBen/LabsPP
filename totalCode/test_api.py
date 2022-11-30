# from FullCourceProject.models import User
# from FullCourceProject.models import Vendor
# from FullCourceProject.models import Good_Category
# from FullCourceProject.models import Good
# from FullCourceProject.models import Order
# from FullCourceProject.models import Delivery
import pytest
from FullCourceProject.models import *
from flask_bcrypt import generate_password_hash, check_password_hash
from FullCourceProject.db_utils import *
from FullCourceProject.app import app


@pytest.fixture
def test_user_1():
    data = {
        "first_name": "user",
        "last_name": "user",
        "login": "user",
        "password": "user",
        "email": "user@gmail.com",
        "address": "Lviv",
        "phone": "0987654323"
    }
    return data



@pytest.fixture(scope='function')
def wrapper(request):
    Session.close()
    Base.metadata.drop_all(sql_engine)
    Base.metadata.create_all(sql_engine)


# Test Units
class TestInsert:
    def test_insert_user(self, wrapper):
        user_data = {
            "first_name": "Alexxx",
            "last_name": "Cheh",
            "login": "user3",
            "password": "123",
            "email": "test@gmailll.com",
            "address": "Lviv",
            "phone": "0987654323"
        }
        response = app.test_client().post('/user', json=user_data)
        assert response.status_code == 200
        # assert create_user(User, phn=user_data['phone'], eml=user_data['email'], lgn=user_data['login']
        #                    , **user_data) not in [406, 407, 408]

    def test_insert_vendor(self, wrapper):
        data = {
            "first_name": "user",
            "last_name": "user",
            "login": "user",
            "password": "user",
            "email": "user@gmail.com",
            "address": "Lviv",
            "phone": "0987654323"
        }
        app.test_client().post('/user', json=data)
        new_user = Session.query(User).filter_by(login=data["login"]).one()

        resp = app.test_client().get('/user/login', json={"username": new_user.login, "password": "user"})
        token = resp.json

        vendor_data = {"company_name": "Epic", "location": "Lviv"}
        response = app.test_client().post('/vendor', json=vendor_data, headers={"Authorization": f"Bearer {token}"})
        # assert create_vendor(Vendor, **vendor_data) not in [405, 400]
        assert response.status_code not in [400, 401, 403, 405]
        # assert response.status_code == 200

    def test_insert_category(self, wrapper):
        # data = {
        #     "first_name": "user",
        #     "last_name": "user",
        #     "login": "user",
        #     "password": "user",
        #     "email": "user@gmail.com",
        #     "address": "Lviv",
        #     "phone": "0987654323"
        # }
        # app.test_client().post('/user', json=data)
        new_user = Session.query(User).filter_by(login="admin").one()

        resp = app.test_client().get('/user/login', json={"username": new_user.login, "password": "admin"})
        token = resp.json
        category_data = {"category_name": "Test cateogry 1"}
        response = app.test_client().post('/vendor', json=category_data, headers={"Authorization": f"Bearer {token}"})
        # assert create_vendor(Vendor, **vendor_data) not in [405, 400]
        assert response.status_code == 200
        # assert create_category(Good_Category, **category_data) not in [405, 400]

    def test_insert_good(self, wrapper):
        good_data = \
            {
                "vendor_id": 1,
                "category_id": 1,
                "name": "Beb",
                "description": None,
                "cost": 20,
                "num_in_stock": 1,
                "creation_date": "2021-05-04",
                "is_reserved": 0
            }
        assert create_entry(Good, **good_data) != 400

    def test_insert_delivery(self, wrapper):
        delivery_data = {"order_id": 1, "type": "courier", "from_": "Beb", "to": "Beb2"}
        assert create_entry(Delivery, **delivery_data) != 400

    def test_insert_order(self, wrapper):
        order_data = {"user_id": 1, "good_id": 1, "buy_date": "2020-02-02"}
        assert create_entry(Order, **order_data) != 400


class TestSelect:
    def test_select_user_by_id(self, wrapper):
        data = {
            "first_name": "user",
            "last_name": "user",
            "login": "user",
            "password": "user",
            "email": "user@gmail.com",
            "address": "Lviv",
            "phone": "0987654323"
        }
        app.test_client().post('/user', json=data)
        new_user = Session.query(User).filter_by(login="user").one()

        resp = app.test_client().get('/user/login', json={"username": "user", "password": "user"})
        token = resp.json

        resp = app.test_client().get(f'/user/{new_user.id}', json={"username": new_user.login, "password": "user"})
        assert resp.status_code == 401

    # def test_select_user_by_login(self, getUserLogin, wrapper):
    #     assert get_user_by_login(getUserLogin) != 405

    def test_select_vendor_by_id(self, wrapper):
        data = {
            "first_name": "user",
            "last_name": "user",
            "login": "user",
            "password": "user",
            "email": "user@gmail.com",
            "address": "Lviv",
            "phone": "0987654323"
        }
        app.test_client().post('/user', json=data)
        new_user = Session.query(User).filter_by(login="user").one()

        resp = app.test_client().get('/user/login', json={"username": "user", "password": "user"})
        token = resp.json

        resp = app.test_client().get(f'/vendor/{new_user.id}', json={"username": new_user.login, "password": "user"})
        assert resp.status_code == 401
        #assert get_entry_by_id(Vendor, getVendorId) != 405

    def test_select_order_by_id(self, getOrderId, wrapper):
        assert get_entry_by_id(Order, getOrderId) != 405

    def test_select_order_by_first_second_id(self, getUserId, getGoodId, wrapper):
        assert get_entry_by_first_and_second_id(Order, getUserId, getGoodId) != 405

    def test_select_order_by_second_id(self, getUserId, getUserFiled, wrapper):
        assert get_entry_by_second_id(Order, getUserId, getUserFiled) != []

    def test_select_good_by_id(self, getGoodId, wrapper):
        assert get_entry_by_id(Good, getGoodId) != 405

    def test_select_category_by_id(self, getCategoryId, wrapper):
        assert get_entry_by_id(Good_Category, getCategoryId) != 405

    def test_select_delivery_by_id(self, getDeliveryId, wrapper):
        assert get_entry_by_id(Delivery, getDeliveryId) != 405

    def test_select_all_users(self, wrapper):
        assert get_entry(User) != []

    def test_select_all_vendors(self, wrapper):
        assert get_entry(Vendor) != []

    def test_select_all_orders(self, wrapper):
        assert get_entry(Order) != []

    def test_select_all_good(self, wrapper):
        assert get_entry(Good) != []

    def test_select_all_category(self, wrapper):
        assert get_entry(Good_Category) != []

    def test_select_all_delivery(self, wrapper):
        assert get_entry(Delivery) != []


class TestUpdate:
    def test_update_user(self, getUserId, getFiledsToUpdateUser):
        user = get_entry_by_id(User, getUserId)
        assert user != 405
        assert update_user(user, **getFiledsToUpdateUser) not in [406, 407, 408]

    def test_update_vendor(self, getVendorId, getFieldsToUpdateVendor):
        vendor = get_entry_by_id(Vendor, getVendorId)
        assert vendor != 405
        assert update_entry(vendor, **getFieldsToUpdateVendor) != []

    def test_update_good(self, getGoodId, getFiledsToUpdateGood):
        good = get_entry_by_id(Good, getGoodId)
        assert good != 405
        assert update_entry(good, **getFiledsToUpdateGood) != []

    def test_update_category(self, getCategoryId, getFieldsToUpdateCategory):
        category = get_entry_by_id(Good_Category, getCategoryId)
        assert category != 405
        assert update_entry(category, **getFieldsToUpdateCategory) != []

    def test_update_delivery(self, getDeliveryId, getFieldsToUpdateDelivery):
        delivery = get_entry_by_id(Delivery, getDeliveryId)
        assert delivery != 405
        assert update_entry(delivery, **getFieldsToUpdateDelivery) != []


class TestDelete:
    def test_delete_user(self, wrapper):
        data = {
            "first_name": "user",
            "last_name": "user",
            "login": "user",
            "password": "user",
            "email": "user@gmail.com",
            "address": "Lviv",
            "phone": "0987654323"
        }
        app.test_client().post('/user', json=data)
        new_user = Session.query(User).filter_by(login="user").one()

        resp = app.test_client().get('/user/login', json={"username": "user", "password": "user"})
        token = resp.json

        resp = app.test_client().delete(f'/user/{new_user.id}', json={"username": new_user.login, "password": "user"})
        assert resp.status_code == 401
        #assert delete_entry(User, getUserId) != 405

    def test_delete_vendor(self, getVendorId):
        assert delete_entry(Vendor, getVendorId) != 405

    def test_delete_order_by_id(self, getOrderId):
        assert delete_entry(Order, getOrderId) != 405

    def test_delete_order(self, getUserId, getOrderId):
        assert delete_entry_by_first_and_second_id(Order, getUserId, getUserId) not in [405, 406]

    def test_delete_good(self, wrapper, getGoodId):
        assert delete_entry(Good, getGoodId) != 405

    def test_delete_category(self, getCategoryId):
        assert delete_entry(Good_Category, getCategoryId) != 405

    def test_delete_delivery(self, getDeliveryId):
        assert delete_entry(Delivery, getDeliveryId) != 405
