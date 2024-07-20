#!/usr/bin/env python
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import os, sys
from functools import partial
import click


class DMenu(QApplication):

    def __init__(self, args, choices, any, ignore_case, starts_with, path):
        super().__init__(args)
        self.any = any
        self.ignore_case = ignore_case
        self.starts_with = starts_with
        self.path = path
        self.window = QWidget()


        self.window.move(0, 0)
        self.window.resize(self.primaryScreen().size().width(), 20)
        self.layout = QHBoxLayout()
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
            self.btns[f].clicked.connect(partial(self.btn_pressed, f))
        self.window.keyPressEvent = self.key_pressed
        self.window.setLayout(self.layout)
        self.window.show()

    def text_changed(self, t):
        self.shown = []
        for k, v in self.btns.items():
            if self.ignore_case:
                t, k = t.lower(), k.lower()
            if k.startswith(t) if self.starts_with else (t in k):
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
@click.option('--path', default=None, type=click.Path(exists=True))
def main(any, i, s, path):
    choices = sys.stdin.read().splitlines()
    app = DMenu(sys.argv, choices, any, i, s, path)
    app.exec()


if __name__ == '__main__':
    main()
