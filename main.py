import os
import time
import pyperclip
import psutil
from pathlib import Path
from datetime import datetime

app_data_count = 4 # The amount of different data types for each app

clear = lambda: os.system('cls')

def process_is_running(process_name):
    for proc in psutil.process_iter(attrs=['name']):
        if process_name.lower() in proc.info['name'].lower():
            return True
    return False

# Class for defining the different apps in runtime
class App:
    def __init__(self, name, time_used, exec_path, last_date):
        self.name           = name.lower()
        self.time_used      = time_used
        self.exec_path      = exec_path
        self.last_used_date = last_date
    
    def open_app(self):
        os.startfile(self.exec_path)
    
    def __str__(self):
        return f"{self.name.capitalize()}\nTime Used: {round(float(self.time_used)/3600, 1)}h\nLast used: {self.last_used_date}\n"

# Main Tool class to setup the program itself
class Tool:
    def __init__(self):

        # Read all available apps and their data into an array
        # Each line in apps.txt will hold 1 type of data of each app
        # Data Count: 4
        self.app_data_file = self.open_app_data_file() # Reads the apps.txt if exists, otherwise creates one
        self.app_data = [] # this will contain the data for each app from the .txt
        self.read_app_data()
        self.current_app = '' # This holds the current running app to keep track of time for it

        # Overall vars for the app to keep track of
        self.apps = []
        self.running = True
        self.app_running = False

        self.opening_time = 0
        self.closing_time = 0

        self.init_apps()

    # Main loop for the app
    def run(self):
        while self.running:
            clear()
            if not self.app_running:
                dt = datetime.now()
                print(dt.strftime("%A, %d. %B %Y %I:%M%p"))
            if self.app_running:
                # Todo: check if the app is opened, only then check if it was closed
                if process_is_running(self.current_app):
                    self.check_running_app()
            else:
                self.show_all_apps()
                self.handle_input()
    
    def open_app_data_file(self):
        # Check if there already is an app list
        try:
            return open(Path("apps.txt"), "r+")
        except FileNotFoundError:
            return open(Path("apps.txt"), "x")
    
    def show_all_apps(self):
        print("\nApps:\n")
        for app in self.apps:
            print(app)
    
    def read_app_data(self):
        try:
            self.app_data = self.app_data_file.readlines()
        except:
            self.app_data = []
    
    def handle_input(self):
        new_input = input("Add new App: <a>\nOpen App: <o>\nExit: <q>\n")
        # Handling the different inputs
        match new_input:
            case 'q':
                self.handling_exit()
                self.running = False
            case 'o':
                self.opening_time = time.time()
                app_to_open = input("Pleaser enter the name of the App from the list: ").strip().lower()
                for app in self.apps:
                    if app.name == app_to_open:
                        self.start_selected_app(app_to_open)
                        self.app_running = True
            case 'a':
                self.add_app_to_data()

    
    def init_apps(self):
        if self.app_data != []:
            for i in range(0, len(self.app_data), app_data_count):
                # Compute the data into an App
                # That then get added to the app list
                # 0: name
                # 1: time used
                # 2: executable path
                # 3: last date of using the app
                name = self.app_data[i].strip()
                time_used = self.app_data[i+1].strip()
                exec_path = self.app_data[i+2].strip()
                last_date = self.app_data[i+3].strip()
                self.apps.append(App(name, time_used, exec_path, last_date))
    
    def add_app_to_data(self):
        new_name = input('Enter the exact name of the App you are adding: ').strip()
        input('Copy the path to the executable with CTRL-C then press Enter.')
        new_path = pyperclip.paste()
        self.apps.append(App(new_name, '0', new_path, str(datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))))
        self.update_appdata_file()
    
    def handling_exit(self):
        self.update_appdata_file()
    
    def update_appdata_file(self):
        new_app_data = []
        self.app_data_file.close()
        self.app_data_file = self.open_app_data_file()

        for app in self.apps:
            new_app_data.append(app.name)
            new_app_data.append(app.time_used)
            new_app_data.append(app.exec_path)
            new_app_data.append(app.last_used_date)

        for value in new_app_data:
            self.app_data_file.write("%s\n" % (value))

    
    def write_to_text(self, data_list):
        for data in data_list:
            self.app_data_file.write(data)


    def start_selected_app(self, app_name):
        for app in self.apps:
            if app.name == app_name.lower():
                self.current_app = app.name
                app.open_app()
    
    def check_running_app(self):
        clear()
        print('App is running...')
        time.sleep(0.5)
        if not process_is_running(self.current_app.lower() + '.exe'):
            self.app_running = False
            self.closing_time = time.time()
            for app in self.apps:
                if app.name == self.current_app:
                    app.time_used = float(app.time_used) + self.closing_time - self.opening_time
                    app.last_used_date = str(datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))


tool = Tool()
tool.run()