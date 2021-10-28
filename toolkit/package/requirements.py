import sys
import threading
import subprocess
from typing import List
from functools import partial

import pkg_resources

from toolkit.helpers.files import read_json
from toolkit.helpers.os import call_subprocess
from toolkit.helpers.network import check_connection

try:
    import tkinter as tk
    import tkinter.ttk as ttk

    run_in_tk = True

except ImportError:
    run_in_tk = False


def process_packages(command: str, *packages) -> int:
    call_subprocess((sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'))
    run_subprocess = subprocess.check_call((sys.executable, '-m', 'pip', command, *packages))

    if run_subprocess != 0:
        raise subprocess.SubprocessError('Сan\'t install package')
    return run_subprocess


def _process_requirements(to_install: List[str], to_delete: List[str]) -> int:
    if to_install:
        if not check_connection():
            raise ConnectionError('Can\'t connect to the internet')
        return process_packages('install', *to_install)

    if to_delete:
        return process_packages('uninstall', *to_delete)


def manage_requirements(requirements_file: str = 'requirements.json', dev: bool = False):
    requirements = read_json(requirements_file)
    requirements = requirements.get('dev') if dev else requirements.get('prod')

    to_install = set(f'{k.lower()}{"==" + v if v else ""}' for (k, v) in requirements.get('install').items())
    to_delete = set(v.project_name for v in pkg_resources.working_set.by_key.values()) \
        .intersection(set(requirements.get('delete')))
    to_delete = list(to_delete)
    if to_delete:
        to_delete.insert(len(to_delete), '-y')

    installed = set(str(v).replace(' ', '==').lower() for v in pkg_resources.working_set.by_key.values())
    to_install = to_install - installed

    if to_install or to_delete:
        function_call = partial(_process_requirements, to_install, to_delete)

        if run_in_tk:
            class App(tk.Tk):
                def __init__(self):
                    super().__init__()
                    self.geometry('500x300')
                    self.attributes('-disabled', True)

                    self.title('Toolkit. Requirements installation')
                    self.label = ttk.Label(self, text='Processing requirements', font=('Arial', 14))
                    self.label.pack(expand=True)

                    self.progress_bar = ttk.Progressbar(
                        self,
                        orient='horizontal',
                        mode='indeterminate',
                        length=280
                    )
                    self.progress_bar.pack()
                    self.progress_bar.start(5)

                    self.start_action()

                def start_action(self):
                    thread = threading.Thread(target=self.run_action)
                    thread.start()
                    self.check_thread(thread)

                def check_thread(self, thread):
                    if thread.is_alive():
                        self.after(100, lambda: self.check_thread(thread))
                    else:
                        self.label.configure(text='Done!')
                        self.after(1500)
                        self.destroy()

                def run_action(self):
                    function_call()

            app = App()
            app.mainloop()

        else:
            function_call()
