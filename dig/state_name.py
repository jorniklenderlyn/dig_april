from aiogram.types import CallbackQuery

from telegramBot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from telegramBot.keyboards.inline.ChooseConfirm import confirm, cancel
from aiogram.dispatcher.filters import Filter
from telegramBot.handlers.dig.db_func import check_user, add_user
from telegramBot.handlers.dig.game_functions import gen_map


class IsNamed(Filter):
    async def check(self, message: types.Message):
        return not check_user(message.from_user.id)


class OrderName(StatesGroup):
    waiting_name = State()
    waiting_submit = State()


async def name_start(message: types.Message):
    await message.answer("Введите имя для рейтинга:\n(не больше 14 символов, неприемлимое имя будет заменено)", reply_markup=cancel)
    await OrderName.waiting_name.set()


async def write_name(message: types.Message, state: FSMContext):
    if len(message.text) < 15:
        await state.update_data(name=message.text)
        await message.answer(text="Установить имя '{}'".format(message.text), reply_markup=confirm)
        await OrderName.waiting_submit.set()
    else:
        await message.answer("Ваше имя больше 14 символов\n"
                             "Введите имя для рейтинга:\n(не больше 18 символов, неприемлимое имя будет заменено)",
                             reply_markup=cancel)


async def submit_name(callback_query: CallbackQuery, state: FSMContext):
    cnf = callback_query.data

    await callback_query.message.delete()

    if cnf == "confirm_yes":
        from telegramBot.handlers.dig.dig_april import dig
        data = await state.get_data()
        add_user(callback_query.from_user.id, data["name"], gen_map())
        await dig(callback_query.from_user.id)
        await state.finish()
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text="Введите имя для рейтинга:\n"
                                                                         "(неприемлимое имя будет заменено)",
                               reply_markup=cancel)
        await OrderName.waiting_name.set()


async def submit_yet(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(text="Установить имя '{}'".format(data["name"]), reply_markup=confirm)


def register_handlers_name():
    dp.register_message_handler(name_start, IsNamed(), commands="dig", state="*")
    dp.register_message_handler(write_name, state=OrderName.waiting_name)
    dp.register_callback_query_handler(submit_name, lambda c: c.data and c.data.startswith('confirm'),
                                       state=OrderName.waiting_submit)
    dp.register_message_handler(submit_yet, state=OrderName.waiting_submit)
