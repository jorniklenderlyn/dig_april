from dataBot.datacode.mySQL.func_db.db_session import global_init, create_session
from dataBot.datacode.mySQL.models.DigTelegramUsers import DigTelegramUser
import datetime


DB_NAME = "kcodbforbots"


def check_user(uid):
    global_init(DB_NAME)
    db_sess = create_session()
    if db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid).first():
        db_sess.close()
        return True
    db_sess.close()
    return False


def add_user(uid, username, dirt_map):
    global_init(DB_NAME)
    db_sess = create_session()
    if not db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid).first():
        model = DigTelegramUser()
        model.user_id = uid
        model.user_name = username
        model.dirt_map = dirt_map
        model.diamonds = 0
        model.efficiency = 0
        model.fortune = 0
        model.level = 0
        model.time = datetime.datetime.now() - datetime.timedelta(1)
        db_sess.add(model)
        db_sess.commit()
    db_sess.close()


def delete_user_telegram(uid):
    global_init(DB_NAME)
    db_sess = create_session()
    user = db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid).first()
    if user:
        db_sess.delete(user)
        db_sess.commit()
    db_sess.close()


def get_map(uid):
    global_init(DB_NAME)
    db_sess = create_session()
    u = db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid).first()
    db_sess.close()
    return u.dirt_map


def get_all_users():
    global_init(DB_NAME)
    db_sess = create_session()
    box = []
    for i in db_sess.query(DigTelegramUser).all():
        box.append((i.diamonds, i.user_name, i.user_id, i.level))
    db_sess.close()
    # print(box)
    return box


def get_user_time(uid):
    global_init(DB_NAME)
    db_sess = create_session()
    u = db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid).first()
    db_sess.close()
    return u.time


def get_user_efficiency(uid):
    global_init(DB_NAME)
    db_sess = create_session()
    u = db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid).first()
    db_sess.close()
    return u.efficiency


def get_user_fortune(uid):
    global_init(DB_NAME)
    db_sess = create_session()
    u = db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid).first()
    db_sess.close()
    return u.fortune


def get_user_diamonds(uid):
    global_init(DB_NAME)
    db_sess = create_session()
    u = db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid).first()
    db_sess.close()
    return u.diamonds


def get_user_level(uid):
    global_init(DB_NAME)
    db_sess = create_session()
    u = db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid).first()
    db_sess.close()
    return u.level


def change_dirt_map(uid, dirt_map):
    global_init(DB_NAME)
    db_sess = create_session()
    user = db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid)
    user.update({DigTelegramUser.dirt_map: dirt_map}, synchronize_session=False)
    db_sess.commit()
    db_sess.close()


def change_diamonds(uid, diamonds):
    global_init(DB_NAME)
    db_sess = create_session()
    user = db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid)
    user.update({DigTelegramUser.diamonds: diamonds}, synchronize_session=False)
    db_sess.commit()
    db_sess.close()



def change_efficiency(uid, efficiency):
    global_init(DB_NAME)
    db_sess = create_session()
    user = db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid)
    user.update({DigTelegramUser.efficiency: efficiency}, synchronize_session=False)
    db_sess.commit()
    db_sess.close()



def change_fortune(uid, fortune):
    global_init(DB_NAME)
    db_sess = create_session()
    user = db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid)
    user.update({DigTelegramUser.fortune: fortune}, synchronize_session=False)
    db_sess.commit()
    db_sess.close()


def change_level(uid, level):
    global_init(DB_NAME)
    db_sess = create_session()
    user = db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid)
    user.update({DigTelegramUser.level: level}, synchronize_session=False)
    db_sess.commit()
    db_sess.close()


def change_time(uid, time):
    global_init(DB_NAME)
    db_sess = create_session()
    user = db_sess.query(DigTelegramUser).filter(DigTelegramUser.user_id == uid)
    user.update({DigTelegramUser.time: time}, synchronize_session=False)
    db_sess.commit()
    db_sess.close()
