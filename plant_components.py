from enum import Enum, auto
import random
from PySide6.QtWidgets import QGraphicsItem

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPixmap, QPainter
import traceback
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')





BRANCH_DISTANCE = 50  # The distance between consecutive branches in pixels
LEAF_DISTANCE = 10  # The distance between consecutive leaves in pixels
BUD_DISTANCE = 10  # The distance between consecutive buds in pixels
FLOWER_DISTANCE = 10  # The distance between consecutive flowers in pixels
BRANCH_HEIGHT_RATIO = 100

# Initialize the stem with the calculated position
initial_image_path = "C:/Users/Nick/Desktop/pictures/Stem/stem seedling.png"
final_image_path = "C:/Users/Nick/Desktop/pictures/Stem/stem adult.png"
# Initialize the leaf with the calculated positions
initial_image_l_leaf = "C:/Users/Nick/Desktop/pictures/Leaf Seedling Left/leaf left seedling.png"
final_image_l_leaf = ":/Users/Nick/Desktop/pictures/Leaf Left/leaf left adult.png"
initial_image_r_leaf = "C:/Users/Nick/Desktop/pictures/Leaf Seedling Right/leaf right seedling.png"
final_image_r_leaf = "C:/Users/Nick/Desktop/pictures/Leaf Right/leaf right adult.png"
#Branches
initial_image_r_branch = "C:/Users/Nick/Desktop/pictures/Branch Right/branch right small.png" 
final_image_r_branch = "C:/Users/Nick/Desktop/pictures/Branch Right/branch right.png"
initial_image_l_branch = "C:/Users/Nick/Desktop/pictures/Branch Left/branch left small.png" 
final_image_l_branch = "C:/Users/Nick/Desktop/pictures/Branch Left/branch left.png"
#Buds
initial_image_bud = "C:/Users/Nick/Desktop/pictures/Bud/bud start.png"
final_image_bud = "C:/Users/Nick/Desktop/pictures/Bud/bud.png"




class Plant:
#    def __init__(self, seed):
    def __init__(self, seed, initial_image_path, final_image_path, min_height, max_height):

        self.seed = seed
        self.stem = Stem(initial_image_path, final_image_path, min_height, max_height)
        self.branches = []
        self.leaves = []
        self.buds = []
        self.flowers = []

        self.seed = seed
        self.stem = Stem(initial_image_path, final_image_path, min_height, max_height)

        self.last_branch_position = 0  # Initialize the last branch position
        self.growth_progress = 0  # Initialize growth progress to 0


    def grow(self, elapsed_time, dx, dy, leaf_dx, leaf_dy, initial_image_l_leaf, final_image_l_leaf, initial_image_r_leaf, final_image_r_leaf):
        self.update_growth_progress(elapsed_time)
        self.add_branches_and_leaves(dx, dy, leaf_dx, leaf_dy, initial_image_l_leaf, final_image_l_leaf, initial_image_r_leaf, final_image_r_leaf)
        self.add_buds_and_flowers()
        self.stem.grow(self.growth_progress)
    
        for branch in self.branches:
            branch.grow(elapsed_time)
            branch.add_sub_branches(dx, dy, leaf_dx, leaf_dy, initial_image_l_branch, final_image_l_branch, initial_image_r_branch, final_image_r_branch)
    
    def update_growth_progress(self, elapsed_time):
        growth_rate = self.get_growth_rate()  # Get the growth rate from the plant's attributes
        self.growth_progress += growth_rate * elapsed_time

        # Make sure growth progress stays within the 0 to 1 range
        self.growth_progress = min(max(self.growth_progress, 0), 1)


    def add_branches_and_leaves(self, dx, dy, leaf_dx, leaf_dy, initial_image_l_leaf, final_image_l_leaf, initial_image_r_leaf, final_image_r_leaf):
        num_branches = self.calculate_number_of_branches()
        if len(self.branches) < num_branches * 2:  # Multiply by 2 since we add 2 branches at once
            # Add branches on both sides of the stem
            branch_y = self.stem.height - BRANCH_HEIGHT_RATIO            #dx, represent the horizontal distance between the stem and the branches
            dx = BRANCH_DISTANCE(random.random() - 0.5)
            left_branch_position = (self.stem.x - dx, self.last_branch_position + BRANCH_DISTANCE)
            right_branch_position = (self.stem.x + dx, self.last_branch_position + BRANCH_DISTANCE)

            left_branch = Branch(left_branch_position)
            right_branch = Branch(right_branch_position)
            self.branches.extend([left_branch, right_branch])

            # Add leaves for the new branches
            #leaf_dx, and leaf_dy, represent the horizontal and vertical distance between the branches and the leaves
        # Add leaves for the new branches
        leaf_dx = LEAF_DISTANCE(random.random() - 0.5)
        leaf_dy = LEAF_DISTANCE(random.random() - 0.5)
        left_leaf_position = (left_branch_position[0] - leaf_dx, left_branch_position[1] + leaf_dy)
        right_leaf_position = (right_branch_position[0] + leaf_dx, right_branch_position[1] + leaf_dy)

        left_leaf = Leaf(initial_image_l_leaf, final_image_l_leaf, left_leaf_position, leaf_type="left")
        right_leaf = Leaf(initial_image_r_leaf, final_image_r_leaf, right_leaf_position, leaf_type="right")
        self.leaves.extend([left_leaf, right_leaf])

            # Update the last branch position
        self.last_branch_position += BRANCH_DISTANCE

        logging.debug('ADDBRANCHES')


    def calculate_number_of_branches(self):
        # The number of branches is proportional to the height of the plant.
        return int(self.stem.height / BRANCH_HEIGHT_RATIO)            


    def stem_height(growth_progress, min_height, max_height):
        return min_height + growth_progress * (max_height - min_height)










#Define growth stages: Create an enumeration using Python's Enum class to define the growth stages (seedling, vegetative, flowering, maturity):

class GrowthStage(Enum):
    SEEDLING = auto()
    VEGETATIVE = auto()
    FLOWERING = auto()
    MATURITY = auto()

#Create component classes: Define classes for each plant component (stem, branches, leaves, buds). Each class should contain properties and methods relevant to the respective component, such as position, size, and rendering:
def stem_height(growth_progress, min_height, max_height):
    return min_height + growth_progress * (max_height - min_height)

from PySide6.QtGui import QPixmap

class Stem(QGraphicsItem):
    def __init__(self, position, initial_image_path, final_image_path, min_height, max_height):
        super().__init__()
        self.position = position
        self.height = min_height
        self.min_height = min_height
        self.max_height = max_height
        self.growth_progress = 0.0
        self.initial_image_path = initial_image_path
        self.final_image_path = final_image_path
        self.initial_pixmap = None
        self.final_pixmap = None

        logging.info('Stem')


    def init_pixmaps(self):
        self.initial_image = QPixmap(self.initial_image_path)
        self.final_image = QPixmap(self.final_image_path)
        self.current_image = QPixmap(self.initial_image.size())

    
    def grow(self, growth_progress):
        self.height = stem_height(growth_progress, self.min_height, self.max_height)
        self.update_image(growth_progress)

    def update_image(self, growth_progress):
        # Calculate the size of the image based on the height
        scale_factor = self.height / self.initial_image.height()
        width = int(self.initial_image.width() * scale_factor)
        height = int(self.initial_image.height() * scale_factor)
        current_image = QPixmap(self.initial_image.size())
        current_image.fill(Qt.transparent)
  

        # Use growth progress to interpolate between initial and final images
        current_image = QPixmap(self.initial_image.size())
        current_image.fill(Qt.transparent)

        painter = QPainter(current_image)
        painter.setOpacity(1 - growth_progress)
        painter.drawPixmap(0, 0, self.initial_image.scaled(width, height))
        painter.setOpacity(growth_progress)
        painter.drawPixmap(0, 0, self.final_image.scaled(width, height))
        painter.end()

        self.current_image = current_image

    def boundingRect(self):
        # You should return a QRectF object representing the bounding box of your stem.
        # This is an example, you may need to adjust the values to fit your case.
        return QRectF(0, 0, 10, self.height)

    def draw(self, painter):
        # Draw the stem image at the specified position
        painter.drawPixmap(self.position, self.current_image)

    def render(self):
        pass  # Render the stem


# Position calculation
window_width = 800
window_height = 600
stem_width = 50

min_height = 50
max_height = 300

stem_x = (window_width - stem_width) // 2
stem_y = window_height - min_height  # Use min_height instead of stem.height
stem_position = (stem_x, stem_y)


stem = Stem(stem_position, initial_image_path, final_image_path, min_height, max_height)

class Branch(QGraphicsItem):
    def __init__(self, position, initial_image, final_image):
        super().__init__()
        self.position = position
        self.sub_branches = []  # Initialize the sub-branches list
        self.last_sub_branch_position = 0  # Initialize the last sub-branch position

    def add_sub_branches(self, dx, dy, leaf_dx, leaf_dy, initial_image, final_image):
        if self.height > self.last_sub_branch_position + BRANCH_DISTANCE:
            left_sub_branch_position = (self.x - dx, self.last_sub_branch_position + BRANCH_DISTANCE)
            right_sub_branch_position = (self.x + dx, self.last_sub_branch_position + BRANCH_DISTANCE)

            left_sub_branch = Branch(left_sub_branch_position, initial_image_l_branch, final_image_l_branch)
            right_sub_branch = Branch(right_sub_branch_position, initial_image_r_branch, final_image_r_branch)
            self.sub_branches.extend([left_sub_branch, right_sub_branch])

            # Add leaves for the new sub-branches
            left_leaf_position = (left_sub_branch_position[0] - leaf_dx, left_sub_branch_position[1] + leaf_dy)
            right_leaf_position = (right_sub_branch_position[0] + leaf_dx, right_sub_branch_position[1] + leaf_dy)

            left_leaf = Leaf(initial_image, final_image, left_leaf_position)
            right_leaf = Leaf(initial_image, final_image, right_leaf_position)
            self.leaves.extend([left_leaf, right_leaf])

            # Update the last sub-branch position
            self.last_sub_branch_position += BRANCH_DISTANCE

    def render(self):
        pass# Render the branch



class Leaf(QGraphicsItem):
    def __init__(self, position, initial_image_l_leaf, final_image_l_leaf, leaf_type="left"):
        self.position = position
        self.initial_image = initial_image_l_leaf
        self.final_image = final_image_l_leaf
        self.growth_progress = 0.0
        self.current_image = self.initial_image
        self.leaf_type = leaf_type

    def __init__(self, position, initial_image_r_leaf, final_image_r_leaf, leaf_type="right"):
        self.position = position
        self.initial_image = initial_image_r_leaf
        self.final_image = final_image_r_leaf
        self.growth_progress = 0.0
        self.current_image = self.initial_image
        self.leaf_type = leaf_type


    def update_growth_progress(self, delta_progress):
        self.growth_progress += delta_progress
        self.growth_progress = min(1.0, max(0.0, self.growth_progress))
        self.update_current_image()

    def update_current_image(self):
        width_diff = self.final_image.width() - self.initial_image.width()
        height_diff = self.final_image.height() - self.initial_image.height()

        new_width = self.initial_image.width() + width_diff * self.growth_progress
        new_height = self.initial_image.height() + height_diff * self.growth_progress

        self.current_image = self.initial_image.scaled(new_width, new_height)

    def render(self):
        if self.leaf_type == "left":
            pass  # Render the left leaf
        elif self.leaf_type == "right":
            pass  # Render the right leaf
        else:
            raise ValueError("Invalid leaf type. Expected 'left' or 'right'.")
        

    

class Bud(QGraphicsItem):
    def __init__(self, initial_image_bud, final_image_bud, min_height, max_height):
        super().__init__()
        self.initial_image = QPixmap(initial_image_bud)
        self.final_image = QPixmap(final_image_bud)
        self.min_height = min_height
        self.max_height = max_height
        self.current_image = self.initial_image
        self.image_ratio = self.initial_image.width() / self.initial_image.height()
        self.current_height = 0
        self.current_width = 0
        self.setPos(0, 0)

    def boundingRect(self):
        return QRectF(0, 0, self.current_width, self.current_height)

    def paint(self, painter, option, widget):
        painter.drawPixmap(0, 0, self.current_image)

    def update_image(self, growth_progress):
        pass

    def grow(self, growth_progress):
        self.update_image(growth_progress)
        self.update_size()
        self.update_position(growth_progress)

    def update_size(self):
        self.current_height = self.min_height + (self.max_height - self.min_height) * self.current_image.height() / self.final_image.height()
        self.current_width = self.current_height * self.image_ratio

    def update_position(self, growth_progress):
        pass

    def render(self):
        pass# Render the bud
    # ...
