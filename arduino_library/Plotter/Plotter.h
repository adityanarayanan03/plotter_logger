#ifndef Plotter_h
#define Plotter_h

#include "Arduino.h"

#define MAX_LINES 5

class Plotter{
    public:
        Plotter();
        void begin(uint32_t baud_rate);

        //Adding a new buffer
        int add_line(int* x_buf, int* y_buf, int buf_size);

        //Managing buffers
        bool push_to_buffer(int line_d, int x, int y);
        void send_buffer(int line_d);

        //should only be used as a helper function from send_buffer for now
        void send_buffer_compact(int* x, int* y, int line_d, int num);

        //lowkey depracated stuff
        void send_point(int x, int y, int line_d);
        
    private:
        int next_line_d;
        int* x_bufs[MAX_LINES];
        int* y_bufs[MAX_LINES];
        int idx_ptr[MAX_LINES];
        int buf_sizes[MAX_LINES];
};

#endif