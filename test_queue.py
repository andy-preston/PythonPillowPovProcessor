"""Test if input queue"""
from imports.stream_input import InputQueue


input_queue = InputQueue("raw-video/dock*")
while True:
    try:
        print(input_queue.next())
    except StopIteration:
        print("END OF QUEUE")
        break
