import pygame #Module, It includes computer graphics and sound libraries designed to be used with the Python programming language.
import random #This module implements pseudo-random number generators for various distributions.
import math
pygame.init() #initialize all imported pygame modules.

class DrawInformation: #defining global variables
	BLACK = 0, 0, 0   # R, G, B  Red Green Blue degrees
	WHITE = 255, 255, 255
	RED = 255, 0, 0
	GREEN = 40, 200, 0

	BACKGROUND_COLOR = WHITE

	GRADIENTS = [      # GRADIENTS of the bar graph, here we have 3
		(152, 175, 199), #Again in RGB format
		(72,99, 160),
		(18, 52, 86)
	]

	FONT = pygame.font.SysFont('comicsans', 20) #which font to use
	LARGE_FONT = pygame.font.SysFont('comicsans', 25)

	SIDE_PAD = 100 #  It's abput pixels , more the pixels the smaller the graphs will look & fit
	TOP_PAD = 150 # Deals with height of the graph

	def __init__(self, width, height, lst): #lst will be the list of numbers with width & height
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))  #window the output will be displayed on
		pygame.display.set_caption("Sorting Algorithm Visualizer") #Title of the window
		self.set_list(lst)

	def set_list(self, lst): #Creating the visualization
		self.lst = lst
		self.min_val = min(lst) #lowest bar graph
		self.max_val = max(lst) # highest bar hraph

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst)) #Area of the screen - Area left over
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val)) #how high a bar should be , relational
		self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)  # FILL the screen with this colour

	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5)) #To fix the title in the screen

	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S- Selection Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

	draw_list(draw_info)
	pygame.display.update()

#FUNCTION to draw the graphs

def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

#Drawing each bar
	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3] #Gives different colour for all 3 bars everytime

		if i in color_positions:
			color = color_positions[i]

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:
		pygame.display.update()

# Generating a list which will be shown once we run the program
def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst


def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True

	return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        min_idx = i
        for j in range(i+1, len(lst)):
            if (lst[j] < lst[min_idx] and ascending) or (lst[j] > lst[min_idx] and not ascending):
                min_idx = j
        if (min_idx != i):
            lst[i], lst[min_idx] = lst[min_idx], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN,
                                  min_idx: draw_info.RED}, True)
            yield True
    return lst


def main():
	run = True
	clock = pygame.time.Clock()

	n = 50 # Number of ELements
	min_val = 0 # min value
	max_val = 100 # max value

	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(800, 600, lst) # WIDTH & HEIGHT of the graph
	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None

	while run:
		clock.tick(5)  # SPEED with which the sorting is running

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue


 # What problem will be executed on pressing that particular key
			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"
			elif event.key == pygame.K_s and not sorting:
				sorting_algorithm = selection_sort
				sorting_algo_name = "Selection Sort"

	pygame.quit()


if __name__ == "__main__":
	main()