from app.telegram_bot import TelegramBot


def main():
    telegram_bot = TelegramBot()
    telegram_bot.run_bot()


if __name__ == "__main__":
    main()
