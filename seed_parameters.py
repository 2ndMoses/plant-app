import random



#Define the Seed class with seed parameters: Create a class to store seed parameters such as growth speed, size, and any other attributes that may vary between plants. You can add as many parameters as needed to make your simulation more interesting:
class Seed:
    def __init__(self, max_height, max_branches, max_leaves, max_buds, growth_speed, seedling_duration, vegetative_duration, flowering_duration):
        self.max_height = max_height
        self.max_branches = max_branches
        self.max_leaves = max_leaves
        self.max_buds = max_buds
        self.growth_speed = growth_speed
        self.seedling_duration = seedling_duration
        self.vegetative_duration = vegetative_duration
        self.flowering_duration = flowering_duration



#Add a randomization method to the Seed class: Implement a class method in the Seed class to generate a random seed with randomized parameters. You can set minimum and maximum values for each parameter to control the range of possible values:
    @classmethod
    def random_seed(cls):
        growth_speed = random.uniform(0.5, 1.5)
        max_height = random.uniform(50, 150)
        max_branches = random.randint(3, 10)
        max_leaves = random.randint(30, 100)
        max_buds = random.randint(10, 50)
        seedling_duration = random.randint(5, 10) #days
        vegetative_duration = random.randint(10, 20) #days
        flowering_duration = random.randint(10, 20) #days
        return cls(max_height, max_branches, max_leaves, max_buds, growth_speed, seedling_duration, vegetative_duration, flowering_duration)
