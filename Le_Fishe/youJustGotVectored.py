

class Vector:
    def __init__(self, coordinates, startx=0, starty=0):
        self.coordinates = coordinates
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.sx = startx
        self.sy = starty
        if len(coordinates) > 2:
            self.z = coordinates[2]
        self.lengthe()  


    def draw(self): #skal implementeres med pygame
        if self.length == 0:
            return
        ax.quiver(self.sx, self.sy, self.x, self.y)

    def lengthe(self):
        self.length = 0
        for i in range(len(self.coordinates)):
            self.length += self.coordinates[i] ** 2 #finder a^2+b^2
        self.length = (self.length) ** 0.5 #tager kvrod af tallet og finde længeden
        
    def get_coordinates(self):
        return self.coordinates    
    
    def Prik(self,other):
        self.psum=0
        for i in range(len(self.coordinates)):#for løkke der finder prikprodukt
            self.psum += self.coordinates[i] * other.coordinates[i] 
        return self.psum
    
    def Vinkelret(self, other):
        if self.Prik(other) == 0:#hvis prikproduktet er 0 er de vinkeltrette
            return True
        else:
            return False
    
    def same(self, other):
        #Hvis begge koordinater er ens, så er vektorerne ens
        if self.coordinates[0] == other.coordinates[0] and self.coordinates[1] == other.coordinates[1]:
            return True
        else:
            return False
    
    def Enhedsvector(self):
        enhedsvektor=[]
        for i in range(len(self.coordinates)):
            enhedsvektor.append(self.coordinates[i]/self.length()) #der udregnes koordinaterne for enhedsvektorerne i en forløkke hver for sig
        normalizedvector=Vector(enhedsvektor) #der skabes en normalizedvector ud af et vectorobjekt der har enhedsvektorens koordinater
        return normalizedvector
    
    def normalize(self):
        coordinates_list = list(self.coordinates) #
        length = self.length 
        normalized_vector = [coord / length for coord in coordinates_list] #her findes koordinaterne hver for sig i en forløkke og bliver derfor tilføjet til et array af koordinater, dette er en comprehension
        return Vector(normalized_vector) #den returner et vectorobjekt med normalize_vectoren som koordinaterne



