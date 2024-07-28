from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    password = State()
    main = State()
    dc = State()
    re = State()
    selfie = State()
    selfie_transaction = State()  # Новое состояние для обработки выбора транзакции
    cc1 = State()
    cc2 = State()
    rko = State()
    finish = State()
    confirm = State()
    edit = State()
