#include <iostream>
#include "AceGenContactRoutines.h"

int main(int argc, char *argv[])
{
    double X[4][3];
    double u[4][3];
    double kN = 1.;
    double radiusBI = 1.;
    double radiusBJ = 1.;
    double T = -0.1;
    double gN;
    double h[2] = {0.3, 0.3};
    double R[12];
    double K[12][12];
    int ExitCode;
    int CubicPenaltyPotential = 0;
    int nn = 4;
    int ndim = 3;
    double penetration = -0.1;
    X[0][0] = -1;
    X[0][1] = 0;
    X[0][2] = -radiusBI;
    X[1][0] = 1;
    X[1][1] = 0;
    X[1][2] = -radiusBI;
    X[2][0] = 0;
    X[2][1] = -1;
    X[2][2] = +radiusBJ + penetration;
    X[3][0] = 0;
    X[3][1] = 1;
    X[3][2] = +radiusBJ + penetration;

    for (int i = 0; i < nn; i++)
    {
        for (int j = 0; j< ndim; j++)
        {
            u[i][j] = 0;
            std::printf("X[%d][%d]:",i,j);
            std::cout<<X[i][j]<<std::endl;
            std::printf("\n");
        }
    }
    CurveToCurve2NodedBeams(X,u, &kN, &radiusBI, &radiusBJ, &T, &gN, h, R, K , &ExitCode, &CubicPenaltyPotential); 
    //     double v[782],double X[4][3]
    //  ,double u[4][3],double (*kN),double (*radiusBI),double (*radiusBJ),double (*T)
    //  ,double (*gN),double h[2],double R[12],double K[12][12],int (*ExitCode),int 
    //  (*CubicPenaltyPotential))

    std::cout<<"Exit code: "<<ExitCode<<std::endl;
    std::cout<<"Local parameter: "<<std::endl;
    for (int i = 0; i <2; i++){
        std::cout<<h[i]<<std::endl;
    }
    std::cout<<"Penetration: "<<gN<<std::endl;

    std::cout<<"contact residual: "<<gN<<std::endl;
    for (int i = 0; i <nn * ndim; i++){
        std::cout<<R[i]<<std::endl;
    }

    return 0;
}
