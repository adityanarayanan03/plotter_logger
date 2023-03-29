import time
import csv

import logging
logging.basicConfig()
logger = logging.getLogger("data.py")
logger.setLevel(logging.DEBUG)

global plot_storage

class DataStorage:

    def __init__(self):
        self.logger = logging.getLogger("DataStorage")
        self.logger.setLevel(logging.DEBUG)

        self.x_points = {0: []}
        self.y_points = {0: []}
        self.next_line = 1
        self.num_points = {0: 0}

        #Put stuff that should be drawn from config below this line
        self.windowSize = 200
        self.prehistory_buffer_size = 1000
        self.prehistory_current_size = {0:0}
        self.prehistory_temp_name = f"temp_{int(time.time())}"

        #Set up prehistory buffer
        self.prehistory = {0: {'x': [None]*self.prehistory_buffer_size, 'y': [None]*self.prehistory_buffer_size}}

        #Why is this even neessary man
        self.kill_update_thread = False

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
    
        self.x_points[line].append(x)
        self.y_points[line].append(y)

        self.num_points[line] += 1

        if (self.get_num_points(line) > self.windowSize):
            self._remove_first_point(line)


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


    def add_line(self):
        '''
        Adds a line to the plot and returns a handle (integer)
        to refer to it by in the future
        '''

        self.x_points[self.next_line] = []
        self.y_points[self.next_line] = []

        #add a prehistory for the new line
        self.prehistory[self.next_line] = {'x': [None]*self.prehistory_buffer_size, 'y': [None]*self.prehistory_buffer_size}

        #add a line to num_points
        self.num_points[self.next_line] = 0
        self.prehistory_current_size[self.next_line] = 0

        to_return = self.next_line

        self.next_line += 1

        return to_return
    
    def get_line(self, line=0):

        line = self._assert_line_exists(line)

        return self.x_points[line], self.y_points[line]
    
    def get_num_lines(self):
        return self.next_line

    def get_num_points(self, line=0):

        line = self._assert_line_exists(line)

        return self.num_points[line]

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

    logger.debug("data.py was imported. Creating global variable plot_storage here.")

    plot_storage = DataStorage()