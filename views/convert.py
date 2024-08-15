from PyQt5 import uic


ui_filename = "EqualGrapher.ui"
py_ui_filename = "view.py"

with open(py_ui_filename, "w", encoding="utf-8") as fout:
    uic.compileUi(ui_filename, fout)