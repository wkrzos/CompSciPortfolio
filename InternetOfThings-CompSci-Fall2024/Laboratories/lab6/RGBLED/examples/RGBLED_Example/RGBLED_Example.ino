#include "RGBLED.h"

RGBLED myRGB(9, 10, 11);

void setup() {

    myRGB.setColor("RED");
    delay(1000);

    myRGB.setColor("GREEN");
    delay(1000);

    myRGB.setColor(128, 128, 128);
    delay(1000);

    myRGB.off();
}

void loop() {
    myRGB.setColor("BLUE");
    delay(1000);
    myRGB.setColor("CYAN");
    delay(1000);
    myRGB.setColor("YELLOW");
    delay(1000);
    myRGB.setColor("MAGENTA");
    delay(1000);
}
