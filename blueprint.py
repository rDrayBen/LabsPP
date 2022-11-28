from flask import Blueprint, request, jsonify
import db_utils
from models import User, Vendor, Good_Category, Good, Order, Delivery
from shemas import *
from flask import make_response
from marshmallow import ValidationError
from flask_jwt import current_identity
from app import *
from flask_jwt_extended import *
from flask_bcrypt import check_password_hash
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/user", methods=["POST"])#working
def createUser():
    try:
        userData = CreateUser().load(request.json)
        user = db_utils.check_entry_for_user(phn=userData['phone'], eml=userData['email'], lgn=userData['login'])
        if user == 405:
            response = make_response("Not unique phone")
            response.status_code = 405
            return response
        elif user == 406:
            response = make_response("Not unique email")
            response.status_code = 406
            return response
        elif user == 407:
            response = make_response("Not unique login")
            response.status_code = 407
            return response
        user = db_utils.create_entry(User, **userData)
    except ValidationError as err:
        response = dict({"message": err.normalized_messages()})
        return response, 400
    response = make_response(jsonify(GetUser().dump(user)))
    response.status_code = 200
    return response

@api_blueprint.route("/user/login", methods=["GET"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response(jsonify("Empty field"), 403)

    user = db_utils.get_user_by_login(auth.username)
    if user == 405:
        return make_response(jsonify("Not found"), 404)

    if check_password_hash(user.password, auth.password):
        access_token = create_access_token(identity=user.login)
        return make_response(jsonify({"token": access_token}))

    return make_response(jsonify("Uncorrect field entered"), 403)

@api_blueprint.route("/user/<int:user_id>", methods=["GET"])#working
@jwt_required()
def getUsersById(user_id):
    current_identity_login = get_jwt_identity()
    curr = db_utils.get_user_by_login(current_identity_login)

    user = db_utils.get_entry_by_id(User, user_id)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if curr == 405:
        response = make_response(jsonify("Access denied"))
        response.status_code = 405
        return response

    if curr.is_admin == 1 or current_identity_login == user.login:
        response = make_response(jsonify(GetUser().dump(user)))
        response.status_code = 200
        return response

    return make_response(jsonify("Access denied"))

@api_blueprint.route("/user/<int:user_id>", methods=["PUT"])#working
@jwt_required()
def updateUser(user_id):
    current_identity_login = get_jwt_identity()
    user = db_utils.get_entry_by_id(User, user_id)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response


    if current_identity_login == user.login:
        try:
            userData = UpdateUser().load(request.json)
        except ValidationError as err:
            response = dict({"message": err.normalized_messages()})
            return response, 400
        user = db_utils.get_entry_by_id(User, user_id)
        if user == 405:
            response = make_response("Invalid user id")
            response.status_code = 405
            return response

        res = db_utils.update_user(user, **userData)
        if res == 406:
            response = make_response("Not unique phone")
            response.status_code = 406
            return response
        elif res == 407:
            response = make_response("Not unique email")
            response.status_code = 407
            return response
        elif res == 408:
            response = make_response("Not unique login")
            response.status_code = 408
            return response
        response = make_response(jsonify(GetUser().dump(user)))
        response.status_code = 200
        return response

    return make_response(jsonify("Access denied"), 403)

@api_blueprint.route("/user", methods=["GET"])#working
@jwt_required()
def getUsers():
    current_identity_login = get_jwt_identity()
    user =db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        return make_response(jsonify("Access denied"), 403)

    users = db_utils.get_entry(User)

    response = make_response(jsonify(GetUser(many=True).dump(users)))
    response.status_code = 200
    return response

@api_blueprint.route("/user/<int:user_id>", methods=["DELETE"])#working
@jwt_required()
def deleteUser(user_id):
    current_identity_login = get_jwt_identity()
    curr = db_utils.get_user_by_login(current_identity_login)

    user = db_utils.get_entry_by_id(User, user_id)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if curr == 405:
        response = make_response(jsonify("Access denied"))
        response.status_code = 405
        return response

    if curr.is_admin == 1 or current_identity_login == user.login:
        if db_utils.delete_entry(User, user_id) == 405:
            response = make_response("Invalid input id")
            response.status_code = 405
            return response
        response = make_response("Success")
        response.status_code = 200
        return response




    return make_response(jsonify("Access denied"))

    #delete user from db

@api_blueprint.route("/order", methods=["POST"])#working
@jwt_required()
def createOrder():
    current_identity_login = get_jwt_identity()
    user = db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response


    if current_identity_login == user.login:
        try:
            orderData = CreateOrder().load(request.json)
            if orderData['user_id'] != user.id:
                response = make_response(jsonify("You can`t to another account"))
                response.status_code = 405
                return response

            if db_utils.get_entry_by_id(User, input_id=orderData['user_id']) == 405 or \
                    db_utils.get_entry_by_id(Good, input_id=orderData['good_id']) == 405:
                response = make_response("Invalid foreign key in input")
                response.status_code = 405
                return response
            order = db_utils.create_entry(Order, **orderData)
        except ValidationError as err:
            response = dict({"message": err.normalized_messages()})
            return response, 400
        response = make_response(jsonify(GetOrders().dump(order)))
        response.status_code = 200
        return response
    return make_response(jsonify("Must login"))
    #create new order

@api_blueprint.route("/order/<int:user_id>", methods=["GET"])#working
@jwt_required()
def getOrders(user_id):
    current_identity_login = get_jwt_identity()
    curr = db_utils.get_user_by_login(current_identity_login)

    user = db_utils.get_entry_by_id(User, user_id)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if curr == 405:
        response = make_response(jsonify("Access denied"))
        response.status_code = 405
        return response

    if curr.is_admin == 1 or current_identity_login == user.login:
        if db_utils.get_entry_by_id(User, input_id=user_id) == 405:
            response = make_response("Invalid id in path")
            response.status_code = 405
            return response
        order = db_utils.get_entry_by_second_id(Order, user_id, 'order')
        response = make_response(jsonify(GetOrders(many=True).dump(order)))
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"))
    #get all orders from certain user by user id

@api_blueprint.route("/order/<int:user_id>/<int:order_id>", methods=["GET"])#working
@jwt_required()
def getOrderById(user_id, order_id):
    current_identity_login = get_jwt_identity()
    curr = db_utils.get_user_by_login(current_identity_login)

    user = db_utils.get_entry_by_id(User, user_id)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if curr == 405:
        response = make_response(jsonify("Access denied"))
        response.status_code = 405
        return response

    if curr.is_admin == 1 or current_identity_login == user.login:
        if db_utils.get_entry_by_id(Order, input_id=order_id) == 405 or \
            db_utils.get_entry_by_id(User, input_id=user_id) == 405:
            response = make_response("Invalid id in path")
            response.status_code = 405
            return response
        order = db_utils.get_entry_by_first_and_second_id(Order, order_id, user_id)
        if order == 405:
            response = make_response("Invalid input id")
            response.status_code = 405
            return response
        response = make_response(jsonify(GetOrders().dump(order)))
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"))
    #get concrete order of certain user by order id and user id

@api_blueprint.route("/order/<int:user_id>/<int:order_id>", methods=["DELETE"])#working
@jwt_required()
def deleteOrder(user_id, order_id):
    current_identity_login = get_jwt_identity()
    curr = db_utils.get_user_by_login(current_identity_login)
    user = db_utils.get_entry_by_id(User, user_id)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if curr == 405:
        response = make_response(jsonify("Access denied"))
        response.status_code = 405
        return response

    if curr.is_admin == 1 or current_identity_login == user.login:
        if db_utils.delete_entry_by_first_and_second_id(Order, order_id, user_id) == 405:
            response = make_response("Invalid input id")
            response.status_code = 405
            return response
        elif db_utils.delete_entry_by_first_and_second_id(Order, order_id, user_id) == 406:
            response = make_response("Foreign key bond with this id")
            response.status_code = 406
            return response
        response = make_response("Success")
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"))
    #delete concrete order of certain user by order id and user id

@api_blueprint.route("/good", methods=["POST"])#working
@jwt_required()
def createGood():
    current_identity_login = get_jwt_identity()
    user = db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if current_identity_login == user.login:
        try:
            goodData = CreateGood().load(request.json)
            if db_utils.get_entry_by_id(Vendor, input_id=goodData['vendor_id']) == 405 or db_utils.get_entry_by_id(Good_Category, input_id=goodData['category_id']) == 405:
                response = make_response("Invalid foreign key in input")
                response.status_code = 405
                return response
            good = db_utils.create_entry(Good, **goodData)
        except ValidationError as err:
            response = dict({"message": err.normalized_messages()})
            return response, 400
        response = make_response(jsonify(GetGood().dump(good)))
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"))
    #create new good

@api_blueprint.route("/good", methods=["GET"])#working take sobi
def getGoods():
    good = db_utils.get_entry(Good)
    response = make_response(jsonify(GetGood(many=True).dump(good)))
    response.status_code = 200
    return response
    #get all goods

@api_blueprint.route("/good/<int:good_id>", methods=["GET"])#working
def getGoodById(good_id):
    good = db_utils.get_entry_by_id(Good, good_id)
    if good == 405:
        response = make_response("Invalid inout id")
        response.status_code = 405
        return response
    response = make_response(jsonify(GetGood().dump(good)))
    response.status_code = 200
    return response
    #get certain good by id

@api_blueprint.route("/good/<int:good_id>", methods=["PUT"])#working
@jwt_required()
def updateGood(good_id):
    current_identity_login = get_jwt_identity()
    curr = db_utils.get_user_by_login(current_identity_login)
    user = db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if curr == 405:
        response = make_response(jsonify("Access denied"))
        response.status_code = 405
        return response

    if current_identity_login == user.login or curr.is_admin == 1:
        try:
            goodData = UpdateGood().load(request.json)
        except ValidationError as err:
            response = dict({"message": err.normalized_messages()})
            return response, 400
        good = db_utils.get_entry_by_id(Good, good_id)
        if good == 405:
            response = make_response("Invalid input id")
            response.status_code = 405
            return response
        db_utils.update_entry(good, **goodData)
        response = make_response(jsonify(GetGood().dump(good)))
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"), 403)
    #update certain good by id

@api_blueprint.route("/good/<int:good_id>", methods=["DELETE"])#working
@jwt_required()
def deleteGood(good_id):
    current_identity_login = get_jwt_identity()
    curr = db_utils.get_user_by_login(current_identity_login)
    user = db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if curr == 405:
        response = make_response(jsonify("Access denied"))
        response.status_code = 405
        return response

    if current_identity_login == user.login or curr.is_admin == 1:
        if db_utils.delete_entry(Good, good_id) == 405:
            response = make_response("Invalid input id")
            response.status_code = 405
            return response
        response = make_response("Success")
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"), 403)
    #delete certain good by id

@api_blueprint.route("/good_category", methods=["POST"])#working
@jwt_required()
def createGoodCategory():
    current_identity_login = get_jwt_identity()
    user = db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if current_identity_login == user.login and user.is_admin == 1:
        try:
            goodCategoryData = CreateGoodCategory().load(request.json)
            goodCategory = db_utils.create_category(Good_Category, nm=goodCategoryData['category_name'], **goodCategoryData)
            if goodCategory == 405:
                response = make_response("Not unique category name")
                response.status_code = 405
                return response
        except ValidationError as err:
            response = dict({"message": err.normalized_messages()})
            return response, 400
        response = make_response(jsonify(GetGoodCategory().dump(goodCategory)))
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"), 403)
    #create new good category

@api_blueprint.route("/good_category", methods=["GET"])#working
def getGoodCategories():
    goodCategory = db_utils.get_entry(Good_Category)
    response = make_response(jsonify(GetGoodCategory(many=True).dump(goodCategory)))
    response.status_code = 200
    return response
    #get all good categories

@api_blueprint.route("/good_category/<int:good_category_id>", methods=["GET"])#working
def getGoodCategoryById(good_category_id):
    goodCategory = db_utils.get_entry_by_id(Good_Category, good_category_id)
    if goodCategory == 405:
        response = make_response("Invalid input id")
        response.status_code = 405
        return response
    response = make_response(jsonify(GetGoodCategory().dump(goodCategory)))
    response.status_code = 200
    return response
    #get good category by id

@api_blueprint.route("/good_category/<int:good_category_id>", methods=["PUT"])#working
@jwt_required()
def updateGoodCategory(good_category_id):
    current_identity_login = get_jwt_identity()
    user = db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if current_identity_login == user.login and user.is_admin == 1:
        try:
            goodCategoryData = UpdateGoodCategory().load(request.json)
        except ValidationError as err:
            response = dict({"message": err.normalized_messages()})
            return response, 400
        goodCategory = db_utils.get_entry_by_id(Good_Category, good_category_id)
        if goodCategory == 405:
            response = make_response("Invalid input id")
            response.status_code = 405
            return response
        db_utils.update_entry(goodCategory, **goodCategoryData)
        response = make_response(jsonify(GetGoodCategory().dump(goodCategory)))
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"), 403)
    #update certain good category by id

@api_blueprint.route("/good_category/<int:good_category_id>", methods=["DELETE"])#working
@jwt_required()
def deleteGoodCategory(good_category_id):
    current_identity_login = get_jwt_identity()
    user = db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if current_identity_login == user.login and user.is_admin == 1:
        if db_utils.delete_entry(Good_Category, good_category_id) == 405:
            response = make_response("Invalid input id")
            response.status_code = 405
            return response
        response = make_response("Success")
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"), 403)
    #delete certain good category by id

@api_blueprint.route("/vendor", methods=["POST"])#working
@jwt_required()
def createVendor():
    current_identity_login = get_jwt_identity()
    user = db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if current_identity_login == user.login and user.is_admin == 1:
        try:
            vendorData = CreateVendor().load(request.json)
            vendor = db_utils.create_vendor(Vendor, nm=vendorData['company_name'], **vendorData)
            if vendor == 405:
                response = make_response("Not unique company name")
                response.status_code = 405
                return response
        except ValidationError as err:
            response = dict({"message": err.normalized_messages()})
            return response, 400
        response = make_response(jsonify(GetUpdateVendor().dump(vendor)))
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"), 403)
    #create new vendor

@api_blueprint.route("/vendor", methods=["GET"])#working
def getVendors():
    vendor = db_utils.get_entry(Vendor)
    response = make_response(jsonify(GetUpdateVendor(many=True).dump(vendor)))
    response.status_code = 200
    return response
    #get all vendors

@api_blueprint.route("/vendor/<int:vendor_id>", methods=["GET"])#working
def getVendorById(vendor_id):
    vendor = db_utils.get_entry_by_id(Vendor, vendor_id)
    if vendor == 405:
        response = make_response("Invalid input id")
        response.status_code = 405
        return response
    response = make_response(jsonify(GetUpdateVendor().dump(vendor)))
    response.status_code = 200
    return response
    #get certain vendor by id

@api_blueprint.route("/vendor/<int:vendor_id>", methods=["PUT"])#working
@jwt_required()
def updateVendor(vendor_id):
    current_identity_login = get_jwt_identity()
    user = db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if current_identity_login == user.login and user.is_admin == 1:

        try:
            vendorData = GetUpdateVendor().load(request.json)
        except ValidationError as err:
            response = dict({"message": err.normalized_messages()})
            return response, 400
        vendor = db_utils.get_entry_by_id(Vendor, vendor_id)
        if vendor == 405:
            response = make_response("Invalid input id")
            response.status_code = 405
            return response
        db_utils.update_entry(vendor, **vendorData)
        response = make_response(jsonify(GetUpdateVendor().dump(vendor)))
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"), 403)
    #update certain vendor by id

@api_blueprint.route("/vendor/<int:vendor_id>", methods=["DELETE"])#working
@jwt_required()
def deleteVendor(vendor_id):
    current_identity_login = get_jwt_identity()
    user = db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if current_identity_login == user.login and user.is_admin == 1:

        if db_utils.delete_entry(Vendor, vendor_id) == 405:
            response = make_response("Invalid input id")
            response.status_code = 405
            return response
        response = make_response("Success")
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"), 403)
    #delete vendor by id

@api_blueprint.route("/delivery", methods=["POST"])#working
@jwt_required()
def createDelivery():
    current_identity_login = get_jwt_identity()
    user = db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if current_identity_login == user.login:
        try:
            deliveryData = CreateDelivery().load(request.json)
            if db_utils.get_entry_by_id(Order, input_id=deliveryData['order_id']) == 405:
                response = make_response("Invalid foreign key in input")
                response.status_code = 405
                return response
            delivery = db_utils.create_entry(Delivery, **deliveryData)
        except ValidationError as err:
            response = dict({"message": err.normalized_messages()})
            return response, 400
        response = make_response(jsonify(GetDelivery().dump(delivery)))
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"), 403)
    #create new delivery

@api_blueprint.route("/delivery/<int:delivery_id>", methods=["GET"])#working
@jwt_required()
def getDeliveryById(delivery_id):
    current_identity_login = get_jwt_identity()
    user = db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if current_identity_login == user.login or user.is_admin == 1:
        delivery = db_utils.get_entry_by_id(Delivery, delivery_id)
        if delivery == 405:
            response = make_response("Invalid input id")
            response.status_code = 405
            return response
        response = make_response(jsonify(GetDelivery().dump(delivery)))
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"), 403)
    #get certain delivery by id of certain user

@api_blueprint.route("/delivery/<int:delivery_id>", methods=["PUT"])
@jwt_required()
def updateDelivery(delivery_id):
    pass
    #update certain delivery by id

@api_blueprint.route("/delivery/<int:delivery_id>", methods=["DELETE"])#working
@jwt_required()
def deleteDelivery(delivery_id):
    current_identity_login = get_jwt_identity()
    user = db_utils.get_user_by_login(current_identity_login)
    if user == 405:
        response = make_response(jsonify("Invalid user id"))
        response.status_code = 405
        return response

    if current_identity_login == user.login:
        if db_utils.delete_entry(Delivery, delivery_id) == 405:
            response = make_response("Invalid input id")
            response.status_code = 405
            return response
        response = make_response("Success")
        response.status_code = 200
        return response
    return make_response(jsonify("Access denied"), 403)
    #delete delivery by id


"""
{
  "first_name": "Stas",
  "last_name": "Semenenko",
  "login": "nulp572",
  "phone": "0900256731",
  "password": "asdasdadsd",
  "email": "testemail@localhost",
  "address": "Lviv, Symonenka73",
}
"""