#define PI 3.1415926535897932384626433832795

uint32_t period = 1000000; // microseconds
uint32_t samples_per_period = 1000;
uint32_t sample_period = period / samples_per_period;
uint32_t current_sample_time = 0; 

void sendValue(uint16_t value) {
    Serial.write(value >> 8);
    Serial.write(value & 0xff);
}

void starting_routine() {
    uint8_t buf[1];
    Serial.readBytes(buf, 1); 
    while(buf[0] != 0x53) {
        Serial.readBytes(buf, 1); 
    }
    delay(10); 
    sendValue(0xFFF2);
    digitalWrite(13, LOW); // turn off LED to indicate that Arduino has started
}

uint16_t dummy_data_generation() {
    return 512 * sin(2 * PI * current_sample_time / period) + 512;
}

uint16_t sample_ADC() {
    return analogRead(A0);
}

// runs the function pointed by funcptr repeatedly
void timer_routine(uint16_t(*funcptr)()) {
    uint32_t elapsed_time = 0;
    while (elapsed_time < sample_period) {
        elapsed_time = micros() - current_sample_time;
    }
    uint8_t buf[2];
    current_sample_time = micros();
    uint16_t value = funcptr();
    sendValue(value);
}

void setup() {
    Serial.begin(230400);
    pinMode(13, OUTPUT);
    digitalWrite(13, HIGH); // turn on LED to indicate that Arduino is ready to start
    Serial.write('R'); // send ready signal to PC
    starting_routine();
}

void loop() {
    timer_routine(dummy_data_generation);
}