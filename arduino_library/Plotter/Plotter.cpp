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

uint8_t Plotter::add_line(int32_t* x_buf, int32_t* y_buf, uint8_t buf_size){
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

bool Plotter::push_to_buffer(uint8_t line_d, int32_t x, int32_t y){
    uint8_t idx = idx_ptr[line_d];

    x_bufs[line_d][idx] = x;
    y_bufs[line_d][idx] = y;
    
    idx_ptr[line_d] = (idx + 1) % buf_sizes[line_d];

    if (idx == buf_sizes[line_d] - 1){
        return true;
    }
    return false;
}

void Plotter::send_buffer(uint8_t line_d){
    int32_t* x_ptr = x_bufs[line_d];
    int32_t* y_ptr = y_bufs[line_d];
    uint8_t num = buf_sizes[line_d];

    send_buffer_compact(x_ptr, y_ptr, line_d, num);
}

void Plotter::send_point(int32_t x, int32_t y, uint8_t line_d){
    //Have to do the actual serial send here
    Serial.print("PLOTTER:add_point,");
    Serial.print(x);
    Serial.print(",");
    Serial.print(y);
    Serial.print(",");
    Serial.print(line_d);
    Serial.print("\n");
}

void Plotter::send_buffer_compact(int32_t* x, int32_t* y, uint8_t line_d, uint8_t num){
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