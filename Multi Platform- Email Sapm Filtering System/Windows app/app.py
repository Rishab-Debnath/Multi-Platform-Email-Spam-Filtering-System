import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QComboBox, QHBoxLayout, QLabel
from simplegmail import Gmail
from simplegmail.query import construct_query
import pickle
from dateutil import parser
import numpy as np
import matplotlib.pyplot as plt


class MyWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.body = ""
        self.setWindowTitle("Email Viewer")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        label = QLabel("Newer Than")
        layout.addWidget(label)
        # Create a horizontal layout for the combo boxes
        combo_box_layout = QHBoxLayout()
        
        

        # Create drop-down for "Older Than"
        self.newer_than_combo = QComboBox()
        self.newer_than_combo.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'])
        combo_box_layout.addWidget(self.newer_than_combo)

        # Create another drop-down for additional options
        self.newer_combo = QComboBox()
        self.newer_combo.addItems(["days","month","year"])
        combo_box_layout.addWidget(self.newer_combo)

        # Add the horizontal layout to the main layout
        layout.addLayout(combo_box_layout)
        label2 = QLabel("Older Than")
        layout.addWidget(label2)
        second_row_layout = QHBoxLayout()
        self.older_than_combo = QComboBox()
        self.older_than_combo.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'])
        second_row_layout.addWidget(self.older_than_combo)
        self.older_combo = QComboBox()
        self.older_combo.addItems(["days","month","year"])
        second_row_layout.addWidget(self.older_combo)
        layout.addLayout(second_row_layout)
        


        # Create "Analyse" button
        analyse_button = QPushButton("Analyse")
        layout.addWidget(analyse_button)
        # Connect the button to the analyse_clicked function
        analyse_button.clicked.connect(self.analyse_clicked)

        #Generate Report
        analyse_button = QPushButton("Generate Report")
        layout.addWidget(analyse_button)
        analyse_button.clicked.connect(self.generate_report)

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        layout.addWidget(self.text_output)

        central_widget.setLayout(layout)
        self.spam_count = []
        self.ham_count = []


    def analyse_clicked(self):
        gmail = Gmail("client_secret.json")

        pipe = pickle.load(open("Spam_detection.pkl","rb"))

        query_params = {
            "newer_than": (int(self.newer_than_combo.currentText()),self.newer_combo.currentText()),
            "older_than": (int(self.older_than_combo.currentText()),self.older_combo.currentText())
        }

        messages = gmail.get_messages(query=construct_query(query_params))
        result_text = ""       
        for message in messages:
            body = message.plain
            if body is not None:
                output = pipe.predict([body])

            else:
                print("Skipping email with None content")
            
            if output == 1:
                
                sender = message.sender
                result_text += f"Spam: It is a spam mail and is from: {sender}\n"
                self.spam_count.append(1)
            elif output == 0:
                
                sender = message.sender
                result_text += f"Ham: It is not a spam mail and is from : {sender}\n"
                self.ham_count.append(1)
            self.text_output.setPlainText(result_text)

    def generate_report(self):
        s_data = len(self.spam_count)
        h_data = len(self.ham_count)
        categories = ['Spam', 'Ham']
        bar_positions = np.arange(len(categories))
        bar_width = 0.35

        plt.bar(bar_positions, [s_data, h_data], width=bar_width, label='Category 1')

        plt.xlabel('Categories')
        plt.ylabel('Values')
        plt.title('Grouped Bar Graph Example')
        plt.xticks(bar_positions, categories)

        # Display the plot
        plt.legend()
        plt.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
