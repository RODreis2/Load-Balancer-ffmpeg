import threading
import logging
import queue
import time
import glob

threads = list()
q = queue.Queue()


def conversion_mp4(
    input_path,
    output_path,
    video_codec="libx264",
    pixel_format="yuv420p",
    extra_args=None
):
    """
    Converte vídeo para MP4 mantendo padrões,
    mas permitindo personalização.

    extra_args: lista opcional de argumentos adicionais do ffmpeg
    """
    command = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", video_codec,
        "-pix_fmt", pixel_format,
    ]

    # adiciona argumentos extras, se existirem
    if extra_args:
        command.extend(extra_args)

    # saída no final do comando
    command.append(output_path)

    return command


def worker():
    output_path = "/videosmp4"
    files = glob.glob("/videos")
    
    conversion_mp4("/videos",output_path)


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
