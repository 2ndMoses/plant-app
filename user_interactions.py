from PySide6.QtGui import QAction

class WateringInteraction:
    def __init__(self, plant_container):
        self.water_action = QAction("Water Plant", None)
        self.water_action.triggered.connect(self.water_plant)
        self.plant_container = plant_container


    def water_plant(self):
        # Update the plant's hydration level and growth rate based on the watering action.
        self.plant_container.current_plant.water()

class FertilizingInteraction:
    def __init__(self, plant_container):
        self.plant_container = plant_container
        self.fertilize_action = QAction("Fertilize Plant", self.plant_container)
        self.fertilize_action.triggered.connect(self.fertilize_plant)

    def fertilize_plant(self):
        # Update the plant's nutrient level and growth rate based on the fertilizing action.
        self.plant_container.current_plant.fertilize()
