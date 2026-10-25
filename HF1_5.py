import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,  
    QPushButton,
    QLabel,
    QLineEdit, 
    QComboBox
)
import matplotlib.pyplot as plt
import numpy as np
import random
import csv
import os
from datetime import datetime

class PerceptionTestWindow(QtWidgets.QMainWindow): 
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Perception test")   #tesztablak létrehozása, méret beállítása
        self.resize(700, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)


        self.output_folder = "" #kimeneti file-ok elérési útvonala, file nevek beállítása
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.csv_output_path = os.path.join(self.output_folder, f"percetion_results_{self.timestamp}.csv")

        self.background_square = QLabel()
        self.background_square.setFixedSize(500, 500)   #kísérleti háttér beállítása
        self.background_square.setStyleSheet("background-color: black")

        self.small_square = QLabel(self.background_square)
        self.small_square.setFixedSize(40, 40)  #megfigyelendő terület alapbeállítása
        self.small_square.setStyleSheet("background-color: black")

        main_layout.addWidget(
            self.background_square,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        mode_layout = QHBoxLayout()

        self.mode_label = QLabel("Test Mode:")                              #gombok, legördülő menü stb. létrehozása, beállítása
        self.mode_dropdown = QComboBox() 
        self.mode_dropdown.addItems(["","Basic Mode", "Random Mode"])

        mode_layout.addWidget(self.mode_label)
        mode_layout.addWidget(self.mode_dropdown)

        main_layout.addLayout(mode_layout)


        trial_layout = QHBoxLayout()
        
        self.trial_label = QLabel("Number of trials:")
        self.trial_number = QLineEdit()
        self.trial_count = 0
        trial_layout.addWidget(self.trial_label)
        trial_layout.addWidget(self.trial_number)

        main_layout.addLayout(trial_layout)
       

        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.clear_button = QPushButton("Next trial")
        self.results_button = QPushButton("Save results")

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.results_button)

        main_layout.addLayout(button_layout)

        self.color_value = 0
                
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.black_2_white)

        self.start_button.clicked.connect(self.start_test)
        self.stop_button.clicked.connect(self.timer.stop)
        self.clear_button.clicked.connect(self.clear)
        self.stop_button.clicked.connect(self.save_results)
        self.results_button.clicked.connect(self.plot_save_results)


        self.results = []
        self.trial_modes = []



    def start_test(self):
        mode_chosen = self.mode_dropdown.currentText() != ""
        trial_set = self.trial_number.text().strip() != ""

        if mode_chosen and trial_set:   #tesztmód beállítása (basic: megfigyelendő terület mindig középen, random: megfigyelendő terület random pozícióban jelenik meg)
            if self.mode_dropdown.currentText() == "Basic Mode":
                self.small_square.move(
                    (self.background_square.width() - self.small_square.width()) // 2,
                    (self.background_square.height() - self.small_square.height()) // 2
                )
            elif self.mode_dropdown.currentText() == "Random Mode":
                x = random.randint(0, self.background_square.width() - self.small_square.width())
                y = random.randint(0, self.background_square.height() - self.small_square.height())

                self.small_square.move(x, y)

            self.max_trials = int(self.trial_number.text())

            if self.trial_count < self.max_trials:
                self.timer.start(100)

    def black_2_white(self):    #fekete-fehér átmenetet generáló függvény
        self.color_value += 1

        self.small_square.setStyleSheet(
            f"background-color: rgb({self.color_value}, {self.color_value}, {self.color_value})"
        )

        if self.color_value >= 255:
            self.timer.stop()

    def clear(self):
        self.timer.stop()
        self.color_value = 0
        self.small_square.setStyleSheet("background-color: black")

    def save_results(self):                                         #eredmények mentés, plot-olása
        self.results.append(self.color_value /255 *100)
        self.trial_modes.append(self.mode_dropdown.currentText())

        self.trial_count += 1
    
        if self.trial_count >= self.max_trials:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.clear_button.setEnabled(False)

    def plot_save_results(self):
        mean = np.mean(self.results)
        SD = np.std(self.results)

        plt.errorbar(
            1, mean,
            yerr=SD,
            fmt="bo",
            capsize=4,
            label=f"Mean: {mean:.1f}% ± {SD:.1f}%"
        )

        plt.ylabel("Whiteness (%)")
        plt.ylim(0, round(mean)+10)
        plt.xticks([1], [f"{self.max_trials} trials"])
        plt.legend()
        plt.title(f"Perception test results-{self.mode_dropdown.currentText()}")

        plot_output_path = os.path.join(self.output_folder, f"perception_plot_{self.mode_dropdown.currentText()}_{self.timestamp}.png")
        plt.savefig(plot_output_path, dpi=300, bbox_inches="tight")
        print("Plot saved")
        plt.close()
        

    
        with open(self.csv_output_path, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["Trial", "Mode", "Whiteness (%)"])


            for i, (mode, result) in enumerate(zip(self.trial_modes, self.results), start=1):
                writer.writerow([
                    i,
                    mode,
                    result
                ])

        print("Data saved.")


        self.small_square.setStyleSheet("background-color: black")  #kiindulási állapot visszaállítása
        self.trial_number.clear()
        self.color_value = 0
        self.max_trials = 0
        self.trial_count = 0
        self.trial_number.setEnabled(True)
        self.mode_dropdown.setEnabled(True)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.clear_button.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = PerceptionTestWindow()
    window.show()

    sys.exit(app.exec())
