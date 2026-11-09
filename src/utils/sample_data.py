"""Generate and provide sample data.

This module provides synthetic sample data for use during application
development.
"""

import random
import pandas as pd
from pathlib import Path

SUBGROUPS = ['All Students', 'Female', 'Male', 'Non-binary',
             'Students with Disabilities',
             'American Indian or Alaska Native',
             'Asian or Native Hawaiian/Other Pacific Islander',
             'Black or African American', 'Hispanic or Latino',
             'White', 'Multiracial', 'Economically Disadvantaged',
             'English Language Learner', 'In Foster Care',
             'Homeless', 'Migrant', 'Parent in Armed Forces']

# Source for ANIMALS list:
# https://gist.github.com/CheeseCake87/c1d222c387ff1342cf3b910456f4865a
ANIMALS = ['Canidae', 'Felidae', 'Cat', 'Cattle', 'Dog', 'Donkey', 'Goat',
           'Horse', 'Pig', 'Rabbit', 'Aardvark', 'Aardwolf', 'Albatross',
           'Alligator', 'Alpaca', 'Amphibian', 'Anaconda', 'Angelfish',
           'Anglerfish', 'Ant', 'Anteater', 'Antelope', 'Antlion', 'Ape',
           'Aphid', 'Armadillo', 'Asp', 'Baboon', 'Badger', 'Bandicoot',
           'Barnacle', 'Barracuda', 'Basilisk', 'Bass', 'Bat', 'Bear',
           'Beaver', 'Bedbug', 'Bee', 'Beetle', 'Bird', 'Bison', 'Blackbird',
           'Boa', 'Boar', 'Bobcat', 'Bobolink', 'Bonobo', 'Bovid', 'Bug',
           'Butterfly', 'Buzzard', 'Camel', 'Canid', 'Capybara', 'Cardinal',
           'Caribou', 'Carp', 'Cat', 'Catshark', 'Caterpillar', 'Catfish',
           'Cattle', 'Centipede', 'Cephalopod', 'Chameleon', 'Cheetah',
           'Chickadee', 'Chicken', 'Chimpanzee', 'Chinchilla', 'Chipmunk',
           'Clam', 'Clownfish', 'Cobra', 'Cockroach', 'Cod', 'Condor',
           'Constrictor', 'Coral', 'Cougar', 'Cow', 'Coyote', 'Crab', 'Crane',
           'Crawdad', 'Crayfish', 'Cricket', 'Crocodile', 'Crow', 'Cuckoo',
           'Cicada', 'Damselfly', 'Deer', 'Dingo', 'Dinosaur', 'Dog',
           'Dolphin', 'Donkey', 'Dormouse', 'Dove', 'Dragonfly', 'Dragon',
           'Duck', 'Eagle', 'Earthworm', 'Earwig', 'Echidna', 'Eel', 'Egret',
           'Elephant', 'Elk', 'Emu', 'Ermine', 'Falcon', 'Ferret', 'Finch',
           'Firefly', 'Fish', 'Flamingo', 'Flea', 'Fly', 'Flyingfish', 'Fowl',
           'Fox', 'Frog', 'Gamefowl', 'Galliform', 'Gazelle', 'Gecko',
           'Gerbil', 'Gibbon', 'Giraffe', 'Goat', 'Goldfish', 'Goose',
           'Gopher', 'Gorilla', 'Grasshopper', 'Grouse', 'Guan', 'Guanaco',
           'Guineafowl', 'Gull', 'Guppy', 'Haddock', 'Halibut', 'Hamster',
           'Hare', 'Harrier', 'Hawk', 'Hedgehog', 'Heron', 'Herring',
           'Hippopotamus', 'Hookworm', 'Hornet', 'Horse', 'Hoverfly',
           'Hummingbird', 'Hyena', 'Iguana', 'Impala', 'Jackal', 'Jaguar',
           'Jay', 'Jellyfish', 'Junglefowl', 'Kangaroo', 'Kingfisher', 'Kite',
           'Kiwi', 'Koala', 'Koi', 'Krill', 'Ladybug', 'Lamprey', 'Landfowl',
           'Lark', 'Leech', 'Lemming', 'Lemur', 'Leopard', 'Leopon', 'Limpet',
           'Lion', 'Lizard', 'Llama', 'Lobster', 'Locust', 'Loon', 'Louse',
           'Lungfish', 'Lynx', 'Macaw', 'Mackerel', 'Magpie', 'Mammal',
           'Manatee', 'Mandrill', 'Marlin', 'Marmoset', 'Marmot', 'Marsupial',
           'Marten', 'Mastodon', 'Meadowlark', 'Meerkat', 'Mink', 'Minnow',
           'Mite', 'Mockingbird', 'Mole', 'Mollusk', 'Mongoose', 'Monkey',
           'Moose', 'Mosquito', 'Moth', 'Mouse', 'Mule', 'Muskox', 'Narwhal',
           'Newt', 'Nightingale', 'Ocelot', 'Octopus', 'Opossum', 'Orangutan',
           'Orca', 'Ostrich', 'Otter', 'Owl', 'Ox', 'Panda', 'Panther',
           'Parakeet', 'Parrot', 'Parrotfish', 'Partridge', 'Peacock',
           'Peafowl', 'Pelican', 'Penguin', 'Perch', 'Pheasant', 'Pig',
           'Pigeon', 'Pike', 'Pinniped', 'Piranha', 'Planarian', 'Platypus',
           'Pony', 'Porcupine', 'Porpoise', 'Possum', 'Prawn', 'Primate',
           'Ptarmigan', 'Puffin', 'Puma', 'Python', 'Quail', 'Quelea',
           'Quokka', 'Rabbit', 'Raccoon', 'Rat', 'Rattlesnake', 'Raven',
           'Reindeer', 'Reptile', 'Rhinoceros', 'Roadrunner', 'Rodent', 'Rook',
           'Rooster', 'Roundworm', 'Sailfish', 'Salamander', 'Salmon',
           'Sawfish', 'Scallop', 'Scorpion', 'Seahorse', 'Shark', 'Sheep',
           'Shrew', 'Shrimp', 'Silkworm', 'Silverfish', 'Skink', 'Skunk',
           'Sloth', 'Slug', 'Smelt', 'Snail', 'Snake', 'Snipe', 'Sole',
           'Sparrow', 'Spider', 'Spoonbill', 'Squid', 'Squirrel', 'Starfish',
           'Stingray', 'Stoat', 'Stork', 'Sturgeon', 'Swallow', 'Swan',
           'Swift', 'Swordfish', 'Swordtail', 'Tahr', 'Takin', 'Tapir',
           'Tarantula', 'Tarsier', 'Termite', 'Tern', 'Thrush', 'Tick',
           'Tiger', 'Tiglon', 'Toad', 'Tortoise', 'Toucan', 'Trout', 'Tuna',
           'Turkey', 'Turtle', 'Tyrannosaurus', 'Urial', 'Vicuna', 'Viper',
           'Vole', 'Vulture', 'Wallaby', 'Walrus', 'Wasp', 'Warbler', 'Weasel',
           'Whale', 'Whippet', 'Whitefish', 'Wildcat', 'Wildebeest',
           'Wildfowl', 'Wolf', 'Wolverine', 'Wombat', 'Woodpecker', 'Worm',
           'Wren', 'Xerinae', 'Yak', 'Zebra', 'Alpaca', 'Cat', 'Cattle',
           'Chicken', 'Dog', 'Donkey', 'Ferret', 'Gayal', 'Goldfish', 'Guppy',
           'Horse', 'Koi', 'Llama', 'Sheep', 'Yak', 'Statewide']


def generate_sample_grad_rate_data():
    """Generate synthetic data for graduation rates.

    This function writes randomly-generated graduation rate data to a csv
    file for use as sample data. The data includes several school districts,
    6 years of data, realistic subgroups, and graduation rates for 4-year,
    5-year, and 6-year cohorts.
    """
    # Define file path for sample data csv
    file_path = "data/sample_grad_rate_data.csv"

    # Check if file already exists
    if Path(file_path).is_file():
        # If the file exists, no need to generate data - exit the funciton
        return

    # Build a list to store rows of data
    data_rows = []

    for animal_name in ANIMALS:

        # Create a name for a fictional school district
        district = animal_name + ' School District'

        for subgroup in SUBGROUPS:

            # Randomly generate sample grad rate data
            base_rate = random.uniform(40, 80)

            # Ensure that 'All Students' has a high base rate
            if subgroup == 'All Students':
                base_rate = 80.0

            # Generate 4-year grad rates for 2020 through 2025
            four_year = [base_rate]
            for i in range(5):
                last_rate = four_year[-1]

                # Generate a random change from one year to the next
                change = random.uniform(-1, 3)
                # Rates capped at 100%
                next_rate = min(last_rate + change, 100.0)

                four_year.append(next_rate)

            # Generate 5-year grad rates as 5% higher than 4-year rates
            # and 6-year grad rates as 5% higher than 5-year rates
            five_year = []
            six_year = []

            for four_rate in four_year:

                five_rate = min(four_rate * 1.05, 100.0)
                five_year.append(five_rate)

                six_rate = min(five_rate * 1.05, 100.0)
                six_year.append(six_rate)

            # Format rows of data
            for i in range(6):
                year = 2020 + i

                # Add 1 row per year for four-year grad rate
                four_row = {'year': year, 'district': district,
                            'subgroup': subgroup,
                            'metric': 'Four-Year Graduation Rate',
                            'value': four_year[i]}
                data_rows.append(four_row)

                # Add 1 row per year for five-year grad rate
                five_row = {'year': year, 'district': district,
                            'subgroup': subgroup,
                            'metric': 'Five-Year Graduation Rate',
                            'value': five_year[i]}
                data_rows.append(five_row)

                # Add 1 row per year for six-year grad rate
                six_row = {'year': year, 'district': district,
                           'subgroup': subgroup,
                           'metric': 'Six-Year Graduation Rate',
                           'value': six_year[i]}
                data_rows.append(six_row)

    # Convert rows to Pandas DataFrame
    sample_grad_rate_df = pd.DataFrame(data_rows)

    # Write data to csv
    sample_grad_rate_df.to_csv(file_path, index=False)


def get_sample_grad_rate_data():
    """Get sample graduation rate data.

    Returns:
        DataFrame: sample data for graduation rates.
    """
    # Define file path for sample data csv
    file_path = "data/sample_grad_rate_data.csv"

    # If file does not exist, generate file
    if not Path(file_path).is_file():
        generate_sample_grad_rate_data()

    # Read csv as DataFrame
    sample_grad_rate_df = pd.read_csv(file_path)
    return sample_grad_rate_df
