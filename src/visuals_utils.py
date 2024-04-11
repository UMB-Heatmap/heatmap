# Color Map Options (directly from MatPlotLib)
# https://matplotlib.org/stable/gallery/color/colormap_reference.html
COLOR_MAPS = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'binary', 
            'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']

# validates int from standard input
# TODO: add error handling to prevent negative values
def getIntFromInput(message):
    while True: 
        try:
            x = int(input(message))
            return x
        except ValueError:
            print("Invalid Input -- Must be Integer")

# validates color map string from standard input
def getColorMap():
    cmap = input("Color Map: ")
    while (cmap not in COLOR_MAPS):
        print("\nInvalid Color Map -- Select From:")
        print("-----------------------------------")
        for cmap in COLOR_MAPS:
            print(cmap)
        print()
        cmap = input("Color Map: ")
    return cmap

# validates yes/no (boolean) input from standard input
def getBoolFromInput(message):
    while True:
        answer = input(message).lower()
        if (answer == 'y' or answer == 'yes'):
            return True
        elif (answer == 'n' or answer == 'no'):
            return False
        else:
            print("Invalid Input -- Must be Yes/No or Y/N")