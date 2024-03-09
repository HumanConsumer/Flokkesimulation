import pygame
from pygame.locals import *
import random as r
from youJustGotVectored import Vector as MyVector #importerer vektorer
from fish import Clownfish, Shark, food #importerer fisken, hajen og maden
import random



clock = pygame.time.Clock() #sætter clock speed
# Bredde og højde på vinduet
windowsize=600
width = 1200
height = windowsize
 
# Initialisering af Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flokkesimulation')
 
# Font til tekst i vinduet
font = pygame.font.SysFont("Arial", 36)

def setup():
    pass
    global cfish1, shark1, foodman #listen over fisk og hajen gøres global
    cfish1=[] #først skabes en tom liste liste 
    foodman=[] #dette er listen der skal indeholde mad
    for i in range(50): #der køres nu en for løkke der køres 50 gange
        cfish1.append(Clownfish(location=MyVector([random.randint(100,300),random.randint(100,300)]),velocity=MyVector([1, 1]),color=(255,0,0))) #hver gang forløkken køres, bliver der tilføjet en klovnefisk med en tilfældig position og hastighed til listen
    shark1=Shark(location=MyVector([500,500]),velocity=MyVector([1.5,1.5]),color=(200,200,200),target = cfish1[0]) #derefter bliver der skabt en haj
    for i in range(5): #der køres nu en liste 5 gange som skaber 5 styker mad i en liste.
        foodman.append(food(location=[random.randint(0,1200),random.randint(0,600)], color=(0,200,0))) #maden bliver skabt med en tilfældig lokation
        
    
    
def draw():
    clock.tick(30) #clock tick sættes til 30

    screen.fill((0, 0, 255)) #sætter baggrunden til blå

    #NB! bruger her dependency injection for at undgå circular import dependencies in other files.
    for i in range(len(cfish1)): #denne for løkke itererer mellem alle klovnefisk i listen
        cfish1[i].swim(shark1,foodman) #for hver fisk i listen cfish1 bliver der kaldt deres swim og show metode
        cfish1[i].show(screen)
        cfish1[i].eat(foodman)
    shark1.consume(cfish1) #hajen kører dens consume, swim og show metode
    shark1.swim()
    shark1.show(screen)

    for i in range(len(foodman)): #der itereres nu over alt maden for at tegne dem
        foodman[i].show(screen)

    if(len(foodman)<5): #hvis der er mindre end 5 stykker mad i madlisten, bliver der skabt en ny
        foodman.append(food(location=[random.randint(0,1200),random.randint(0,600)], color=(0,200,0))) #dette stykke mad har en tilfældig lokation når den er skabt
        
    
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