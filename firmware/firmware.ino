#define PI 3.1415926535897932384626433832795

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
    delay(500); 
    sendValue(0xFFF2);
    digitalWrite(13, LOW); // turn off LED to indicate that Arduino has started
}

uint32_t period = 1000000; // microseconds
uint32_t samples_per_period = 1000;
uint32_t sample_period = period / samples_per_period;
uint16_t value; 
uint32_t current_sample_time = 0; 
uint32_t elapsed_time = 0;

void setup() {
    Serial.begin(230400);
    pinMode(13, OUTPUT);
    digitalWrite(13, HIGH); // turn on LED to indicate that Arduino is ready to start
    starting_routine();
}

void loop() {
    for (int i = 0; i < samples_per_period; i++) {
        while (elapsed_time < sample_period) {
            elapsed_time = micros() - current_sample_time;
        }
        current_sample_time = micros();
        value = 512 * sin(2 * PI * current_sample_time / period) + 512;
        sendValue(value);
        elapsed_time = 0;
    }
    while(1); 
}