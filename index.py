import logging
from aiogram import Bot, Dispatcher, types
from geopy.geocoders import Nominatim

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
TOKEN = '6991515761:AAHn-f6eZc7xRjenl-nfuuBAbXSNHJ_EjbY'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Initialize geocoder
geolocator = Nominatim(user_agent="telegram_bot")

# Handler for start command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Hello! Send me a location.")

# Handler for location messages
@dp.message_handler(content_types=types.ContentType.LOCATION)
async def handle_location(message: types.Message):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude

    # Reverse geocode to get the address
    try:
        address_info = await get_location_info(latitude, longitude)
        await message.reply(f"Location Information:\n{address_info}")
    except Exception as e:
        logging.error("Error getting location information: %s", e)
        await message.reply("Failed to retrieve location information.")

async def get_location_info(latitude, longitude):
    location = geolocator.reverse((latitude, longitude), exactly_one=True, language="en")
    if location:
        address_info = {
            "Country": location.raw["address"].get("country"),
            "Region": location.raw["address"].get("state"),
            "City": location.raw["address"].get("city"),
            "Street": location.raw["address"].get("road"),
            "Description": location.address
        }
        return "\n".join([f"{key}: {value}" for key, value in address_info.items()])
    else:
        return "Location information not available."

if __name__ == '__main__':
    # Start the bot
    logging.info("Starting bot...")
    import asyncio
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(dp.start_polling())
    except Exception as e:
        logging.error("Error: %s", e)
    finally:
        loop.run_until_complete(dp.stop_polling())
