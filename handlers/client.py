from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

person = {}


class FSMInput(StatesGroup):
    number_first = State()


async def cm_start(message: types.Message):
    await FSMInput.number_first.set()
    await message.answer("Введите строку из цифр")


async def load_number(message: types.Message, state: FSMContext):
    global person
    print(message.from_user.id)
    if " " in message.text:
        person[message.from_user.id] = list(map(int, message.text.split()))
    else:
        person[message.from_user.id] = [int(x) for x in message.text]
    await state.finish()


async def find_average(message: types.Message):
    number = person[message.from_user.id]
    await message.reply(f"{sum(number) / len(number)} ")


async def sort_bubble(message: types.Message):
    number = person[message.from_user.id]
    N = len(number)
    for i in range(0, N - 1):  # N-1 итераций работы алгоритма
        for j in range(0, N - 1 - i):  # проход по оставшимся не отсортированным парам массива
            if number[j] > number[j + 1]:
                number[j], number[j + 1] = number[j + 1], number[j]
    number = " ".join(map(str, number))
    await message.reply(number)


async def find_max(message: types.Message):
    number = person[message.from_user.id]
    number.sort()
    await message.reply(number[-1])


async def find_min(message: types.Message):
    number = person[message.from_user.id]
    number.sort()
    await message.reply(number[0])


async def find_median(message: types.Message):
    number = person[message.from_user.id]
    number.sort()
    await message.reply(number[(len(number) + 2) / 2]) if len(number) % 2 != 0 else await \
        message.reply(number[(len(number) / 2)] + number[len(number / 2) - 1])


async def quantity_symbol(message: types.Message()):
    number = person[message.from_user.id]
    number.sort()
    for y in set(number):
        if number.count(y) > 1:
            await message.answer(f"Цифраа {y} встречается в строке {number.count(y)} раз. В процентном отношении: {number.count(y) / len(number) * 100}%")
    await message.answer(f"введите следующую команду")


async def find_moda(message: types.Message()):
    number = person[message.from_user.id]
    a = []
    b = []
    number.sort()
    for y in set(number):
        if number.count(y) > 1:
            a.append(y)
            b.append(number.count(y))
    await message.reply(a[b.index(max(b))])


async def find_spread(message: types.Message()):
    number = person[message.from_user.id]
    number.sorted()
    await message.answer(number[-1] - number[0])


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['input_number'])
    dp.register_message_handler(load_number, state=FSMInput.number_first)
    dp.register_message_handler(find_average, commands=['average'])
    dp.register_message_handler(sort_bubble, commands=['sorted_bubble'])
    dp.register_message_handler(find_min, commands=['find_min'])
    dp.register_message_handler(find_max, commands=['find_max'])
    dp.register_message_handler(find_median, commands=['find_median'])
    dp.register_message_handler(quantity_symbol, commands=['quantity_symbol'])
    dp.register_message_handler(find_moda, commands=['find_moda'])
