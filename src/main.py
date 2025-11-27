import threading
import subprocess
import logging
import queue
import glob

threads = list()
q = queue.Queue()
output_path = "./videosmp4"
video_codec="libx264"
pixel_format="yuv420p"

def ask_yes_no(prompt):
    while True:
        ans = input(prompt + " [y/n]: ").lower()
        if ans in ("y", "yes"):
            return True
        elif ans in ("n", "no"):
            return False
        else:
            print("Please answer with 'y' or 'n'.")

def conversion(input_path,output_path,video_codec,pixel_format):
    import os

    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    output_file = os.path.join(output_path, f"{name}.mp4")

    command = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", video_codec,
        "-pix_fmt", pixel_format,
        output_file
    ]

    return command

def worker():
    while True:
        file = q.get()  

        if file is None:
            q.task_done()
            break      

        command = conversion(file,output_path,video_codec,pixel_format)

        subprocess.run(command)

        q.task_done()

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    modify_params = ask_yes_no("Do you want to modify the default encoding parameters?")

    if modify_params:
        video_codec = input("Write your video codec parameter: ")
        pixel_format = input("Write your pixel format parameter: ")

    for file in glob.glob("./videos/*"):
        q.put(file)

    for index in range(3):
        logging.info("Main   : create and start a thread %d.", index)
        x = threading.Thread(target=worker)
        threads.append(x)
        x.start()
    
    q.join()

    for _ in range(3):  
        q.put(None)

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
