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
