# Capture output from very long running python subprocess event driven

#### The problem
The problem I am facing is that I have a subprocess in python (ffmpeg process) that runs for hours or even days from which I'd like to capture the output. The subprocess its stdout/err.PIPE can easily grow huge and needs to be flushed otherwise the program will grow out of memory (limit of PIPE size). I do not like to constantly parse the output but ondemand (event driven) and very important, get the latest output from the sub-process.

#### Current approach
My current approach is to send the output to a LifoQueue with size 0 so I only keep the last result for when I need to process it.

#### Other attempts
I an other attempt I've tried to assign stdout to /dev/null and when needed re-assign it when I'd like to read the output but failed miserably thus far.

#### POC
As a proof of concept I have made these programs but I'd like to know if there is a more efficient/pythonic way of handling this issue, also I'd like to avoid using threads.

This is the best solution I could come-up with for now.

###### poc.py

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

##### print_date.py

    #!/usr/bin/env python
    import time

    if __name__ == "__main__":
        while True:
            print str(time.time())
            time.sleep(0.01)


##### output:

    >>>1520535158.51
    >>>1520535161.01
    >>>1520535163.51
    >>>1520535166.01
