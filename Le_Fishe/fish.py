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
                
    def swim(self,shark,foody):
        sharkdistande=(((self.loc[0]-shark.loc[0])**2 + (self.loc[1]-shark.loc[1])**2)**0.5)-shark.size-self.size # finder afstanden til hajen
        shortest=2000 #en startagstand der bruges til maden
        fooder=None #denne variabel er den tætteste mad
        for food in foody: #food er mad objecter og foody er arrayet der indeholder maden
            fooddistance=(((self.loc[0]-food.loc[0])**2 + (self.loc[1]-food.loc[1])**2)**0.5) #denne finder afstanden til det specifikke mad
            if(fooddistance< shortest): #Hvis dette stykke mad er tættere på end de andre der kigges på før, bliver dette statement true
                shortest=fooddistance #dette mad bliver nu sat til at være det tætteste mad
                fooder=food #den tætteste mad bliver nu sat ind i variablen fooder
        
        if sharkdistande< shortest*1.5: #denne ser om maden eller hajen er tættest på fisken. da hajen er hurtigere, skal maden være mindst 50% tættere end hajen før den targeter. Hvis hajen er tættere på end maden, flygter fisken
            direction=Vector([self.loc[i]-shark.loc[i] for i in range(len(self.loc))]) #Finder retningen mellem hajen og fisken med en comprehension over alle koordinaterne og laver et array af koordinaterne, denne vektor peger fra hajen mod fisken
            normalizedDirection=direction.normalize().get_coordinates() #Finder normalvektoren af retningen fra hajen til fisken
        
        else: #hvis hajen er langt væk, går fisken efter det nærmeste mad fooder
            direction=Vector([fooder.loc[i]-self.loc[i] for i in range(len(self.loc))]) #Finder retningen mellem maden og fisken med en comprehension over alle koordinaterne og laver et array af koordinaterne, denne vektor peger fra hajen mod fisken
            normalizedDirection=direction.normalize().get_coordinates() #Finder normalvektoren af retningen fra fisken til maden
  
        iteration=2 #da højden er halvdelen af bredden, laves denne variabel. den første iteration er bredden 1200 for x koordinatet, og i anden iteration er højden 600 for y koordinaten. med denne variabel kan man bruge den samme kode, hvor tallene er halvt så store i anden iteration
        for i in range(len(self.loc)):
            self.loc[i] += normalizedDirection[i]*self.vel[i] #Her bevæger klovnefisken sig enten væk fra hajen elelr mod maden, hvis maden er tættere end hajen
            if self.loc[i] > 600*iteration: #hvis fisken rammer kanten så teleporterer den ind i midten, dette er lavet så fisken ikke sidder fast i kanten
                self.loc[i]=100*iteration
            elif self.loc[i] < 0:
                self.loc[i]=500*iteration
            iteration-=1
                
    def eat(self, food_list):
        to_remove=[] #Da der er en chance for at fisken spiser flere forskellige stykker mad i en frame, laves denne liste der skal indeholde alt det mad som fisken rammer
        for food in food_list: #der itereres gennem alle mad i listen af mad
            distance = ((self.loc[0] - food.x) ** 2 + (self.loc[1] - food.y) ** 2) ** 0.5 #Først findes afstanden mellem klovnefisken og maden
            if distance < (self.size + food.size): #Hvis maden rammer en klovnefisk, bliver klovnefisken større og maden bliver slettet fra listen
                self.size = self.size*2 #klovnefisken bliver dobbelt så stor for hver mad den rammer
                to_remove.append(food) #den mad som fisken rammer kommer ind i to remove listen
                self.vel[0]*0.9 #da den bliver større, bliver den 10% langsommere
                self.vel[1]*0.9
        
        for food in to_remove: #her kører en for løkke over to remove listen og fjerner alt det mad fisken har rørt
            food_list.remove(food)
                        
class Shark(fishMoment):
    def __init__(self, location, velocity, color,target):
        self.target = target #target er en specifik klovenfisk som hajen skal vømme efter
        super().__init__(location, velocity, color) #den tager atributtenre fra superclassen
 
    def swim(self):
        direction=Vector([self.target.loc[i]-self.loc[i] for i in range(len(self.loc))]) #her er self.target en specifik klovnefisk. der findes nu retningen fra hajen til den specifikke klovnefisk. dette gøres ved at finde afstanden mellem deres x og y koordinater i en comprehension
        normalizedDirection=direction.normalize().get_coordinates() #Der findes normalvektoren for retningen, og der tages derefter dens koordinater som bliver til variablne nomalizeddirection
        for i in range(len(self.loc)):
            self.loc[i] += self.vel[i]*normalizedDirection[i] #her bevæger hajen sig mod fisken med normalvektoren som retning
            if self.loc[i] > 1200: #hvis hajen rammer den ene side af skærmen teleporterer den over i den anden side
                self.loc[i]=0 #da hajens eneste formål er at følge efter fisken, bevæger den sig aldrig ud af skærmen da fiskene heller ikke kan gøre dette. Denne kode er der som en nødsituation hvis den alligevel ender med at bevæge sid ud af skærmen. 
            elif self.loc[i] < 0:
                self.loc[i]=1200

         
    def consume(self, clownfish_list):
        newtarget=2000 #dette er en startværdi som bruges til at finde fiskens afstand til hajen, denne værdi kommer kun til at falde gennem funktionen
        target2=0 #Dette er den specifikke klovnefisk som hajen skal jage
        for clownfish in clownfish_list: #der itereres gennem alle klovnefisk i listen af klovnefisk
            distance = ((self.loc[0] - clownfish.loc[0]) ** 2 + (self.loc[1] - clownfish.loc[1]) ** 2) ** 0.5 #Først findes afstanden mellem klovnefisken og hajen
            if distance < (self.size + clownfish.size): #Hvis hajen rammer en klovnefisk, bliver hajen større og klovnefisken bliver slettet fra listen
                self.size += 1 #hajen bliver 1 større når den rammer klovnefisken
                clownfish_list.remove(clownfish) #klovnefisken bliver fjernet fra listen
                target2=clownfish_list[0] #der bliver med det samme sat et nyt target, så denne variabel ikke bliver invalid
            elif distance < newtarget: #Hvis ikke der rammes en fisk, finder hajen en klovnefisk at gå efter. Hvis afstanden er mindre end newtarget, er der fundet en klovnefisk der er tættere på og if statementet aktiveres
                newtarget = distance #nu bliver newtarget sat til distance så der nu er en ny afstand som skal overgås
                target2=clownfish #target2 bliver sat til at være den specifikke klovnefisk som er tættest på lige nu
        self.target = target2 #Når for løkken er færdig, bliver self.target sat til at være den specifikke klovnefisk
        return len(clownfish_list) < 1 #denne kode sender enten en true eller false for at se om alle fiskene er spist
    
    
class food(): #dette objekt er maden der skal spises, den har kun en show metode da resten af dens funktioner ligger ovre i klovnefisken
    def __init__(self, location, color):
        self.loc=location
        self.x=location[0]
        self.y=location[1]
        self.color=color
        self.size=8
    
    def show(self, surface):
        pygame.draw.circle(surface, self.color, self.loc, self.size)