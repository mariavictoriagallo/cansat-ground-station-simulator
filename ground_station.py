import tkinter as tk
import random
import matplotlib.pyplot as plt # graphing library

class GroundStationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 CanSat Mission Control")
        self.root.geometry("550x500")
        self.root.configure(bg="#1e1e2e") # clean dark theme

        # data tracking states
        self.altitude = 500.0 
        self.temp = 18.5
        self.lat = -32.9475  
        self.lon = -60.6303  
        self.last_yaw = 120.0

        # lists for storing data over time (crucial course milestone)
        self.alt_history = []
        self.temp_history = []
        self.time_history = []
        self.time_elapsed = 0 
        self.has_landed = False 

        # user interface layout (all centered by default)
        self.title_label = tk.Label(root, text="🛰️ CANSAT GROUND STATION", font=("Arial", 18, "bold"), bg="#1e1e2e", fg="#cdd6f4")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=25)

        self.alt_label = tk.Label(root, text="altitude: -- m", font=("Arial", 14), bg="#1e1e2e", fg="#a6e3a1")
        self.alt_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.temp_label = tk.Label(root, text="temperature: -- °C", font=("Arial", 14), bg="#1e1e2e", fg="#f9e2af")
        self.temp_label.grid(row=2, column=0, columnspan=2, pady=10)

        self.gps_label = tk.Label(root, text="gps coordinates: --, --", font=("Arial", 13), bg="#1e1e2e", fg="#89b4fa")
        self.gps_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.imu_label = tk.Label(root, text="imu orientation (p/r/y): --", font=("Arial", 13), bg="#1e1e2e", fg="#cba6f7")
        self.imu_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.raw_data_label = tk.Label(root, text="[waiting for radio packet...]", font=("Courier", 9), bg="#1e1e2e", fg="#6c7086")
        self.raw_data_label.grid(row=5, column=0, columnspan=2, pady=30)

        self.alert_label = tk.Label(root, text="MISSION STATUS: READY", font=("Arial", 12, "bold"), bg="#1e1e2e", fg="#89b4fa")
        self.alert_label.grid(row=6, column=0, columnspan=2, pady=10)

        # configure the grid columns to stretch evenly so elements center perfectly
        root.grid_columnconfigure(0, weight=1)

        # start parsing data strings
        self.update_telemetry()

    def generate_simulated_sms(self):
        # calculate changes if still in transit
        if self.altitude > 0:
            self.altitude -= random.uniform(8.0, 14.0)
            self.temp += random.uniform(-0.1, 0.3) # gets warmer closer to ground
            self.lat += random.uniform(-0.0001, 0.0001) 
            self.lon += random.uniform(-0.0001, 0.0001)
            
            pitch = random.uniform(-6.0, 6.0)
            roll = random.uniform(-6.0, 6.0)
            self.last_yaw = (self.last_yaw + random.uniform(-4.0, 4.0)) % 360
            
            if self.altitude < 0:
                self.altitude = 0
        else:
            self.altitude = 0
            pitch = 0.0
            roll = 0.0

        # packages values into a single raw text payload string
        sms_payload = f"{self.altitude:.1f},{self.temp:.1f},{self.lat:.4f},{self.lon:.4f},{pitch:.1f},{roll:.1f},{self.last_yaw:.1f}"
        return sms_payload

    def generate_post_flight_graphs(self):
        # uses matplotlib to display post-mission metrics
        plt.figure(figsize=(10, 5))
        
        # graph 1: descent curve
        plt.subplot(1, 2, 1) 
        plt.plot(self.time_history, self.alt_history, color="#a6e3a1", linewidth=2.5)
        plt.title("altitude profile (descent curve)")
        plt.xlabel("time (seconds)")
        plt.ylabel("altitude (meters)")
        plt.grid(True, linestyle="--", alpha=0.6)

        # graph 2: thermal shifts
        plt.subplot(1, 2, 2) 
        plt.plot(self.time_history, self.temp_history, color="#f9e2af", linewidth=2.5)
        plt.title("ambient temperature shifts")
        plt.xlabel("time (seconds)")
        plt.ylabel("temperature (°C)")
        plt.grid(True, linestyle="--", alpha=0.6)

        plt.tight_layout()
        plt.show() 

    def update_telemetry(self):
        incoming_data = self.generate_simulated_sms()
        self.raw_data_label.config(text=f"rx string: {incoming_data}")

        # string parsing via splits 
        parsed_data = incoming_data.split(",")
        alt_val = float(parsed_data[0])
        temp_val = float(parsed_data[1])

        # feed parsed metrics to the interface labels
        self.alt_label.config(text=f"altitude: {alt_val:.1f} m")
        self.temp_label.config(text=f"temperature: {temp_val:.1f} °C")
        self.gps_label.config(text=f"gps data: {parsed_data[2]} Lat, {parsed_data[3]} Lon")
        self.imu_label.config(text=f"imu (pitch/roll/yaw): {parsed_data[4]}° / {parsed_data[5]}° / {parsed_data[6]}°")

        # append into our list arrays
        self.alt_history.append(alt_val)
        self.temp_history.append(temp_val)
        self.time_history.append(self.time_elapsed)
        self.time_elapsed += 1

        # evaluation states
        if alt_val == 0:
            self.alert_label.config(text="MISSION STATUS: TOUCHDOWN SUCCESSFUL", fg="#f38ba8")
            if not self.has_landed:
                self.has_landed = True
                self.root.after(1200, self.generate_post_flight_graphs) 
        else:
            if alt_val < 60:
                self.alert_label.config(text="MISSION STATUS: WARNING - LOW ALTITUDE", fg="#fab387")
            else:
                self.alert_label.config(text="MISSION STATUS: DESCENDING VIA PARACHUTE", fg="#89b4fa")
            
            self.root.after(1000, self.update_telemetry)

if __name__ == "__main__":
    window = tk.Tk()
    app = GroundStationApp(window)
    window.mainloop()