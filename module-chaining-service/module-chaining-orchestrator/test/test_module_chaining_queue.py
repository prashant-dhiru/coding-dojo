import unittest

from module_chaining_queue import Module_Chaining_Queue


class MyTestCase(unittest.TestCase):
    def test_module_chaining_queue(self):
        data = "data"
        module_chaining_queue = Module_Chaining_Queue()
        module_chaining_queue.submit_job_to_queue(data)
        return_data = module_chaining_queue.fetch_job_from_queue()
        self.assertEqual(data, return_data)  # add assertion here

    def test_assert_raised_when_queue_overflow(self):
        data = "data"
        module_chaining_queue = Module_Chaining_Queue(1)
        module_chaining_queue.submit_job_to_queue(data)
        with self.assertRaises(RuntimeError):
            module_chaining_queue.submit_job_to_queue(data)

    def test_assert_raised_when_queue_underflow(self):
        data = "data"
        module_chaining_queue = Module_Chaining_Queue(1)
        module_chaining_queue.submit_job_to_queue(data)
        with self.assertRaises(RuntimeError):
            print(module_chaining_queue.fetch_job_from_queue())
            print(module_chaining_queue.fetch_job_from_queue())


if __name__ == '__main__':
    unittest.main()
