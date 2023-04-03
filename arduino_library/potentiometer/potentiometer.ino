#include <Plotter.h>

#define BUFFER_SIZE 10

Plotter plotter;

int line_1;
int buffer_x[BUFFER_SIZE];
int buffer_y[BUFFER_SIZE];

int pot_val;

void setup(){
    plotter.begin(115200);

    line_1 = plotter.add_line(buffer_x, buffer_y, BUFFER_SIZE);
}

void loop(){
    pot_val = analogRead(A0);

    if (plotter.push_to_buffer(line_1, millis(), pot_val)){
        plotter.send_buffer(line_1);
    }

    delay(1);
}