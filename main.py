import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QVBoxLayout, QTextEdit, QWidget, \
    QLineEdit, QScrollArea, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QMessageBox, QFrame, QTabWidget, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from Service.LinearFactory import LinearFactory
from Service.NonLinearFactory import NonLinearFactory
from Service.plotter import Plotter


class MyWindow(QMainWindow):
    rows = 0
    columns = 0

    def __init__(self):
        super(MyWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(700, 700)
        self.setWindowTitle('Linear Equations Solver')
        self.setWindowIcon(QIcon('app_icon.png'))
        self.setMinimumSize(700, 700)
        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout(self.main_widget)

        win_font = QFont()
        win_font.setPointSize(10)
        win_font.setFamily('Segoe UI')
        self.setFont(win_font)

        font = win_font
        font.setBold(True)
        font.setPointSize(12)

        self.tab = QTabWidget(self.main_widget)
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.addContentToTab1(self.tab1)
        self.addContentToTab2(self.tab2)

        self.tab.addTab(self.tab1, 'Linear')
        self.tab.addTab(self.tab2, 'Non Linear')

        self.layout.addWidget(self.tab)
        self.setCentralWidget(self.main_widget)

    def addContentToTab1(self, tab):
        self.tips_label = QLabel('Enter equations in terms of coefficients')
        self.tips_label.setAlignment(Qt.AlignHCenter)

        self.equation_label = QLabel('Equations')
        # self.equation_label.setFont(font)
        self.text_edit = QPlainTextEdit(tab)
        self.scroll_area = QScrollArea(tab)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.text_edit)
        self.scroll_area.setMinimumWidth(400)
        self.text_edit.setPlainText('2x + 3y + 4z =0\n-2x-y+z=0\n2x- z=0')
        self.param_label = QLabel('Parameters')  # adjust it
        self.param_label.setAlignment(Qt.AlignHCenter)
        # self.param_label.setFont(font)
        self.solver_dropdown = QComboBox(tab)
        self.solver_dropdown.addItem("Select a method")
        self.solver_dropdown.addItems(
            ['Gauss Elimination', 'Gauss Jordan', 'LU Decomposition', 'Gauss Seidel', 'Jacobi Iteration'])
        self.solver_dropdown.activated.connect(self.update_linear)

        #  show for lu only
        self.lu_dropdown = QComboBox(tab)
        self.lu_dropdown.addItem("Select a format")
        self.lu_dropdown.addItems(['Doolittle', 'Crout', 'Cholesky'])
        self.lu_dropdown.hide()

        #  show for gauss seidel & jacobi
        self.initial_guess = QLineEdit(tab)
        self.initial_guess.setText('Enter initial guess ex: "1 0.5 1"')
        self.initial_guess.hide()

        self.stopping_cond = QLabel('Stopping Conditions', tab)
        self.stopping_cond.setAlignment(Qt.AlignHCenter)
        # self.stopping_cond.setFont(font)
        self.stopping_cond.hide()

        self.iterations_label = QLabel('Number of iterations:')

        self.iterations_spinbox = QSpinBox(tab)
        self.iterations_spinbox.setRange(1, 100000)
        self.iterations_spinbox.setFixedSize(150, 30)

        self.iterations_label.hide()
        self.iterations_spinbox.hide()

        self.error_label = QLabel('Absolute Relative Error:')

        self.error_spinbox = QDoubleSpinBox(tab)  # set float
        self.error_spinbox.setMinimum(0.0)
        self.error_spinbox.setSingleStep(0.001)
        self.error_spinbox.setDecimals(10)
        self.error_spinbox.setFixedSize(150, 30)

        self.error_label.hide()
        self.error_spinbox.hide()

        self.precision_label = QLabel('Precision:')

        self.precision_spinbox = QSpinBox(tab)
        self.precision_spinbox.setMinimum(2)
        self.precision_spinbox.setValue(5)
        self.precision_spinbox.setRange(2, 100000)
        self.precision_spinbox.setFixedSize(150, 30)

        self.solve_button = QPushButton('Solve', tab)
        self.solve_button.clicked.connect(self.solve_linear)
        self.solve_button.setFixedSize(150, 30)
        self.solve_button.setStyleSheet('background-color: #b0b0b0;')
        self.solve_button.setCursor(Qt.PointingHandCursor)

        self.solution_label = QLabel('Solution')
        self.solution_label.setAlignment(Qt.AlignHCenter)
        # self.solution_label.setFont(font)

        self.solution_area = QTextEdit(tab)
        self.solution_area.setReadOnly(True)
        self.solution_area.setTextColor(QColor('red'))
        self.solution_area.setMinimumHeight(250)

        self.scroll_sol = QScrollArea(tab)
        self.scroll_sol.setWidgetResizable(True)
        self.scroll_sol.setWidget(self.solution_area)
        self.scroll_sol.setFont(QFont("Open Sans", 12))

        # self.layout.addWidget(self.tips_label)
        # self.layout.addSpacing(30)
        layout = QVBoxLayout(tab)
        layout.addWidget(self.equation_label, alignment=Qt.AlignHCenter)
        layout.addWidget(self.scroll_area, alignment=Qt.AlignHCenter)
        layout.addWidget(self.param_label)
        layout.addWidget(self.solver_dropdown)
        layout.addWidget(self.lu_dropdown)
        layout.addWidget(self.initial_guess)
        layout.addWidget(self.stopping_cond)
        layout.addWidget(self.iterations_label)
        layout.addWidget(self.iterations_spinbox)
        layout.addWidget(self.error_label)
        layout.addWidget(self.error_spinbox)
        layout.addWidget(self.precision_label)
        layout.addWidget(self.precision_spinbox)
        layout.addWidget(self.solve_button, alignment=Qt.AlignHCenter)
        layout.addWidget(self.solution_label)
        layout.addWidget(self.scroll_sol)

    def addContentToTab2(self, tab):
        self.equation_label2 = QLabel('Equations')
        # self.equation_label.setFont(font)
        self.text_edit2 = QPlainTextEdit(tab)
        self.scroll_area2 = QScrollArea(tab)
        self.scroll_area2.setWidgetResizable(True)
        self.scroll_area2.setWidget(self.text_edit2)
        self.scroll_area2.setMinimumWidth(400)
        self.scroll_area2.setMinimumHeight(150)
        self.text_edit2.setPlainText('x**3 - 3*x + 4')
        self.param_label2 = QLabel('Parameters')  # adjust it
        self.param_label2.setAlignment(Qt.AlignHCenter)
        # self.param_label.setFont(font)
        self.solver_dropdown2 = QComboBox(tab)
        self.solver_dropdown2.addItem("Select a method")
        self.solver_dropdown2.addItems(
            ['Bisection', 'False Position', 'Fixed point', 'Newton Raphson 1', 'Newton Raphson 2', 'Secant Method'])
        self.solver_dropdown2.activated.connect(self.update_nonlinear)

        self.initial_guess2 = QLineEdit(tab)
        self.initial_guess2.setText('Enter the initial guess')
        # self.initial_guess2.hide()

        self.multiplicity_label = QLabel('Multiplicity', tab)
        self.multiplicity_spinbox = QSpinBox(tab)
        self.multiplicity_spinbox.setMinimum(1)
        self.multiplicity_spinbox.setValue(1)

        self.multiplicity_label.hide()
        self.multiplicity_spinbox.hide()

        self.stopping_cond2 = QLabel('Stopping Conditions', tab)
        self.stopping_cond2.setAlignment(Qt.AlignHCenter)
        # self.stopping_cond.setFont(font)
        self.stopping_cond2.hide()

        self.iterations_label2 = QLabel('Max number of iterations:')

        self.iterations_spinbox2 = QSpinBox(tab)
        self.iterations_spinbox2.setRange(1, 100000)
        self.iterations_spinbox2.setFixedSize(150, 30)
        self.iterations_spinbox2.setValue(50)

        self.error_label2 = QLabel('EPSILON:')

        self.error_spinbox2 = QDoubleSpinBox(tab)  # set float
        self.error_spinbox2.setMinimum(0.0)
        self.error_spinbox2.setSingleStep(0.001)
        self.error_spinbox2.setDecimals(10)
        self.error_spinbox2.setFixedSize(150, 30)
        self.error_spinbox2.setValue(0.00001)

        self.precision_label2 = QLabel('Precision:')

        self.precision_spinbox2 = QSpinBox(tab)
        self.precision_spinbox2.setMinimum(2)
        self.precision_spinbox2.setValue(5)
        self.precision_spinbox2.setRange(2, 100000)
        self.precision_spinbox2.setFixedSize(150, 30)

        horizontal_layout2 = QHBoxLayout()
        horizontal_layout2.addWidget(self.iterations_spinbox2)
        horizontal_layout2.addWidget(self.error_spinbox2)
        horizontal_layout2.addWidget(self.precision_spinbox2)

        horizontal_layout3 = QHBoxLayout()
        horizontal_layout3.addWidget(self.iterations_label2)
        horizontal_layout3.addWidget(self.error_label2)
        horizontal_layout3.addWidget(self.precision_label2)

        self.solve_button2 = QPushButton('Solve', tab)
        self.solve_button2.clicked.connect(self.solve_nonlinear)
        self.solve_button2.setFixedSize(150, 30)
        self.solve_button2.setStyleSheet('background-color: #b0b0b0;')
        self.solve_button2.setCursor(Qt.PointingHandCursor)

        self.plot_button2 = QPushButton('Plot', tab)
        self.plot_button2.clicked.connect(self.plot_function)
        self.plot_button2.setFixedSize(150, 30)
        self.plot_button2.setStyleSheet('background-color: #b0b0b0;')
        self.plot_button2.setCursor(Qt.PointingHandCursor)

        horizontal_layout1 = QHBoxLayout()
        horizontal_layout1.addWidget(self.solve_button2)
        horizontal_layout1.addWidget(self.plot_button2)

        self.solution_label2 = QLabel('Solution')
        self.solution_label2.setAlignment(Qt.AlignHCenter)
        # self.solution_label.setFont(font)

        self.solution_area2 = QTextEdit(tab)
        self.solution_area2.setReadOnly(True)
        self.solution_area2.setTextColor(QColor('red'))
        self.solution_area2.setMinimumHeight(250)

        self.scroll_sol2 = QScrollArea(tab)
        self.scroll_sol2.setWidgetResizable(True)
        self.scroll_sol2.setWidget(self.solution_area2)
        self.scroll_sol2.setFont(QFont("Open Sans", 12))

        layout = QVBoxLayout(tab)
        layout.addWidget(self.equation_label2, alignment=Qt.AlignHCenter)
        layout.addWidget(self.scroll_area2, alignment=Qt.AlignHCenter)
        layout.addWidget(self.param_label2)
        layout.addWidget(self.solver_dropdown2)
        layout.addWidget(self.initial_guess2)
        layout.addWidget(self.multiplicity_label)
        layout.addWidget(self.multiplicity_spinbox)
        layout.addWidget(self.stopping_cond2)
        layout.addLayout(horizontal_layout3)
        layout.addLayout(horizontal_layout2)
        layout.addLayout(horizontal_layout1)
        layout.addWidget(self.solution_label2)
        layout.addWidget(self.scroll_sol2)

    def update_linear(self):

        if self.solver_dropdown.currentIndex() == 1 or self.solver_dropdown.currentIndex() == 2:
            self.lu_dropdown.hide()
            self.initial_guess.hide()
            self.stopping_cond.hide()
            self.iterations_label.hide()
            self.iterations_spinbox.hide()
            self.error_label.hide()
            self.error_spinbox.hide()
        elif self.solver_dropdown.currentIndex() == 3:
            self.lu_dropdown.show()
            self.lu_dropdown.setCurrentIndex(0)
            self.initial_guess.hide()
            self.stopping_cond.hide()
            self.iterations_label.hide()
            self.iterations_spinbox.hide()
            self.error_label.hide()
            self.error_spinbox.hide()
        elif self.solver_dropdown.currentIndex() == 4 or self.solver_dropdown.currentIndex() == 5:
            self.lu_dropdown.hide()
            self.stopping_cond.show()
            self.initial_guess.show()
            self.iterations_label.show()
            self.iterations_spinbox.show()
            self.error_label.show()
            self.error_spinbox.show()

    def update_nonlinear(self):
        if self.solver_dropdown2.currentIndex() == 4 or self.solver_dropdown2.currentIndex() == 5:
            self.multiplicity_label.show()
            self.multiplicity_spinbox.show()
        else:
            self.multiplicity_label.hide()
            self.multiplicity_spinbox.hide()

    def solve_linear(self):
        equations = self.text_edit.toPlainText()
        equations_list = equations.split('\n')
        self.rows = len(equations_list)

        print(self.rows)
        print(equations_list)

        method_ind = self.solver_dropdown.currentIndex()
        precision = self.precision_spinbox.text()
        solution = ""
        if len(equations) == 0 or equations.isspace():
            QMessageBox.warning(self, "Warning", "Please enter equations")
        else:
            if method_ind == 0:
                QMessageBox.warning(self, "Warning", "Please select method")
            elif method_ind == 1:
                start = time.perf_counter()
                # call gauss function with param >> matrix, significant figures
                solution = LinearFactory(self.solver_dropdown.currentText(), equations_list, precision).create().execute() + f'\nTime consumed : {time.perf_counter() - start} s'
            elif method_ind == 2:
                start = time.perf_counter()
                # call gauss-jordan function with param >> matrix, significant figures
                solution = LinearFactory(self.solver_dropdown.currentText(), equations_list, precision).create().execute() + f'\nTime consumed : {time.perf_counter() - start} s'
            elif method_ind == 3:
                lu_ind = self.lu_dropdown.currentIndex()
                if lu_ind == 0:
                    QMessageBox.warning(self, "Warning", "Please select lu format")
                elif lu_ind == 1:
                    start = time.perf_counter()
                    # call lu-doolittle function with param >> matrix, significant figures
                    solution = LinearFactory(self.lu_dropdown.currentText(), equations_list, precision).create().execute() + f'\nTime consumed : {time.perf_counter() - start} s'
                elif lu_ind == 2:
                    start = time.perf_counter()
                    # call lu-crout function with param >> matrix, significant figures
                    solution = LinearFactory(self.lu_dropdown.currentText(), equations_list, precision).create().execute() + f'\nTime consumed : {time.perf_counter() - start} s'
                else:
                    start = time.perf_counter()
                    # call lu-cholesky function with param >> matrix, significant figures
                    solution = LinearFactory(self.lu_dropdown.currentText(), equations_list, precision).create().execute() + f'\nTime consumed : {time.perf_counter() - start} s'
            elif method_ind == 4:
                # init_guess = self.handle_initial_guess(self.initial_guess.text())
                init_guess = self.handle_initial_guess(self.initial_guess.text())
                if len(init_guess) != 0:
                    iterations = self.iterations_spinbox.text()
                    start = time.perf_counter()
                    error = self.error_spinbox.text()
                    # aug = [[2, 3, 4, 0],
                    #        [-2, -1, 1, 0],
                    #        [2, 0, -1, 0]]
                    # guess = [0, 0, 0]
                    # call seidel function with param >> matrix, significant figures, iterations, error
                    # solution = f'Solution for {self.solver_dropdown.currentText()} of equation "{equations} with precision {precision}".' + f'\nTime consumed : {time.perf_counter() - start} s'
                    solution = LinearFactory(self.solver_dropdown.currentText(), equations_list, precision, init_guess, iterations, error).create().execute() + f'\nTime consumed : {time.perf_counter() - start} s'
            else:
                init_guess = self.handle_initial_guess(self.initial_guess.text())
                # init_guess = self.initial_guess.text()
                if len(init_guess) != 0:
                    iterations = self.iterations_spinbox.text()
                    error = self.error_spinbox.text()
                    start = time.perf_counter()
                    # aug = [[5, -1, 1, 10],
                    #        [2, 8, -1, 11],
                    #        [-1, 1, 4, 3]]
                    # guess = [0, 0, 0]
                    print(init_guess)
                    # call jacobi function with param >> matrix, significant figures, iterations, error
                    solution = LinearFactory(self.solver_dropdown.currentText(), equations_list, precision, init_guess, iterations, error).create().execute() + f'\nTime consumed : {time.perf_counter() - start} s'

        self.solution_area.setPlainText(solution)

    def plot_function(self):
        equations = self.text_edit2.toPlainText()
        Plotter(equations).plot_fun()

    def solve_nonlinear(self):
        equation = self.text_edit2.toPlainText()
        equations_list = equation.split('\n')
        self.rows = len(equations_list)

        print(self.rows)
        print(equations_list)

        method_ind = self.solver_dropdown2.currentIndex()
        precision = self.precision_spinbox2.text()
        epsilon = self.error_spinbox2.text()
        max_it = self.iterations_spinbox2.text()
        guess = self.initial_guess2.text().split(", ")

        solution = ""
        if len(equation) == 0 or equation.isspace():
            QMessageBox.warning(self, "Warning", "Please enter equations")
        else:
            if method_ind == 0:
                QMessageBox.warning(self, "Warning", "Please select method")
            elif method_ind == 1: #Bisection
                start = time.perf_counter()
                # call bisection function with param >> function, precision, initial_guess, max_iterations, epsilon
                solution = NonLinearFactory(self.solver_dropdown2.currentText(), equation, precision, guess, max_it, epsilon).create().execute() + f'\nTime consumed : {time.perf_counter() - start} s'
            elif method_ind == 2:
                start = time.perf_counter()
                # call regula falsi function with param >> function, precision, initial_guess, max_iterations, epsilon
                solution = NonLinearFactory(self.solver_dropdown2.currentText(), equation, precision, guess, max_it, epsilon).create().execute() + f'\nTime consumed : {time.perf_counter() - start} s'
            elif method_ind == 3:
                start = time.perf_counter()
                # call fixed point function with param >>
                solution = NonLinearFactory(self.solver_dropdown2.currentText(), equation, precision, guess, max_it, epsilon).create().execute() + f'\nTime consumed : {time.perf_counter() - start} s'
            elif method_ind == 4:
                # call newton raphson 1
                start = time.perf_counter()
                multiplicity = self.multiplicity_spinbox.text()
                solution = NonLinearFactory(self.solver_dropdown2.currentText(), equation, precision, guess, max_it, epsilon).create().execute(float(guess[0]), int(multiplicity)) + f'\nTime consumed : {time.perf_counter() - start} s'
            elif method_ind == 5:
                start = time.perf_counter()
                # call newton raphson 2
                solution = NonLinearFactory(self.solver_dropdown2.currentText(), equation, precision, guess, max_it, epsilon).create().execute() + f'\nTime consumed : {time.perf_counter() - start} s'
            else:
                start = time.perf_counter()
                # call secant
                solution = NonLinearFactory(self.solver_dropdown2.currentText(), equation, precision, guess, max_it, epsilon).create().execute(float(guess[1]), float(guess[0])) + f'\nTime consumed : {time.perf_counter() - start} s'

        self.solution_area2.setPlainText(solution)

    def handle_initial_guess(self, initial_guess):
        guess_list = initial_guess.split(' ')
        print(guess_list)
        if len(guess_list) == 0:
            QMessageBox.warning(self, 'Warning', 'Please enter initial guess vector')
            return []
        if len(guess_list) != self.rows:
            QMessageBox.warning(self, 'Warning', 'Initial guess vector size must be equal the number of equations')
            return []
        try:
            k = 0
            for i in guess_list:
                guess_list[k] = float(i)
                k += 1
            return guess_list
        except ValueError:
            return []


if __name__ == '__main__':
    app = QApplication(sys.argv)
    equation_solver_app = MyWindow()
    equation_solver_app.show()
    sys.exit(app.exec_())
