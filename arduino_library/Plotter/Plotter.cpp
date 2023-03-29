#include "Arduino.h"
#include "Plotter.h"

Plotter::Plotter(){
    //Constructor, just needs to init next_line_d
}

void Plotter::begin(){
    next_line_d = 0;
    Serial.begin(9600);
}

int Plotter::add_line(){
    //Have to send some shit here
    Serial.print("PLOTTER:add_line\n");

    return next_line_d++;
}

void Plotter::add_point(int x, int y, int line_d){
    //Have to do the actual serial send here
    Serial.print("PLOTTER:add_point,");
    Serial.print(x);
    Serial.print(",");
    Serial.print(y);
    Serial.print(",");
    Serial.print(line_d);
    Serial.print("\n");
}