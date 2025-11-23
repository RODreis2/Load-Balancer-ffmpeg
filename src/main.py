import threading
import logging
import queue
import time
import glob

threads = list()
q = queue.Queue()


def conversion(
    input_path,
    output_path,
    video_codec="libx264",
    pixel_format="yuv420p",
    extra_args=None
):
  
    command = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", video_codec,
        "-pix_fmt", pixel_format,
    ]

    if extra_args:
        command.extend(extra_args)

    command.append(output_path)

    return command


def worker():
    output_path = "/videosmp4"
    files = glob.glob("/videos")

    extra_args = input(str("Do you wanna modify the standard comand: [Y/N]"))
    if extra_args == "Y" or "y" or "yes" or "Yes" or "YES":
        video_codec = input("Video codec: ")
        pixel_format = input("Pixel format: ")
        conversion_mp4(files,output_path,video_codec,pixel_format)

    else:
        conversion_mp4(files,output_path)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    for index in range(3):
        logging.info("Main   : create and start a thread %d.", index)
        x = threading.Thread(target=worker,)
        threads.append(x)
        x.start()
    
    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
