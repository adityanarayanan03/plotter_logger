#include "Arduino.h"
#include "Plotter.h"

Plotter::Plotter(){
    //Constructor, just needs to init next_line_d
}

void Plotter::begin(uint32_t baud_rate){
    next_line_d = 0;
    Serial.begin(baud_rate);
    Serial.print("\nPLOTTER:begin\n");
}

int Plotter::add_line(int* x_buf, int* y_buf, int buf_size){
    if (next_line_d >= MAX_LINES){
        return -1;
    }

    Serial.print("PLOTTER:add_line:" + String(next_line_d) + "\n");

    //Setup all the buffer tracking stuff
    x_bufs[next_line_d] = x_buf;
    y_bufs[next_line_d] = y_buf;
    buf_sizes[next_line_d] = buf_size;
    idx_ptr[next_line_d] = 0;

    //Increment after return
    return next_line_d++;
}

bool Plotter::push_to_buffer(int line_d, int x, int y){
    int idx = idx_ptr[line_d];

    x_bufs[line_d][idx] = x;
    y_bufs[line_d][idx] = y;
    
    idx_ptr[line_d] = (idx + 1) % buf_sizes[line_d];

    if (idx == buf_sizes[line_d] - 1){
        return true;
    }
    return false;
}

void Plotter::send_buffer(int line_d){
    int* x_ptr = x_bufs[line_d];
    int* y_ptr = y_bufs[line_d];
    int num = buf_sizes[line_d];

    send_buffer_compact(x_ptr, y_ptr, line_d, num);
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

void Plotter::send_buffer_compact(int* x, int* y, int line_d, int num){
    String to_return = "PLOTTER:add_points:" + String(line_d) + ":[";
    for(int i=0; i<num; i++){
        to_return += String(x[i]);
        if(i != num-1){
            to_return += ",";
        }
    }
    to_return += "]:[";
    for(int i=0; i<num; i++){
        to_return += String(y[i]);
        if(i != num-1){
            to_return += ",";
        }
    }
    to_return += "]\n";
    Serial.print(to_return);
}