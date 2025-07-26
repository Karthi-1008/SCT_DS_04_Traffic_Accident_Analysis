import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
import os

class Class431242000029:
    def __init__(self, filepath):
        print("📁 Loading dataset...")
        self.df = pd.read_csv(filepath)
        print(f"✅ Dataset loaded with {len(self.df)} rows.")

    def clean_data(self):
        print("🧹 Cleaning data...")
        self.df.dropna(subset=['Start_Time', 'Weather_Condition', 'Start_Lat', 'Start_Lng'], inplace=True)
        self.df['Start_Time'] = pd.to_datetime(self.df['Start_Time'], errors='coerce')
        self.df['Hour'] = self.df['Start_Time'].dt.hour
        self.df['Day'] = self.df['Start_Time'].dt.day_name()
        print("✅ Data cleaned.")

    def analyze_by_hour(self):
        print("📊 Plotting accidents by hour...")
        plt.figure(figsize=(10,6))
        sns.countplot(data=self.df, x='Hour', palette='viridis')
        plt.title("Accidents by Hour")
        plt.savefig("accidents_by_hour.png")
        plt.close()
        print("✅ Saved: accidents_by_hour.png")

    def analyze_by_weather(self):
        print("🌦️ Plotting top weather conditions...")
        top_weather = self.df['Weather_Condition'].value_counts().nlargest(10)
        plt.figure(figsize=(10,6))
        top_weather.plot(kind='bar', color='orange')
        plt.title("Top 10 Weather Conditions")
        plt.savefig("accidents_by_weather.png")
        plt.close()
        print("✅ Saved: accidents_by_weather.png")

    def analyze_by_day(self):
        print("📅 Plotting accidents by day of week...")
        plt.figure(figsize=(10,6))
        sns.countplot(x='Day', data=self.df, order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], palette='mako')
        plt.title("Accidents by Day of Week")
        plt.savefig("accidents_by_day.png")
        plt.close()
        print("✅ Saved: accidents_by_day.png")

    def visualize_hotspots(self):
        print("🗺️ Generating accident hotspot map (sampling 1000 points)...")
        sample = self.df[['Start_Lat', 'Start_Lng']].dropna().sample(1000, random_state=42)
        m = folium.Map(location=[sample['Start_Lat'].mean(), sample['Start_Lng'].mean()], zoom_start=5)
        HeatMap(sample.values.tolist()).add_to(m)
        m.save("accident_hotspots.html")
        print("✅ Hotspot map saved as output/accident_hotspots.html")

if __name__ == "__main__":
    file_path = "US_Accidents_March23.csv"  # Or "data/US_Accidents_March23.csv" if moved
    analysis = Class431242000029(file_path)
    analysis.clean_data()
    analysis.analyze_by_hour()
    analysis.analyze_by_weather()
    analysis.analyze_by_day()
    analysis.visualize_hotspots()
    print("🎉 All tasks completed!")
