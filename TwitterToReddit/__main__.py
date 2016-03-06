def main():
    from TwitterToReddit import bot
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    bot.main()


if __name__ == '__main__':
    main()
