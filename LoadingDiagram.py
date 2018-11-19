import matplotlib.pyplot as plt
from matplotlib2tikz import save as tikz_save
from math import sin, cos, radians, pi

class LoadingDiagram:
    def __init__(self,
    span,           #wingspan
    rootChord,      #chord length of the root
    taperRatio,
    sweep,          #sweep of the wing [deg]
    alpha,  	    #angle of attack [deg]
    loadFactor,     #load factor for this specific case
    Cls:list,       #[(cl1, cla1 ,x1),(cl2, cla2, x2)] x1< x <x2 gives cl1< cl <cl2 in a linear relation. x>x2 or x<x1 , cl=cl2 and cl=cl1 respectively. all at alpha = 0
    Cm25s:list,     #[(cm1, cma1 ,x1),(cm2, cma2, x2)] x1< x <x2 gives cm1< cm <cm2 in a linear relation. x>x2 or x<x1 , cm=cm2 and cm=cm1 respectively. all at alpha = 0
    c_l_alpha = 2*pi,    #change in cl per radian for now only a global average is assumed. If not given the standard solution for thin airfoils is used
    tank:tuple = None    # not yet implemented at all. 
    ):
        self.b = span
        self.cr = rootChord
        self.TR = taperRatio
        self.sweep = radians(sweep)
        self.a = radians(alpha)
        self.loadFactor = loadFactor
        self.cls = Cls
        self.cms = Cm25s
        self.c_l_alpha = c_l_alpha
        self.tank = tank
        self.segmentcount = 20
        self.fuelLevel = 0.0
        self.__segments = None
        self.generateSegments()
        
    def getCl(self, x1, x2):
        #c_l_alpha = 5.723848
        cl1 = None
        cl2 = None
        if x2 > 1.0: x2 = 1.0
        for i in range(len(self.cls)):
            if x1<self.cls[i][2]:
                if i > 0:
                    cl1 = ((
                        #c_l_alpha_2   *alpha_2+ cl0_2         -(c_l_alpha_1     *alpha_1+ cl0_1)
                        (self.cls[i][1]*self.a + self.cls[i][0]-(self.cls[i-1][1]*self.a + self.cls[i-1][0]))
                        /
                        #   x2         -    x1                  + (c_l_alpha_1    *alpha_1+ cl0_1)
                        (self.cls[i][2]-self.cls[i-1][2])) * x1 + self.cls[i-1][1]*self.a + self.cls[i-1][0])
                else:
                    cl1 = self.cls[i][1]*self.a + self.cls[i][0]
                break
        if cl1 == None: cl1 = self.cls[-1][1]*self.a + self.cls[-1][0]
        for i in range(len(self.cls)):
            if x2<self.cls[i][2]:
                if i > 0:
                    cl2 = ((
                        #c_l_alpha_2   *alpha_2+ cl0_2         -(c_l_alpha_1     *alpha_1+ cl0_1)
                        (self.cls[i][1]*self.a + self.cls[i][0]-(self.cls[i-1][1]*self.a + self.cls[i-1][0]))
                        /
                        #   x2         -    x1                  + (c_l_alpha_1    *alpha_1+ cl0_1)
                        (self.cls[i][2]-self.cls[i-1][2])) * x2 + self.cls[i-1][1]*self.a + self.cls[i-1][0])
                else:
                    cl2 = self.cls[i][1]*self.a + self.cls[i][0]
                break 
        if cl2 == None: cl2 = self.cls[-1][1]*self.a + self.cls[-1][0]

        return (cl1+cl2)/2

    def getChord(self, x):
        return self.cr - self.cr*x*(1-self.TR)
    def getMass(self, segment):
        #Mwing = -13.99*(segment+1) + 401.86 
        Mfuel = 0.0 if segment > 13 else 1.8306*(segment+1)**2 - 104.7*(segment+1) + 1497.3
        return Mfuel*self.fuelLevel

    def getCm(self, x1,x2):
        cm1 = None
        cm2 = None
        if x1 < 0.0: x1 = 0.0
        if x2 > 1.0: x2 = 1.0
        for i in range(len(self.cms)):
            if x1<self.cms[i][2]:
                if i > 0:
                    cm1 = ((
                        #c_m_alpha_2   *alpha_2+ cm0_2         -(c_m_alpha_1     *alpha_1+ cm0_1)
                        (self.cms[i][1]*self.a + self.cms[i][0]-(self.cms[i-1][1]*self.a + self.cms[i-1][0]))
                        /
                        #   x2         -    x1                  + (c_l_alpha_1    *alpha_1+ cl0_1)
                        (self.cms[i][2]-self.cms[i-1][2])) * x1 + self.cms[i-1][1]*self.a + self.cms[i-1][0])
                else:
                    cm1 = self.cms[i][1]*self.a + self.cms[i][0]
                break
        if cm1 == None: cm1 = self.cms[-1][1]*self.a + self.cms[-1][0]
        for i in range(len(self.cms)):
            if x2<self.cms[i][2]:
                if i > 0:
                    cm2 = ((
                        #c_l_alpha_2   *alpha_2+ cl0_2         -(c_l_alpha_1     *alpha_1+ cl0_1)
                        (self.cms[i][1]*self.a + self.cms[i][0]-(self.cms[i-1][1]*self.a + self.cms[i-1][0]))
                        /
                        #   x2         -    x1                  + (c_l_alpha_1    *alpha_1+ cl0_1)
                        (self.cms[i][2]-self.cms[i-1][2])) * x2 + self.cms[i-1][1]*self.a + self.cms[i-1][0])
                else:
                    cm2 = self.cms[i][1]*self.a + self.cms[i][0]
                break 
        if cm2 == None: cm2 = self.cms[-1][1]*self.a + self.cms[-1][0]

        return (cm1+cm2)/2

    def generateSegments(self):
        self.__segments = [] #half of the wing
        segmentwidth = self.b/2/self.segmentcount
        for i in range(self.segmentcount):
            x1 = i/self.segmentcount
            x2 = (i+1)/self.segmentcount
            S  =  (self.getChord(x1)+self.getChord(x2))*segmentwidth/2
            cl = self.getCl(x1,x2)
            cm = self.getCm(x1,x2)
            m = self.getMass(i)
            self.__segments.append((S, cl, cm, m, x1, x2))
    
    def getSegments(self):
        return self.__segments
        
    def genLiftDist(self, V, rho):
        V = V*cos(self.sweep)
        Xs = []
        Ls = []
        segmentwidth = self.b/2/self.segmentcount
        for segment in self.__segments:
            Li = 0.5*V*V*rho*segment[0]*segment[1] * self.loadFactor *cos(self.a)
            Xs.append((segment[3]+segment[4])/2*(self.b/2))
            Ls.append(Li/segmentwidth)
        print("total lift:", sum(Ls))
        plt.plot(Xs,Ls)
        plt.show()

    def genMomentDiagram(self, V, rho):
        V = V*cos(self.sweep)
        Xs = []
        Ms = []
        for i in range(len(self.__segments)):
            segment = self.__segments[i]
            moment = 0.0
            x1 = segment[4]*(self.b/2)
            for j in range(i,len(self.__segments)):
                segi = self.__segments[j]
                Fi = 0.5*V*V*rho*segi[0]*segi[1] * self.loadFactor*cos(self.a) - segi[3]
                x2 = (segi[4]+segi[5])/2*(self.b/2)
                moment += Fi*(x2-x1)

            Ms.append(moment)
            Xs.append(x1)

        Xs.append(self.b/2)
        Ms.append(0)

        
        plt.plot(Xs, Ms)
        plt.ylim(ymin=0)
        plt.xlim(xmin=0)
        plt.show()
        return {"Xs":Xs, "Ms":Ms}

    def genShearDiagram(self, V, rho):
        V = V*cos(self.sweep)
        Xs = []
        Vs = []
        for i in range(len(self.__segments)):
            segment = self.__segments[i]
            shear = 0.0
            x1 = segment[4]*(self.b/2)
            for j in range(i,len(self.__segments)):
                segi = self.__segments[j]
                Fi = 0.5*V*V*rho*segi[0]*segi[1] * self.loadFactor*cos(self.a) - segi[3]
                shear += Fi
            Vs.append(shear)
            Xs.append(x1)

        Xs.append(self.b/2)
        Vs.append(0)

        plt.plot(Xs, Vs)
        plt.ylim(ymin=0)
        plt.xlim(xmin=0)
        plt.show()
        return {"Xs":Xs, "Vs":Vs}

    def genTorqueDiagram(self, V, rho):
        V = V*cos(self.sweep)
        Xs = []
        Ts = []
        for i in range(len(self.__segments)):
            segment = self.__segments[i]
            torque = 0.0
            x1 = segment[4]*(self.b/2)
            for j in range(i,len(self.__segments)):
                segi = self.__segments[j]
                d_shear = self.getChord(segi[4])/4
                ct = segi[2] + segi[1]*d_shear
                Fi = 0.5*V*V*rho*segi[0]*ct*self.loadFactor*cos(self.a)
                torque += Fi
            Ts.append(torque)
            Xs.append(x1)

        plt.plot(Xs, Ts)
        plt.ylim(ymin=0)
        plt.xlim(xmin=0)
        plt.show()
        return {"Xs":Xs, "Ts":Ts}

    def genDiagrams(self, V, rho):
        return {
        "Moment":self.genMomentDiagram(V,rho),
        "Shear":self.genShearDiagram(V, rho),
        "Torque":self.genTorqueDiagram(V, rho)
        }