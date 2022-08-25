import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram_timepicker import FullTimePicker, full_timep_callback, full_timep_default, \
    HourTimePicker, hour_timep_callback


# insert your telegram bot API key here
API_TOKEN = '' or os.getenv('token')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

start_kb = ReplyKeyboardMarkup(resize_keyboard=True,)
start_kb.row('Full Time Picker')
start_kb.row('Hour Picker', )


# starting bot when user sends `/start` command, answering with inline timepicker
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    await message.reply('Pick a timepicker', reply_markup=start_kb)


@dp.message_handler(Text(equals=['Full Time Picker'], ignore_case=True))
async def full_picker_handler(message: Message):
    await message.answer(
        "Please select a time: ",
        reply_markup=await FullTimePicker().start_picker()
    )


# full timepicker usage
@dp.callback_query_handler(full_timep_callback.filter())
async def process_full_timepicker(callback_query: CallbackQuery, callback_data: dict):
    selected, time = await FullTimePicker().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {time.strftime("%H:%M:%S")}',
            reply_markup=start_kb
        )
        await callback_query.message.delete_reply_markup()


@dp.message_handler(Text(equals=['Hour Picker'], ignore_case=True))
async def full_picker_handler(message: Message):
    await message.answer(
        "Please select a hour: ",
        reply_markup=await HourTimePicker().start_picker()
    )


@dp.callback_query_handler(hour_timep_callback.filter())
async def process_full_timepicker(callback_query: CallbackQuery, callback_data: dict):
    selected, time = await HourTimePicker().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.edit_text(
            f'You selected {time}h.',
        )


if __name__ == '__main__':
    full_timep_default(
        label_up='⇪', label_down='⇓',
        hour_format='{0:02}h', minute_format='{0:02}m', second_format='{0:02}s'
    )
    executor.start_polling(dp, skip_updates=True)