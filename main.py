from LoadingDiagram import LoadingDiagram as LD

def main():
    case1 = LD(
                41.1,   #wingspan [m]
                6.76,      #rootchord [m]
                0.29,   #taperratio
                31.2,     #sweep0.25c [deg]
                0.0,    #AoA [deg]
                1.0,    #load factor
                [(0.5313, 6.06189, 0.0), (0.3715, 5.723848, 0.7)],  # (cl, clalpha, x) assumed to be linear between two points and constant if otherwise 
                [(-0.1507, 0.252101, 0.0),(-0.1147, 0.257831, 0.7)],      #cms, same as cls just not given yet
                [( 0.14 ,0.0),(0.1,0.7)] #T/C's for the airfoils
                #c_l_alpha = 5.723848
                )
    case1.loadFactor = 2.6827
    case1.genDiagrams(82.2418, 1.225)#, filename="case1.tex")
    print(case1.tipDeflection(0.001))
    print(case1.getRequiredThicknessDefl(6.16))



if __name__ == "__main__":
    main()