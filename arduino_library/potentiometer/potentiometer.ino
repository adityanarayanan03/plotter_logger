#include <Plotter.h>

#define BUFFER_SIZE 10

Plotter plotter;

uint8_t line_1;
int32_t buffer_x[BUFFER_SIZE];
int32_t buffer_y[BUFFER_SIZE];

int32_t pot_val;

void setup(){
    plotter.begin(115200);

    line_1 = plotter.add_line(buffer_x, buffer_y, BUFFER_SIZE, 3, 0);
}

void loop(){
    pot_val = analogRead(A0);

    if (plotter.push_to_buffer(line_1, millis(), pot_val)){
        plotter.send_buffer(line_1); //Takes roughly 3 ms
    }

    //Max I want is 60Hz, so 15ms wait is roughly ok
    delay(1);
}