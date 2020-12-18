import multiprocessing


class TaskData:
    def __init__(self,
                 Data: any = None,
                 IsFinished: bool = False):
        self.Data: any = Data
        self.IsFinished: bool = IsFinished


class ParallelMultiProcessing:
    def __init__(self, number_of_process=5):
        self.number_of_process = number_of_process

    def configure_process(self):
        self.manager = multiprocessing.Manager()
        # Define a list (queue) for tasks and computation results
        self.tasks = self.manager.Queue()
        self.results = self.manager.Queue()
        # Create process pool with four processes
        num_cores = multiprocessing.cpu_count()
        self.pool = multiprocessing.Pool(processes=self.number_of_process)
        self.processes = []

    def start_processes(self, process_id,process_function):
        # Initiate the worker processes
        for i in range(self.number_of_process):
            # Set process name
            process_name = 'P%i' % i
            # Create the process, and connect it to the worker function
            new_process = multiprocessing.Process(target=process_function, args=(process_id,process_name, self.tasks, self.results))
            # Add new process to the list of processes
            self.processes.append(new_process)
            # Start the process
            new_process.start()

    def add_task(self, task):
        self.tasks.put(task)

    def finish_tasks(self):
        # Quit the worker processes by sending them -1
        for i in range(self.number_of_process):
            finish_task = TaskData(IsFinished=True)
            self.tasks.put(finish_task)

    def check_processes(self, result_function):
        # Read calculation results
        num_finished_processes = 0
        while True:
            # Read result
            new_result = self.results.get()

            # Have a look at the results
            if new_result.IsFinished == True:
                # Process has finished
                num_finished_processes += 1
                if num_finished_processes == self.number_of_process:
                    break
            else:
                # Output result
                # print('Result:' + str(new_result))
                result_function(new_result)
