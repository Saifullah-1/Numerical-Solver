import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QVBoxLayout, QTextEdit, QWidget, \
    QLineEdit, QScrollArea, QPlainTextEdit, QSpinBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
# from linear_methods import *


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(600, 600)
        self.setWindowTitle('Linear Equations Solver')
        self.setWindowIcon(QIcon('app_icon.png'))
        self.setMinimumSize(600, 500)
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
        self.solver_dropdown.addItems(['Gauss Elimination', 'Gauss Jordan', 'LU Decomposition', 'Gauss Seidel', 'Jacobi Iteration'])
        self.solver_dropdown.activated.connect(self.update_ui)
        self.figures_label = QLabel('Number of significant figures:')
        self.figures_spinbox = QSpinBox(self)
        self.figures_spinbox.setMinimum(2)

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

        self.layout.addWidget(self.figures_label)
        self.layout.addWidget(self.figures_spinbox)
        self.layout.addWidget(self.solve_button)
        self.layout.addWidget(self.solution_label)
        self.layout.addWidget(self.solution_area)

        self.setCentralWidget(self.main_widget)

    def update_ui(self):
        self.layout.removeWidget(self.figures_label)
        self.layout.removeWidget(self.figures_spinbox)
        self.layout.removeWidget(self.solve_button)
        self.layout.removeWidget(self.solution_label)
        self.layout.removeWidget(self.solution_area)

        if self.solver_dropdown.currentIndex() == 2:
            self.method_choice('lu')
        elif self.solver_dropdown.currentIndex() == 3:
            self.method_choice('seidel')
        else:
            self.method_choice('jacobi')

        self.layout.addWidget(self.figures_label)
        self.layout.addWidget(self.figures_spinbox)
        self.layout.addWidget(self.solve_button)
        self.layout.addWidget(self.solution_label)
        self.layout.addWidget(self.solution_area)

    def solve_equation(self):
        equations = self.text_edit.toPlainText()
        solver = self.solver_dropdown.currentText()
        precision = self.figures_spinbox.text()
        solution = f'Solution for {solver} of equation "{equations} with precision {precision}".'

        self.solution_area.setPlainText(solution)

    def method_choice(self, method):
        if method == 'lu':
            self.lu_dropdown = QComboBox(self)
            self.lu_dropdown.addItems(['Doolittle', 'Crout', 'Cholesky'])
            self.layout.addWidget(self.lu_dropdown)
        elif method == 'seidel' or method == 'jacobi':
            self.initial_guess = QLineEdit(self)
            self.initial_guess.setText('Enter initial guess ex: "1 0 1"')

            stopping_cond = QLabel('Stopping Conditions', self)
            iterations_label = QLabel('Number of significant figures:')
            self.iterations_spinbox = QSpinBox(self)
            self.iterations_spinbox.setMinimum(1)

            error_label = QLabel('Absolute Relative Error:')
            self.error_spinbox = QSpinBox(self) # set float
            self.error_spinbox.setMinimum(0)

            self.layout.addWidget(self.initial_guess)
            self.layout.addWidget(stopping_cond)
            self.layout.addWidget(iterations_label)
            self.layout.addWidget(self.iterations_spinbox)
            self.layout.addWidget(error_label)
            self.layout.addWidget(self.error_spinbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    equation_solver_app = MyWindow()
    equation_solver_app.show()
    sys.exit(app.exec_())
