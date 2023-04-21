

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtCore import QObject, Signal




class PlantMaintenance:
    
    @staticmethod
    def get_water_factor(plant):
        if plant.water_level <= plant.min_water_level:
            return 0.0
        elif plant.water_level >= plant.max_water_level:
            return 1.0
        else:
            return (plant.water_level - plant.min_water_level) / (plant.max_water_level - plant.min_water_level)

    @staticmethod
    def get_fertilizer_factor(plant):
        if plant.fertilizer_level <= plant.min_fertilizer_level:
            return 0.0
        elif plant.fertilizer_level >= plant.max_fertilizer_level:
            return 1.0
        else:
            return (plant.fertilizer_level - plant.min_fertilizer_level) / (plant.max_fertilizer_level - plant.min_fertilizer_level)



class PlantFood(QObject):
    hydrationChanged = Signal()

    def __init__(self, seed):
        super().__init__()
        self.seed = seed
        self.hydration = 0
        self.nutrient = 0
        self.water_absorption_rate = 1
        self.nutrient_absorption_rate = 1


    def water(self, amount):
        absorbed_water = amount * self.water_absorption_rate
        self.hydration += absorbed_water
        self.adjust_growth_rate()
        self.hydrationChanged.emit()

    def fertilize(self, amount):
        absorbed_nutrients = amount * self.nutrient_absorption_rate
        self.nutrient += absorbed_nutrients
        self.adjust_growth_rate()

    def adjust_growth_rate(self):
        # Update the growth rate based on hydration and nutrient levels.
        # You can use a simple formula or a more complex one, depending on your requirements.
        growth_rate_factor = (self.hydration + self.nutrient) / 2
        self.growth_rate = self.seed.base_growth_rate * growth_rate_factor



class HydrationBar(QWidget):
    def __init__(self, plant):
        super().__init__()
        self.plant = plant
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Hydration")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)  # Assuming hydration is a percentage (0-100)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        # Update the progress bar when the plant's hydration level changes.
    def update_hydration(self):
        hydration = self.plant.hydration
        self.progress_bar.setValue(hydration)



