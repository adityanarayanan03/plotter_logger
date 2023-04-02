#include "Arduino.h"
#include "Plotter.h"

Plotter::Plotter(){
    //Constructor, just needs to init next_line_d
}

void Plotter::begin(int baud_rate){
    next_line_d = 0;
    Serial.begin(baud_rate);
    Serial.print("\nPLOTTER:begin\n");
}

int Plotter::add_line(){
    //Have to send some shit here
    Serial.print("PLOTTER:add_line\n");

    return next_line_d++;
}

void Plotter::send_point(int x, int y, int line_d){
    //Have to do the actual serial send here
    Serial.print("PLOTTER:add_point,");
    Serial.print(x);
    Serial.print(",");
    Serial.print(y);
    Serial.print(",");
    Serial.print(line_d);
    Serial.print("\n");
}

void Plotter::send_buffer(int* x, int* y, int line_d, int num){
    for(int i=0; i<num; i++){
        send_point(x[i], y[i], line_d);
    }
}

void Plotter::send_buffer_compact(int* x, int* y, int line_d, int num){
    String to_return = "PLOTTER:add_points:" + String(line_d) + ":";
    for(int i=0; i<num; i++){
        to_return += String(x[i]);
        if(i != num-1){
            to_return += ",";
        }
    }
    to_return += ":";
    for(int i=0; i<num; i++){
        to_return += String(y[i]);
        if(i != num-1){
            to_return += ",";
        }
    }
    to_return += "\n";
    Serial.print(to_return);
}