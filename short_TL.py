import streamlit as st
from output_func_short import *
from cmath import *
from math import *

def rect_to_polar(rect):
    z = complex(rect)
    r = abs(z)
    theta = phase(z)
    theta_deg = theta * 180 / pi
    return f"{r} ∠ {theta_deg:.2f}°"

def isfloat(value):
    try:
        float_value = float(value)
        return float_value
    except ValueError:
        return False

# Input Fields
def input_page_short():
    st.title("🎯SHORT TRANSMISSION LINE")

    st.header("Input Parameters")

    MGMD = 0
    Type = st.radio("Type of system", ("Symmetrical Spacing", "Unsymmetrical Spacing(Transposed)"))
    if Type == "Unsymmetrical Spacing":
        D1 = st.text_input("Spacing between the phase conductors a-b")
        D2 = st.text_input("Spacing between the phase conductors b-c")
        D3 = st.text_input("Spacing between the phase conductors c-a")
        if D1 and D2 and D3:
            if D1.isnumeric() and D2.isnumeric() and D3.isnumeric():
                D1 = float(D1)
                D2 = float(D2)
                D3 = float(D3)
                
                # Calculate MGMD
                MGMD = (D1 * D3 * D2) ** (1/3)
            else:
                st.write("Please enter valid numbers for the spacings")
    elif  Type == "Symmetrical Spacing":
        D = st.text_input("Spacing between the phase conductors")
        if D.isnumeric():
            MGMD = float(D)
    k = st.text_input("Number of sub-conductors per bundle")
    d = st.text_input("Spacing between the sub-conductors")
    values = [1, 7, 19, 37, 61, 91]
    N = st.select_slider("Number of strands in each sub conductor", options=values)
    d_strand = st.text_input("Diameter of each strand")
    l = st.text_input("Length of the line in km")
    R = st.text_input("Resistance of the line per phase per km")
    f = st.text_input("Power Frequency")
    sys_vol = st.text_input("Nominal System Voltage")
    P_r = st.text_input("Receiving end load in MW")
    pf = st.text_input("Power factor of the receiving end load")

    # Calculate and Display Results
    if st.button("Calculate"):
        if isfloat(sys_vol) and isfloat(R) and isfloat(l) and isfloat(f) and isfloat(P_r) and isfloat(pf) and isfloat(N) and isfloat(k) and isfloat(d) and isfloat(d_strand):
            results = output(sys_vol=float(sys_vol),
                             R=float(R),
                             l=float(l),
                             f=float(f),
                             MGMD=float(MGMD),
                             P_r=float(P_r),
                             pf=float(pf),
                             N=float(N),
                             k=float(k),
                             d=float(d),
                             d_strand=float(d_strand))

            st.header("Output Results")
            col1, col2 = st.columns(2)

            col1.write("Inductance per phase per km:")
            col1.write("Capacitance per phase per km:")
            col1.write("Inductive Reactance of the line:")
            col1.write("Capacitive Reactance of the line:")
            col1.write("A Parameter:")
            col1.write("B Parameter:")
            col1.write("C Parameter:")
            col1.write("D Parameter:")
            col1.write("Charging current from sending end substation:")
            col1.write("Sending end voltage:")
            col1.write("Sending end current:")
            col1.write("Percentage Voltage Regulation:")
            col1.write("Power Loss in the line:")
            col1.write("Transmission Efficiency:")

            col2.write(f"{abs(results.Inductance_per_phase()):.2f} H/km")
            col2.write(f"{abs(results.Capacitance_per_phase()):.2f} F/km")
            col2.write(f"{abs(results.Inductive_Reactance()):.2f} \u03A9")
            col2.write(f"{abs(results.Capacitive_Reactance()):.2f} \u03A9")
            col2.write(f"{rect_to_polar(results.A_parameter())}")
            col2.write(f"{rect_to_polar(results.B_parameter())}")
            col2.write(f"{rect_to_polar(results.C_parameter())}")
            col2.write(f"{rect_to_polar(results.D_parameter())}")
            col2.write(f"{results.Charging_current_sending_substation():.2f} A")
            col2.write(f"{abs(results.Sending_voltage()) * pow(3, 0.5) / 1000:.2f} kV")
            col2.write(f"{abs(results.Sending_current()):.2f} A")
            col2.write(f"{results.Voltage_regulation():.2f}")
            col2.write(f"{results.Power_loss():.2f} MW")
            col2.write(f"{results.Efficiency():.2f}")