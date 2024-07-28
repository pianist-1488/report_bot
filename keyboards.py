from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("DC", callback_data='dc'),
        InlineKeyboardButton("RE", callback_data='re'),
        InlineKeyboardButton("Селфи", callback_data='selfie'),
        InlineKeyboardButton("CC1", callback_data='cc1'),
        InlineKeyboardButton("CC2", callback_data='cc2'),
        InlineKeyboardButton("РКО", callback_data='rko')
    )


def dc_keyboard():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("Комбо или ККК", callback_data='Комбо или ККК'),
        InlineKeyboardButton("БС с покупкой акций", callback_data='БС с покупкой акций'),
        InlineKeyboardButton("НС до 50 т.р.", callback_data='НС до 50 т.р.'),
        InlineKeyboardButton("НС от 50 т.р.", callback_data='НС от 50 т.р.'),
        InlineKeyboardButton("Реферальная программа", callback_data='Реферальная программа'),
        InlineKeyboardButton("Цифровой профиль", callback_data='Цифровой профиль'),
        InlineKeyboardButton("КэшБэк", callback_data='КэшБэк'),
        InlineKeyboardButton("AlfaPay", callback_data='AlfaPay'),
        InlineKeyboardButton("Завершить выбор", callback_data='finish')
    )


def re_keyboard():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("Установка пин кода", callback_data='Установка пин кода'),
        InlineKeyboardButton("Цифровой профиль (пин)", callback_data='Цифровой профиль (пин)'),
        InlineKeyboardButton("КэшБэк (пин)", callback_data='КэшБэк (пин)'),
        InlineKeyboardButton("AlfaPay (пин)", callback_data='AlfaPay (пин)'),
        InlineKeyboardButton("Завершить выбор", callback_data='finish')
    )


def selfie_keyboard():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("Селфи ДК", callback_data='Селфи ДК'),
        InlineKeyboardButton("Селфи СС", callback_data='Селфи СС')
    )


def selfie_transaction_keyboard():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("Есть транзакция", callback_data='Есть транзакция'),
        InlineKeyboardButton("Нет транзакции", callback_data='Нет транзакции')
    )


def cc1_keyboard():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("Транзакция", callback_data='Транзакция (CC1)'),
        InlineKeyboardButton("PPI", callback_data='PPI (CC1)'),
        InlineKeyboardButton("БС с покупкой акций (CC1)", callback_data='БС с покупкой акций (CC1)'),
        InlineKeyboardButton("КДК к CC1", callback_data='КДК к CC1'),
        InlineKeyboardButton("НС до 50 т.р. (CC1)", callback_data='НС до 50 т.р. (CC1)'),
        InlineKeyboardButton("НС от 50 т.р. (CC1)", callback_data='НС от 50 т.р. (CC1)'),
        InlineKeyboardButton("Реферальная программа (CC1)", callback_data='Реферальная программа (CC1)'),
        InlineKeyboardButton("Цифровой профиль (CC1)", callback_data='Цифровой профиль (CC1)'),
        InlineKeyboardButton("КэшБэк (CC1)", callback_data='КэшБэк (CC1)'),
        InlineKeyboardButton("AlfaPay (CC1)", callback_data='AlfaPay (CC1)'),
        InlineKeyboardButton("Завершить выбор", callback_data='finish')
    )


def cc2_keyboard():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("Транзакция", callback_data='Транзакция (CC2)'),
        InlineKeyboardButton("PPI (CC2)", callback_data='PPI (CC2)'),
        InlineKeyboardButton("БС с покупкой акций (CC2)", callback_data='БС с покупкой акций (CC2)'),
        InlineKeyboardButton("КДК к CC2", callback_data='КДК к CC2'),
        InlineKeyboardButton("НС до 50 т.р. (CC2)", callback_data='НС до 50 т.р. (CC2)'),
        InlineKeyboardButton("НС от 50 т.р. (CC2)", callback_data='НС от 50 т.р. (CC2)'),
        InlineKeyboardButton("Реферальная программа (CC2)", callback_data='Реферальная программа (CC2)'),
        InlineKeyboardButton("Цифровой профиль (CC2)", callback_data='Цифровой профиль (CC2)'),
        InlineKeyboardButton("КэшБэк (CC2)", callback_data='КэшБэк (CC2)'),
        InlineKeyboardButton("AlfaPay (CC2)", callback_data='AlfaPay (CC2)'),
        InlineKeyboardButton("Завершить выбор", callback_data='finish')
    )


def rko_keyboard():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("ДК для Кор счета", callback_data='ДК для Кор счета'),
        InlineKeyboardButton("ДК для физ.", callback_data='ДК для физ.'),
        InlineKeyboardButton("Завершить выбор", callback_data='finish')
    )


def confirm_keyboard():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Подтвердить выбор", callback_data='confirm'),
        InlineKeyboardButton("Изменить выбор", callback_data='edit')
    )


def start_over_keyboard():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Начать заново", callback_data='start_over')
    )
