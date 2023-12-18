import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QVBoxLayout, QTextEdit, QWidget, \
    QLineEdit, QScrollArea, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QMessageBox, QFrame
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from Service.LinearFactory import LinearFactory


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

        self.tips_label = QLabel('Enter equations in terms of coefficients')
        self.tips_label.setAlignment(Qt.AlignHCenter)

        self.equation_label = QLabel('Equations:')
        self.equation_label.setFont(font)
        self.text_edit = QPlainTextEdit(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.text_edit)
        self.scroll_area.setMinimumWidth(400)
        self.text_edit.setPlainText('2x + 3y + 4z =0\n-2x-y+z=0\n2x- z=0')

        self.param_label = QLabel('Parameters')  # adjust it
        self.param_label.setAlignment(Qt.AlignHCenter)
        self.param_label.setFont(font)
        self.solver_dropdown = QComboBox(self)
        self.solver_dropdown.addItem("Select a method")
        self.solver_dropdown.addItems(['Gauss Elimination', 'Gauss Jordan', 'LU Decomposition', 'Gauss Seidel', 'Jacobi Iteration'])
        self.solver_dropdown.activated.connect(self.update_ui)

        #  show for lu only
        self.lu_dropdown = QComboBox(self)
        self.lu_dropdown.addItem("Select a format")
        self.lu_dropdown.addItems(['Doolittle', 'Crout', 'Cholesky'])
        self.lu_dropdown.hide()

        #  show for gauss seidel & jacobi
        self.initial_guess = QLineEdit(self)
        self.initial_guess.setText('Enter initial guess ex: "1 0.5 1"')
        self.initial_guess.hide()

        self.stopping_cond = QLabel('Stopping Conditions', self)
        self.stopping_cond.setAlignment(Qt.AlignHCenter)
        self.stopping_cond.setFont(font)
        self.stopping_cond.hide()

        self.iterations_label = QLabel('Number of iterations:')

        self.iterations_spinbox = QSpinBox(self)
        self.iterations_spinbox.setRange(1, 100000)

        self.iterations_spinbox.setFixedSize(150, 30)

        self.iterations_label.hide()
        self.iterations_spinbox.hide()

        self.error_label = QLabel('Absolute Relative Error:')

        self.error_spinbox = QDoubleSpinBox(self)  # set float
        self.error_spinbox.setMinimum(0.0)
        self.error_spinbox.setSingleStep(0.001)
        self.error_spinbox.setDecimals(10)
        self.error_spinbox.setFixedSize(150, 30)

        self.error_label.hide()
        self.error_spinbox.hide()

        self.precision_label = QLabel('Precision:')

        self.precision_spinbox = QSpinBox(self)
        self.precision_spinbox.setMinimum(2)
        self.precision_spinbox.setValue(5)
        self.precision_spinbox.setFixedSize(150, 30)

        self.solve_button = QPushButton('Solve', self)
        self.solve_button.clicked.connect(self.solve_equation)
        self.solve_button.setFixedSize(150, 30)
        self.solve_button.setStyleSheet('background-color: #b0b0b0;')
        self.solve_button.setCursor(Qt.PointingHandCursor)


        self.solution_label = QLabel('Solution')
        self.solution_label.setAlignment(Qt.AlignHCenter)
        self.solution_label.setFont(font)

        self.solution_area = QTextEdit(self)
        self.solution_area.setReadOnly(True)
        self.solution_area.setTextColor(QColor('red'))
        self.solution_area.setMinimumHeight(250)

        self.scroll_sol = QScrollArea(self)
        self.scroll_sol.setWidgetResizable(True)
        self.scroll_sol.setWidget(self.solution_area)
        self.scroll_sol.setFont(QFont("Open Sans", 12))

        self.layout.addWidget(self.tips_label)
        self.layout.addSpacing(30)
        self.layout.addWidget(self.equation_label)
        self.layout.addWidget(self.scroll_area, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.param_label)
        self.layout.addWidget(self.solver_dropdown)
        self.layout.addWidget(self.lu_dropdown)
        self.layout.addWidget(self.initial_guess)
        self.layout.addWidget(self.stopping_cond)
        self.layout.addWidget(self.iterations_label)
        self.layout.addWidget(self.iterations_spinbox)
        self.layout.addWidget(self.error_label)
        self.layout.addWidget(self.error_spinbox)
        self.layout.addWidget(self.precision_label)
        self.layout.addWidget(self.precision_spinbox)
        self.layout.addWidget(self.solve_button, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.solution_label)
        self.layout.addWidget(self.scroll_sol)
        self.setCentralWidget(self.main_widget)

    def update_ui(self):

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

    def solve_equation(self):
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
                    solution = f'Solution for {self.solver_dropdown.currentText()} of equation "{equations} with precision {precision}".'+ f'\nTime consumed : {time.perf_counter() - start} s'
                elif lu_ind == 2:
                    start = time.perf_counter()
                    # call lu-crout function with param >> matrix, significant figures
                    solution = f'Solution for {self.solver_dropdown.currentText()} of equation "{equations} with precision {precision}".' + f'\nTime consumed : {time.perf_counter() - start} s'
                else:
                    start = time.perf_counter()
                    # call lu-cholesky function with param >> matrix, significant figures
                    solution = f'Solution for {self.solver_dropdown.currentText()} of equation "{equations} with precision {precision}".' + f'\nTime consumed : {time.perf_counter() - start} s'
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

    @staticmethod
    def handle_equations(self):
        return 'handle'

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
