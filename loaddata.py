from sqlalchemy import *
from models import *

session = Session()
stmt = User(
                first_name="testuser_first_name1",
                last_name="testuser_last_name1",
                login="testuser1",
                password="123qwe123",
                phone="0688275212",
                email="testuser1@localhost",
                address="City, Street 1",
                is_admin=0)

stmt2 = User(
                first_name="testuser_first_name2",
                last_name="testuser_last_name2",
                login="testuser2",
                password="123qwe123",
                phone="0688275213",
                email="testuser2@localhost",
                address="City, Street 2",
                is_admin=0)

data2 = Vendor(
        company_name="TestCompanyName",
        location="TestCity, TestStreet 1"
    )
data2_ = Vendor(
        company_name="TestCompanyName2",
        location="TestCity, TestStreet 2"
    )

data3 = Good_Category(
        category_name="testcategory"
    )
data3_ = Good_Category(
        category_name="testcategory2"
    )

data4 = Good(
        vendor_id=1,
        category_id=1,
        name="Test good",
        description="Lorem ipsum....",
        cost=541,
        num_in_stock=5,
        creation_date=datetime.datetime.now(),
        is_reserved=1
    )
data4_ = Good(
        vendor_id=2,
        category_id=2,
        name="Test good2",
        description="Lorem ipsum....",
        cost=541,
        num_in_stock=5,
        creation_date=datetime.datetime.now(),
        is_reserved=1
    )

data5 = Order(
        user_id=1,
        good_id=1,
        buy_date=datetime.datetime.now()
    )
data5_ = Order(
        user_id=2,
        good_id=2,
        buy_date=datetime.datetime.now()
    )

data6 = Delivery(
      order_id=1,
      type='courier',
      from_='Lviv',
      to='Kyiv'
    )

data6_ = Delivery(
      order_id=2,
      type='self pickup',
      from_='Odesa',
      to='Lviv'
    )

session.add(stmt)
session.add(stmt2)
session.add(data2)
session.add(data2_)
session.add(data3)
session.add(data3_)
session.add(data4)
session.add(data4_)
session.add(data5)
session.add(data5_)

session.add(data6)
session.add(data6_)
session.commit()