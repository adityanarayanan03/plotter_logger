#ifndef Plotter_h
#define Plotter_h

#include "Arduino.h"

class Plotter{
    public:
        Plotter();
        void begin(int baud_rate);
        int add_line();
        void send_point(int x, int y, int line_d);
        void send_buffer(int* x, int* y, int line_d, int num);
        
    private:
        int next_line_d;
};

#endif