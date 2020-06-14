from argparse import ArgumentParser
from enum import Enum


class Action(Enum):
    SERVER_PROD = 'server'
    SERVER_DEV = 'server_dev'
    RELOAD_MODEL = 'reload'
    TRAIN_MODEL = 'train_model'
    GUI = 'gui'

    def __str__(self):
        return self.value


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-action', type=Action, choices=list(Action), required=True)
    opts = parser.parse_args()

    if opts.action == Action.RELOAD_MODEL:
        pass
    if opts.action == Action.TRAIN_MODEL:
        pass
    elif opts.action == Action.GUI:
        from src.gui import app
        app.main()
    elif opts.action == Action.SERVER_PROD:
        from src.server import server
        server.run()
    elif opts.action == Action.SERVER_DEV:
        from src.server import server
        server.run(dev=True)
    else:
        print("Wrong action!")
