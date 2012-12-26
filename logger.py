# coding:utf-8
import time
import codecs
import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def pprint(*args):
    f = open('log\program.log', 'a')
    s = ' '.join([str(arg) for arg in args])
    print s
    f.write(s + '\n')
    f.close()


class MoveEventHandler(FileSystemEventHandler):
    """Saves all events, except modifing, into file log/move.log"""

    def on_moved(self, event):
        super(MoveEventHandler, self).on_moved(event)
        what = 'directory' if event.is_directory else 'file'
        str = u"Moved {0}: from {1} to {2}".format(what, event.src_path, event.dest_path)
        self._write_move(str)

    def on_created(self, event):
        super(MoveEventHandler, self).on_created(event)
        what = 'directory' if event.is_directory else 'file'
        str = u"Created {0}: {1}".format(what, event.src_path)
        self._write_move(str)

    def on_deleted(self, event):
        super(MoveEventHandler, self).on_deleted(event)
        what = 'directory' if event.is_directory else 'file'
        str = u"Deleted {0}: {1}".format(what, event.src_path)
        self._write_move(str)

    def on_modified(self, event):
        super(MoveEventHandler, self).on_modified(event)

    def _write_move(str):
        f = codecs.open('log\move.log', 'a', 'utf-8')
        f.write(datetime.datetime.now().strftime("%d.%m.%Y %H:%M") + " ")
        f.write(str)
        f.write('\n')
        f.close()


if __name__ == "__main__":
    path = 'C:\Program Files\Holter\Inbox\Doctors'
    event_handler = MoveEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
