from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from keyboards import (
    main_keyboard, dc_keyboard, re_keyboard, selfie_keyboard,
    selfie_transaction_keyboard, cc1_keyboard, cc2_keyboard,
    rko_keyboard, confirm_keyboard, start_over_keyboard
)
from google_sheets import get_or_create_worksheet, create_worksheet_from_template, increment_category, \
    increment_cells_based_on_selection, get_current_date_column
from states import Form
from config import PASSWORD
from user_data import get_user_data, set_user_data, is_user_logged_in_today


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state="*")
    dp.register_message_handler(register_name, state=Form.name)
    dp.register_message_handler(check_password, state=Form.password)
    dp.register_callback_query_handler(process_product_selection, state=Form.main)
    dp.register_callback_query_handler(process_dc_selection, state=Form.dc)
    dp.register_callback_query_handler(process_re_selection, state=Form.re)
    dp.register_callback_query_handler(process_selfie_selection, state=Form.selfie)
    dp.register_callback_query_handler(process_selfie_transaction_selection, state=Form.selfie_transaction)
    dp.register_callback_query_handler(process_cc1_selection, state=Form.cc1)
    dp.register_callback_query_handler(process_cc2_selection, state=Form.cc2)
    dp.register_callback_query_handler(process_rko_selection, state=Form.rko)
    dp.register_callback_query_handler(finish_selection, state=Form.finish)
    dp.register_callback_query_handler(confirm_selection, state=Form.confirm)
    dp.register_callback_query_handler(edit_selection, state=Form.edit)
    dp.register_callback_query_handler(start_over, text="start_over", state="*")


async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if is_user_logged_in_today(user_id):
        user_data = get_user_data(user_id)
        await state.update_data(user_full_name=user_data["full_name"])
        await message.reply(f"Добро пожаловать обратно, {user_data['full_name']}. Выберите продукт:",
                            reply_markup=main_keyboard())
        await Form.main.set()
    else:
        await message.reply("Привет! Введите ваше имя и фамилию:")
        await Form.name.set()


async def register_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_full_name = message.text.strip()
    worksheet = get_or_create_worksheet(user_full_name)

    if worksheet:
        await state.update_data(user_full_name=user_full_name)
        set_user_data(user_id, user_full_name)
        await message.reply(f"Добро пожаловать, {user_full_name}. Выберите продукт:", reply_markup=main_keyboard())
        await Form.main.set()
    else:
        await state.update_data(user_full_name=user_full_name)
        await message.reply("Такого пользователя не существует. Введите пароль для создания нового пользователя:")
        await Form.password.set()


async def check_password(message: types.Message, state: FSMContext):
    if message.text.strip() == PASSWORD:
        async with state.proxy() as data:
            user_id = message.from_user.id
            user_full_name = data['user_full_name']
            create_worksheet_from_template(user_full_name)
            set_user_data(user_id, user_full_name)
        await message.reply(f"Пользователь {user_full_name} успешно создан. Выберите продукт:",
                            reply_markup=main_keyboard())
        await Form.main.set()
    else:
        await message.reply("Неверный пароль. Попробуйте еще раз:")


async def process_product_selection(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if 'user_full_name' not in data:
            await callback_query.message.reply(
                "Пожалуйста, сначала введите ваше имя и фамилию с помощью команды /start.")
            return

    action = callback_query.data
    user_full_name = (await state.get_data())['user_full_name']
    worksheet = get_or_create_worksheet(user_full_name)

    # Определение текущего столбца по дате
    current_column = get_current_date_column()

    if action == 'dc':
        increment_category(worksheet, f'{current_column}7')  # Координаты для DC
        await callback_query.message.reply("Выберите опцию DC:", reply_markup=dc_keyboard())
        await Form.dc.set()
    elif action == 're':
        increment_category(worksheet, f'{current_column}16')  # Координаты для RE
        await callback_query.message.reply("Выберите опцию RE:", reply_markup=re_keyboard())
        await Form.re.set()
    elif action == 'selfie':
        increment_category(worksheet, f'{current_column}21')  # Координаты для Селфи
        await callback_query.message.reply("Выберите тип Селфи:", reply_markup=selfie_keyboard())
        await Form.selfie.set()
    elif action == 'cc1':
        increment_category(worksheet, f'{current_column}25')  # Координаты для CC1
        await callback_query.message.reply("Выберите опцию CC1:", reply_markup=cc1_keyboard())
        await Form.cc1.set()
    elif action == 'cc2':
        increment_category(worksheet, f'{current_column}36')  # Координаты для CC2
        await callback_query.message.reply("Выберите опцию CC2:", reply_markup=cc2_keyboard())
        await Form.cc2.set()
    elif action == 'rko':
        increment_category(worksheet, f'{current_column}47')  # Координаты для РКО
        await callback_query.message.reply("Выберите опцию РКО:", reply_markup=rko_keyboard())
        await Form.rko.set()


async def process_dc_selection(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        selected_products = data.get('selected_products', [])
        selected_products.append(callback_query.data)
        data['selected_products'] = selected_products

    await callback_query.answer(f"Вы выбрали {callback_query.data}.")
    await callback_query.message.reply("Выберите еще или завершите выбор:", reply_markup=dc_keyboard())
    if callback_query.data == 'finish':
        await finish_selection(callback_query, state)


async def process_re_selection(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        selected_products = data.get('selected_products', [])
        selected_products.append(callback_query.data)
        data['selected_products'] = selected_products

    await callback_query.answer(f"Вы выбрали {callback_query.data}.")
    await callback_query.message.reply("Выберите еще или завершите выбор:", reply_markup=re_keyboard())
    if callback_query.data == 'finish':
        await finish_selection(callback_query, state)


async def process_selfie_selection(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if 'selfie_type' not in data:
            data['selfie_type'] = callback_query.data
            await callback_query.message.reply("Была ли транзакция?", reply_markup=selfie_transaction_keyboard())
            await Form.selfie_transaction.set()
        else:
            selected_products = data.get('selected_products', [])
            selfie_type = data['selfie_type']
            transaction = callback_query.data == 'Есть транзакция'

            selected_products.append(selfie_type)
            if transaction:
                selected_products.append('Транзакция')

            data['selected_products'] = selected_products
            await callback_query.answer(f"Вы выбрали {callback_query.data}.")
            await finish_selection(callback_query, state)


async def process_selfie_transaction_selection(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        selected_products = data.get('selected_products', [])
        selfie_type = data.get('selfie_type', '')

        if callback_query.data == 'Есть транзакция':
            selected_products.extend([selfie_type, 'Транзакция'])
        else:
            selected_products.append(selfie_type)

        data['selected_products'] = selected_products
        await callback_query.answer(f"Вы выбрали {callback_query.data}.")
        await finish_selection(callback_query, state)


async def process_cc1_selection(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        selected_products = data.get('selected_products', [])
        selected_products.append(callback_query.data)
        data['selected_products'] = selected_products

    await callback_query.answer(f"Вы выбрали {callback_query.data}.")
    await callback_query.message.reply("Выберите еще или завершите выбор:", reply_markup=cc1_keyboard())
    if callback_query.data == 'finish':
        await finish_selection(callback_query, state)


async def process_cc2_selection(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        selected_products = data.get('selected_products', [])
        selected_products.append(callback_query.data)
        data['selected_products'] = selected_products

    await callback_query.answer(f"Вы выбрали {callback_query.data}.")
    await callback_query.message.reply("Выберите еще или завершите выбор:", reply_markup=cc2_keyboard())
    if callback_query.data == 'finish':
        await finish_selection(callback_query, state)


async def process_rko_selection(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        selected_products = data.get('selected_products', [])
        selected_products.append(callback_query.data)
        data['selected_products'] = selected_products

    await callback_query.answer(f"Вы выбрали {callback_query.data}.")
    await callback_query.message.reply("Выберите еще или завершите выбор:", reply_markup=rko_keyboard())
    if callback_query.data == 'finish':
        await finish_selection(callback_query, state)


async def finish_selection(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        selected_products = data.get('selected_products', [])
        selected_products_str = ', '.join(selected_products)
        await callback_query.message.reply(
            f"Вы выбрали следующие продукты:\n{selected_products_str}\n\nПодтвердите выбор или измените его.",
            reply_markup=confirm_keyboard()
        )
        await Form.confirm.set()


async def confirm_selection(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if 'user_full_name' not in data:
            await callback_query.message.reply(
                "Пожалуйста, сначала введите ваше имя и фамилию с помощью команды /start.")
            return

        user_full_name = data['user_full_name']
        worksheet = get_or_create_worksheet(user_full_name)

        if callback_query.data == 'confirm':
            selected_products = data.get('selected_products', [])
            increment_cells_based_on_selection(worksheet, selected_products)
            data['selected_products'] = []  # Очищаем список после подтверждения

            await callback_query.message.reply("Выбор подтвержден. Данные записаны в таблицу.",
                                               reply_markup=start_over_keyboard())
            await state.finish()
        elif callback_query.data == 'edit':
            await callback_query.message.reply("Выберите продукт:", reply_markup=main_keyboard())
            await Form.edit.set()


async def edit_selection(callback_query: types.CallbackQuery, state: FSMContext):
    action = callback_query.data
    await state.update_data(selected_products=[])  # Сброс списка выбранных продуктов

    if action == 'dc':
        await callback_query.message.reply("Выберите опцию DC:", reply_markup=dc_keyboard())
        await Form.dc.set()
    elif action == 're':
        await callback_query.message.reply("Выберите опцию RE:", reply_markup=re_keyboard())
        await Form.re.set()
    elif action == 'selfie':
        await callback_query.message.reply("Выберите тип Селфи:", reply_markup=selfie_keyboard())
        await Form.selfie.set()
    elif action == 'cc1':
        await callback_query.message.reply("Выберите опцию CC1:", reply_markup=cc1_keyboard())
        await Form.cc1.set()
    elif action == 'cc2':
        await callback_query.message.reply("Выберите опцию CC2:", reply_markup=cc2_keyboard())
        await Form.cc2.set()
    elif action == 'rko':
        await callback_query.message.reply("Выберите опцию РКО:", reply_markup=rko_keyboard())
        await Form.rko.set()


async def start_over(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if 'user_full_name' not in data:
            await callback_query.message.reply(
                "Пожалуйста, сначала введите ваше имя и фамилию с помощью команды /start.")
            return

    await callback_query.message.reply("Выберите продукт:", reply_markup=main_keyboard())
    await Form.main.set()
