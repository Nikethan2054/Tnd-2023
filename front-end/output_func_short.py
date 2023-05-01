from cmath import *
from math import *
import sys

# constants

eps = 8.854187817 * pow(10, -12)

# Output Functions

class output:
    def __init__(self, sys_vol, R, l, f, MGMD, P_r, pf, N, k, d, d_strand):
        self.sys_vol = sys_vol
        self.pf = pf
        self.k = k
        self.N = N
        self.d = d
        self.d_strand = d_strand
        self.P_r = P_r * pow(10, 6)
        self.R = R
        self.l = l
        self.f = f
        self.MGMD = MGMD
    
    def SGMD_L(self):
        dict = {1:1, 7:2, 19:3, 37:4, 61:5, 91:6}
        if self.N not in dict:
            sys.exit()

        number_of_layers = dict[self.N]
        radius = (number_of_layers - 0.5) * self.d_strand / 1000
        r_dash = 0.7788 * radius
        product_of_distances = (self.k * pow(self.d / 1000 * sin(pi/self.k), self.k-1) / pow(2, self.k-1))

        return (r_dash * product_of_distances)**(1/self.k)

    def SGMD_C(self):
        dict = {1:1, 7:2, 19:3, 37:4, 61:5, 91:6}
        if self.N not in dict:
            sys.exit()

        number_of_layers = dict[self.N]
        radius = (number_of_layers - 0.5) * self.d_strand / 1000
        product_of_distances = (self.k * pow(self.d / 1000 * sin(pi/self.k), self.k-1) / pow(2, self.k-1))

        return (radius * product_of_distances)**(1/self.k)

    def Inductance_per_phase(self):
        return pow(10, -4) * 2 * log(self.MGMD/self.SGMD_L())

    def Capacitance_per_phase(self):
        return (2 * pi * eps * pow(10, 3)) / log(self.MGMD/self.SGMD_C())

    def Inductive_Reactance(self):
        L = self.l * self.Inductance_per_phase()
        return 2 * pi * self.f * L

    def Capacitive_Reactance(self):
        C = self.l * self.Capacitance_per_phase()
        return pow(2 * pi * self.f * C, -1)

    def B_parameter(self):
        return complex((self.R * self.l) + (self.Inductive_Reactance() *1j))

    def A_parameter(self):
        return 1

    def C_parameter(self):
        return 0

    def D_parameter(self):
        return 1

    def Charging_current_sending_substation(self):
        return 0
    
    def V_R(self):
        return self.sys_vol * 1000 / pow(3, 0.5)

    def I_R(self):
        Ir =  self.P_r / (self.V_R() * self.pf * 3)
        return complex((Ir * self.pf) + (Ir * pow((1 - pow(self.pf, 2)), 0.5)) *1j)

    def Sending_voltage(self):
        ReV_s = (self.A_parameter().real * self.V_R()) + (self.B_parameter().imag * self.I_R().imag)
        ImV_s = (self.A_parameter().imag * self.V_R()) - (self.B_parameter().real * self.I_R().imag)
        return complex(ReV_s + (ImV_s*1j))

    def Sending_current(self):
        return self.I_R()

    def Voltage_regulation(self):
        return (abs(self.Sending_voltage()) - self.V_R()) * 100 / self.V_R()

    def Power_loss(self):
        return 3 * (((self.Sending_voltage() * self.Sending_current()).real) - ((self.V_R() * self.I_R()).real)) / pow(10, 6)

    def Efficiency(self):
        return (self.V_R() * self.I_R()).real * 100 / (self.Sending_voltage() * self.Sending_current()).real