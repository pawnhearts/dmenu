#!/usr/bin/env python
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import os, sys
from functools import partial
import click



class DMenu(QApplication):

    def __init__(self, args, choices, any, ignore_case, starts_with, vertical, path, max_buttons):
        super().__init__(args)
        self.any = any
        self.ignore_case = ignore_case
        self.starts_with = starts_with
        self.path = path
        self.max_buttons = max_buttons
        self.window = QWidget()


        self.window.move(0, 0)
        self.window.resize(self.primaryScreen().size().width(), 20)
        self.layout = QVBoxLayout() if vertical else QHBoxLayout()
        self.text = QLabel('')
        self.shown = []

        #self.text.textEdited.connect(self.text_changed)
        #self.text.returnPressed.connect(self.return_pressed)
        self.layout.addWidget(self.text)
        self.btns = {}
        if self.path:
            choices = os.listdir(self.path)
        for f in choices:
            self.btns[f] = QPushButton(f)
            self.layout.addWidget(self.btns[f])
            if len(self.btns) > self.max_buttons:
                self.btns[f].hide()
            self.btns[f].clicked.connect(partial(self.btn_pressed, f))

        self.window.keyPressEvent = self.key_pressed
        self.window.setLayout(self.layout)
        self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.window.show()

    def text_changed(self, t):
        self.shown = []
        for k, v in self.btns.items():
            if self.ignore_case:
                t, k = t.lower(), k.lower()
            if len(self.shown) <= self.max_buttons and (k.startswith(t) if self.starts_with else (t in k)):
                self.shown.append(k)
                v.show()
            else:
                v.hide()

    def get_value(self, value):
        if self.path:
            return os.path.join(self.path, value)
        return value

    def return_pressed(self):
        if self.any:
            print(self.get_value(self.text.text()))
        else:
            if self.shown:
                print(self.get_value(self.shown[0]))
        sys.exit(0 if self.shown else 1)

    def btn_pressed(self, b):
        print(b)
        sys.exit(0)

    def key_pressed(self, event):
        k = event.key()
        if k == 16777216:
            sys.exit(1)
        if k == 16777220:
            for k, v in self.btns.items():
                if self.focusWidget() is v:
                    print(self.get_value(k))
                    sys.exit(0)

        if k == 16777219:
            self.text.setText(self.text.text()[:-1])
        else:
            if t := event.text():
                self.text.setText(self.text.text()+t)
        self.text_changed(self.text.text())




@click.command()
@click.option('--any', is_flag=True, default=False, help='Allows to type anything, not just select from list')
@click.option('-i', is_flag=True, default=False, help='Ignore case when searching')
@click.option('-s', is_flag=True, default=False, help='Should start with string you typed not just contain it')
@click.option('-v', is_flag=True, default=False, help='Vertical')
@click.option('--path', default=None, type=click.Path(exists=True))
@click.option('--max-buttons', default=20, type=int, help='Max number of buttons to show at the same time')
def main(any, i, s, v, path, max_buttons):
    choices = sys.stdin.read().splitlines() if not path else None
    app = DMenu(sys.argv, choices, any, i, s, v, path, max_buttons)
    app.exec()


if __name__ == '__main__':
    main()

