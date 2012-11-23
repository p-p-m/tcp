# coding:utf-8
import os
import sys
import time
import codecs
import logging
import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def pprint(*args):
    f = open('log\program.log', 'a')
    s = ' '.join([str(arg) for arg in args])
    f.write(s + '\n')
    f.close()


def _write_move(str): 
    f = codecs.open('log\move.log', 'a', 'utf-8')
    f.write(datetime.datetime.now().strftime("%d.%m.%Y %H:%M") + " ")
    f.write(str)
    f.write('\n')
    f.close() 


class MoveEventHandler(FileSystemEventHandler):
    """Saves all events, except modifing, into file log/move.log"""

    def on_moved(self, event):
        super(MoveEventHandler, self).on_moved(event)
        what = 'directory' if event.is_directory else 'file'
        str = u"Moved {0}: from {1} to {2}".format(what, event.src_path, event.dest_path)
        _write_move(str)
        
    def on_created(self, event):
        super(MoveEventHandler, self).on_created(event)
        what = 'directory' if event.is_directory else 'file'
        str = u"Created {0}: {1}".format(what, event.src_path)
        _write_move(str)

    def on_deleted(self, event):
        super(MoveEventHandler, self).on_deleted(event)
        what = 'directory' if event.is_directory else 'file'
        str = u"Deleted {0}: {1}".format(what, event.src_path)
        _write_move(str)

    def on_modified(self, event):
        super(MoveEventHandler, self).on_modified(event)
        # what = 'directory' if event.is_directory else 'file'
        # str = "Modified {0}: {1}".format(what, event.src_path)
        # _write_move(str)


if __name__ == "__main__":
    # import glob
    # path = 'C:\Program Files\Holter\Inbox\Doctors'
    # for d in glob.glob('C:\Program Files\Holter\Inbox\Doctors\*'):
    #     print unicode(d)
    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s - %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')
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