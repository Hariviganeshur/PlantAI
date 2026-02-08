import serial
import time
import re
import numpy as np
import joblib

print("🌿 Starting Plant Prediction from ESP32...")

# Load model and label encoder
print("📥 Loading model and label encoder...")
model = joblib.load('plant_suggestion_model.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# Connect to ESP32
print("🔌 Connecting to ESP32 Serial Port...")
ser = serial.Serial('COM9', 115200, timeout=5)  # Change COM port if needed
time.sleep(2)  # Wait for ESP32 to reset

# Read sensor data from ESP32
print("📡 Reading sensor data from ESP32...")
raw_data = ""
while True:
    line = ser.readline().decode('utf-8', errors='ignore').strip()
    if line == "------ FINAL SENSOR READINGS ------":
        raw_data = ""
    raw_data += line + "\n"
    if line == "-----------------------------------":
        break

print("📈 Received raw data:")
print(raw_data)

# Parse sensor readings
try:
    clean_data = re.sub(r'[\x1b\x9b][\[\]()#;?]*[0-9]*[A-Za-z]*', '', raw_data)

    sensor_data = {}
    air_temp_match = re.search(r'Air Temp \(DHT11\): ([\d\.\-]+)', clean_data)
    humidity_match = re.search(r'Humidity \(DHT11\): ([\d\.\-]+)', clean_data)
    smoke_match = re.search(r'Smoke Level \(MQ-2\): (\d+)', clean_data)
    soil_moisture_match = re.search(r'Soil Moisture: (\d+)', clean_data)

    if air_temp_match:
        sensor_data['Air Temp'] = float(air_temp_match.group(1))
    if humidity_match:
        sensor_data['Humidity'] = float(humidity_match.group(1))
    if smoke_match:
        sensor_data['Smoke'] = int(smoke_match.group(1))
    if soil_moisture_match:
        sensor_data['Soil Moisture'] = int(soil_moisture_match.group(1))

    print("✅ Parsed Sensor Data:", sensor_data)

    # Prepare input for model (only 4 features)
    input_data = np.array([[ 
        sensor_data['Air Temp'], 
        sensor_data['Humidity'], 
        sensor_data['Smoke'], 
        sensor_data['Soil Moisture']
    ]])

    # Predict plant
    prediction = model.predict(input_data)
    plant = label_encoder.inverse_transform(prediction)[0]

    print(f"🌱 Suggested Plant: {plant}")

except Exception as e:
    print("❌ Error parsing data:", str(e))
