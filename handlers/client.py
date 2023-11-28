from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3 as sq
from handlers import text_list


person = {}


class FSMInput(StatesGroup):
    number_first = State()


class Take_num:
    def __init__(self):
        pass

    # Запуск машины состояний
    async def cm_start(message: types.Message):
        await FSMInput.number_first.set()
        await message.answer("Введите строку из цифр")

    async def load_number(message: types.Message, state: FSMContext):
        global person
        if " " in message.text:
            person[message.from_user.id] = list(map(int, message.text.split()))

        else:
            person[message.from_user.id] = [int(x) for x in message.text]

        # вызов класса добавления в бд
        new_v = Add_in_bd(message.from_user.id, message.text)
        new_v.add_val()
        # Завершение машины состояний
        await state.finish()


class Add_in_bd:

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

    # добавление введенных чисел в бд, запись порядкового номера введения
    def add_val(self):
        with sq.connect("C:\\Users\\user\\Desktop\\analitics_bot_2\\handlers\\first_p.db") as con:
            cur = con.cursor()
            m = cur.execute(
                f"""SELECT (EXISTS (SELECT user_id FROM count_num WHERE user_id == {self.user_id}))""").fetchall()
            m = list(*m)[0]
            if str(m) != "0":
                f = cur.execute(f"""SELECT attemps FROM count_num WHERE user_id == {self.user_id}""").fetchall()
                f = int(list(*f)[0])
                cur.execute(f"""UPDATE count_num SET attemps = {f + 1} WHERE user_id == {self.user_id}""")
            else:
                cur.execute(f"""INSERT INTO count_num VALUES ({self.user_id}, 1)""")
            cur.execute(f"""INSERT INTO inp_us VALUES ({self.user_id}, {self.message}, (SELECT attemps FROM
            count_num WHERE user_id == {self.user_id}))""")


class Check_num:
    def __init__(self, user_id):
        self.user_id = user_id

    def check(self):
        with sq.connect("C:\\Users\\user\\Desktop\\analitics_bot_2\\handlers\\first_p.db") as con:
            cur = con.cursor()
            m = list(*cur.execute(
                f"""SELECT (EXISTS (SELECT user_id FROM count_num WHERE user_id == {self.user_id}))""").fetchall())[0]
            if m == 0:
                return False
            else:
                return True


class Launch_func:

    async def check_val(message:types.Message):
        f = Check_num.check(message.from_user.id)
        if f is True:
            pass
        else:
            await message.answer("Вы ни разу не писали боту")

    async def find_average(message: types.Message):
        number = person[message.from_user.id]
        await message.reply(f"{sum(number) / len(number)} ")

    #
    async def sort_bubble(message: types.Message):
        number = person[message.from_user.id]
        N = len(number)
        for i in range(0, N - 1):  # N-1 итераций работы алгоритма
            for j in range(0, N - 1 - i):  # проход по оставшимся не отсортированным парам массива
                if number[j] > number[j + 1]:
                    number[j], number[j + 1] = number[j + 1], number[j]
        number = " ".join(map(str, number))
        if len(number) > 4096:

            for x in range(0, len(number), 4096):
                await message.reply(number[x:x + 4096])
        else:
            await message.reply(number)

    # Быстрая сортировка
    async def fast_sort(message: types.Message):
        def partition(sort_nums, begin, end):
            part = begin
            for i in range(begin + 1, end + 1):
                if sort_nums[i] <= sort_nums[begin]:
                    part += 1
                    sort_nums[i], sort_nums[part] = sort_nums[part], sort_nums[i]
            sort_nums[part], sort_nums[begin] = sort_nums[begin], sort_nums[part]
            return part

        def quick_sort(sort_nums, begin=0, end=None):
            if end is None:
                end = len(sort_nums) - 1

            def quick(sort_nums, begin, end):
                if begin >= end:
                    return
                part = partition(sort_nums, begin, end)
                quick(sort_nums, begin, part - 1)
                quick(sort_nums, part + 1, end)

            return quick(sort_nums, begin, end)

        number = person[message.from_user.id]
        quick_sort(number)
        number = " ".join([str(i) for i in number])
        if len(number) > 4096:
            for x in range(0, len(number), 4096):
                print(number[x:x + 4096])
                await message.answer(number[x:(x + 4096)])
        else:
            await message.reply(number)

    # Поиск максимума
    async def find_max(message: types.Message):
        number = person[message.from_user.id]
        number.sort()
        await message.reply(number[-1])

    # Поиск минимума
    async def find_min(message: types.Message):
        number = person[message.from_user.id]
        number.sort()
        await message.reply(number[0])

    # Вывод медианы
    async def find_median(message: types.Message):
        number = person[message.from_user.id]
        number.sort()
        await message.reply(number[(len(number) + 2) // 2]) if len(number) % 2 != 0 else await \
            message.reply((number[len(number) // 2] + number[len(number) // 2 - 1]) / 2)

    # Вывод часто встречающихся символов
    async def quantity_symbol(message: types.Message):
        number = person[message.from_user.id]
        number.sort()
        for y in set(number):
            if number.count(y) > 1:
                await message.answer(
                    f"Цифра {y} встречается в строке {number.count(y)} раз. В процентном отношении: {number.count(y) / len(number) * 100}%")
        await message.answer(f"введите следующую команду")

    # Поиск моды
    async def find_moda(message: types.Message):
        number = person[message.from_user.id]
        a = []
        b = []
        number.sort()
        for y in set(number):
            if number.count(y) > 1:
                a.append(y)
                b.append(number.count(y))
        await message.reply(a[b.index(max(b))])

    # Поиск разности между наименьшим и наибольшим
    async def find_spread(message: types.Message):
        number = person[message.from_user.id]
        number.sort()
        await message.answer(number[-1] - number[0])

    # Вывод приветственного текста
    async def text_helper(message: types.Message):
        await message.answer(text_list.greet_text)


a = Take_num
create_func = Launch_func


def register_handlers_client(dp: Dispatcher):
    # dp.register_message_handler(a.cm_start, commands=['average', 'sorted_bubble', "find_min", 'find_max',
    #                                     'find_median', 'quantity_symbol', 'find_moda', 'fast_sort', "start", "help"])
    dp.register_message_handler(a.cm_start, commands=['input_number'])
    dp.register_message_handler(a.load_number, state=FSMInput.number_first)
    dp.register_message_handler(create_func.find_average, commands=['average'])
    dp.register_message_handler(create_func.sort_bubble, commands=['sorted_bubble'])
    dp.register_message_handler(create_func.find_min, commands=['find_min'])
    dp.register_message_handler(create_func.find_max, commands=['find_max'])
    dp.register_message_handler(create_func.find_median, commands=['find_median'])
    dp.register_message_handler(create_func.quantity_symbol, commands=['quantity_symbol'])
    dp.register_message_handler(create_func.find_moda, commands=['find_moda'])
    dp.register_message_handler(create_func.find_spread, commands=['find_spread', "average"])
    dp.register_message_handler(create_func.fast_sort, commands=['fast_sort'])
    dp.register_message_handler(create_func.text_helper, commands=["start", "help"])
