from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QWidget, QVBoxLayout
from PySide6.QtGui import QAction, QPainter
from PySide6.QtCore import Qt, QPointF
from plant_container import PlantContainer
from seed_parameters import Seed
from plant_growth import PlantGrowthTiming
from save_load import PlantStateIO
import sys
import signal
from user_interactions import WateringInteraction, FertilizingInteraction
from plant_maintenance import HydrationBar, Plant
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from plant_components import *

#app = QApplication([])

scene = QGraphicsScene()
view = QGraphicsView(scene)
view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
view.setRenderHint(QPainter.Antialiasing)

# Add the plant container to the scene
stem_position = QPointF(0, 0)
initial_image_path = "path/to/initial_image.png"
final_image_path = "path/to/final_image.png"
min_height = 0
max_height = 100


# Add the plant container to the scene
class CustomMainWindow(QMainWindow):
    def __init__(self, plant_growth_simulator, plant_container):
        super().__init__()
        self.plant_growth_simulator = plant_growth_simulator
        self.plant_container = plant_container

        # Add the watering and fertilizing interactions to the plant container
        self.watering_interaction = WateringInteraction(self.plant_container)
        self.fertilizing_interaction = FertilizingInteraction(self.plant_container)

        # Add hydration bar to the main window
        seed = Seed.random_seed()
        plant = Plant(seed)
        hydration_bar = HydrationBar(plant)
        plant.hydrationChanged.connect(hydration_bar.update_hydration)

        # Add the hydration bar to the main window layout
        layout = QVBoxLayout()
        layout.addWidget(hydration_bar)
        layout.addWidget(self.plant_container)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        # Add the generate seed action to the context menu
        generate_seed_action = QAction("Generate a Seed", self)
        generate_seed_action.triggered.connect(self.generate_random_seed)
        context_menu.addAction(generate_seed_action)

        # Add the watering and fertilizing actions to the context menu
        context_menu.addAction(self.watering_interaction.water_action)
        context_menu.addAction(self.fertilizing_interaction.fertilize_action)

        # Show the context menu
        context_menu.exec(event.globalPos())

    def generate_random_seed(self):
        random_seed = Seed.random_seed()
        self.plant_container.generate_plant(random_seed)

class PlantGrowthSimulator:
    def __init__(self):
        self.app = QApplication([])
        self.plant_container = PlantContainer(stem_position, initial_image_path, final_image_path, min_height, max_height)

        self.plant_growth_timing = PlantGrowthTiming(self.plant_container)
        self.plant_growth_timing.start()

        self.main_window = CustomMainWindow(self, self.plant_container)
        self.main_window.setWindowTitle("Plant Growth Simulator")
        self.main_window.setAttribute(Qt.WA_TranslucentBackground)
        self.main_window.setCentralWidget(self.plant_container)

        self.load_plant_state()

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    def save_plant_state(self):
        PlantStateIO.save_plant_state(self.main_window, self.plant_container.current_plant)

    def load_plant_state(self):
        plant_state = PlantStateIO.load_plant_state(self.main_window)
        if plant_state is not None:
            self.plant_container.current_plant = plant_state
            self.plant_container.update()

    def handle_signal(self, signum, frame):
        self.save_plant_state()
        sys.exit(0)
    
    def run(self):
        self.main_window.show()
        self.app.exec()


container = PlantContainer(QPoint(400, 400), initial_image_path, final_image_path, min_height, max_height)
scene.addItem(container)
#stem = Stem(stem_position, initial_image_path, final_image_path, min_height, max_height)
#stem.init_pixmaps()


if __name__ == "__main__":
    simulator = PlantGrowthSimulator()
    simulator.run()
