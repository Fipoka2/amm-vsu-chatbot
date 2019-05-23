from argparse import ArgumentParser
from enum import Enum


class Action(Enum):
    SERVER = 'server'
    RELOAD_MODEL = 'reload'
    GUI = 'gui'

    def __str__(self):
        return self.value


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-action', type=Action, choices=list(Action), required=True)
    opts = parser.parse_args()

    if opts.action == Action.RELOAD_MODEL:
        from src.core import reload_model
        reload_model.reload()
    elif opts.action == Action.GUI:
        from src.gui import app
        app.main()
    elif opts.action == Action.SERVER:
        from src.server import server
        server.run()
    else:
        print("Wrong action!")
