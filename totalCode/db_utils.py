from models import Session, User, Delivery


def create_entry(model_class, *, commit=True, **kwargs):
    session = Session()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    if not session.query(model_class).filter_by(**kwargs).one():
        return 400
    return session.query(model_class).filter_by(**kwargs).one()

def create_user(model_class, phn, eml, lgn, *, commit=True, **kwargs):
    session=Session()
    if session.query(model_class).filter_by(phone=phn).all() != [] :
        return 406
    elif session.query(model_class).filter_by(email=eml).all() != []:
        return 407
    elif session.query(model_class).filter_by(login=lgn).all() != []:
        return 408
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    if not session.query(model_class).filter_by(**kwargs).one():
        return 400
    return session.query(model_class).filter_by(**kwargs).one()

def create_category(model_class, nm, *, commit=True, **kwargs):
    session=Session()
    if session.query(model_class).filter_by(category_name=nm).all() != []:
        return 405
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    if not session.query(model_class).filter_by(**kwargs).one():
        return 400
    return session.query(model_class).filter_by(**kwargs).one()

def create_vendor(model_class, nm, *, commit=True, **kwargs):
    session = Session()
    if session.query(model_class).filter_by(company_name=nm).all() != []:
        return 405
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    if not session.query(model_class).filter_by(**kwargs).one():
        return 400
    return session.query(model_class).filter_by(**kwargs).one()

def get_entry_by_id(model_class, input_id, **kwargs):
    session = Session()
    if session.query(model_class).filter_by(id=input_id).all() == []:
        return 405
    return session.query(model_class).filter_by(id=input_id).one()


def get_user_by_login(input_login):
    session = Session()
    if session.query(User).filter_by(login=input_login).all() == []:
        return 405
    return session.query(User).filter_by(login=input_login).one()


def update_entry(entry, *, commit=True, **kwargs):
    session = Session()
    for key, value in kwargs.items():
        setattr(entry, key, value)
    if commit:
        session.commit()
    return entry


def update_user(entry, *, commit=True, **kwargs):
    session=Session()
    for key, value in kwargs.items():
        if key == 'phone':
            if check_entry_for_user(phn=value, eml="notvalidgmail", lgn="notlogin") != 200:
                return 406
        elif key == 'email':
            if check_entry_for_user(phn='+380000000000', eml=value, lgn="notlogin") != 200:
                return 407
        elif key == 'login':
            if check_entry_for_user(phn='+380000000000', eml="notvalidgmail", lgn=value) != 200:
                return 408
        setattr(entry, key, value)
    if commit:
        session.commit()
    return entry

def get_entry(model_class):
    session = Session()
    return session.query(model_class).all()


def get_entry_by_second_id(model_class, second_id, field_name):
    session=Session()
    if field_name == 'order':
        return session.query(model_class).filter_by(user_id=second_id).all()
    elif field_name == 'delivery':
        return session.query(model_class).filter_by(order_id=second_id).all()


def get_entry_by_first_and_second_id(model_class, first_id, second_id):
    session = Session()
    if not session.query(model_class).filter_by(id=first_id).one():
        return 405
    return session.query(model_class).filter_by(user_id=second_id, id=first_id).one()


def get_entry_for_delivery(user_id, deliv_id):
    session = Session()
    if session.query(Delivery).filter_by(id=deliv_id).one() == []:
        return 405
    return session.query(Delivery).filter_by(to=user_id, id=deliv_id).one()


def delete_entry_by_first_and_second_id(model_class, first_id, second_id, *, commit=True, **kwargs):
    session = Session()
    if not session.query(model_class).filter_by(user_id=second_id, id=first_id, **kwargs).one():
        return 405
    elif not session.query(model_class).filter_by(user_id=second_id).one():
        return 406
    session.query(model_class).filter_by(user_id=second_id, id=first_id, **kwargs).delete()
    if commit:
        session.commit()


def delete_entry(model_class, input_id, *, commit=True, **kwargs):
    session = Session()
    if not session.query(model_class).filter_by(id=input_id).all():
        return 405
    session.query(model_class).filter_by(id=input_id).delete()
    if commit:
        session.commit()


def check_entry_for_user(phn, eml, lgn):
    session = Session()
    if session.query(User).filter_by(phone=phn).all() != []:
        return 406
    elif session.query(User).filter_by(email=eml).all() != []:
        return 407
    elif session.query(User).filter_by(login=lgn).all() != []:
        return 408
    else:
        return 200