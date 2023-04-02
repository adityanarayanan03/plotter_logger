#include <Plotter.h>

#define BUFFER_SIZE 10

Plotter plotter;
int a;
int b;
int count;

int buffer_x[BUFFER_SIZE];
int buffer_y[BUFFER_SIZE];
int buffer_y2[BUFFER_SIZE];

bool high;

void setup(){
    plotter.begin(19200);
    a = plotter.add_line();
    b = plotter.add_line();

    high = true;
    count = 1;
}

void loop(){
    //plotter.add_point(10, 30, a);
    for(int i=0; i<BUFFER_SIZE; i++){
        buffer_x[i] = millis();
        if(high) buffer_y[i] = 1, buffer_y2[i] = 0;
        else buffer_y[i] = 0, buffer_y2[i] = 1;
        delay(1);
    }
    
    //Should generate a 1 Hz clock signal.
    if(millis()/1000 == count){
        count ++;
        high = !high;
    }

    plotter.send_buffer_compact(buffer_x, buffer_y, a, BUFFER_SIZE);
    plotter.send_buffer_compact(buffer_x, buffer_y2, b, BUFFER_SIZE);
    //delay(100);
}