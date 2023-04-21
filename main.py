from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QAction, QPainter
from PySide6.QtCore import Qt, QPointF, QPoint, QTimer
from plant_container import PlantContainer
from seed_parameters import Seed
from plant_growth import PlantGrowthTiming
from save_load import PlantStateIO
import sys
import signal
from user_interactions import WateringInteraction, FertilizingInteraction
from plant_maintenance import HydrationBar, PlantFood
from plant_components import *
import logging
import traceback

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')





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
        plant = plant(seed)
        hydration_bar = HydrationBar(plant)
        plant.hydrationChanged.connect(hydration_bar.update_hydration)

        # Add the hydration bar to the main window layout
        layout = QVBoxLayout()
        layout.addWidget(hydration_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Add the plant container to the scene
        self.scene = QGraphicsScene()
        self.scene.addItem(self.plant_container)

        logging.debug('customwindow')

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

        logging.debug('contextMenu')

    def generate_random_seed(self):
        random_seed = Seed.random_seed()
        self.plant_container.current_plant = Plant(random_seed)
        self.plant_container.update()



class PlantGrowthSimulator(QApplication):
    def __init__(self):
        super(PlantGrowthSimulator, self).__init__(sys.argv)

        self.app = QApplication([])
        self.scene = QGraphicsScene()
        self.plant_container = PlantContainer(self.scene, stem_position, initial_image_path, final_image_path, min_height, max_height)

        self.plant_growth_timing = PlantGrowthTiming(self.plant_container)
        self.plant_growth_timing.start()

        self.main_window = CustomMainWindow(self, self.plant_container)
        self.main_window.setWindowTitle("Plant Growth Simulator")
        self.main_window.setAttribute(Qt.WA_TranslucentBackground)
        self.main_window.setCentralWidget(self.plant_container)

        self.load_plant_state()

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        self.view = QGraphicsView()
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setScene(self.scene)

        logging.debug('PlantGrowthSimulator')


    def __init__(self):
        super().__init__(sys.argv)

        # Define seed
        seed = random.randint(0, 10000)

        # Define initial_image_path, final_image_path, min_height, and max_height here
        initial_image_path = "C:/Users/Nick/Desktop/pictures/Stem/stem seedling.png"
        final_image_path = "C:/Users/Nick/Desktop/pictures/Stem/stem adult.png"
        min_height = 0
        max_height = 100

        # Create a new Plant object with the required arguments
        #plant = Plant(seed, initial_image_path, final_image_path, min_height, max_height)
        self.plant = Plant(seed, initial_image_path, final_image_path, min_height, max_height)

    
    def update_plant(self):
        elapsed_time = 0.1
        dx = 0
        dy = 0
        leaf_dx = 0
        leaf_dy = 0
        initial_image_l_leaf = 'path/to/initial_image_l_leaf.png'
        final_image_l_leaf = 'path/to/final_image_l_leaf.png'
        initial_image_r_leaf = 'path/to/initial_image_r_leaf.png'
        final_image_r_leaf = 'path/to/final_image_r_leaf.png'

        self.plant.grow(elapsed_time, dx, dy, leaf_dx, leaf_dy, initial_image_l_leaf, final_image_l_leaf, initial_image_r_leaf, final_image_r_leaf)
        # Update the graphics or user interface with the new plant state
        self.plant_container.update()
        self.scene.addItem(self.plant_container)

    def save_plant_state(self):
        PlantStateIO.save_plant_state(self.main_window, self.plant_container.current_plant)

    def load_plant_state(self):
        plant_state = PlantStateIO.load_plant_state(self.main_window)
        if plant_state is not None:
            self.plant_container.current_plant = plant_state
            self.plant_container.update()
            self.scene.addItem(self.plant_container)

    def handle_signal(self, signum, frame):
        self.save_plant_state()
        sys.exit(0)

    def run(self):
        logging.debug("Application running")
        try:
            self.main_window.show()
            self.app.exec_()
        except Exception as e:
            logging.exception(f"Unhandled exception occurred: {e}")
            traceback.print_exc()
        




simulator = PlantGrowthSimulator()
simulator.run()


if __name__ == "__main__":
    app = QApplication([])
    main_window = QMainWindow()
    plant_simulation = PlantGrowthSimulator()
    main_window.setCentralWidget(plant_simulation)
    main_window.show()
    app.exec()