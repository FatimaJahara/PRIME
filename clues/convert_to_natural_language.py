from together import Together
import os

key = os.getenv("TOGETHER_API_KEY", None)

def llama_inference(prompt,api_key=key):
    active_key = api_key or key or os.getenv("TOGETHER_API_KEY")
    if not active_key:
        raise ValueError(" No Together API key provided. Use --api_key or set TOGETHER_API_KEY.")
    client = Together(api_key=active_key)
    response = client.completions.create(
    temperature=0,
    model= "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    prompt=f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>
{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    stream=False,)
    return response.choices[0].text


def true_false_nlt(logic_clue):

    prompt = f"""
    System:
    You are an AI agent specialized in translating logical statements into natural language.
    You are given a logical statement enclosed within ####.
    Your task is to convert the "True/False" logical statement into a single, clear and natural English sentence, ensuring accuracy and readability.

    Here are some examples:

    Logic Clue: !(( favorite food = pasta ) <=> ( house color = green ))
    Natural Language Explanation: The person whose favorite food is pasta does not have a green house.

    Logic Clue: ( Pet = cat ) <=> ( Hobby = fishing )
    Natural Language Explanation: The person who has cat likes fishing.

    Logic Clue: !(( Fruit = apple ) <=> ( Vehicle = truck ))
    Natural Language Explanation: The person who likes apples does not own a truck.

    Logic Clue: !(( Occupation = doctor ) <=> ( Pet= dog ))
    Natural Language Explanation: The person whose occupation is doctor does not own a pet dog.

    Logic Clue: ( Name = Eric ) <=> ( vehicle = car )
    Natural Language Explanation: The person whose name is Eric owns a car.

    Logic Clue: ( Sport = soccer ) <=> ( Favorite drink = coffee )
    Natural Language Explanation: The person who likes soccer prefers coffee.

    Logic Clue: !(( Reptile = black racer ) <=> ( Baby Food = asparagus puree ))
    Natural Language Explanation: The person whose reptile is a black racer does not have asparagus puree as baby food.

    Logic Clue: !(( Name = Alice ) <=> ( Day = 24th day ))
    Natural Language Explanation: The day designated to Alice is not the 24th day.

    Logic Clue: ( Language = Spanish ) <=> ( Organ = bones )
    Natural Language Explanation: The person who speaks Spanish has bones as their associated organ.

    Logic Clue: !(( Personality = rational ) <=> ( Types of Clock = pillar clock ))
    Natural Language Explanation: The person with the rational personality does not have a pillar clock.

    User:
    Convert the following logic clue into a single natural language sentence:
    ####{logic_clue}####
    Only return the sentence without explanations, formatting, or additional text.
    """
    try:
        response = llama_inference(prompt)
        return response
    except Exception as e:
        print(f"Error processing text: {logic_clue}\n{e}")
        return None


def neither_nor_nlt(logic_clue):

    prompt = f"""
    System:
    You are an AI agent specialized in translating logical statements into natural language.
    You are given a logical statement enclosed within ####.
    Your task is to convert the "Neither Nor" logical statement into a single, clear and natural English sentence, ensuring accuracy and readability.

    Here are some examples:

    Logic Clue: (!( Maze = labyrinth ) and !( Maze = maze race )) <=> ( Traffic sign = height limit )
    Natural Language Explanation: Neither the person with labyrinth nor the one with maze race has height limit as their traffic sign.

    Logic Clue: (!( Pet = dog ) and !( Pet = parrot )) <=> ( Occupation = doctor )
    Natural Language Explanation: Neither the person with a dog nor the one with parrot is a doctor.

    Logic Clue: (!( Hobby = painting ) and !( Hobby = hiking )) <=> ( Favorite Book = "1984" )
    Natural Language Explanation: Neither the person who enjoys painting nor the one who enjoys hiking has 1984 as their favorite book.

    Logic Clue: (!( Musical Instrument = guitar ) and !( Musical Instrument = violin )) <=> ( Pet = rabbit )
    Natural Language Explanation: Neither the guitar player nor violin player has a rabbit.

    Logic Clue: (!( Types of Pies = mango pie ) and !( Types of Pies = zucchini pie )) <=> ( Train = sleeper train )
    Natural Language Explanation: Neither the person who has mango pie nor the one who has zucchini pie has a sleeper train.

    Logic Clue: (!(Movie Genre = horror ) and !( Movie Genre = comedy )) <=> ( Favorite Author = Agatha Christie )
    Natural Language Explanation: Neither the person who enjoys horror movies nor the one who enjoys comedies favors Agatha Christie.

    Logic Clue: (!(Food = chocolate ) and !( Food = mint )) <=> ( Superpower = invisibility )
    Natural Language Explanation: Neither the person who prefers chocolate nor the one who prefers mint has invisibility as their superpower.

    Logic Clue: (!( Name = courtney ) and !( Name = billy )) <=> ( Types of Pies = strawberry pie )
    Natural Language Explanation: Neither Courtney nor Billy prefers strawberry pie.

    Logic Clue: (!( Car Brand = Tesla ) and !( Car Brand = Toyota )) <=> ( Name = Bob )
    Natural Language Explanation: Neither the Tesla owner nor the Toyota owner is Bob.

    Logic Clue: (!( Sport = basketball ) and !( Sport = tennis )) <=> ( Tea Type = green tea )
    Natural Language Explanation: Neither the basketball player nor tennis player drinks green tea.

    User:
    Convert the following logic clue into a single natural language sentence:
    ####{logic_clue}####
    Only return the sentence without explanations, formatting, or additional text.
    """
    try:
        response = llama_inference(prompt)
        return response
    except Exception as e:
        print(f"Error processing text: {logic_clue}\n{e}")
        return None


def either_or_nlt(logic_clue):

    prompt = f"""
    System:
    You are an AI agent specialized in translating logical statements into natural language.
    You are given a logical statement enclosed within ####.
    Your task is to convert the "Either Or" logical statement into a single, clear and natural English sentence, ensuring accuracy and readability.

    Here are some examples:

    Logic Clue: ((( Types of Pies = strawberry pie ) or ( Types of Pies=elderberry pie )) and !(( Types of Pies = strawberry pie ) and ( Types of Pies = elderberry pie ))) <=> ( Traffic sign = no parking )
    Natural Language Explanation: The person with no parking traffic sign eats either strawberry pie or elderberry pie.

    Logic Clue: ((( Pet = dog ) or ( Occupation = nurse )) and !((Pet = dog) and ( Occupation = nurse ))) <=> ( Car Brand = tesla )
    Natural Language Explanation: The person who drives a Tesla either has a dog or works as a nurse.

    Logic Clue: ((( Age = 25 ) or ( age = 30 )) and !(( age = 25 ) and ( age = 30 ))) <=> ( Name = bob )
    Natural Language Explanation: Bob is either 25 or 30.

    Logic Clue: ((( Hobby = painting ) or ( Board Game = monopoly )) and !(( Hobby = painting ) and ( Board Game = monopoly )) <=> ( Book Genre = mystery )
    Natural Language Explanation: The person who enjoys reading mystery books either likes painting or plays monopoly.

    Logic Clue: ((( Board Game = chess ) or ( Board Game = scrabble )) and !(( Board Game = chess ) and ( Board Game = scrabble ))) <=> ( Animal = dolphin )
    Natural Language Explanation: The person whose associated animal is dolphin either plays chess or Scrabble.

    Logic Clue: ((( Clothing = shirt ) or ( Shoe Brand = adidas )) and !(( Clothing = shirt ) and ( Shoe Brand = adidas ))) <=> ( Dessert = cheesecake )
    Natural Language Explanation: The person who enjoys cheesecake either wears a shirt or owns Adidas shoes.

    Logic Clue: ((( Satellite = AcrimSat ) or ( Programming Language = java )) and !(( Satellite = AcrimSat ) and ( Programming Language = java ))) <=> ( Job Title = data scientist )
    Natural Language Explanation: The person who is a Data Scientist either has the AcrimSat satellite or programs in Java.


    Logic Clue: ((( Name = Bob ) or ( Age = 53 years )) and !(( Name = Bob ) and ( Age = 53 years ))) <=> ( Swimming Stroke = kickboard drill )
    Natural Language Explanation: The person who uses the kickboard drill swimming stroke is either named Bob or is 53 years old.

    Logic Clue: ((( Name = anthony ) or ( Name = sean )) and !(( Name = anthony ) and ( Name = sean ))) <=> ( Landform Type = volcano )
    Natural Language Explanation: The person who has a volcano as their landform type is either Anthony or Sean.

    Logic Clue: (( Galaxy = ngc 253 ) or ( Shapes = hypersphere )) and !(( Galaxy = ngc 253 ) and ( Shapes = hypersphere ))) <=> ( Swimming Stroke = hand-over-hand crawl )
    Natural Language Explanation: The person who uses the hand-over-hand crawl swimming stroke either has the NGC 253 galaxy or the hypersphere shape.

    User:
    Convert the following logic clue into a single natural language sentence:
    ####{logic_clue}####
    Only return the sentence without explanations, formatting, or additional text.
    """
    try:
        response = llama_inference(prompt)
        return response
    except Exception as e:
        print(f"Error processing text: {logic_clue}\n{e}")
        return None


def unaligned_nlt(logic_clue):

    prompt = f"""
    System:
    You are an AI agent specialized in translating logical statements into natural language.
    You are given a logical statement enclosed within ####.
    Your task is to convert the "Unaligned Pair" logical statement into a single, clear and natural English sentence, ensuring accuracy and readability.

    Here are some examples:

    Logic Clue: !(( Types of Grains = buckwheat ) <=> ( Name = stacy )) and ((( Types of Grains = buckwheat ) <=> ( Road Type = freeway )) or (( Types of Grains = buckwheat ) <=> ( Road Type = dirt road ))) and ((( Name = stacy ) <=> ( Road Type = freeway )) or (( Name = stacy ) <=> ( Road Type = dirt road )))
    Natural Language Explanation: Of Stacy and the person who has buckwheat, one is on a freeway and the other is on a dirt road.

    Logic Clue: !(( Types of Plants = grasses ) <=> ( Name = edward )) and ((( Types of Plants = grasses ) <=> ( Types of Grains = semolina )) or (( Types of Plants = grasses ) <=> ( Types of Grains = grain ))) and ((( Name = edward ) <=> ( Types of Grains = semolina )) or (( Name = edward ) <=> ( Types of Grains = grain )))
    Natural Language Explanation: Of Edward and the person who has grasses, one has semolina, and the other has grain.

    Logic Clue: !(( Train = bullet train ) <=> ( Weather Condition = sleet )) and ((( Train = bullet train ) <=> ( Name = dennis )) or (( Train = bullet train ) <=> ( Name = kenneth ))) and ((( Weather Condition = sleet ) <=> ( Name = dennis )) or (( Weather Condition = sleet ) <=> ( Name = kenneth )))
    Natural Language Explanation: Of the person who has a bullet train and the one experiencing sleet, one is Dennis, and the other is Kenneth.

    Logic Clue: !(( Birth Year = 1980.0 ) <=> ( Train = diesel-electric train )) and ((( Birth Year = 1980.0 ) <=> ( Name = sarah )) or (( Birth Year = 1980.0 ) <=> ( Name = kenneth ))) and ((( Train = diesel-electric train ) <=> ( Name = sarah )) or (( Train = diesel-electric train ) <=> ( Name = kenneth )))
    Natural Language Explanation: Of Sarah and Kenneth, one was born in 1980, and the other has a diesel-electric train.

    Logic Clue: !(( Name = derrick ) <=> ( Algorithm = longest common subsequence )) and ((( Name = derrick ) <=> ( Maze = cylindrical maze )) or (( Name = derrick ) <=> ( Maze = picture maze ))) and ((( Algorithm = longest common subsequence ) <=> ( Maze = cylindrical maze )) or (( Algorithm = longest common subsequence ) <=> ( Maze = picture maze )))
    Natural Language Explanation: Of Derrick and the person using the longest common subsequence algorithm, one has a cylindrical maze, and the other has a picture maze.

    Logic Clue: !(( Hair Color = mahogany ) <=> ( Types of Nuts = noisette )) and ((( Hair Color = mahogany ) <=> ( Herb = carob )) or (( Hair Color = mahogany ) <=> ( Herb = wintergreen ))) and ((( Types of Nuts = noisette ) <=> ( Herb = carob )) or (( Types of Nuts = noisette ) <=> ( Herb = wintergreen )))
    Natural Language Explanation: Of the person with mahogany hair and the one with noisette nuts, one has carob, and the other has wintergreen as their herb.

    Logic Clue: !(( Name = kristen ) <=> ( Types of Leaves = linear leaf )) and ((( Name = kristen ) <=> ( Monster = abominable snowman )) or (( Name = kristen ) <=> ( Monster = demon ))) and ((( Types of Leaves = linear leaf ) <=> ( Monster = abominable snowman )) or (( Types of Leaves = linear leaf ) <=> ( Monster = demon )))
    Natural Language Explanation: Of Kristen and the person with a linear leaf, one has the abominable snowman, and the other has the demon as their associated monster.

    Logic Clue: !(( Train = sleeper train ) <=> ( DC Comic Characters = plastic man )) and ((( Train = sleeper train ) <=> ( Age = 42 years )) or (( Train = sleeper train ) <=> ( Age = 24 years ))) and ((( DC Comic Characters = plastic man ) <=> ( Age = 42 years )) or (( DC Comic Characters = plastic man ) <=> ( Age = 24 years )))
    Natural Language Explanation: Of the person with the sleeper train and the one with plastic man, one is 42 years old, and the other is 24 years old.

    Logic Clue: !(( Landform Type = volcano ) <=> ( Types of Leaves = scale leaf )) and ((( Landform Type = volcano ) <=> ( Name = anthony )) or (( Landform Type = volcano ) <=> ( Name = sean ))) and ((( Types of Leaves = scale leaf ) <=> ( Name = anthony )) or (( Types of Leaves = scale leaf ) <=> ( Name = sean )))
    Natural Language Explanation: Of the person who has a volcano as their landform type and the one who has a scale leaf, one is Anthony, and the other is Sean.

    Logic Clue: !(( Swimming Stroke = kickboard drill ) <=> ( Name = chad )) and ((( Swimming Stroke = kickboard drill ) <=> ( Age = 53 years )) or (( Swimming Stroke = kickboard drill ) <=> ( Age = 30 years ))) and ((( Name = chad ) <=> ( Age = 53 years )) or (( Name = chad ) <=> ( Age = 30 years )))
    Natural Language Explanation: Of the person who uses the kickboard drill and the one named Chad, one is 53 years old, and the other is 30 years old.

    User:
    Convert the following logic clue into a single natural language sentence:
    ####{logic_clue}####
    Only return the sentence without explanations, formatting, or additional text.
    """
    try:
        response = llama_inference(prompt)
        return response
    except Exception as e:
        print(f"Error processing text: {logic_clue}\n{e}")
        return None



def multi_elimination_nlt(logic_clue):

    prompt = f"""
    System:
    You are an AI agent specialized in translating logical statements into natural language.
    You are given a logical statement enclosed within ####.
    Your task is to convert the "Multi-Elimination" logical statement into a single, clear and natural English sentence, ensuring accuracy and readability.

    Here are some examples:

    Logic Clue: !(( Weather Condition = thunderstorm ) <=> ( Birth Year = 1988.0 )) and !(( Weather Condition = thunderstorm ) <=> ( Train = tanker train ))  and !(( Birth Year = 1988.0 ) <=> ( Train = tanker train ))
    Natural Language Explanation: The three people are the one experiencing a thunderstorm, the one born in 1988, and the one with the tanker train.

    Logic Clue: !(( Name = derrick ) <=> ( Algorithm = minimax algorithm )) and !(( Name = derrick ) <=> ( Train = commuter train ))  and !(( Algorithm = minimax algorithm ) <=> ( Train = commuter train ))
    Natural Language Explanation: The three people are the one named Derrick, the one using the minimax algorithm, and the one with the commuter train.

    Logic Clue: !(( Types of Nuts = almond ) <=> ( Movie Genre = romantic comedy )) and !(( Types of Nuts = almond ) <=> ( Name = christy ))  and !(( Movie Genre = romantic comedy ) <=> ( Name = christy ))
    Natural Language Explanation: The three people are the one with almonds, the one who likes romantic comedies, and Christy.

    Logic Clue: !(( Monster = godzilla ) <=> ( Age = 30 years )) and !(( Monster = godzilla ) <=> ( Name = christy ))  and !(( Age = 30 years ) <=> ( Name = christy ))
    Natural Language Explanation: The three people are the one with the monster Godzilla, the one who is 30 years old, and Christy.

    Logic Clue: !(( Insect = darkling beetle ) <=> ( Name = heather )) and !(( Insect = darkling beetle ) <=> ( Plant Parts = axillary bud ))  and !(( Name = heather ) <=> ( Plant Parts = axillary bud ))
    Natural Language Explanation: The three people are the one with the darkling beetle, the one named Heather, and the one with the axillary bud.

    Logic Clue: !(( Chemical Compund = radium ) <=> ( Rocks = peridotite )) and !(( Chemical Compund = radium ) <=> ( Mathematical Theorem = cauchy's integral theorem ))  and !(( Rocks = peridotite ) <=> ( Mathematical Theorem = cauchy's integral theorem ))
    Natural Language Explanation: The three people are the one with radium, the one with peridotite, and the one with Cauchy's integral theorem.

    Logic Clue: !(( Soil Type = entisol soil ) <=> ( Name = billy )) and !(( Soil Type = entisol soil ) <=> ( Organ = smooth muscles ))  and !(( Name = billy ) <=> ( Organ = smooth muscles ))
    Natural Language Explanation: The three people are the one with entisol soil, the one named Billy, and the one with smooth muscles organ.

    Logic Clue: !(( Dog = portuguese water dog ) <=> ( Chemical Compound = holmium )) and !(( Dog = portuguese water dog ) <=> ( Name = nathan ))  and !(( Chemical Compound = holmium ) <=> ( Name = nathan ))
    Natural Language Explanation: The three people are the one with the Portuguese Water Dog, the one with holmium, and Nathan.

    Logic Clue: !(( Favourite Season = monsoon ) <=> ( Day in a Month = 22nd day )) and !(( Favourite Season = monsoon ) <=> ( Name = lori ))  and !(( Day in a Month = 22nd day ) <=> ( Name = lori ))
    Natural Language Explanation: The three people are the one who likes monsoon, the one born on the 22nd day, and Lori.

    Logic Clue: !(( Dinosaur = parasaurolophus ) <=> ( Name = natasha )) and !(( Dinosaur = parasaurolophus ) <=> ( Types of Pizza = mexican street corn pizza ))  and !(( Name = natasha ) <=> ( Types of Pizza = mexican street corn pizza ))
    Natural Language Explanation: The three people are the one with the Parasaurolophus, the one named Natasha, and the one with Mexican street corn pizza.

        User:
    Convert the following logic clue into a single natural language sentence:
    ####{logic_clue}####
    Only return the sentence without explanations, formatting, or additional text.
    """
    try:
        response = llama_inference(prompt)
        return response
    except Exception as e:
        print(f"Error processing text: {logic_clue}\n{e}")
        return None


import re
def detect_clue_type(clue):

    allowed_chars = r"[\wÀ-ÖØ-öø-ÿ\s_\-–—'ʻ’\"\/\\&,:#(){}\[\]=!<>?+*/%^.\d]+"

    patterns = {
        "True-False": rf"\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*[!=]=\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)",
        "Neither-Nor": rf"\(!\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*and\s*!\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\)\s*=\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)",
        "Either-Or": rf"\(\(\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*or\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\)\s*and\s*!\(\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*and\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\)\)\s*=\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)",
        "Unaligned-Pair": rf"!.*?\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*and\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*and\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)",
        "Multi-Elimination": rf"!.*?\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*and\s*!.*?\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*and\s*!.*?\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)"
    }

    for clue_type, pattern in patterns.items():
        if re.fullmatch(pattern, clue.replace(" ", "")):
            return clue_type

    return "Unknown"


import os
import json

def generate_natural_clues(source_file_path, destination_file_path):

    with open(source_file_path, "r") as f:
        puzzle = json.load(f)

    if puzzle["versions"]['generic']["clues"]["solution_clues_nl"] == []:
        for version in ['generic', 'stereotypical', 'anti_stereotypical']:
            nl_clues = []
            version_data = puzzle["versions"].get(version)
            solution = version_data["puzzle_table"]
            soln_clues = version_data["clues"]["solution_clues"]

            for clue in soln_clues:
                clue_type = detect_clue_type(clue)
                # print(clue_type)
                if clue_type == "True-False":
                    nl_clues.append(true_false_nlt(clue).strip())
                elif clue_type == "Neither-Nor":
                    nl_clues.append(neither_nor_nlt(clue).strip())
                elif clue_type == "Either-Or":
                    nl_clues.append(either_or_nlt(clue).strip())
                elif clue_type == "Unaligned-Pair":
                    nl_clues.append(unaligned_nlt(clue).strip())
                elif clue_type == "Multi-Elimination":
                    nl_clues.append(multi_elimination_nlt(clue).strip())
                else:
                    print(f"Unknown clue: {clue}")


            if len(nl_clues) == len(soln_clues):
                version_data["clues"]["solution_clues_nl"] = list(nl_clues)
            else:
                version_data["clues"]["solution_clues_nl"] = []
                print(f"Warning: Puzzle {puzzle['id']} version {version} did not produce the required natural language clue set.")

        os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

        with open(destination_file_path, "w") as f:
            json.dump(puzzle, f, indent=4)
        # print(f"Updated puzzle file saved: {destination_file_path}")

    else:
        print(f"Puzzle {puzzle['id']} already has natural language clues.")

def process_puzzles_in_folder(source_dir, destination_dir):

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".json"):
                source_file_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, source_dir)
                dest_folder = os.path.join(destination_dir, rel_path)
                destination_file_path = os.path.join(dest_folder, file)
                generate_natural_clues(source_file_path, destination_file_path)

# puzzle_directory = ""
# destination_directory = ""
# process_puzzles_in_folder(puzzle_directory, destination_directory)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate natural language clues from logical clues using Llama 3.3 via Together API.")
    parser.add_argument("--src", type=str, required=True, help="Path to the folder containing JSON puzzle files")
    parser.add_argument("--dest", type=str, required=True, help="Output folder to save puzzles with natural-language clues")
    parser.add_argument("--api_key", type=str, required=False, default=None, help="Together API key (optional; falls back to the script default)")

    args = parser.parse_args()

    if args.api_key:
        key = args.api_key  # overwrite default if provided

    process_puzzles_in_folder(args.src, args.dest)
