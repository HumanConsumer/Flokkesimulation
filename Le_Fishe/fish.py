import pygame
from youJustGotVectored import Vector #importerer vektorer

class fishMoment:
    def __init__(self, location, velocity, color):
        self.loc = location.get_coordinates()
        self.x=self.loc[0] 
        self.y=self.loc[1]
        self.vel = velocity.get_coordinates()
        self.color=color
        self.size=6  
        
    def show(self, surface):
        pygame.draw.circle(surface, self.color, self.loc, self.size)     

class Clownfish(fishMoment):
    def __init__(self, location, velocity, color):
        super().__init__(location, velocity, color) #tager atributterne fra superclassen
                
    def swim(self,shark):
        direction=Vector([self.loc[i]-shark.loc[i] for i in range(len(self.loc))]) #Finder afstanden mellem hajen og fisken med en comprehension over alle koordinaterne og laver et array af koordinaterne, denne vektor peger fra hajen mod fisken
        normalizedDirection=direction.normalize().get_coordinates() #Finder normalvektoren af retningen fra hajen til fisken
        for i in range(len(self.loc)):
            self.loc[i] += normalizedDirection[i] #Her bevæger klovnefisken sig væk fra hajen, da vektoren peger fra hajen til fisken, svømmer den direkte væk fra hajen
            if self.loc[i] > 600: #hvis fisken rammer kanten så teleporterer den ind i midten, dette er lavet så fisken ikke sidder fast i kanten
                self.loc[i]=200
            elif self.loc[i] < 0:
                self.loc[i]=400
                        
class Shark(fishMoment):
    def __init__(self, location, velocity, color,target):
        self.target = target #target er en specifik klovenfisk som hajen skal vømme efter
        super().__init__(location, velocity, color) #den tager atributtenre fra superclassen
 
    def swim(self):
        direction=Vector([self.target.loc[i]-self.loc[i] for i in range(len(self.loc))]) #her er self.target en specifik klovnefisk. der findes nu retningen fra hajen til den specifikke klovnefisk. dette gøres ved at finde afstanden mellem deres x og y koordinater i en comprehension
        normalizedDirection=direction.normalize().get_coordinates() #Der findes normalvektoren for retningen, og der tages derefter dens koordinater som bliver til variablne nomalizeddirection
        for i in range(len(self.loc)):
            self.loc[i] += self.vel[i]*normalizedDirection[i] #her bevæger hajen sig mod fisken med normalvektoren som retning
            if self.loc[i] > 600: #hvis hajen rammer den ene side af skærmen teleporterer den over i den anden side
                self.loc[i]=0
            elif self.loc[i] < 0:
                self.loc[i]=600

         
    def consume(self, clownfish_list):
        newtarget=1000 #dette er en startværdi som bruges til at finde fiskens afstand til hajen, denne værdi kommer kun til at falde gennem funktionen
        target2=0 #Dette er den specifikke klovnefisk som hajen skal jage
        for clownfish in clownfish_list: #der itereres gennem alle klovnefisk i listen af klovnefisk
            distance = ((self.loc[0] - clownfish.loc[0]) ** 2 + (self.loc[1] - clownfish.loc[1]) ** 2) ** 0.5 #Først findes afstanden mellem klovnefisken og hajen
            if distance < (self.size + clownfish.size): #Hvis hajen rammer en klovnefisk, bliver hajen større og klovnefisken bliver slettet fra listen
                self.size += 1
                clownfish_list.remove(clownfish)
            elif distance < newtarget: #Hvis ikke der rammes en fisk, finder hajen en klovnefisk at gå efter. Hvis afstanden er mindre end newtarget, er der fundet en klovnefisk der er tættere på og if statementet aktiveres
                newtarget = distance #nu bliver newtarget sat til distance så der nu er en ny afstand som skal overgås
                target2=clownfish #target2 bliver sat til at være den specifikke klovnefisk som er tættest på lige nu
        self.target = target2 #Når for løkken er færdig, bliver self.target sat til at være den specifikke klovnefisk
        return len(clownfish_list) < 1