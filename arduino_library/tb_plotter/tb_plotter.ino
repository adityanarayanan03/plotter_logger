#include <Plotter.h>

Plotter plotter;
int a;

void setup(){
    plotter.begin();
    a = plotter.add_line();
}

void loop(){
    plotter.add_point(10, 20, a);
    delay(1000);
}