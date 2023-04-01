#include <Plotter.h>

#define BUFFER_SIZE 50

Plotter plotter;
int a;

int buffer_x[BUFFER_SIZE];
int buffer_y[BUFFER_SIZE];

void setup(){
    plotter.begin(19200);
    a = plotter.add_line();
}

void loop(){
    //plotter.add_point(10, 30, a);
    for(int i=0; i<BUFFER_SIZE; i++){
        buffer_x[i] = i;
        buffer_y[i] = i;
    }
    plotter.send_buffer_compact(buffer_x, buffer_y, 0, BUFFER_SIZE);
    //delay(100);
}