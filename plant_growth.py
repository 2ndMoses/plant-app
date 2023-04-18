
from plant_components import GrowthStage, Stem, Branch, Leaf, Bud
from plant_maintenance import PlantMaintenance
from PySide6.QtCore import QTimer, QObject, Signal
from seed_parameters import Seed





class PlantGrowthTiming(QObject):
    def __init__(self, plant_container):
        super().__init__()
        self.plant_container = plant_container
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plant_growth)


        #Create a PlantGrowth instance,Initialize a PlantGrowth instance using the random seed generated using the random_seed method provided in the Seed class.
        self.seed = Seed.random_seed()
        self.plant = PlantGrowth(stem=None, branches=[], leaves=[], buds=[], seed=self.seed)

        #Create a QTimer instance to periodically trigger growth updates. You can adjust the timer interval to control the frequency of updates. A shorter interval will result in more frequent updates, while a longer interval will result in less frequent updates.
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plant_growth)

    #Define a slot function to update plant growth:
    #Create a function that will be called each time the timer fires. Inside the function, update the plant's growth using the update_growth method of the PlantGrowth class. You'll need to pass the current growth stage and elapsed time as arguments.
    def update_plant_growth(self):
        growth_stage = self.plant.get_growth_stage()
        elapsed_time = self.timer.interval() / 1000
        self.plant.update_growth(growth_stage, elapsed_time)
        # You may also need to update the display of the plant here

    def start(self, interval=1000):
        self.timer.start(interval)

    def stop(self):
        self.timer.stop()
    




class PlantGrowth:
    def __init__(self, stem, branches, leaves, buds, seed):
        self.stem = stem
        self.branches = branches
        self.leaves = leaves
        self.buds = buds
        self.seed = seed
        self.age = 0  # Initialize the plant age to 0


    def update_growth(self, growth_stage, elapsed_time):
        self.age += elapsed_time

        if growth_stage == GrowthStage.SEEDLING:
            self.update_stem_growth(elapsed_time)
            self.update_branches_growth(elapsed_time)
            self.update_leaves_growth(elapsed_time)
            self.update_buds_growth(elapsed_time)

        elif growth_stage == GrowthStage.VEGETATIVE:
            self.update_stem_growth(elapsed_time)
            self.update_branches_growth(elapsed_time, vegetative=True)
            self.update_leaves_growth(elapsed_time, vegetative=True)
            self.update_buds_growth(elapsed_time)

        elif growth_stage == GrowthStage.FLOWERING:
            self.update_stem_growth(elapsed_time)
            self.update_branches_growth(elapsed_time)
            self.update_leaves_growth(elapsed_time)
            self.update_buds_growth(elapsed_time, flowering=True)

        elif growth_stage == GrowthStage.MATURITY:
            self.update_stem_maintenance(elapsed_time)
            self.update_branches_maintenance(elapsed_time)
            self.update_leaves_maintenance(elapsed_time)
            self.update_buds_maintenance(elapsed_time)
            self.update_seeds_or_fruits_production(elapsed_time)

    def update_stem_growth(self, elapsed_time):
        growth_amount = self.seed.growth_speed * elapsed_time
        new_height = self.stem.height + growth_amount

        if new_height > self.seed.max_height:
            new_height = self.seed.max_height

        self.stem.height = new_height
#When vegetative is set to True, the growth speed of branches and leaves is increased by a factor of 1.5. This simulates the accelerated growth that occurs during the vegetative stage.
    def update_branches_growth(self, elapsed_time, vegetative=False):
        branches_to_add = int(self.seed.max_branches * self.seed.growth_speed * elapsed_time)

        if len(self.branches) + branches_to_add > self.seed.max_branches:
            branches_to_add = self.seed.max_branches - len(self.branches)

        for _ in range(branches_to_add):
            new_branch = Branch()
            if vegetative:
                new_branch.growth_speed *= 1.5
            self.branches.append(new_branch)

    def update_leaves_growth(self, elapsed_time, vegetative=False):
        leaves_to_add = int(self.seed.max_leaves * self.seed.growth_speed * elapsed_time)

        if len(self.leaves) + leaves_to_add > self.seed.max_leaves:
            leaves_to_add = self.seed.max_leaves - len(self.leaves)

        for _ in range(leaves_to_add):
            new_leaf = Leaf()
            if vegetative:
                new_leaf.growth_speed *= 1.5
            self.leaves.append(new_leaf)


    def update_buds_growth(self, elapsed_time, flowering=False):
        growth_factor = 1.5 if flowering else 1
        buds_to_add = int(self.seed.max_buds * self.seed.growth_speed * growth_factor * elapsed_time)

        # Ensure the number of buds doesn't exceed the max number specified in the seed parameters
        if len(self.buds) + buds_to_add > self.seed.max_buds:
            buds_to_add = self.seed.max_buds - len(self.buds)

        # Add new buds
        for _ in range(buds_to_add):
            self.buds.append(Bud())



#Now you should define the maintenance and production methods for each component (stem, branches, leaves, buds, and seeds/fruits). These methods should focus on maintaining the health of the plant, repairing any damage, and producing seeds or fruits, if applicable. Here's an example of how you can define these methods:
   
    def update_stem_maintenance(self, elapsed_time):
        water_factor = PlantMaintenance.get_water_factor(self)
        fertilizer_factor = PlantMaintenance.get_fertilizer_factor(self)

        if water_factor < 0.5:
            # Reduce stem attributes (e.g., length, thickness) due to lack of water
            self.stem_length *= 1 - (0.5 - water_factor) * elapsed_time
            self.stem_thickness *= 1 - (0.5 - water_factor) * elapsed_time

        if fertilizer_factor < 0.5:
            # Slow down stem growth and change the plant's color due to lack of fertilizer
            self.stem_growth_rate *= 1 - (0.5 - fertilizer_factor) * elapsed_time
            self.color = self.adjust_color_based_on_fertilizer(fertilizer_factor)

    def adjust_color_based_on_fertilizer(self, fertilizer_factor):
        # Assuming the color is a tuple of RGB values (0-255)
        r, g, b = self.color

        # Decrease the green component of the color based on the fertilizer factor
        green_adjustment = int((1 - fertilizer_factor) * 50)
        g = max(0, g - green_adjustment)

        return r, g, b
    


    def update_branches_maintenance(self, elapsed_time):
        water_factor = PlantMaintenance.get_water_factor(self)
        fertilizer_factor = PlantMaintenance.get_fertilizer_factor(self)

        if water_factor < 0.5:
            # Reduce stem attributes (e.g., length, thickness) due to lack of water
            self.stem_length *= 1 - (0.5 - water_factor) * elapsed_time
            self.stem_thickness *= 1 - (0.5 - water_factor) * elapsed_time

        if fertilizer_factor < 0.5:
            # Slow down stem growth and change the plant's color due to lack of fertilizer
            self.stem_growth_rate *= 1 - (0.5 - fertilizer_factor) * elapsed_time
            self.color = self.adjust_color_based_on_fertilizer(fertilizer_factor)

    def adjust_color_based_on_fertilizer(self, fertilizer_factor):
        # Assuming the color is a tuple of RGB values (0-255)
        r, g, b = self.color

        # Decrease the green component of the color based on the fertilizer factor
        green_adjustment = int((1 - fertilizer_factor) * 50)
        g = max(0, g - green_adjustment)

        return r, g, b

    def update_leaves_maintenance(self, elapsed_time):
        water_factor = PlantMaintenance.get_water_factor(self)
        fertilizer_factor = PlantMaintenance.get_fertilizer_factor(self)

        if water_factor < 0.5:
            # Reduce stem attributes (e.g., length, thickness) due to lack of water
            self.stem_length *= 1 - (0.5 - water_factor) * elapsed_time
            self.stem_thickness *= 1 - (0.5 - water_factor) * elapsed_time

        if fertilizer_factor < 0.5:
            # Slow down stem growth and change the plant's color due to lack of fertilizer
            self.stem_growth_rate *= 1 - (0.5 - fertilizer_factor) * elapsed_time
            self.color = self.adjust_color_based_on_fertilizer(fertilizer_factor)

    def adjust_color_based_on_fertilizer(self, fertilizer_factor):
        # Assuming the color is a tuple of RGB values (0-255)
        r, g, b = self.color

        # Decrease the green component of the color based on the fertilizer factor
        green_adjustment = int((1 - fertilizer_factor) * 50)
        g = max(0, g - green_adjustment)

        return r, g, b

    def update_buds_maintenance(self, elapsed_time):
        water_factor = PlantMaintenance.get_water_factor(self)
        fertilizer_factor = PlantMaintenance.get_fertilizer_factor(self)

        if water_factor < 0.5:
            # Reduce stem attributes (e.g., length, thickness) due to lack of water
            self.stem_length *= 1 - (0.5 - water_factor) * elapsed_time
            self.stem_thickness *= 1 - (0.5 - water_factor) * elapsed_time

        if fertilizer_factor < 0.5:
            # Slow down stem growth and change the plant's color due to lack of fertilizer
            self.stem_growth_rate *= 1 - (0.5 - fertilizer_factor) * elapsed_time
            self.color = self.adjust_color_based_on_fertilizer(fertilizer_factor)

    def adjust_color_based_on_fertilizer(self, fertilizer_factor):
        # Assuming the color is a tuple of RGB values (0-255)
        r, g, b = self.color

        # Decrease the green component of the color based on the fertilizer factor
        green_adjustment = int((1 - fertilizer_factor) * 50)
        g = max(0, g - green_adjustment)

        return r, g, b



    def get_growth_stage(self):
        if self.age < self.seed.seedling_duration:
            return GrowthStage.SEEDLING
        elif self.age < self.seed.seedling_duration + self.seed.vegetative_duration:
            return GrowthStage.VEGETATIVE
        elif self.age < self.seed.seedling_duration + self.seed.vegetative_duration + self.seed.flowering_duration:
            return GrowthStage.FLOWERING
        else:
            return GrowthStage.MATURITY