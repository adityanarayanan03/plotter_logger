#ifndef Plotter_h
#define Plotter_h

#include "Arduino.h"

class Plotter{
    public:
        Plotter();
        void begin();
        int add_line();
        void add_point(int x, int y, int line_d);
        
    private:
        int next_line_d;
};

#endif