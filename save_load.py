import pickle
from PySide6.QtWidgets import QFileDialog

class PlantStateIO:
    @staticmethod
    def save_plant_state(parent, plant):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(parent, "Save Plant State", "", "Plant State Files (*.pstate);;All Files (*)", options=options)
        if filename:
            with open(filename, 'wb') as file:
                pickle.dump(plant, file)

    @staticmethod
    def load_plant_state(parent):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(parent, "Load Plant State", "", "Plant State Files (*.pstate);;All Files (*)", options=options)
        if filename:
            with open(filename, 'rb') as file:
                plant = pickle.load(file)
            return plant
