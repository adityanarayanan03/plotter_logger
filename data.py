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

        self.x_points[line] = self.x_points[line][1:]
        self.y_points[line] = self.y_points[line][1:]

        self.num_points[line] -= 1

    def add_line(self):
        '''
        Adds a line to the plot and returns a handle (integer)
        to refer to it by in the future
        '''

        self.x_points[self.next_line] = []
        self.y_points[self.next_line] = []

        to_return = self.next_line

        self.next_line += 1

        return to_return
    
    def get_line(self, line=0):

        line = self._assert_line_exists(line)

        return self.x_points[line], self.y_points[line]

    def get_num_points(self, line=0):

        line = self._assert_line_exists(line)

        return self.num_points[line]

    
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