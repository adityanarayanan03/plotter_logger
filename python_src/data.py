import time
import csv

import logging
logging.basicConfig()
logger = logging.getLogger("data.py")
logger.setLevel(logging.DEBUG)

from threading import Lock

global plot_storage

class DataStorage:

    def __init__(self):
        self.logger = logging.getLogger("DataStorage")
        self.logger.setLevel(logging.DEBUG)

        self.x_points = dict()#{0: []}
        self.y_points = dict()#{0: []}
        self.next_line = 0#1
        self.num_points = dict()#{0: 0}
        self.fp_digits = dict()

        #Put stuff that should be drawn from config below this line
        self.windowSize = 1000
        self.prehistory_buffer_size = 1000
        self.prehistory_current_size = dict()#{0:0}
        self.prehistory_temp_name = f"temp_{int(time.time())}"

        #Set up some window data that the grapher will read from here
        self.window_min = 0
        self.window_max = 0

        #Set up prehistory buffer
        self.prehistory = dict()#{0: {'x': [None]*self.prehistory_buffer_size, 'y': [None]*self.prehistory_buffer_size}}

        #Why is this even neessary man
        self.kill_update_thread = False

        #synch
        self.lock = Lock()

    def _assert_line_exists(self, line):
        '''
        Makes sure the line exists, if it doesn't 
        exist, prints an error message and sets line to 0.
        '''
        if line not in self.x_points.keys():
            self.logger.error(f"No line {line}. Adding point to line 0 instead.")
            line = 0
        
        return line
    
    def add_point(self, x, y, line=0):
        '''
        Adds a point to the specified line.
        If no line passed, adds to the 0'th line.
        '''

        line = self._assert_line_exists(line)

        #Modify inputs x and y to account for (possible) fixed-point parameter
        x = x/(10**(self.fp_digits[line]['x']))
        y = y/(10**(self.fp_digits[line]['y']))

        self.lock.acquire(blocking=True)
    
        self.x_points[line].append(x)
        self.y_points[line].append(y)

        self.num_points[line] += 1

        if (self.get_num_points(line) > self.windowSize):
            self._remove_first_point(line)
        
        self.lock.release()
    
    def add_points(self, x_arr, y_arr, line):
        '''
        Adds a whole x buffer and y buffer to the line.
        Going to start without locking, but we might have 
        to lock this later.
        '''
        if(len(x_arr) != len(y_arr)):
            logger.error(f"Length mismatch in add_points, x_arr was len {len(x_arr)} and y_arr was len {len(y_arr)}")

        line = self._assert_line_exists(line)

        #fix x_arr and y_arr to take fp logic into account
        x_arr = [x/(10**(self.fp_digits[line]['x'])) for x in x_arr]
        y_arr = [y/(10**(self.fp_digits[line]['y'])) for y in y_arr]

        self.lock.acquire(blocking=True)

        self.x_points[line] += x_arr
        self.y_points[line] += y_arr

        self.num_points[line] += len(x_arr)

        if (self.get_num_points(line) > self.windowSize):
            n = self.get_num_points(line) - self.windowSize
            #logger.debug(f"in add_points, computed n is {n}")
            self._remove_first_n_points(line, n)
        
        self.lock.release()



    def _remove_first_point(self, line=0):
        '''
        Removes the oldest point from the history of 
        a specific line
        '''
        line = self._assert_line_exists(line)

        x_removed = self.x_points[line][0]
        y_removed = self.y_points[line][0]

        self.x_points[line] = self.x_points[line][1:]
        self.y_points[line] = self.y_points[line][1:]

        self.num_points[line] -= 1

        #Write to prehistory
        self._write_to_prehistory(x_removed, y_removed, line)
    
    def _remove_first_n_points(self, line, n):
        '''
        Removes the oldest n points from the history of 
        a specific line

        _remove_first_point is now just a special case 
        of _remove_first_n_points
        '''
        line = self._assert_line_exists(line)

        x_removed = self.x_points[line][0:n]
        y_removed = self.y_points[line][0:n]

        self.x_points[line] = self.x_points[line][n:]
        self.y_points[line] = self.y_points[line][n:]

        self.num_points[line] -= n

        #Write to prehistory
        for i in range(len(x_removed)):
            self._write_to_prehistory(x_removed[i], y_removed[i], line)

    
    def _write_to_prehistory(self, x, y, line):
        '''
        Writes a datapoint to the prehistory buffer. 
        Calls _save_prehistory_buffer when buffer is full
        '''

        if (self.prehistory_current_size[line] == self.prehistory_buffer_size):
            logger.debug("Reached prehistory buffer limit. Saving prehistory.")
            self._save_prehistory_buffer(line)
            self.prehistory_current_size[line] = 0
            return
        
        self.prehistory[line]['x'][self.prehistory_current_size[line]] = x
        self.prehistory[line]['y'][self.prehistory_current_size[line]] = y
        self.prehistory_current_size[line] += 1

        #logger.debug(f"Prehistory buffer size is {self.prehistory_current_size[line]}")
    
    def _save_prehistory_buffer(self, line):
        iterator = zip(self.prehistory[line]['x'], self.prehistory[line]['y'])

        with open(self.prehistory_temp_name + f"_line_{line}", "a", newline = "") as prehistory_csv:
            prehistory_out = csv.writer(prehistory_csv, delimiter=",")
            i=0
            for row in iterator:
                if(i<= self.prehistory_current_size[line]):
                    prehistory_out.writerow(row)
                    i += 1
                else:
                    break
        
        logger.debug("Successfully saved to prehistory file.")
    
    def _save_history(self, line):
        iterator = zip(self.x_points[line], self.y_points[line])

        with open(self.prehistory_temp_name + f"_line_{line}", "a", newline="") as csvfile:
            history_out = csv.writer(csvfile, delimiter=",")
            for row in iterator:
                history_out.writerow(row)


    def add_line(self, x_fp_digits = 0, y_fp_digits = 0):
        '''
        Adds a line to the plot and returns a handle (integer)
        to refer to it by in the future
        '''

        self.x_points[self.next_line] = []
        self.y_points[self.next_line] = []

        self.fp_digits[self.next_line] = {'x': x_fp_digits, 'y': y_fp_digits}

        #add a prehistory for the new line
        self.prehistory[self.next_line] = {'x': [None]*self.prehistory_buffer_size, 'y': [None]*self.prehistory_buffer_size}

        #add a line to num_points
        self.num_points[self.next_line] = 0
        self.prehistory_current_size[self.next_line] = 0

        to_return = self.next_line

        self.next_line += 1

        return to_return
    
    def get_line(self, line=0):

        self.lock.acquire(blocking = True)

        line = self._assert_line_exists(line)

        a, b = self.x_points[line], self.y_points[line]

        self.lock.release()

        return a,b
    
    def get_num_lines(self):
        return self.next_line

    def get_num_points(self, line=0):

        line = self._assert_line_exists(line)

        return self.num_points[line]
    
    def set_window_min_max(self, window_min, window_max):
        self.window_min = window_min
        self.window_max = window_max


    def cleanup(self):
        '''
        Saves the prehistory and current history
        '''
        self.logger.debug("Running cleanup routine on graph exit")
        for line in range(self.next_line):
            #save anything remaining in the prehistory buffer
            self._save_prehistory_buffer(line)

            #save the history buffer
            self._save_history(line)
        
        logger.debug("Setting kill to true in cleaup")
        self.kill_update_thread = True
    
    def __str__(self):
        '''string method, called on cast to string'''

        output = "\n"
        for line in self.x_points.keys():
            output += f"---LINE {line}---\n"

            for data_ind in range(len(self.x_points[line])):
                output += f" ({self.x_points[line][data_ind]},{self.y_points[line][data_ind]}) "

            output += f"\n---END OF LINE---\n\n\n"
        
        return output


if __name__ == "__main__":
    logger.info("data.py was run directly. Running test.")

    test_storage = DataStorage()

    test_storage.add_point(0, 0)
    test_storage.add_point(0, 1)

    second_line_handle = test_storage.add_line()

    test_storage.add_point(0, 0, second_line_handle)

    logger.info(str(test_storage))

else:
    global plot_storage

    logger.debug("data.py was imported. Creating global variable plot_storage in data.py")

    plot_storage = DataStorage()