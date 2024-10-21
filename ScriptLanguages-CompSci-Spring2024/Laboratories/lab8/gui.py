import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QFileDialog, QFormLayout, QDateEdit, QSplitter, QLineEdit
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon
from datetime import datetime
import apache_log_parser as aph

class LogBrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Log Browser')
        self.setGeometry(100, 100, 1500, 600)
        self.all_log_entries = []
        self.current_index = -1
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Splitter for resizable sections
        splitter = QSplitter(Qt.Horizontal)

        # Master section (list and controls)
        master_layout = QVBoxLayout()
        self.log_list = QListWidget()
        self.log_list.itemSelectionChanged.connect(self.update_detail_view)
        master_layout.addWidget(self.log_list)

        # Controls setup
        controls_layout = QHBoxLayout()

        self.load_button = QPushButton("Open")
        self.load_button.clicked.connect(self.load_log_file)
        controls_layout.addWidget(self.load_button)

        self.from_date = QDateEdit(calendarPopup=True)
        self.from_date.setDate(QDate.currentDate().addDays(-1))
        self.from_date.setDisplayFormat("yyyy-MM-dd")
        controls_layout.addWidget(self.from_date)

        self.to_date = QDateEdit(calendarPopup=True)
        self.to_date.setDate(QDate.currentDate())
        self.to_date.setDisplayFormat("yyyy-MM-dd")
        controls_layout.addWidget(self.to_date)

        self.filter_button = QPushButton("Filter Logs")
        self.filter_button.clicked.connect(self.filter_logs)
        controls_layout.addWidget(self.filter_button)

        self.reset_button = QPushButton("Reset Filter")
        self.reset_button.clicked.connect(self.reset_filter)
        controls_layout.addWidget(self.reset_button)

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.show_previous_log)
        self.prev_button.setEnabled(False)
        controls_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.show_next_log)
        self.next_button.setEnabled(False)
        controls_layout.addWidget(self.next_button)

        master_layout.addLayout(controls_layout)

        # Creating master and detail widgets
        master_widget = QWidget(); master_widget.setLayout(master_layout)
        detail_widget = QWidget(); detail_widget.setLayout(self.setup_detail_view())

        # Add to splitter
        splitter.addWidget(master_widget)
        splitter.addWidget(detail_widget)
        main_layout.addWidget(splitter)

    def setup_detail_view(self):
        detail_layout = QFormLayout()
        self.remote_host_label = QLineEdit(); self.remote_host_label.setReadOnly(True)
        self.date_label = QLineEdit(); self.date_label.setReadOnly(True)
        self.time_label = QLineEdit(); self.time_label.setReadOnly(True)
        self.timezone_label = QLineEdit(); self.timezone_label.setReadOnly(True)
        self.method_label = QLineEdit(); self.method_label.setReadOnly(True)
        self.resource_label = QLineEdit(); self.resource_label.setReadOnly(True)
        self.status_code_label = QLineEdit(); self.status_code_label.setReadOnly(True)
        self.size_label = QLineEdit(); self.size_label.setReadOnly(True)

        detail_layout.addRow("Remote Host:", self.remote_host_label)
        detail_layout.addRow("Date:", self.date_label)
        detail_layout.addRow("Time:", self.time_label)
        detail_layout.addRow("Timezone:", self.timezone_label)
        detail_layout.addRow("Status Code:", self.status_code_label)
        detail_layout.addRow("Method:", self.method_label)
        detail_layout.addRow("Resource:", self.resource_label)
        detail_layout.addRow("Size:", self.size_label)

        return detail_layout

    def load_log_file(self):
        print("Loading log file...")
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Log File", "", "Log Files (*.log);;All Files (*)", options=options)
        if file_path:
            self.all_log_entries = aph.read_log_file(file_path)
            self.display_logs(self.all_log_entries)
            self.update_navigation_buttons()

    def display_logs(self, log_entries):
        print("Displaying logs...")
        self.log_list.clear()
        for entry in log_entries:
            display_text = f"{entry['date']} - {entry['remote_host']} - {entry['status_code']}"
            self.log_list.addItem(display_text)

    def update_detail_view(self):
        print("Updating detail view...")
        self.current_index = self.log_list.currentRow()
        if self.current_index >= 0:
            log_details = self.all_log_entries[self.current_index]
            self.display_log_details(log_details)
            self.update_navigation_buttons()

    def display_log_details(self, log_details):
        print(f"Displaying log details: {log_details}")
        self.remote_host_label.setText(log_details['remote_host'])
        self.date_label.setText(log_details['date'])
        self.time_label.setText(log_details['time'])
        self.timezone_label.setText(log_details['timezone'])
        self.method_label.setText(log_details['method'])
        self.resource_label.setText(log_details['resource'])
        self.status_code_label.setText(str(log_details['status_code']))
        self.size_label.setText(f"{log_details['response_size']} B")

    def filter_logs(self):
        print("Filtering logs...")
        from_date = self.from_date.date().toPyDate()
        to_date = self.to_date.date().toPyDate()
        filtered_logs = [entry for entry in self.all_log_entries if from_date <= datetime.strptime(entry['date'], '%Y-%m-%d').date() <= to_date]
        self.display_logs(filtered_logs)
        self.update_navigation_buttons()

    def reset_filter(self):
        print("Resetting filter...")
        self.display_logs(self.all_log_entries)
        self.update_navigation_buttons()

    def show_previous_log(self):
        if self.current_index > 0:
            self.log_list.setCurrentRow(self.current_index - 1)

    def show_next_log(self):
        if self.current_index < len(self.all_log_entries) - 1:
            self.log_list.setCurrentRow(self.current_index + 1)

    def update_navigation_buttons(self):
        print("Updating navigation buttons...")
        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.all_log_entries) - 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LogBrowserApp()
    ex.show()
    sys.exit(app.exec_())
