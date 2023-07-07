from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import mimetypes as mime

""" Create Handler for new audio files in working directory"""
class AudioFilesHandler(FileSystemEventHandler):
    def __init__(self, queue) -> None:
         super().__init__()
         self.queue = queue

    def on_created(self, event):
        #if event.is_directory == False:
        if event and ('audio' in mime.guess_type(event.src_path)[0]):
            self.queue.put(event.src_path)
            print("added_to_queue", event.src_path)

def create_observer(dir_to_observe, queue) -> None:
    event_handler = AudioFilesHandler(queue)
    observer = Observer()
    observer.schedule(event_handler, path= dir_to_observe, recursive= False)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    #observer.join()
    #TODO: create exceptions to avoid process stop