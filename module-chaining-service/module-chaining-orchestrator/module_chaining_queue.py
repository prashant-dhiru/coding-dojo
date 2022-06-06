from queue import Queue, Full, Empty


class Module_Chaining_Queue:
    """
    serves as a single ready queue for all the task-trees
    """

    def __init__(self, maxsize=10):
        self.MAXSIZE = maxsize
        self.shared_ready_job_queue = Queue(maxsize=self.MAXSIZE)

    def submit_job_to_queue(self, task):
        try:
            self.shared_ready_job_queue.put_nowait(task)
        except Full as error:
            raise RuntimeError(f'Ready queue is full, current maxsize of queue is {self.MAXSIZE}') from error

    def fetch_job_from_queue(self):
        try:
            return self.shared_ready_job_queue.get_nowait()
        except Empty as error:
            raise RuntimeError(f'Ready queue is empty') from error

    def is_empty(self):
        return self.shared_ready_job_queue.empty()
