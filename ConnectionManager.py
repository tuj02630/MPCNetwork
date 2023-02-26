import threading

class ConnectionManager(threading.Thread):
    dc_array = []
    def run(self):
        
