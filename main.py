from LoadingDiagram import LoadingDiagram as LD

def main():
    case1 = LD(
                41.1,   #wingspan [m]
                7,      #rootchord [m]
                0.18,   #taperratio
                30,     #sweep [deg]
                0.0,    #AoA [deg]
                1.0,    #load factor
                [(0.5313, 6.06189, 0.0), (0.3715, 5.723848, 0.7)],  # (cl, clalpha, x) assumed to be linear between two points and constant if otherwise 
                [(-0.1507, 0.252101, 0.0),(-0.1147, 0.257831, 0.7)],      #cms, same as cls just not given yet
                c_l_alpha = 5.723848
                )
    print(case1.getCl(0.7,0.71))
    print(case1.getSegments())
    #case1.genLiftDist(70,1.225)
    case1.genDiagrams(70,1.225)
    pass



if __name__ == "__main__":
    main()