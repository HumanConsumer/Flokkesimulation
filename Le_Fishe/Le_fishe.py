import pygame
from pygame.locals import *
import random as r
from youJustGotVectored import Vector as MyVector #importerer vektorer
from fish import Clownfish, Shark #importerer fisken og hajen
import random



clock = pygame.time.Clock() #sætter clock speed
# Bredde og højde på vinduet
windowsize=600
width = windowsize
height = windowsize
 
# Initialisering af Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flokkesimulation')
 
# Font til tekst i vinduet
font = pygame.font.SysFont("Arial", 36)

def setup():
    pass
    global cfish1, shark1 #listen over fisk og hajen gøres global
    cfish1=[] #først skabes en tom liste liste 
    for i in range(50): #der køres nu en for løkke der køres 50 gange
        cfish1.append(Clownfish(location=MyVector([random.randint(100,300),random.randint(100,300)]),velocity=MyVector([random.randint(-2,2),random.randint(-2,2)]),color=(255,0,0))) #hver gang forløkken køres, bliver der tilføjet en klovnefisk med en tilfældig position og hastighed til listen
    shark1=Shark(location=MyVector([500,500]),velocity=MyVector([1,1]),color=(200,200,200),target = cfish1[0]) #derefter bliver der skabt en haj
 
def draw():
    clock.tick(30) #clock tick sættes til 30

    screen.fill((0, 0, 255)) #sætter baggrunden til blå

    #NB! bruger her dependency injection for at undgå circular import dependencies in other files.
    for i in range(len(cfish1)):
        cfish1[i].swim(shark1) #for hver fisk i listen cfish1 bliver der kaldt deres swim og show metode
        cfish1[i].show(screen)
    shark1.consume(cfish1) #hajen kører dens consume, swim og show metode
    shark1.swim()
    shark1.show(screen)

    
    # Vis vindhastighed og retning i vinduet
    text = f"Something"
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (10, 50))
 
    pygame.display.update()
 
setup() #setup kaldes
 
running = True
while running: #et infinite loop som er draw funktionen, men den lukker programmet hvis man lukker den
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    draw()


 
if __name__ == "__main__":
    pass
pygame.quit()