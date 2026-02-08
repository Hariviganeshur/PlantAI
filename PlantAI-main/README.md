
🌱 Smart Plant Recommendation System using ESP32 + AI
This project integrates an ESP32 microcontroller with various environmental sensors and an AI-based plant recommendation system. It reads real-time environmental data and suggests suitable plants using a machine learning model trained on a dataset from Kaggle.

🔧 Hardware Components
Component	        Quantity	Description
ESP32 Board	        1	        Microcontroller
DHT11 Sensor	        1	        For measuring air temperature & humidity
MQ-2 Gas Sensor	        1	        For detecting smoke levels
Soil Moisture Sensor	1	        For measuring soil moisture content
Breadboard	        1	        For connecting sensors
Jumper Wires	       ~10	        For connections
USB Cable	        1	        For connecting ESP32 to PC

🔌 Circuit Connections
ESP32 Pin	Component	             Notes
GPIO5	     DHT11 Data Pin	        Air Temp & Humidity
GPIO36	     MQ-2 Analog Out	        Smoke level input
GPIO39	   Soil Moisture Analog Out	Soil moisture input
3.3V	      All VCCs	                Power supply to sensors
GND	      All Grounds	        Common ground

Connect all components on a breadboard and power the ESP32 using your PC via USB.

📦 Project Structure
graphql
Copy
Edit
├── Crop_recommendation.csv     # Kaggle dataset for training
├── label_encoder.pkl           # Label encoder for plant names
├── plant_suggestion_model.pkl  # Trained ML model
├── predict_plant.py            # Script to read from serial & suggest plant
├── train_model.py              # Script to train and save model
└── esp32_sensor_code.ino       # Arduino IDE code for ESP32
📜 ESP32 Arduino Code (C++)
Code: esp32_sensor_code.ino

cpp
Copy
Edit
#include <DHT.h>

#define DHTPIN 5
#define DHTTYPE DHT11
#define MQ2_PIN 36
#define SOIL_PIN 39

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  delay(1000);
}

void loop() {
  float tempSum = 0, humidSum = 0;
  int smokeSum = 0, soilMoistureSum = 0;
  const int samples = 5;

  for (int i = 0; i < samples; i++) {
    tempSum += dht.readTemperature();
    humidSum += dht.readHumidity();
    smokeSum += analogRead(MQ2_PIN);
    soilMoistureSum += analogRead(SOIL_PIN);
  }

  float avgTemp = tempSum / samples;
  float avgHumidity = humidSum / samples;
  int avgSmoke = smokeSum / samples;
  int avgSoilMoisture = soilMoistureSum / samples;

  Serial.println("------ FINAL SENSOR READINGS ------");
  Serial.print("Air Temp (DHT11): "); Serial.print(avgTemp); Serial.println(" °C");
  Serial.print("Humidity (DHT11): "); Serial.print(avgHumidity); Serial.println(" %");
  Serial.print("Smoke Level (MQ-2): "); Serial.println(avgSmoke);
  Serial.print("Soil Moisture: "); Serial.println(avgSoilMoisture);
  Serial.println("-----------------------------------");

  while (true); // Hold to avoid continuous loop
}


🤖 AI Plant Suggestion (Python)
1. Dataset
Source: Kaggle – Crop_recommendation.csv

Contains features like: temperature, humidity, smoke level, soil moisture, soil temperature, etc.

2. Training the Model
File: train_model.py

Loads dataset

Encodes plant labels

Trains ML model (e.g., RandomForest)

Saves the model and label encoder as .pkl files

3. Predicting from Serial Input
File: predict_plant.py

Reads real-time data from ESP32 Serial Port (e.g., COM9 @ 115200 baud)

Parses temperature, humidity, smoke, soil moisture

Loads trained model

Outputs the best plant recommendation

✅ How It Works
ESP32 collects environmental data via sensors and prints it over Serial.

Python script (predict_plant.py) reads this serial data.

The ML model uses the sensor values to predict the most suitable plant to grow in those conditions.

💻 Requirements
Arduino IDE (for ESP32 firmware)

Python 3.x

Python libraries:

bash
Copy
Edit
pip install pandas scikit-learn pyserial
🧪 Sample Output
bash
Copy
Edit
------ FINAL SENSOR READINGS ------
Air Temp (DHT11): 29.5 °C
Humidity (DHT11): 65.2 %
Smoke Level (MQ-2): 220
Soil Moisture: 580
-----------------------------------
Suggested Plant: 🍀 Mint
📈 Future Improvements
Integrate OLED or LCD display to show plant suggestion

Automate irrigation or ventilation based on plant needs

Add mobile app integration using Blynk or Firebase

📚 Credits
Dataset: Kaggle - Crop Recommendation Dataset

Developed as a part of Environmental Monitoring and AI-based Smart Agriculture Project using ESP32.