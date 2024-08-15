import sys
import os
from views.view import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl, QRegExp
from PyQt5.QtGui import QDesktopServices, QRegExpValidator,  QIcon
from PyQt5.QtWidgets import QGraphicsScene, QTableWidgetItem, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backend_bases import NavigationToolbar2
import numpy as np
import csv


class MyNavigationToolbar(NavigationToolbar2, QtWidgets.QToolBar):
    def __init__(self, canvas, parent, coordinates=True):
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
          )
        NavigationToolbar2.__init__(self, canvas)
        QtWidgets.QToolBar.__init__(self, parent)


class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):  # encapsulation
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('views/icons8-sine-80.png'))
        self.scene = QGraphicsScene()
        self.tableWidget.setColumnCount(7)
        self.reset_func_1()
        self.reset_func_2()
        self.reset_func_3()
        self.reset_func_4()
        self.clear_all_funcs()

        # Matplotlib Figure and Canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)


        # Setup toolbar
        self.toolbar = MyNavigationToolbar(self.canvas, self)
        self.addToolBar(self.toolbar)
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self._pan_start = None


        # Setup scene
        self.scene.addWidget(self.canvas)
        self.graphicsView.setScene(self.scene)

        # Connect canvas with scroll event
        self.canvas.mpl_connect('scroll_event', self.mouse_scroll_event)

        self.setup_validators()
        self.connect_signals()
        self.draw_func()

    def mouse_scroll_event(self, event):

        ax = self.figure.gca()
        base_scale = 1.1
        if event.button == 'up':
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            scale_factor = base_scale
        else:
            scale_factor = 1

        curr_xlim = ax.get_xlim()
        curr_ylim = ax.get_ylim()

        new_width = (curr_xlim[1] - curr_xlim[0]) * scale_factor
        new_height = (curr_ylim[1] - curr_ylim[0]) * scale_factor

        relx = (curr_xlim[1] - event.xdata) / (curr_xlim[1] - curr_xlim[0])
        rely = (curr_ylim[1] - event.ydata) / (curr_ylim[1] - curr_ylim[0])

        ax.set_xlim([event.xdata - new_width * (1 - relx), event.xdata + new_width * relx])
        ax.set_ylim([event.ydata - new_height * (1 - rely), event.ydata + new_height * rely])
        ax.figure.canvas.draw()

    def on_mouse_press(self, event):
        if event.button == 1:  # left click
            self._pan_start = (event.xdata, event.ydata)

    def on_mouse_release(self, event):
        self._pan_start = None

    def on_mouse_move(self, event):
        # if the mouse is outside the graphic area.
        if not event.inaxes or event.xdata is None or event.ydata is None:
            return
    
        if self._pan_start is not None and event.button == 1:
            dx = event.xdata - self._pan_start[0]
            dy = event.ydata - self._pan_start[1]
            ax = self.figure.gca()
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            ax.set_xlim([xlim[0] - dx, xlim[1] - dx])
            ax.set_ylim([ylim[0] - dy, ylim[1] - dy])
            self.figure.canvas.draw_idle()


    def connect_signals(self):
        # functions inputs signals
        self.lineEdit_20.textChanged.connect(self.update_equation_label)
        self.lineEdit_21.textChanged.connect(self.update_equation_label)
        self.lineEdit_22.textChanged.connect(self.update_equation_label)
        self.lineEdit_23.textChanged.connect(self.update_equation_label)
        self.lineEdit_24.textChanged.connect(self.update_equation_label)
        self.lineEdit_25.textChanged.connect(self.update_equation_label)
        self.lineEdit_26.textChanged.connect(self.update_equation_label)
        self.lineEdit_27.textChanged.connect(self.update_equation_label)
        self.lineEdit_28.textChanged.connect(self.update_equation_label)
        self.lineEdit_29.textChanged.connect(self.update_equation_label)
        self.lineEdit_30.textChanged.connect(self.update_equation_label)
        self.lineEdit_31.textChanged.connect(self.update_equation_label)
        self.lineEdit_32.textChanged.connect(self.update_equation_label)
        self.lineEdit_33.textChanged.connect(self.update_equation_label)
        self.lineEdit_34.textChanged.connect(self.update_equation_label)
        self.lineEdit_35.textChanged.connect(self.update_equation_label)
        self.lineEdit_36.textChanged.connect(self.update_equation_label)
        self.lineEdit_37.textChanged.connect(self.update_equation_label)

        #checkbox buttons
        self.checkBox_1.stateChanged.connect(self.draw_func)
        self.checkBox_2.stateChanged.connect(self.draw_func)
        self.checkBox_3.stateChanged.connect(self.draw_func)
        self.checkBox_4.stateChanged.connect(self.draw_func)

        # Coordinate Range Buttons
        self.lineEdit_18.textChanged.connect(self.update_equation_label)
        self.lineEdit_19.textChanged.connect(self.update_equation_label)

        # reset buttons
        self.pushButton_3.clicked.connect(self.reset_func_1)
        self.pushButton_5.clicked.connect(self.reset_func_2)
        self.pushButton_2.clicked.connect(self.reset_func_3)
        self.pushButton_6.clicked.connect(self.reset_func_4)
        self.pushButton_8.clicked.connect(self.clear_all_funcs)
        # draw button
        self.pushButton_4.clicked.connect(self.draw_func)
        # set scene
        self.graphicsView.setScene(self.scene)
        # export as png
        self.actionExport_as_PNG.triggered.connect(self.export_as_png)
        # save (csv)
        self.actionSave.triggered.connect(self.save_functions_to_csv)
        # Draw Action in menu
        self.actionDraw.triggered.connect(self.draw_func)
        # Functions x^2 and x^3
        self.actionX.triggered.connect(lambda: self.draw_preset_function([0, 0, 0, 1]))
        self.actionX_2.triggered.connect(lambda: self.draw_preset_function([0, 0, 1, 0]))
        # help/ user Guide Action
        self.actionUser_Guide.triggered.connect(self.open_user_guide)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
    def update_equation_label(self):
        # get functions values inputs
        # function 1
        f1_x_cube = self.lineEdit_20.text().strip()
        f1_x_square = self.lineEdit_21.text().strip()
        f1_x = self.lineEdit_22.text().strip()
        f1_c = self.lineEdit_23.text().strip()
        # function 2
        f2_x_cube = self.lineEdit_24.text().strip()
        f2_x_square = self.lineEdit_25.text().strip()
        f2_x = self.lineEdit_26.text().strip()
        f2_c = self.lineEdit_27.text().strip()
        # function 3
        f3_x_cube = self.lineEdit_28.text().strip()
        f3_x_square = self.lineEdit_29.text().strip()
        f3_x = self.lineEdit_30.text().strip()
        f3_c = self.lineEdit_31.text().strip()
        # function 4
        f4_x_cube = self.lineEdit_32.text().strip()
        f4_x_square = self.lineEdit_33.text().strip()
        f4_x = self.lineEdit_34.text().strip()
        f4_c = self.lineEdit_35.text().strip()

        # equation label for each function
        # function 1
        f1_equation_parts = []

        if f1_x_cube and f1_x_cube != "0":
            f1_equation_parts.append(f"{f1_x_cube}x^3")
        if f1_x_square and f1_x_square != "0":
            prefix = " - " if f1_x_square.startswith('-') else " + "
            f1_equation_parts.append(f"{prefix}{f1_x_square.lstrip('-')}x^2")
        if f1_x and f1_x != "0":
            prefix = " - " if f1_x.startswith('-') else " + "
            f1_equation_parts.append(f"{prefix}{f1_x.lstrip('-')}x")
        if f1_c and f1_c != "0":
            prefix = " - " if f1_c.startswith('-') else " + "
            f1_equation_parts.append(f"{prefix}{f1_c.lstrip('-')}")

        # if first term is '-', prefix shouldn't start a space
        if f1_equation_parts:
            first_term = f1_equation_parts.pop(0)
            f1_equation = "y = " + first_term
            if f1_equation_parts:
                f1_equation += " " + " ".join(f1_equation_parts)
        else:
            f1_equation = ""

        self.label_33.setText(f1_equation)


        # function 2
        f2_equation_parts = []

        if f2_x_cube and f2_x_cube != "0":
            f2_equation_parts.append(f"{f2_x_cube}x³")
        if f2_x_square and f2_x_square != "0":
            prefix = " - " if f2_x_square.startswith('-') else " + "
            f2_equation_parts.append(f"{prefix}{f2_x_square.lstrip('-')}x²")
        if f2_x and f2_x != "0":
            prefix = " - " if f2_x.startswith('-') else " + "
            f2_equation_parts.append(f"{prefix}{f2_x.lstrip('-')}x")
        if f2_c and f2_c != "0":
            prefix = " - " if f2_c.startswith('-') else " + "
            f2_equation_parts.append(f"{prefix}{f2_c.lstrip('-')}")

        # if first term is '-', prefix shouldn't start a space
        if f2_equation_parts:
            first_term = f2_equation_parts.pop(0)
            f2_equation = "y = " + first_term
            if f2_equation_parts:
                f2_equation += " " + " ".join(f2_equation_parts)
        else:
            f2_equation = ""

        self.label_34.setText(f2_equation)

        # function 3
        f3_equation_parts = []

        if f3_x_cube and f3_x_cube != "0":
            f3_equation_parts.append(f"{f3_x_cube}x³")
        if f3_x_square and f3_x_square != "0":
            prefix = " - " if f3_x_square.startswith('-') else " + "
            f3_equation_parts.append(f"{prefix}{f3_x_square.lstrip('-')}x²")
        if f3_x and f3_x != "0":
            prefix = " - " if f3_x.startswith('-') else " + "
            f3_equation_parts.append(f"{prefix}{f3_x.lstrip('-')}x")
        if f3_c and f3_c != "0":
            prefix = " - " if f3_c.startswith('-') else " + "
            f3_equation_parts.append(f"{prefix}{f3_c.lstrip('-')}")

        # if first term is '-', prefix shouldn't start a space
        if f3_equation_parts:
            first_term = f3_equation_parts.pop(0)
            f3_equation = "y = " + first_term
            if f3_equation_parts:
                f3_equation += " " + " ".join(f3_equation_parts)
        else:
            f3_equation = ""

        self.label_35.setText(f3_equation)

        # function 4
        f4_equation_parts = []

        if f4_x_cube and f4_x_cube != "0":
            f4_equation_parts.append(f"{f4_x_cube}x³")
        if f4_x_square and f4_x_square != "0":
            prefix = " - " if f4_x_square.startswith('-') else " + "
            f4_equation_parts.append(f"{prefix}{f4_x_square.lstrip('-')}x²")
        if f4_x and f4_x != "0":
            prefix = " - " if f4_x.startswith('-') else " + "
            f4_equation_parts.append(f"{prefix}{f4_x.lstrip('-')}x")
        if f4_c and f4_c != "0":
            prefix = " - " if f4_c.startswith('-') else " + "
            f4_equation_parts.append(f"{prefix}{f4_c.lstrip('-')}")

        # if first term is '-', prefix shouldn't start a space
        if f4_equation_parts:
            first_term = f4_equation_parts.pop(0)
            f4_equation = "y = " + first_term
            if f4_equation_parts:
                f4_equation += " " + " ".join(f4_equation_parts)
        else:
            f4_equation = ""

        self.label_36.setText(f4_equation)
        # equation label for each functions end

    def setup_validators(self):
        # validator for all inputs
        reg_ex_1 = QRegExp("^[-+]?[0-9]*$")  # for coeff inputs
        reg_ex_2 = QRegExp("^[-+]?[0-9]+(\.[0-9]+)?$")  # for coordinate range inputs
        input_validator = QRegExpValidator(reg_ex_1, self)
        input_validator_coord_range = QRegExpValidator(reg_ex_2, self)

        # Binding to the textChanged signal and validate for a QLineEdit widgets
        lineEdits = [self.lineEdit_20, self.lineEdit_21, self.lineEdit_22, self.lineEdit_23,
                     self.lineEdit_24, self.lineEdit_25, self.lineEdit_26, self.lineEdit_27,
                     self.lineEdit_28, self.lineEdit_29, self.lineEdit_30, self.lineEdit_31,
                     self.lineEdit_32, self.lineEdit_33, self.lineEdit_34, self.lineEdit_35
                     ]

        for lineEdit in lineEdits:
            lineEdit.textChanged.connect(self.check_validity)
            lineEdit.setValidator(input_validator)
        # validate for coordinate range inputs
        self.lineEdit_18.setValidator(input_validator_coord_range)
        self.lineEdit_19.setValidator(input_validator_coord_range)
        self.lineEdit_36.setValidator(input_validator_coord_range)
        self.lineEdit_37.setValidator(input_validator_coord_range)


    def check_validity(self, text):
        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(text, 0)[0]
        '''
        the QRegExpValidator is set to accept only +, - and 0-9 characters, 
        there is no need to show the error message in the screen below. 
        but I wrote this in case it wants to be added in the future. hence the comment. 
        '''
        '''
        if state != QRegExpValidator.Acceptable:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter a valid number.')
            sender.clear()
        '''

    # functions for drawing graphics
    def plot_polynomial(self, ax, coefficients, x_range):

        x_values = np.linspace(x_range[0], x_range[1], 5000)
        y_values = np.polyval(coefficients, x_values)
        ax.plot(x_values, y_values, label='', antialiased=True)
        ax.set_aspect('auto')
        return x_values, y_values




    def find_intercepts(self, coefficients):
        y_intercept = np.polyval(coefficients, 0)
        roots = np.roots(coefficients)
        x_intercepts = roots[np.isreal(roots)].real
        return x_intercepts, y_intercept

    def find_extrema(self, coefficients, x_range):
        # calculate derivative
        derivative_coeffs = np.polyder(coefficients)
        # roots
        critical_points = np.roots(derivative_coeffs)
        # get reel roots
        critical_points = critical_points[np.isreal(critical_points)].real

        # get second derivative for max and min points
        second_derivative_coeffs = np.polyder(derivative_coeffs)

        max_points = []
        min_points = []

        # at each critical point, determine max/min by looking at the sign of the second derivative
        for point in critical_points:
            second_derivative_value = np.polyval(second_derivative_coeffs, point)

            # if the second derivative is positive, it's minimum, if the second derivative is negative, it's maximum
            if second_derivative_value > 0:
                min_points.append((point, np.polyval(coefficients, point)))
            elif second_derivative_value < 0:
                max_points.append((point, np.polyval(coefficients, point)))

        # Filter points outside of x_range
        max_points = [(point, value) for point, value in max_points if x_range[0] <= point <= x_range[1]]
        min_points = [(point, value) for point, value in min_points if x_range[0] <= point <= x_range[1]]

        return max_points, min_points

    # get from inputs functions
    def get_function_from_input(self, lineEdit_x3, lineEdit_x2, lineEdit_x, lineEdit_c):
        # Get function coefficients from user inputs
        coefficients = [
            float(lineEdit_x3.text() if lineEdit_x3.text() else 0),
            float(lineEdit_x2.text() if lineEdit_x2.text() else 0),
            float(lineEdit_x.text() if lineEdit_x.text() else 0),
            float(lineEdit_c.text() if lineEdit_c.text() else 0)
        ]
        return coefficients


    def find_turning_points(self, coefficients):
        # derivate and turning points
        derivative = np.polyder(coefficients)
        roots = np.roots(derivative)
        turning_points = roots[np.isreal(roots)].real
        return turning_points

    def find_derivative(self, coefficients):
        derivative = np.polyder(np.poly1d(coefficients))
        derivative_coeffs = derivative.coefficients
        # Format coefficients
        formatted_coeffs = [int(c) if c.is_integer() else c for c in derivative_coeffs]
        return np.array(formatted_coeffs)
    def calculate_integral(self, coefficients, x_range):
        # Integral
        integral = np.polyint(coefficients)
        area = np.polyval(integral, x_range[1]) - np.polyval(integral, x_range[0])
        return area

    def get_coordinate_range(self, lineEdit_x_start, lineEdit_x_end, lineEdit_y_start, lineEdit_y_end):
        # Get coordinate range from user inputs
        x_start = float(lineEdit_x_start.text() if lineEdit_x_start.text() else -10)
        x_end = float(lineEdit_x_end.text() if lineEdit_x_end.text() else 10)
        y_start = float(lineEdit_y_start.text() if lineEdit_y_start.text() else -10)
        y_end = float(lineEdit_y_end.text() if lineEdit_y_end.text() else 10)

        return [(x_start, x_end), (y_start, y_end)]



    def set_function_inputs(self, function_number, coefficients):
        # This sets the input fields for the chosen function
        inputs = [self.findChild(QtWidgets.QLineEdit, f'lineEdit_{20 + 4 * (function_number - 1) + i}') for i in
                  range(4)]
        for line_edit, coeff in zip(inputs, coefficients[::-1]):
            line_edit.setText(str(coeff))

   # draw
    def draw_func(self):
        try:
            # graphic clearing
            self.figure.clear()
            ax = self.figure.add_subplot(111)

            # get function from checkbox
            functions_to_plot = []
            labels = []  # for labels.

            # add list
            function_inputs = [
                (self.checkBox_1, self.lineEdit_20, self.lineEdit_21, self.lineEdit_22, self.lineEdit_23),
                (self.checkBox_2, self.lineEdit_24, self.lineEdit_25, self.lineEdit_26, self.lineEdit_27),
                (self.checkBox_3, self.lineEdit_28, self.lineEdit_29, self.lineEdit_30, self.lineEdit_31),
                (self.checkBox_4, self.lineEdit_32, self.lineEdit_33, self.lineEdit_34, self.lineEdit_35),
            ]
            for index, (checkbox, *line_edits) in enumerate(function_inputs, start=1):
                if checkbox.isChecked():
                    coeffs = self.get_function_from_input(*line_edits)
                    functions_to_plot.append(coeffs)
                    labels.append(f"Function {index}")

            # Get x-axis range from user input
            x_range = self.get_coordinate_range(self.lineEdit_18, self.lineEdit_19, self.lineEdit_36, self.lineEdit_37)[0]

            y_range = self.get_coordinate_range(self.lineEdit_18, self.lineEdit_19, self.lineEdit_36, self.lineEdit_37)[1]
            x_range_func = [-200, 200]
            # Draw functions and add labels
            for i, coeffs in enumerate(functions_to_plot):
                x_values, y_values = self.plot_polynomial(ax, coeffs, x_range_func)
                ax.plot(x_values, y_values, label=labels[i])
                # print(coeffs)

                self.update_table(i, coeffs, x_range)

            # Graphic Settings
            ax.set_xlim(x_range)
            ax.set_ylim(y_range)
            ax.axhline(y=0, color='black', linewidth=1)
            ax.axvline(x=0, color='black', linewidth=1)
            ax.grid(linestyle="--")
            if functions_to_plot:
                ax.legend()

            # update canvas
            self.canvas.draw()

            # Add canvas to QGraphicsScene and show it
            self.scene.addWidget(self.canvas)
            self.graphicsView.setScene(self.scene)

        except Exception as e {e}")
:
            print(f"Error:
    def update_table(self, row, coeffs, x_range):
        x_intercepts, y_intercept = self.find_intercepts(coeffs)
        max_points, min_points = self.find_extrema(coeffs, x_range)

        # find the largest max and largest min values
        max_value = max(max_points, key=lambda item: item[1])[1] if max_points else 'N/A'
        min_value = min(min_points, key=lambda item: item[1])[1] if min_points else 'N/A'

        turning_points = self.find_turning_points(coeffs)
        derivative_coeffs = self.find_derivative(coeffs)
        integral = self.calculate_integral(coeffs, x_range)

        derivative_str = self.coeffs_to_str(derivative_coeffs)

        # Update Table
        self.tableWidget.setItem(row, 0, QTableWidgetItem(f"{max_value}"))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(f"{min_value}"))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(', '.join(f"{x:.2f}" for x in x_intercepts)))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(f"{y_intercept:.2f}"))
        self.tableWidget.setItem(row, 4, QTableWidgetItem(', '.join(f"{tp:.2f}" for tp in turning_points)))
        self.tableWidget.setItem(row, 5, QTableWidgetItem(derivative_str))
        self.tableWidget.setItem(row, 6, QTableWidgetItem(f"{integral:.2f}"))


    def coeffs_to_str(self, coeffs):
        # to convert coeffs to str
        terms = []
        degree = len(coeffs) - 1

        for i, coeff in enumerate(coeffs):
            if coeff == 0:
                continue  # if coeff == 0 =>> continue

            coeff_str = f"{int(coeff)}" if coeff.is_integer() else f"{coeff:.2f}"

            if degree - i == 0:
                # If x^0, do not add x
                terms.append(f"{coeff_str}")
            elif degree - i == 1:
                # If x^1, just add x
                terms.append(f"{coeff_str}*x")
            else:
                # Add x and its power in other cases
                terms.append(f"{coeff_str}*x^{degree - i}")
        return " + ".join(terms).replace("+-", "-")






    # reset functions
    def reset_func_1(self):
        self.lineEdit_20.clear()
        self.lineEdit_21.clear()
        self.lineEdit_22.clear()
        self.lineEdit_23.clear()
        self.checkBox_1.setChecked(False)
        self.clear_table_row(0)
        # update label
        self.update_equation_label()

    def reset_func_2(self):
        self.lineEdit_24.clear()
        self.lineEdit_25.clear()
        self.lineEdit_26.clear()
        self.lineEdit_27.clear()
        self.checkBox_2.setChecked(False)
        self.clear_table_row(1)
        # update label
        self.update_equation_label()

    def reset_func_3(self):
        self.lineEdit_28.clear()
        self.lineEdit_29.clear()
        self.lineEdit_30.clear()
        self.lineEdit_31.clear()
        self.checkBox_3.setChecked(False)
        self.clear_table_row(2)
        # update label
        self.update_equation_label()

    def reset_func_4(self):
        self.lineEdit_32.clear()
        self.lineEdit_33.clear()
        self.lineEdit_34.clear()
        self.lineEdit_35.clear()
        self.checkBox_4.setChecked(False)
        self.clear_table_row(3)
        # update label
        self.update_equation_label()

    def clear_all_funcs(self):
        self.reset_func_1()
        self.reset_func_2()
        self.reset_func_3()
        self.reset_func_4()
        self.lineEdit_18.clear()
        self.lineEdit_19.clear()
        self.lineEdit_36.clear()
        self.lineEdit_37.clear()
        self.tableWidget.clearContents()

    # To Clear Table row when use reset button
    def clear_table_row(self, row):
        for column in range(self.tableWidget.columnCount()):
            self.tableWidget.setItem(row, column, None)

    # reset functions end

    # MENUBAR ACTIONS


    # Preset Functions x^2 and x^3
    def draw_preset_function(self, coefficients):
        # Check if any function is not checked and use that one
        for i in range(1, 5):
            checkbox = getattr(self, f'checkBox_{i}')
            if not checkbox.isChecked():
                self.set_function_inputs(i, coefficients)
                checkbox.setChecked(True)
                self.draw_func()
                break

    # Help/ Open User Guide Functions
    def open_user_guide(self):
        guide_url = 'https://spiny-bronze-6b4.notion.site/EqualGrapher-User-Guide-0777fd5d9bca48d6b91a48c5275d900b'
        QDesktopServices.openUrl(QUrl(guide_url))


    #Export as Png
    def export_as_png(self):
        # Get the name and location of the file the user wants to save
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        default_file_path = os.path.join(desktop_path, "")
        fileName, _ = QFileDialog.getSaveFileName(self, "Export as PNG", default_file_path, "PNG Files (*.png)", options=options)
        if fileName:
            if not fileName.endswith('.png'):
                fileName += '.png'
            # Save the canvas on which the chart is drawn as PNG
            self.figure.savefig(fileName, bbox_inches='tight')


    def save_functions_to_csv(self):
        # get file path for saving
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        default_file_path = os.path.join(desktop_path, "")
        fileName, _ = QFileDialog.getSaveFileName(self, "Save CSV", default_file_path, "CSV Files (*.csv)", options=options)

        if fileName:
            if not fileName.endswith('.csv'):
                fileName += '.csv'

            with open(fileName, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # write CSV file headers
                writer.writerow(['Label', 'Max', 'Min', 'X Int', 'Y Int','Turning Points', 'Derivative', 'Area'])

                # write checked records
                for i in range(4):  # because of 4 functions
                    checkBox = getattr(self, f'checkBox_{i + 1}')
                    if checkBox.isChecked():
                        # Get function's information
                        label = f'Function {i + 1}'
                        coeffs = self.get_function_from_input(
                            *[getattr(self, f'lineEdit_{j}') for j in range(20 + i * 4, 24 + i * 4)])
                        max_points, min_points = self.find_extrema(coeffs, self.get_coordinate_range(self.lineEdit_18, self.lineEdit_19,self.lineEdit_36, self.lineEdit_37)[0])
                        # find the largest max and largest min values
                        max_value = max(max_points, key=lambda item: item[1])[1] if max_points else 'N/A'
                        min_value = min(min_points, key=lambda item: item[1])[1] if min_points else 'N/A'


                        x_intercepts, y_intercept = self.find_intercepts(coeffs)
                        turning_points = self.find_turning_points(coeffs)
                        derivative_coeffs = self.find_derivative(coeffs)
                        derivative_str = self.coeffs_to_str(derivative_coeffs)
                        integral = self.calculate_integral(coeffs,
                                                           self.get_coordinate_range(self.lineEdit_18, self.lineEdit_19, self.lineEdit_36, self.lineEdit_37)[0])

                        # write csv
                        writer.writerow([
                            label,
                            f"{max_value}",
                            f"{min_value}",
                            ', '.join(f"{x:.2f}" for x in x_intercepts),
                            f"{y_intercept:.2f}",
                            ', '.join(f"{point:.2f}" for point in turning_points),
                            ' '.join(f"{derivative_str}"),
                            f"{integral:.2f}"
                        ])

app = QtWidgets.QApplication(sys.argv)
main_window = MainApp()
main_window.show()
sys.exit(app.exec_())
