#define PI 3.1415926535897932384626433832795

void setup() {
    Serial.begin(921600);
    Serial.println("Hello, World!");

}
uint32_t period = 100000; // microseconds
uint32_t samples_per_period = 500;
uint32_t sample_period = period / samples_per_period;
uint16_t value; 
uint32_t current_sample_time = 0;  
uint32_t elapsed_time = 0;

void loop() {
    while (elapsed_time < sample_period) {
        elapsed_time = micros() - current_sample_time;
    }
    current_sample_time = micros();
    value = 512 * sin(2 * PI * current_sample_time / period) + 512;
    Serial.println(value);
    elapsed_time = 0;






    // uint32_t time = micros(); // microseconds
    // double angle = 2 * PI * time / period;
    // uint32_t elapsed_time = micros() - time;
    // while (elapsed_time < period / samples_per_period) {
    //     elapsed_time = micros() - time;
    // }
    // angle = 2 * PI * time / period;
    // value = 512 * sin(angle) + 512;
    // Serial.println(value); 
}