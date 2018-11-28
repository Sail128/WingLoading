from LoadingDiagram import LoadingDiagram as LD

def saveToFile(filename , diagram, lift=None, stiffnesses = False):
    outfile = open(filename, "w")
    outfile.write("Lift[N], moment[Nm], shear[N], torque[Nm], moment of inertia, polar moment of inertia\n")
    if lift != None:
        if stiffnesses == True:
            for i in range(len(lift["Ls"])):
                line = "{}, {}, {}, {}, {}, {}\n".format(lift["Ls"][i], diagram["Moment"]["Ms"][i],diagram["Shear"]["Vs"][i],diagram["Torque"]["Ts"][i],diagram["BendStiffness"]["Is"][i],diagram["TorStiffness"]["Js"][i])
                outfile.write(line)
        else : 
            for i in range(len(lift["Ls"])):
                line = "{}, {}, {}, {}\n".format(lift["Ls"][i], diagram["Moment"]["Ms"][i],diagram["Shear"]["Vs"][i],diagram["Torque"]["Ts"][i])
                outfile.write(line)
    else:
        for i in range(len(diagram["Torque"]["Ts"])):
            line = "{}, {}, {}, {}, {}\n".format(diagram["Moment"]["Ms"][i],diagram["Shear"]["Vs"][i],diagram["Torque"]["Ts"][i],diagram["BendStiffness"]["Is"][i],diagram["TorStiffness"]["Js"][i])
            outfile.write(line)

    outfile.close()

def calculateCases():
    case2 = LD(
                41.1,   #wingspan [m]
                6.76,      #rootchord [m]
                0.29,   #taperratio
                31.2,     #sweep0.25c [deg]
                0.0,    #AoA [deg]
                1.0,    #load factor
                [(0.675, 6.06189, 0.0), (0.55, 5.723848, 0.7)],  # (cl, clalpha, x) assumed to be linear between two points and constant if otherwise 
                [(-0.1507, 0.252101, 0.0),(-0.1147, 0.257831, 0.7)],      #cms, same as cls just not given yet
                [( 0.14 ,0.0),(0.1,0.7)] #T/C's for the airfoils
                #c_l_alpha = 5.723848
                )
    case2.loadFactor = -1.0
    case2.fuelLevel = 0.0
    lift2 = case2.genLiftDist(118.4, 1.225)
    diagram2 =case2.genDiagrams(118.4, 1.225, filename="case2.tex")
    case2.fuelLevel = 0.7
    diagram2b =case2.genDiagrams(118.4, 1.225, filename="case2b.tex")
    case2.fuelLevel = 0.7
    diagram2c =case2.genDiagrams(118.4, 1.225, filename="case2c.tex")
    saveToFile("case2.txt", diagram2, lift2)
    print(case2.tipDeflection(0.001))
    print(case2.getRequiredThicknessDefl(6.16))


    case3 = LD(
                41.1,   #wingspan [m]
                6.76,      #rootchord [m]
                0.29,   #taperratio
                31.2,     #sweep0.25c [deg]
                0.0,    #AoA [deg]
                1.0,    #load factor
                [(0.675, 6.06189, 0.0), (0.55, 5.723848, 0.7)],  # (cl, clalpha, x) assumed to be linear between two points and constant if otherwise 
                [(-0.1507, 0.252101, 0.0),(-0.1147, 0.257831, 0.7)],      #cms, same as cls just not given yet
                [( 0.14 ,0.0),(0.1,0.7)] #T/C's for the airfoils
                #c_l_alpha = 5.723848
                )
    case3.loadFactor = 2.5
    case3.fuelLevel = 0.0
    lift3 = case3.genLiftDist(118.38, 1.225)
    diagram3 =case3.genDiagrams(118.38, 1.225, filename="case3.tex")
    case3.fuelLevel = 0.7
    diagram3b =case3.genDiagrams(118.38, 1.225, filename="case3b.tex")
    case3.fuelLevel = 1.0
    diagram3c =case3.genDiagrams(118.38, 1.225, filename="case3c.tex")
    saveToFile("case3.txt", diagram3, lift3)


    case4 = LD(
                41.1,   #wingspan [m]
                6.76,      #rootchord [m]
                0.29,   #taperratio
                31.2,     #sweep0.25c [deg]
                0.0,    #AoA [deg]
                1.0,    #load factor
                [(0.675, 6.06189, 0.0), (0.55, 5.723848, 0.7)],  # (cl, clalpha, x) assumed to be linear between two points and constant if otherwise 
                [(-0.1507, 0.252101, 0.0),(-0.1147, 0.257831, 0.7)],      #cms, same as cls just not given yet
                [( 0.14 ,0.0),(0.1,0.7)] #T/C's for the airfoils
                #c_l_alpha = 5.723848
                )
    case4.loadFactor = 2.0
    lift4 = case4.genLiftDist(147.98, 1.225,)
    diagram4 = case4.genDiagrams(147.98, 1.225, filename="case4.tex")
    saveToFile("case4.txt", diagram4, lift4)

def main():
    case1 = LD(
                41.1,   #wingspan [m]
                6.76,      #rootchord [m]
                0.29,   #taperratio
                31.2,     #sweep0.25c [deg]
                0.0,    #AoA [deg]
                1.0,    #load factor
                [(0.675, 6.06189, 0.0), (0.55, 5.723848, 0.7)],  # (cl, clalpha, x) assumed to be linear between two points and constant if otherwise 
                [(-0.1507, 0.252101, 0.0),(-0.1147, 0.257831, 0.7)],      #cms, same as cls just not given yet
                [( 0.14 ,0.0),(0.1,0.7)] #T/C's for the airfoils
                #c_l_alpha = 5.723848
                )
    case1.loadFactor = 2.5
    case1.fuelLevel = 0.0
    lift1 = case1.genLiftDist(148, 1.225)
    diagram1 = case1.genDiagrams(148, 1.225, filename="case1.tex")

    print(case1.tipDeflection(0.001))
    print(case1.getRequiredThicknessDefl(6.16))
    print(case1.getRequiredThickness(6.16, 10.0))
    print(case1.diagrams["BendStiffness"]["Is"])
    saveToFile("case1.txt", diagram1, lift1, stiffnesses=True)

    case1.fuelLevel = 0.7
    diagram1b = case1.genDiagrams(148, 1.225, filename="case1b.tex")
    case1.fuelLevel = 1.0
    diagram1c = case1.genDiagrams(148, 1.225, filename="case1c.tex")
    
    calculateCases()


if __name__ == "__main__":
    main()