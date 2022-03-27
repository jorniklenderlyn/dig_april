import datetime, texttable
from aiogram import types
from aiogram.dispatcher.filters import Command

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegramBot.handlers.dig.db_func import get_map, get_all_users, change_dirt_map, get_user_time,\
    get_user_efficiency, get_user_fortune, change_diamonds, get_user_diamonds, get_user_level, change_time,\
    change_fortune, change_efficiency, change_level
from telegramBot.loader import dp, bot
from telegramBot.handlers.dig.game_functions import dig_cell, time_for_dig, buy_efficiency, buy_fortune,\
    FORTUNE_PRICES, EFFICIENCY_PRICES


def get_markup(uid):
    dirt_map = InlineKeyboardMarkup()
    num_map = get_map(uid)
    for i in range(15):
        if num_map[i] == "0" or num_map[i] == "2":
            dirt_map.insert(InlineKeyboardButton(text="🗿", callback_data="dirt" + str(i)))
        # elif num_map[i] == "2":
        #     dirt_map.insert(InlineKeyboardButton(text="💎", callback_data="dirt" + str(i)))
        else:
            dirt_map.insert(InlineKeyboardButton(text="🕳️", callback_data="dirt" + str(i)))

    dirt_map.row(InlineKeyboardButton(text="-Улучшения-", callback_data="-"))

    efficiency = get_user_efficiency(uid)
    if efficiency + 1 == len(EFFICIENCY_PRICES):
        text = f"⛏Эффективность:{efficiency + 1}lvl"
    else:
        text = f"⛏Эффективность:{efficiency + 1}lvl>{efficiency + 2}lvl\n{EFFICIENCY_PRICES[efficiency]}💎"
    dirt_map.row(InlineKeyboardButton(text=text, callback_data="efficiency"))
    # dirt_map.insert()
    fortune = get_user_fortune(uid)
    if fortune + 1 == len(FORTUNE_PRICES):
        text = f"🌈Удача: {fortune + 1}lvl"
    else:
        text = f"🌈Удача: {fortune + 1}lvl>{fortune + 2}lvl\n{FORTUNE_PRICES[fortune]}💎"
    dirt_map.row(InlineKeyboardButton(text=text, callback_data="fortune"))
    return dirt_map


def get_name_id(uid):
    users = sorted(get_all_users(), reverse=True)
    for i in range(len(users)):
        if str(uid) == users[i][2]:
            return i + 1, users[i][1]


def get_delta_time(uid):
    tdelta = datetime.datetime.now() - get_user_time(uid)
    tdelta = tdelta.total_seconds()
    tdelta = round(time_for_dig(get_user_efficiency(uid)) - tdelta, 2)
    if tdelta < 0:
        tdelta = 0
    return tdelta


def get_text(uid):
    rating, name = get_name_id(uid)
    text = "<b>DIGрадация</b>\n" \
           "<em>Вы оказались на архипелаге Пасхи.\n" \
           "На каждом острове в одной из статуй находится алмаз.\n" \
           "Так как вы начинающий охотник за сокровищами, точно определить статую с алмазом невозможно.\n" \
           "Приходится разбивать каждую...\n" \
           "Вы находитесь в необычном месте, поэтому можно потратить несколько алмазов на зачаровывание своих" \
           " инструментов.</em>\n" \
           "<ins>окончание ивента 02.04.2022 00:00</ins>\n" \
           f"<pre>Ваше место: {rating}; Имя: {name}\n" \
           f"Уровень: {get_user_level(uid)}\n" \
           f"Алмазы💎: {get_user_diamonds(uid)}</pre>\n" \
           "/rating - рейтинг /dig - игра"
    return text


async def dig(uid):
    dirt_map = get_markup(uid)
    await bot.send_message(chat_id=uid, text=get_text(uid), reply_markup=dirt_map)


@dp.message_handler(Command("dig"))
async def dig_start(message: types.Message):
    await dig(message.from_user.id)


@dp.message_handler(Command("rating"))
async def dig_rating(message: types.Message):
    users = get_all_users()
    users.sort(reverse=True)

    tb = texttable.Texttable()
    tb.add_row(["Имя", "Алмазы", "Уровень"])

    for i in users:
        tb.add_row([i[1], i[0], i[3]])
    await message.answer("<pre>" + tb.draw() + "</pre>")
    # <pre></pre>


async def load_dig(uid, callback_query):
    try:
        await callback_query.answer(f"Время до попытки: {get_delta_time(uid)}")
        await callback_query.message.edit_text(get_text(uid), reply_markup=get_markup(uid))
    except:
        pass


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('efficiency'))
async def up_efficiency(callback_query: CallbackQuery):
    uid = callback_query.from_user.id
    user_efficiency = get_user_efficiency(uid)
    buy_data = buy_efficiency(user_efficiency, get_user_diamonds(uid))
    if buy_data[0]:
        change_diamonds(uid, buy_data[1])
        change_efficiency(uid, user_efficiency + 1)
        await callback_query.answer("Вы зачаровали кирку")
    else:
        if user_efficiency + 1 == len(EFFICIENCY_PRICES):
            await callback_query.answer("Вы и так сильны")
        else:
            await callback_query.answer("недостаточно алмазов")
    await load_dig(uid, callback_query)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('fortune'))
async def up_fortune(callback_query: CallbackQuery):
    uid = callback_query.from_user.id
    user_fortune = get_user_fortune(uid)
    buy_data = buy_fortune(user_fortune, get_user_diamonds(uid))
    if buy_data[0]:
        change_diamonds(uid, buy_data[1])
        change_fortune(uid, user_fortune + 1)
        await callback_query.answer("Вы зачаровались")
    else:
        if user_fortune + 1 == len(FORTUNE_PRICES):
            await callback_query.answer("Вы и так сильны")
        else:
            await callback_query.answer("недостаточно алмазов")
    await load_dig(uid, callback_query)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('dirt'))
async def choose_dirt(callback_query: CallbackQuery):
    uid = callback_query.from_user.id
    ind = int(callback_query.data.replace("dirt", ""))
    dig_data = dig_cell((datetime.datetime.now() - get_user_time(uid)).total_seconds(),
                        get_map(uid), ind, get_user_efficiency(uid), get_user_fortune(uid))
    if dig_data[1] == -1:
        pass
    elif dig_data[1] == -2:
        pass
    else:
        change_time(uid, datetime.datetime.now())
        if dig_data[1] > 0:
            change_diamonds(uid, get_user_diamonds(uid) + dig_data[1])
            change_level(uid, get_user_level(uid) + 1)
        change_dirt_map(uid, "".join(dig_data[0]))

    await load_dig(uid, callback_query)
