import subprocess
import time
import threading
import Queue


class FlushPipe(object):
    def __init__(self):
        self.command = ['python', './print_date.py']
        self.process = None
        self.process_output = Queue.LifoQueue(0)
        self.capture_output = threading.Thread(target=self.output_reader)

    def output_reader(self):
        for line in iter(self.process.stdout.readline, b''):
            self.process_output.put_nowait(line)

    def start_process(self):
        self.process = subprocess.Popen(self.command,
                                        stdout=subprocess.PIPE)
        self.capture_output.start()

    def get_output_for_processing(self):
        return self.process_output.get()

if __name__ == "__main__":
    flush_pipe = FlushPipe()
    flush_pipe.start_process()

    now = time.time()
    while time.time() - now < 10:
        print ">>>" + flush_pipe.get_output_for_processing()
        time.sleep(2.5)

    flush_pipe.capture_output.join(timeout=0.001)
    flush_pipe.process.kill()
