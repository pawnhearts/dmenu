#!/usr/bin/env python
from PyQt5.QtCore import Qt
from PyQt6.QtWidgets import *
import os, sys
from functools import partial


class DMenu(QApplication):

    def __init__(self, args, choices):
        super().__init__(args)
        self.window = QWidget()


        self.window.move(0, 0)
        self.window.resize(self.primaryScreen().size().width(), 20)
        self.layout = QHBoxLayout()
        self.text = QLineEdit()
        self.shown = []

        self.text.textEdited.connect(self.text_changed)
        self.text.returnPressed.connect(self.return_pressed)
        self.layout.addWidget(self.text)
        self.btns = {}
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
            if t in k:
                self.shown.append(k)
                v.show()
            else:
                v.hide()

    def return_pressed(self):
        if self.shown:
            print(self.shown[0])
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
                    print(k)
            sys.exit(0)

        if k == 16777219:
            self.text.setText(self.text.text()[:-1])
        else:
            if t := event.text():
                self.text.setText(self.text.text()+t)
                self.text_changed(self.text.text())




def main():
    choices = sys.stdin.read().splitlines()
    app = DMenu(sys.argv, choices)
    app.exec()


if __name__ == '__main__':
    main()

