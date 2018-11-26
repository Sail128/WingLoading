import matplotlib.pyplot as plt
from matplotlib2tikz import save as tikz_save
from math import sin, cos, radians, pi
from numpy import arange

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
    Tcs:list,       #[(t/c,x1), (t/c,x2)]
    #c_l_alpha = 2*pi,    #change in cl per radian for now only a global average is assumed. If not given the standard solution for thin airfoils is used
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
        self.Tcs = Tcs
        #self.c_l_alpha = c_l_alpha
        self.tank = tank
        self.segmentcount = 20
        self.fuelLevel = 0.0
        self.__segments = None
        self.generateSegments()
        self.diagrams = {}
        
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

    def getThickness(self, x, cr):
        tc = None
        for i in range(len(self.Tcs)):
            if x<self.Tcs[i][1]:
                if i>0:
                    tc = (self.Tcs[i][0] - self.Tcs[i-1][0])/(self.Tcs[i][1] - self.Tcs[i-1][1])*x + self.Tcs[i-1][0]
                else: tc = self.Tcs[i-1][0]
                break
        if tc == None: tc = self.Tcs[-1][0]
        return tc*cr

    def getMass(self, segment): #THIS IS NOT INDEPENDENT OF SEGMENTCOUNT. ONLY WORKS FOR 20 SEGMENTS
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
            cr = (self.getChord(x1)+self.getChord(x2))/2
            h = self.getThickness((x1+x2)/2, cr)
            self.__segments.append((S, cl, cm, m, x1, x2, cr, h))
    
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

        #plt.plot(Xs, Ts)
        #plt.ylim(ymin=0)
        #plt.xlim(xmin=0)
        #plt.show()
        return {"Xs":Xs, "Ts":Ts}

    def genDiagrams(self, V, rho, filename=None):
    #generate moment diagram
        moments =self.genMomentDiagram(V,rho)
        ax1 = plt.subplot(311
        #title="Momentdiagram"
        )
        plt.plot(moments["Xs"], moments["Ms"])
        plt.xlim(xmin=0.0)
        plt.ylim(ymin=0.0)
        plt.ylabel("Moment [N*m]")
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.setp(ax1.get_xticklabels(), visible=False)
        
    #generate shear diagram
        shears = self.genShearDiagram(V, rho)

        ax2 = plt.subplot(312, 
        #title="sheardiagram",
        sharex=ax1
        )
        plt.plot(shears["Xs"], shears["Vs"])
        plt.xlim(xmin=0.0)
        plt.ylim(ymin=0.0)
        plt.ylabel("Shear [N]")
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.setp(ax2.get_xticklabels(), visible=False)

    #generate torque diagram
        torques = self.genTorqueDiagram(V, rho)
        ax3 = plt.subplot(313, 
        #title="torquediagram",
        sharex=ax1
        )
        plt.plot(torques["Xs"], torques["Ts"])
        plt.xlim(xmin=0.0)
        plt.ylim(ymin=0.0)
        plt.ylabel("Torque [N*m]")
        plt.xlabel("x position along the wing [m]")
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

        
        if filename!=None:
            tikz_save(filename)
            print("Plots saved to file")
        else:
            plt.show()

        diagrams =  {
        "Moment":moments,
        "Shear":shears,
        "Torque":torques
        }
        self.diagrams = diagrams
        return diagrams

    def tipDeflection(self, t): #determines the tip defelction given a spar thickness. Uses the last call to gen diagrams
        Lseg = (self.b/2)/self.segmentcount
        E = 73*(10**9)
        moments = self.diagrams["Moment"]["Ms"]
        deltas = []
        for i in range(len(self.__segments)):
            seg = self.__segments[i]
            EI = E*2*((1/12)*t*seg[7]**3)
            EI2 = E*2*((1/12)*t*self.__segments[i-1][7]**3) if i>0 else EI
            delta = (moments[i+1]*Lseg**2)/(2*EI) 
            delta += Lseg*(moments[i]*Lseg)/(EI2)if i>0 else 0.0
            deltas.append(delta)
        return sum(deltas)

    def getRequiredThicknessDefl(self,delta):
        t = 0.00001
        d = 0.0
        while t < 0.2:
            d = self.tipDeflection(t)
            if d<delta:
                break
            t+=0.00001
        if t >= 0.2: 
            print("No answer reached until a required thickness of 0.2m")
            return None
        else:
            return (t,d)

    def tipTwist(self, V, rho):
        pass