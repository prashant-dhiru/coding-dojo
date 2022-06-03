from abc import abstractmethod


class Task:
    def __int__(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def report(self):
        pass


class COCTask(Task):
    def __int__(self):
        pass

    def run(self):
        print("running coc task")

    def report(self):
        print("moving reports to desired directory")
