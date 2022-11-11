from marshmallow import validate, Schema, fields
from flask_bcrypt import generate_password_hash
from datetime import date

class UserData(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    login = fields.String()
    password = fields.String()
    email = fields.String()
    address = fields.String()
    is_admin = fields.Bool()
    phone = fields.String()
#validate=validate.Regexp('^[a-zA-Z]+ [a-zA-Z]+$'),
#validate=validate.Email()


class CreateUser(Schema):
    first_name = fields.String(
        validate=validate.Regexp("^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$",
                                 error="Invalid name input"), required=True)
    last_name = fields.String(validate=validate.Regexp("^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$",
                                 error="Invalid surname input"), required=True)
    login = fields.String(required=True)
    password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj), load_only=True, required=True
    )
    email = fields.String(validate=validate.Email(error="Invalid email"), required=True)
    address = fields.String(required=True)
    phone = fields.String(validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$', error="Invalid phone"), required=True)


class GetUser(Schema):
    first_name = fields.String()
    last_name = fields.String()
    login = fields.String()
    email = fields.String()
    address = fields.String()
    phone = fields.String()


class UpdateUser(Schema):
    first_name = fields.String(validate=validate.Regexp("^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$",
                                 error="Invalid name input"))
    last_name = fields.String(validate=validate.Regexp("^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$",
                                 error="Invalid surname input"))
    login = fields.String()
    email = fields.String(validate=validate.Email(error="Invalid email"))
    address = fields.String()
    phone = fields.String(validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$', error="Invalid phone"))
    password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj), load_only=True
    )


class VendorData(Schema):
    id = fields.Integer()
    company_name = fields.String()
    location = fields.String()


class CreateVendor(Schema):
    company_name = fields.String(required=True)
    location = fields.String(required=True)


class GetUpdateVendor(Schema):
    company_name = fields.String()
    location = fields.String()


class GoodCategoryData(Schema):
    id = fields.Integer()
    category_name = fields.String()


class CreateGoodCategory(Schema):
    category_name = fields.String(validate=validate.Regexp('^[a-z]*$', error="Invalid category name"), required=True)


class UpdateGoodCategory(Schema):
    category_name = fields.String(validate=validate.Regexp('^[a-z]*$', error="Invalid category name"))


class GetGoodCategory(Schema):
    category_name = fields.String()


class GoodData(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    cost = fields.Integer()
    num_in_stock = fields.Integer()
    creation_date = fields.DateTime()
    is_reserved = fields.Bool()
    #vendor_id = fields.Nested(VendorData(only=('id',)))
    #category_id = fields.Nested(GoodCategoryData(only=('id',)))
    vendor_id = fields.Integer()
    category_id = fields.Integer()

class CreateGood(Schema):
    name = fields.String(validate=validate.Regexp("^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$", error="Invalid goods name"), required=True)
    description = fields.String(required=True)
    cost = fields.Integer(validate=validate.Range(min_inclusive = 0, error="Invalid cost input") , required=True)
    num_in_stock = fields.Integer(validate=validate.Range(min_inclusive = 0, error="Invalid number in stock input"), required=True)
    creation_date = fields.Date(validate=lambda obj: obj < date.today(), required=True)
    is_reserved = fields.Bool(required=True)
    #vendor_id = fields.Nested(VendorData(only=('id',)), required=True)
    #category_id = fields.Nested(GoodCategoryData(only=('id',)), required=True)
    vendor_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)


class GetGood(Schema):
    name = fields.String()
    description = fields.String()
    cost = fields.Integer()
    num_in_stock = fields.Integer()
    creation_date = fields.DateTime()
    is_reserved = fields.Bool()
    #vendor_id = fields.Nested(VendorData(only=('id',)))
    #category_id = fields.Nested(GoodCategoryData(only=('id',)))
    vendor_id = fields.Integer()
    category_id = fields.Integer()


class UpdateGood(Schema):
    name = fields.String(validate=validate.Regexp('^[a-zA-Z]', error="Invalid goods name"))
    description = fields.String()
    cost = fields.Integer(validate=validate.Range(min_inclusive = 0, error="Invalid cost input"))
    num_in_stock = fields.Integer(validate=validate.Range(min_inclusive = 0, error="Invalid number in stock input"))
    creation_date = fields.Date(validate=lambda obj: obj < date.today())
    is_reserved = fields.Bool()


class OrderData(Schema):
    id = fields.Integer()
    #user_id = fields.Nested(UserData(only=('id',)))
    #good_id = fields.Nested(GoodData(only=('id',)))
    user_id = fields.Integer()
    good_id = fields.Integer()
    buy_date = fields.DateTime()


class CreateOrder(Schema):
    #user_id = fields.Nested(UserData(only=('id',)), required=True)
    #good_id = fields.Nested(GoodData(only=('id',)), required=True)
    user_id = fields.Integer(required=True)
    good_id = fields.Integer(required=True)
    buy_date = fields.Date(validate=lambda obj: obj < date.today(), required=True)


class GetOrders(Schema):
    user_id = fields.Integer()
    good_id = fields.Integer()
    buy_date = fields.DateTime()


class UpdateOrder(Schema):
    buy_date = fields.DateTime(validate=lambda obj: obj < date.today())


class DeliveryData(Schema):
    id = fields.Integer()
    type = fields.String()
    from_ = fields.String()
    to = fields.String()
    #order_id = fields.Nested(OrderData(only=('id',)))
    order_id = fields.Integer()


class CreateDelivery(Schema):
    type = fields.String(validate=validate.OneOf(["self pickup", "courier"]))
    from_ = fields.String()
    to = fields.String()
    #order_id = fields.Nested(OrderData(only=('id',)))
    order_id = fields.Integer()


class GetDelivery(Schema):
    type = fields.String()
    #order_id = fields.Nested(OrderData(only=('id',)))
    order_id = fields.Integer()
    from_ = fields.String()
    to = fields.String()


class UpdateDelivery(Schema):
    type = fields.String(validate=validate.OneOf(["self pickup", "courier"]))
    from_ = fields.String()
    to = fields.String()

