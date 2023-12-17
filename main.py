import sys
# from sympy import *
# import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QVBoxLayout, QTextEdit, QWidget, \
    QLineEdit, QScrollArea, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
# from linear_methods import *


class MyWindow(QMainWindow):
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

        self.font = QFont()
        self.font.setPointSize(10)
        self.font.setBold(True)
        self.font.setFamily('Segoe UI')

        self.tips_label = QLabel('Enter equations in terms of coefficients')
        self.tips_label.setAlignment(Qt.AlignHCenter)

        self.equation_label = QLabel('Equations:')
        self.equation_label.setFont(self.font)
        self.text_edit = QPlainTextEdit(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.text_edit)

        self.solver_label = QLabel('Select Method:')
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
        self.initial_guess.setText('Enter initial guess ex: "1 0 1"')
        self.initial_guess.hide()

        self.stopping_cond = QLabel('Stopping Conditions', self)
        self.cond_dropdown = QComboBox(self)
        self.cond_dropdown.addItem("Select a stopping condition")
        self.cond_dropdown.addItems(['Number of iterations', 'Absolute Relative Error'])
        self.cond_dropdown.activated.connect(self.non_direct_cond)

        self.stopping_cond.hide()
        self.cond_dropdown.hide()

        self.iterations_label = QLabel('Number of iterations:')
        self.iterations_spinbox = QSpinBox(self)
        self.iterations_spinbox.setMinimum(1)

        self.iterations_label.hide()
        self.iterations_spinbox.hide()

        self.error_label = QLabel('Absolute Relative Error:')
        self.error_spinbox = QDoubleSpinBox(self)  # set float
        self.error_spinbox.setMinimum(0.0)
        self.error_spinbox.setSingleStep(0.001)
        self.error_spinbox.setDecimals(10)

        self.error_label.hide()
        self.error_spinbox.hide()

        self.precision_label = QLabel('Precision:')
        self.precision_spinbox = QSpinBox(self)
        self.precision_spinbox.setMinimum(2)
        self.precision_spinbox.setValue(5)

        self.solve_button = QPushButton('Solve', self)
        self.solve_button.clicked.connect(self.solve_equation)

        self.solution_label = QLabel('Solution')
        self.solution_label.setAlignment(Qt.AlignHCenter)
        self.solution_label.setFont(self.font)
        self.solution_area = QTextEdit(self)
        self.solution_area.setReadOnly(True)

        self.layout.addWidget(self.tips_label)
        self.layout.addWidget(self.equation_label)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.solver_label)
        self.layout.addWidget(self.solver_dropdown)
        self.layout.addWidget(self.lu_dropdown)
        self.layout.addWidget(self.initial_guess)
        self.layout.addWidget(self.stopping_cond)
        self.layout.addWidget(self.cond_dropdown)
        self.layout.addWidget(self.iterations_label)
        self.layout.addWidget(self.iterations_spinbox)
        self.layout.addWidget(self.error_label)
        self.layout.addWidget(self.error_spinbox)
        self.layout.addWidget(self.precision_label)
        self.layout.addWidget(self.precision_spinbox)
        self.layout.addWidget(self.solve_button)
        self.layout.addWidget(self.solution_label)
        self.layout.addWidget(self.solution_area)
        self.setCentralWidget(self.main_widget)

    def update_ui(self):
        print(self.solver_dropdown.currentIndex())

        if self.solver_dropdown.currentIndex() == 1 or self.solver_dropdown.currentIndex() == 2:
            self.lu_dropdown.hide()
            self.initial_guess.hide()
            self.stopping_cond.hide()
            self.cond_dropdown.hide()
        elif self.solver_dropdown.currentIndex() == 3:
            self.lu_dropdown.show()
            self.lu_dropdown.setCurrentIndex(0)
            self.initial_guess.hide()
            self.stopping_cond.hide()
            self.cond_dropdown.hide()
        elif self.solver_dropdown.currentIndex() == 4 or self.solver_dropdown.currentIndex() == 5:
            self.lu_dropdown.hide()
            self.stopping_cond.show()
            self.initial_guess.show()
            self.cond_dropdown.show()
            self.cond_dropdown.setCurrentIndex(0)

        self.iterations_label.hide()
        self.iterations_spinbox.hide()
        self.error_label.hide()
        self.error_spinbox.hide()

    def non_direct_cond(self):
        print(self.cond_dropdown.currentIndex())
        if self.cond_dropdown.currentIndex() == 1:
            self.iterations_label.show()
            self.iterations_spinbox.show()
            self.error_label.hide()
            self.error_spinbox.hide()
        elif self.cond_dropdown.currentIndex() == 2:
            self.iterations_label.hide()
            self.iterations_spinbox.hide()
            self.error_label.show()
            self.error_spinbox.show()

    def solve_equation(self):
        equations = self.text_edit.toPlainText()
        method_ind = self.solver_dropdown.currentIndex()
        precision = self.precision_spinbox.text()
        solution = ""
        if len(equations) == 0 or equations.isspace():
            QMessageBox.warning(self, "Warning", "Please enter equations")
        else:
            if method_ind == 0:
                QMessageBox.warning(self, "Warning", "Please select method")
            elif method_ind == 1:
                # call gauss function with param >> matrix, significant figures
                solution = f'Solution for {self.solver_dropdown.currentText()} of equation "{equations} with precision {precision}".'
            elif method_ind == 2:
                # call gauss-jordan function with param >> matrix, significant figures
                solution = f'Solution for {self.solver_dropdown.currentText()} of equation "{equations} with precision {precision}".'
            elif method_ind == 3:
                lu_ind = self.lu_dropdown.currentIndex()
                if lu_ind == 0:
                    QMessageBox.warning(self, "Warning", "Please select lu format")
                elif lu_ind == 1:
                    # call lu-doolittle function with param >> matrix, significant figures
                    solution = f'Solution for {self.solver_dropdown.currentText()} of equation "{equations} with precision {precision}".'
                elif lu_ind == 2:
                    # call lu-crout function with param >> matrix, significant figures
                    solution = f'Solution for {self.solver_dropdown.currentText()} of equation "{equations} with precision {precision}".'
                else:
                    # call lu-cholesky function with param >> matrix, significant figures
                    solution = f'Solution for {self.solver_dropdown.currentText()} of equation "{equations} with precision {precision}".'
            elif method_ind == 4:
                init_guess = self.initial_guess.text()
                seidel_ind = self.cond_dropdown.currentIndex()
                if len(init_guess) == 0 or init_guess.isspace():
                    QMessageBox.warning(self, "Warning", "Please enter intiall guess")
                else:
                    if seidel_ind == 0:
                        QMessageBox.warning(self, "Warning", "Please select stopping condition")
                    elif seidel_ind == 1:
                        iterations = self.iterations_spinbox.text()
                        # call seidel-iterative function with param >> matrix, significant figures, iterations
                        solution = f'Solution for {self.solver_dropdown.currentText()} of equation "{equations} with precision {precision}".'
                    else:
                        error = self.error_spinbox.text()
                        # call seidel-tolerance function with param >> matrix, significant figures, error
                        solution = f'Solution for {self.solver_dropdown.currentText()} of equation "{equations} with precision {precision}".'
            else:
                init_guess = self.initial_guess.text()
                jacobi_ind = self.cond_dropdown.currentIndex()
                if len(init_guess) == 0 or init_guess.isspace():
                    QMessageBox.warning(self, "Warning", "Please enter intiall guess")
                else:
                    if jacobi_ind == 0:
                        QMessageBox.warning(self, "Warning", "Please select stopping condition")
                    elif jacobi_ind == 1:
                        iterations = self.iterations_spinbox.text()
                        # call seidel-iterative function with param >> matrix, significant figures, iterations
                        solution = f'Solution for {self.solver_dropdown.currentText()} of equation "{equations} with precision {precision}".'
                    else:
                        error = self.error_spinbox.text()
                        # call seidel-tolerance function with param >> matrix, significant figures, error
                        solution = f'Solution for {self.solver_dropdown.currentText()} of equation "{equations} with precision {precision}".'
        self.solution_area.setPlainText(solution)

    @staticmethod
    def handle_equations(self):
        return 'handle'

    @staticmethod
    def handle_initial_guess(self):
        return 'handle'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    equation_solver_app = MyWindow()
    equation_solver_app.show()
    sys.exit(app.exec_())
