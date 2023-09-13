from turtle import *

class Navigation:
    compass = { # values to be used for seth() function to turn turtle
        'east' : 0,
        'north' : 90,
        'west' : 180,
        'south' : 270,
        'northeast' : 45,
        'northwest' : 135,
        'southeast' : 315,
        'southwest' : 225 }

    def __init__(self):
        self.facing = 'straight'
        self.angle = 90
        self.distance = 0


def read_directions_file(file_name):
    """Returns a list where each index is a single direction when passed a file
    of directions where each direction is separated by a new line"""
    with open(file_name, "r") as data:
        return data.read().split("\n\n")


def get_distances(list_of_directions):
    """returns a list of the distances to drive in miles. 1st element in list =
    first direction in file, 2nd element = 2nd line, and so on"""
    unit_check = ["mi", "miles", "miles", "ft", "feet"]
    distances = []
    for eachDirection in list_of_directions:
        eachDirection = eachDirection.lower()
        for check in unit_check:
            if check in eachDirection:
                if "min" in eachDirection: # "mi" is in "min" so need to get rid of "min" if in line
                    eachDirection = eachDirection.replace('min', '')
                if eachDirection.count(' ' + check) > 1: # case of "pass by x in y units"
                    eachDirection = eachDirection.replace(' ' + check, '', 1) # replace first instance
                    dist_to_check = eachDirection.split(" " + check)
                else:
                    dist_to_check = eachDirection.split(" " + check)
                for eachDist in dist_to_check:
                    index = 0
                    test = eachDist[(-1 - index):]
                    while test.isnumeric() or test == ".": # until string is no longer a number
                        index += 1
                        test = eachDist[-1 - index]

                    try:
                        current_dist = float(eachDist[(-1 - (index-1)):])
                        if check in ('ft', 'feet'): # convert ft to miles
                            current_dist /= 5280
                            distances.append(current_dist)
                            break
                        else:
                            distances.append(current_dist)
                            break

                    except ValueError:
                        pass

    return distances


def get_direction(current_line):
    """Returns the tuple ("direction", angle) when passed a single instruction from the
    list of instructions"""
    current_line = current_line.lower()

    turns = ['right', 'left']
    for turn in turns: # looking for "right" and "left"
        if turn in current_line:
            tokens = current_line.split()
            index = tokens.index(turn)
            if 'turn' in tokens[index - 1] or 'turn' in tokens[index + 1]:
                # checks if "turn" is in the index that is either directly before or after
                # the index which contains either "right" or "left"
                return (turn, 90)
            elif 'slight' in tokens[index - 1] or 'slight' in tokens[index + 1]:
                # same check but for "slight" indicating a slight turn in that direction
                # 30 is value to pass right and left functions for turtle
                return (turn, 30)

    for orientation in Navigation.compass: # looking for NE, NW, SW, SE
        if orientation in current_line:
            tokens = current_line.split()
            try: # need to use try here because some roads have something like "east" in in
                index = tokens.index(orientation)
                if orientation == tokens[index]:
                    return(orientation, Navigation.compass[orientation])
            except ValueError:
                pass
    # means "right" or "left" or anything from the compass (NE, NW, SW, SE)
    # didn't appear in line so keep straight, right(0) or left(0)
    return ('straight', 0)


def print_action(direction, distance):
    """Prints the action that the turtle is about to draw"""
    action, angle = direction
    units = 'miles'
    if distance < 0.2: # not much of a point in saying drive for 0.1 miles, use feet
        distance *= 5280
        units = 'feet'
    turns = 'right', 'left'
    if action in turns:
        if angle < 90: # means we made a slight turn, rather say "slight turn" than "turn"
            print("Making a slight {} and then continuing for {} {}"
              .format(action, distance, units))
        else:
            print("Turning {} and then continuing for {} {}"
              .format(action, distance, units))
    elif action in Navigation.compass:
        print("Heading {} for {} {}".format(action, distance, units))
    else:
        print("Continuing ahead for {} {}".format(distance, units))


def make_move(direction, distance, scale):
    """Prints the action the turtle is about to make to the console then makes the move on
    the turtle canvas"""
    print_action(direction, distance)
    action, angle = direction
    if action == 'right':
        right(angle)
        forward(distance / scale)
    elif action == 'left':
        left(angle)
        forward(distance / scale)

    elif action in Navigation.compass: # ne nw se sw directions
        seth(Navigation.compass[action])
        forward(distance / scale)

    else: # there was no turn so keep going straight
        forward(distance / scale)


def main():
    file = "Easterwood2Coulter.txt"

    directions = read_directions_file(file)
    distances = get_distances(directions) # list of distances in miles
    scale = max(distances) / 500 # scale for the turtle. based off max distance in file
    
    speed(1)

    for i in range(len(directions)):
        line = directions[i]
        make_move(get_direction(line), distances[i], scale)
    done()

if __name__ == '__main__':
    main()
