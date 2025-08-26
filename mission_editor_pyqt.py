import sys, os
import folium
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QListWidget, QListWidgetItem
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class MissionEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mission Editor (PyQt5)")
        self.resize(1200, 700)

        # Track waypoints
        self.waypoints = []

        # === Main Layout: Horizontal Split ===
        layout = QHBoxLayout(self)

        # === Map Pane (Left) ===
        self.map_view = QWebEngineView()
        self.base_location = [25.276987, 55.296249]  # Dubai
        self.map = folium.Map(location=self.base_location, zoom_start=12)
        self.data_path = os.path.abspath("map.html")
        self.map.save(self.data_path)
        self.map_view.setUrl(QUrl.fromLocalFile(self.data_path))

        # === Coordinate Input Pane (Right) ===
        sidebar = QVBoxLayout()
        sidebar.addWidget(QLabel("Add Waypoint"))

        self.lat_input = QLineEdit(self)
        self.lat_input.setPlaceholderText("Enter Latitude")
        self.lon_input = QLineEdit(self)
        self.lon_input.setPlaceholderText("Enter Longitude")
        self.alt_input = QLineEdit(self)
        self.alt_input.setPlaceholderText("Enter Altitude (msl)")

        self.add_btn = QPushButton("Add Waypoint")
        self.delete_btn = QPushButton("Delete All Waypoints")

        # Waypoint list
        self.wp_list = QListWidget()

        sidebar.addWidget(QLabel("Latitude:"))
        sidebar.addWidget(self.lat_input)
        sidebar.addWidget(QLabel("Longitude:"))
        sidebar.addWidget(self.lon_input)
        sidebar.addWidget(QLabel("Altitude msl:"))
        sidebar.addWidget(self.alt_input)
        sidebar.addWidget(self.add_btn)
        sidebar.addWidget(self.delete_btn)
        sidebar.addWidget(QLabel("Waypoints:"))
        sidebar.addWidget(self.wp_list)

        sidebar.addStretch(1)

        # === Add both panes to main layout ===
        layout.addWidget(self.map_view, 3)
        layout.addLayout(sidebar, 1)

        # === Button actions ===
        self.add_btn.clicked.connect(self.add_waypoint)
        self.delete_btn.clicked.connect(self.delete_all_waypoints)

    def refresh_map(self, center=None, zoom=16):
        """Recreate map and markers. Optionally center on last waypoint."""
        if center is None:
            center = self.base_location
            zoom = 12

        # Create new map centered on given location
        self.map = folium.Map(location=center, zoom_start=zoom)

        # Re-add markers
        for wp_name, lat, lon, alt in self.waypoints:
            folium.Marker(
                [lat, lon],
                popup=f"{wp_name}<br>Lat: {lat}<br>Lon: {lon}<br>Alt: {alt}m"
            ).add_to(self.map)

        # Save and reload
        self.map.save(self.data_path)
        self.map_view.setUrl(QUrl.fromLocalFile(self.data_path))

    def add_waypoint(self):
        try:
            lat = float(self.lat_input.text())
            lon = float(self.lon_input.text())
            alt = float(self.alt_input.text())
            wp_number = len(self.waypoints) + 1
            wp_name = f"Waypoint {wp_number}"

            # Save and show in list
            self.waypoints.append((wp_name, lat, lon, alt))
            self.wp_list.addItem(QListWidgetItem(f"{wp_name}: {lat}, {lon}, {alt}"))

            # Refresh map centered at new waypoint
            self.refresh_map(center=[lat, lon], zoom=13)

            # Clear inputs
            self.lat_input.clear()
            self.lon_input.clear()
            self.alt_input.clear()
            print(self.waypoints)

        except ValueError:
            print("⚠ Invalid coordinates")

    def delete_all_waypoints(self):
        # Reset waypoints
        self.waypoints = []
        self.wp_list.clear()

        # Reset map to base
        self.refresh_map()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MissionEditor()
    win.show()
    sys.exit(app.exec_())
