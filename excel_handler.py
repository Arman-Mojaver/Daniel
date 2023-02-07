import os
import psutil
import keyboard

from time import sleep


class Process:
    def __init__(self, process_name, path):
        self.process_name = process_name
        self.path = path

    def start(self):
        os.startfile(self.path)

    @staticmethod
    def send_key(key):
        keyboard.send(hotkey=key)

    @staticmethod
    def wait(sec=1):
        sleep(sec)

    def kill(self):
        process_names = [process.name() for process in psutil.process_iter()]
        process = [process for process in psutil.process_iter() if process.name() == self.process_name]

        if not process:
            raise ValueError(
                f'The introduced process ({self.process_name}) is incorrect or not running: {process_names}'
            )

        if len(process) != 1:
            raise ValueError(
                f'There are more than one processes called {self.process_name} '
                f'that are currently running: {process_names}'
            )

        process[0].kill()


class ExcelProcess(Process):
    REFRESH_DATA_KEY = 'F9'
    PROCESS_NAME = 'EXCEL.EXE'

    def __init__(self, path, save_command='ctrl+g'):
        super().__init__(process_name=self.PROCESS_NAME, path=path)
        self.save_command = save_command

    def refresh_data(self):
        self.send_key(self.REFRESH_DATA_KEY)

    def save_file(self):
        self.send_key(self.save_command)

    def run(self):
        self.start()
        self.wait(sec=2)
        self.refresh_data()
        self.wait()
        self.save_file()
        self.wait()
        self.kill()


# file_path = 'Book1.xlsx'
file_path = 'Apertura.xlsx'
excel_process = ExcelProcess(path=file_path, save_command='ctrl+s')
excel_process.run()
