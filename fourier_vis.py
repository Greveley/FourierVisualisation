import pygame
import numpy as np

pygame.init()

# Pygame Variables
width = 1200
height = 600
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
yellow = (255,255,0)
disp = pygame.display.set_mode((width,height))
pygame.display.set_caption("Fourier Transform Visualisation")
pygame.display.update()
disp.fill(white)
font_style = pygame.font.SysFont('applegothic', 20)

# Visualisation Variables
cx = 300
cy = height/2
angle = 0
delta_a = 0.005
x_wave = [cx+400]
y_wave = []
y_square_wave = []
y_opt = []
const = cx/2
pt_x = 0
pt_y = 0
prev_x = 0
prev_y = 0

def draw_circle(x,y,radius):
    # circle_surface = pygame.Surface((radius, radius), pygame.SRCALPHA)
    # pygame.draw.circle(circle_surface, (255,255,255,20), (int(x), int(y)), radius)
    # disp.blit(circle_surface, (int(x), int(y)))
    pygame.draw.circle(disp,white,(int(x),int(y)),radius,1)

def draw_point(x,y):
    pygame.draw.circle(disp,red,(int(x),int(y)),5)

def draw_wave(x,y,colour):
    pygame.draw.circle(disp,colour,(int(x),int(y)),2)

def draw_line(x1,y1,x2,y2):
    pygame.draw.line(disp, yellow, (int(x1), int(y1)),(int(x2), int(y2)), 4)

    # Setting up for message display
def message(msg,x,y):
    mesg = font_style.render(msg, True, white)
    disp.blit(mesg, [x,y])

close = False

# Initiate Game Loop
while not close:
    disp.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = True

    # Getting mouse position from Pygame
    (mouse_x,mouse_y) = pygame.mouse.get_pos()
    # Varying the number of circles with mouse position
    num_circles = int(round((float(mouse_x)/float(800))*20)+1)
    # Plotting number of circles to screen
    message("Number of coefficients in fourier series = " +str(num_circles),width/2,height*0.05)
    pt_x = 0
    pt_y = 0
    # Loop to calculate the points and draw circles.
    for i in range(0,num_circles):
        n = (i*2)+1
        prev_x = pt_x
        prev_y = pt_y
        # Circle Points
        rad = const * (4 / (n * np.pi))
        # Drawing Paths
        draw_circle(cx+pt_x,cy+pt_y, int(rad))
        pt_x += rad * np.cos(n * angle)
        pt_y += rad * np.sin(n * angle)
        draw_line(cx+prev_x,cy+prev_y,cx+pt_x,cy+pt_y)
        #Drawing points on paths
        draw_point(pt_x+cx,pt_y+cy)

    angle += delta_a

    # Plotting the wave
    y_wave.insert(0, pt_y+cy)
    x_wave.append(x_wave[-1] + 2)

    # Plotting the square wave
    if y_wave[0] > cy:
        y_opt.insert(0,cy+const)
    elif y_wave[0] < cy:
        y_opt.insert(0,cy-const)
    elif y_wave[0] ==cy:
        y_opt.insert(0,cy)

    #Preventing wave array from getting too large if you run the program for a long time
    if len(y_wave) > 300:
        y_wave.pop()
        y_opt.pop()

    # Drawing waves (calc and opt)
    for i in np.arange(0,len(y_wave)):
        draw_wave(x_wave[i],y_wave[i],white)
        draw_wave(x_wave[i],y_opt[i],yellow)
    
    # Drawing line from wave to point
    draw_line(pt_x+cx,pt_y+cy,x_wave[0],y_wave[0])

    num_elements = 100
    # Calculating root mean squared error between the two
    temp = []
    temp.append(np.sqrt((np.sum(pow(np.array(y_wave[0:num_elements])-np.array(y_opt[0:num_elements]),2)))/len(y_wave)))
    rmse = np.mean(temp)
    #Preventing wave array from getting too large if you run the program for a long time
    if len(temp) > 20:
        temp.pop()
    # Displaying RMSE to screen
    message("RMSE of first 100 elements = %.2f" %rmse,width/2,height*0.1)

    pygame.display.update()



