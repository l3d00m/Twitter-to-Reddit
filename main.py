def main():
    from TwitterToReddit.bot import start
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    start()


if __name__ == '__main__':
    main()
