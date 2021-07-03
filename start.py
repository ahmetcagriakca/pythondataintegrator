import os
import subprocess
from multiprocessing import current_process
from multiprocessing.context import Process

from flask_restplus import api
class SubprocessService:
    @staticmethod
    def start(python_executable,application_name,path:str):
        print(f"Application : {application_name}")
        print(f"Process Name : {current_process().name}")
        print(f"Pid : {os.getpid()}")
        print(f"Parent Pid : {os.getppid()}")
        
        subprocess.call(f"{python_executable} {path}")
    
    @staticmethod
    def start_process(python_executable,application_name,path):
        
        proc = subprocess.Popen(f"{python_executable} {path}")
        # subprocess=Process(name=application_name,target=SubprocessService.start,args=(python_executable,application_name,path,))
        # subprocess.start()
        return proc
if __name__ == '__main__':

    python_executable= os.getenv("PYTHON_EXECUTABLE", "python")
    root_directory = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)))),'src')
    api_subprocess=SubprocessService.start_process(python_executable=python_executable, application_name="Pdi-Api",path=os.path.join(root_directory, "api", "app.py"))
    SubprocessService.start_process(python_executable=python_executable,application_name="Pdi-Scheduler",path=os.path.join(root_directory, "scheduler", "app.py"))
    SubprocessService.start_process(python_executable=python_executable,application_name="Pdi-Process",path=os.path.join(root_directory, "process", "app.py"))
    api_subprocess.wait()
    print("finished")