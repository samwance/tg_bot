import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Replace with your bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables.")


# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Command to start the bot
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text="Open Mini App",
        web_app={"url": "https://your-github-pages-url.com"}
    ))
    await message.answer("Welcome! Click the button below to open the mini app.", reply_markup=keyboard.as_markup())

# Handle data sent from the mini app
@dp.message(lambda message: message.web_app_data is not None)
async def handle_web_app_data(message: types.Message):
    data = message.web_app_data.data
    await message.answer(f"Received data from mini app: {data}")

# Start the bot
async def on_startup(app):
    await bot.delete_webhook(drop_pending_updates=True)

# Run the bot
async def main():
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dp, bot)
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    app.on_startup.append(on_startup)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())