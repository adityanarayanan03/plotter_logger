#include <Plotter.h>

#define BUFFER_SIZE 10

Plotter plotter;
int a;

int buffer_x[BUFFER_SIZE];
int buffer_y[BUFFER_SIZE];

bool high;

void setup(){
    plotter.begin(19200);
    a = plotter.add_line();

    high = true;
}

void loop(){
    //plotter.add_point(10, 30, a);
    for(int i=0; i<BUFFER_SIZE; i++){
        buffer_x[i] = millis();
        if(high) buffer_y[i] = 1;
        else buffer_y[i] = 0;
        delay(1);
    }
    high = !high;
    plotter.send_buffer_compact(buffer_x, buffer_y, 0, BUFFER_SIZE);
    //delay(100);
}