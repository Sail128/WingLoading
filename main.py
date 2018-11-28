from LoadingDiagram import LoadingDiagram as LD

def saveToFile(filename , diagram, lift=None):
    outfile = open(filename, "w")
    outfile.write("Lift[N], moment[Nm], shear[N], torque[Nm]\n")
    if lift != None:
        for i in range(len(lift["Ls"])):
            line = "{}, {}, {}, {}\n".format(lift["Ls"][i], diagram["Moment"]["Ms"][i],diagram["Shear"]["Vs"][i],diagram["Torque"]["Ts"][i])
            outfile.write(line)
    else:
        for i in range(len(diagram["Torque"]["Ts"])):
            line = "{}, {}, {}\n".format(diagram["Moment"]["Ms"][i],diagram["Shear"]["Vs"][i],diagram["Torque"]["Ts"][i])
            outfile.write(line)

    outfile.close()

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
    lift1 = case1.genLiftDist(148, 1.225)
    diagram1 = case1.genDiagrams(148, 1.225, filename="case1.tex")
    saveToFile("case1.txt", diagram1, lift1)
    print(case1.tipDeflection(0.001))
    print(case1.getRequiredThicknessDefl(6.16))
    
    case1B = LD(
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
    case1B.loadFactor = -1.0
    lift1B = case1B.genLiftDist(148, 1.225)
    diagram1B =case1B.genDiagrams(148, 1.225, filename="case1B.tex")
    saveToFile("case1B.txt", diagram1B, lift1B)
    print(case1B.tipDeflection(0.001))
    print(case1B.getRequiredThicknessDefl(6.16))


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
    case2.loadFactor = 2.5
    lift2 = case2.genLiftDist(118.38, 1.225)
    diagram2 =case2.genDiagrams(118.38, 1.225, filename="case2.tex")
    saveToFile("case2.txt", diagram2, lift2)


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
    case3.loadFactor = 2.0
    lift3 = case3.genLiftDist(147.98, 1.225,)
    diagram3 = case3.genDiagrams(147.98, 1.225, filename="case3.tex")
    saveToFile("case3.txt", diagram3, lift3)


if __name__ == "__main__":
    main()