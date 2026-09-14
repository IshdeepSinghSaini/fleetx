import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# --- Connect to the FleetX database ---
engine = create_engine("postgresql+psycopg2://postgres:Ishu%402107@localhost:5432/fleetx")

# --- Load tables into DataFrames (pandas' version of an Excel sheet) ---
vehicles = pd.read_sql("SELECT * FROM vehicles", engine)
bookings = pd.read_sql("SELECT * FROM bookings", engine)
payments = pd.read_sql("SELECT * FROM payments", engine)
users = pd.read_sql("SELECT * FROM users", engine)

print("Vehicles loaded:", len(vehicles))
print("Bookings loaded:", len(bookings))
print("Payments loaded:", len(payments))
print("Users loaded:", len(users))

# --- Metric 1: Total Revenue ---
total_revenue = payments[payments["status"] == "SUCCESS"]["amount"].sum()
print("\nTotal Revenue: Rs.", total_revenue)

# --- Metric 2: Bookings per vehicle ---
bookings_with_names = bookings.merge(vehicles[["id", "name"]], left_on="vehicle_id", right_on="id", suffixes=("", "_vehicle"))
bookings_per_vehicle = bookings_with_names.groupby("name").size().sort_values(ascending=False)
print("\nBookings per vehicle:\n", bookings_per_vehicle)

# --- Metric 3: Cancellation rate ---
total_bookings = len(bookings)
cancelled = len(bookings[bookings["status"] == "CANCELLED"])
cancellation_rate = round((cancelled / total_bookings) * 100, 2) if total_bookings else 0
print(f"\nCancellation Rate: {cancellation_rate}%")

# --- Chart 1: Bookings per vehicle (bar chart) ---
plt.figure(figsize=(6, 4))
bookings_per_vehicle.plot(kind="bar", color="#38bdf8")
plt.title("Bookings per Vehicle")
plt.ylabel("Number of Bookings")
plt.xlabel("")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("output/bookings_per_vehicle.png")
plt.close()

# --- Chart 2: Booking status breakdown (pie chart) ---
status_counts = bookings["status"].value_counts()
plt.figure(figsize=(5, 5))
plt.pie(status_counts, labels=status_counts.index, autopct="%1.0f%%",
        colors=["#38bdf8", "#ef4444", "#f59e0b"])
plt.title("Booking Status Breakdown")
plt.tight_layout()
plt.savefig("output/booking_status.png")
plt.close()

print("\nCharts saved in analytics/python/output/")
