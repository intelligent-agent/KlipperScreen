import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Keyboard(Gtk.Box):
    def __init__(self, screen, set_text_cb, close_cb):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        _ = screen.lang.gettext
        self.set_text_cb = set_text_cb
        self.close_cb = close_cb
        self.keyboard = Gtk.Grid()
        self.keyboard.set_direction(Gtk.TextDirection.LTR)
        self.text = ""

        self.keys = [
         [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "⌫"],
          ["a", "s", "d", "f", "g", "h", "j", "k", "l", "'"],
          ["ABC", "z", "x", "c", "v", "b", "n", "m", ",", ".", "?123"],
          ["✕", " ", "✔"]
          ],
         [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "⌫"],
          ["A", "S", "D", "F", "G", "H", "J", "K", "L", "'"],
          ["?123","Z", "X", "C", "V", "B", "N", "M", ",", ".", "abc"],
          ["✕", " ", "✔"]
          ],
         [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "⌫"],
          ["=", "-", "+", "*", "/", "\\", ":", ";", "'", "\""],
          ["abc","(", ")", "#", "$", "!", "?", "@", "_", ",", "ABC"],
          ["✕", " ", "✔"]
          ]
         ]

        self.labels = self.keys.copy()
        for p, pallet in enumerate(self.keys):
            for r, row in enumerate(pallet):
                for k, key in enumerate(row):
                    self.labels[p][r][k] = Gtk.Button(key)
                    self.labels[p][r][k].set_hexpand(True)
                    self.labels[p][r][k].set_vexpand(True)
                    self.labels[p][r][k].connect('clicked', self.update_entry, key)
                    self.labels[p][r][k].get_style_context().add_class("keyboard_pad")

        self.layout = {}
        self.layout["keyboard"] = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.pallet_nr = 0
        self.set_pallet(self.pallet_nr)
        self.add(self.keyboard)

    def set_pallet(self, p):
        pallet = self.keys[p]
        for r, row in enumerate(pallet[:-1]):
            for k, key in enumerate(row):
                x = k*2+1 if r == 1 else k*2
                span = 2
                old = self.keyboard.get_child_at(x, r)
                if old:
                    self.keyboard.remove(old)
                self.keyboard.attach(self.labels[p][r][k], x, r, span, 1)
        if not self.keyboard.get_child_at(0, 4):
            self.keyboard.attach(self.labels[p][3][0], 0, 4, 3, 1)
            self.keyboard.attach(self.labels[p][3][1], 3, 4, 16, 1)
            self.keyboard.attach(self.labels[p][3][2], 19, 4, 3, 1)
        self.show_all()

    def update_entry(self, widget, key):
        if key == "⌫":
            if len(self.text) < 1:
                return
            self.text = self.text[0:-1]
        elif key == "✔":
            self.close_cb(self.text)
            return
        elif key == "✕":
            self.text = ""
            self.close_cb(self.text)
            return
        elif key == "abc":
            self.set_pallet(0)
        elif key == "ABC":
            self.set_pallet(1)
        elif key == "?123":
            self.set_pallet(2)
        else:
            self.text += key
        self.set_text_cb(self.text)
