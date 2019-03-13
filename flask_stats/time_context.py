import sys
import time


class time_context():
    """ Debug context to trace any function calls inside the context """
    profile = None

    def __enter__(self):
        import line_profiler
        self.profile = line_profiler.LineProfiler()

    def __exit__(self, *args, **kwargs):
        print("***")
        #self.profile.print_stats()
        import atexit
        atexit.register(self.profile.print_stats)
