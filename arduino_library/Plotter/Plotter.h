#ifndef Plotter_h
#define Plotter_h

#include "Arduino.h"

#define MAX_LINES 5

class Plotter{
    public:
        Plotter();
        void begin(uint32_t baud_rate);
        void begin(uint32_t baud_rate, int32_t window_min, int32_t window_max);

        //Adding a new buffer
        uint8_t add_line(int32_t* x_buf, int32_t* y_buf, uint8_t buf_size);
        uint8_t add_line(int32_t* x_buf, int32_t* y_buf, uint8_t buf_size, uint8_t x_fp_digits, uint8_t y_fp_digits);

        //Managing buffers
        bool push_to_buffer(uint8_t line_d, int32_t x, int32_t y);
        void send_buffer(uint8_t line_d);

        //should only be used as a helper function from send_buffer for now
        void send_buffer_compact(int32_t* x, int32_t* y, uint8_t line_d, uint8_t num);

        //lowkey depracated stuff
        void send_point(int32_t x, int32_t y, uint8_t line_d);
        
    private:
        uint8_t next_line_d;
        int32_t* x_bufs[MAX_LINES];
        int32_t* y_bufs[MAX_LINES];

        //Capping buffer sizes at 256 here. Might want to make larger later.
        uint8_t idx_ptr[MAX_LINES];
        uint8_t buf_sizes[MAX_LINES];
};

#endif