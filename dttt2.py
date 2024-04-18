import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.pyplot as plt
import imghdr



def calculate_L_section(Zin, RL, f):
    RS = np.real(Zin)
    if RS > RL:
        Q = np.sqrt(RS / RL - 1)
        XS = Q * RL
        XP = RS / Q
    else:
        Q = np.sqrt(RL / RS - 1)
        XS = Q * RS
        XP = RL / Q

    # Calculate inductance and capacitance for low-pass L-section
    L_low = XS / (2 * np.pi * f)
    C_low = 1 / (2 * np.pi * f * XP)

    # Calculate inductance and capacitance for high-pass L-section
    L_high = XP / (2 * np.pi * f)
    C_high = 1 / (2 * np.pi * f * XS)

    return (L_low, C_low), (L_high, C_high)
def calculate_pi_network(RS, RL, f, Q):
    # Calculate reactances
    Rvirt = RL /(1 + Q**2)
    Xparallello = RL / Q
    Xserieslo = Q * Rvirt
    Q2 = np.sqrt(RS / Rvirt - 1)
    Xparallelhi = RS / Q2
    Xserieshi = Q2 * Rvirt

    # Calculate Lo-side and Hi-side shunt elements
    C_lo = 1 / (2 * np.pi * f * np.abs(Xparallello))
    L_lo = np.abs(Xserieslo) / (2 * np.pi * f)
    C_hi = 1 / (2 * np.pi * f * np.abs(Xparallelhi))
    L_hi = np.abs(Xserieshi) / (2 * np.pi * f)

    # Calculate combined series elements
    C_combined = 1 / (2 * np.pi * f * np.abs(Xserieslo + Xserieshi))
    L_combined = np.abs(Xserieslo + Xserieshi) / (2 * np.pi * f)

    return Rvirt, C_lo, L_lo, C_hi, L_hi, C_combined, L_combined



def calculate_T_network(Zin, RL, f, Q):
    RS = Zin
    Rvirt = min(RS, RL) / (1 + Q**2)
    Xparallelhi = Rvirt / Q
    Xserieshi = RS * Q
    Q2 = Rvirt / RL
    Xparallello = Rvirt / Q2
    Xserieslo = RL * Q2

    # Calculate Lo-side and Hi-side series elements
    L_lo = np.abs(Xserieslo) / (2 * np.pi * f)
    C_lo = 1 / (2 * np.pi * f * np.abs(Xparallello))
    L_hi = np.abs(Xserieshi) / (2 * np.pi * f)
    C_hi = 1 / (2 * np.pi * f * np.abs(Xparallelhi))

    return Rvirt, L_lo, C_lo, L_hi, C_hi



def main():
    matching_type = input("Choose matching type (L, Pi or T): ")
    if matching_type not in ['L', 'Pi', 'T']:
        print("Invalid matching type!")
        return

    

    if matching_type == 'Pi':
        # Input values from the user
        Zin = float(input("Enter the real part of Zin (RS): "))
        RL = float(input("Enter the load resistance (RL): "))
        f = float(input("Enter the frequency (in Hz): "))
        Q = float(input("Enter the quality factor (Q): "))

        # Calculate Pi-network components
        Rvirt, C_lo, L_lo, C_hi, L_hi, C_combined, L_combined = calculate_pi_network(Zin, RL, f, Q)

        # Output the results
        print("\nResults:")
        print("Rvirt:", "{:.3f}".format(Rvirt * 1000), "mΩ")
        print("Lo-side (50 Ω) Shunt - Capacitive:", "{:.3f}".format(C_lo * 1e9), "nF")
        print("Lo-side (50 Ω) Shunt - Inductive:", "{:.3f}".format(L_lo * 1e6), "uH")
        print("Hi-side (50 Ω) Shunt - Capacitive:", "{:.3f}".format(C_hi * 1e9), "nF")
        print("Hi-side (50 Ω) Shunt - Inductive:", "{:.3f}".format(L_hi * 1e6), "uH")
        print("Combined Series - Capacitive:", "{:.3f}".format(C_combined * 1e9), "nF")
        print("Combined Series - Inductive:", "{:.3f}".format(L_combined * 1e6), "uH")
        
        image_path = 'C:/Users/linhd/OneDrive/Desktop/dttt2/PiNetwork.png'
        # Đọc hình ảnh bằng Pillow
        image = Image.open(image_path)
        # Chuyển đổi hình ảnh thành mảng numpy
        image_array = np.array(image)
        # Hiển thị hình ảnh bằng matplotlib
        plt.imshow(image_array)
        plt.axis('off')  # Ẩn trục
        plt.show()

    elif matching_type == 'T':
        # Input values from the user
        RS = float(input("Enter the real part of Zin (RS): "))
        RL = float(input("Enter the load resistance (RL): "))
        f = float(input("Enter the frequency (in Hz): "))
        Q = float(input("Enter the quality factor (Q): "))

        # Calculate T-network components
        Rvirt, L_lo, C_lo, L_hi, C_hi = calculate_T_network(RS, RL, f, Q)

        # Output the results
        print("\nResults:")
        print("Rvirt:", "{:.3f}".format(Rvirt * 1000), "mΩ")
        print("Lo-side (50 Ω) Series - Inductive:", "{:.3f}".format(L_lo * 1e6), "uH")
        print("Lo-side (50 Ω) Shunt - Capacitive:", "{:.3f}".format(C_lo * 1e9), "nF")
        print("Hi-side (50 Ω) Series - Inductive:", "{:.3f}".format(L_hi * 1e6), "uH")
        print("Hi-side (50 Ω) Shunt - Capacitive:", "{:.3f}".format(C_hi * 1e9), "nF")
        
        image_path = 'C:/Users/linhd/OneDrive/Desktop/dttt2/TNetwork.png'
        # Đọc hình ảnh bằng Pillow
        image = Image.open(image_path)
        # Chuyển đổi hình ảnh thành mảng numpy
        image_array = np.array(image)
        # Hiển thị hình ảnh bằng matplotlib
        plt.imshow(image_array)
        plt.axis('off')  # Ẩn trục
        plt.show()
    else: # Input from the user
        # Input values from the user
        Zin = float(input("Enter Zin: "))
        RL = float(input("Enter RL: "))
        f = float(input("Enter the frequency (in Hz): "))

        # Calculate L-section
        (L_low, C_low), (L_high, C_high) = calculate_L_section(Zin, RL, f)

        # Output the results
        print("\nFor L section:")
        print("Low-Pass: {:.3f} uH, {:.3f} nF".format(L_low * 1e6, C_low * 1e9))
        print("High-Pass: {:.3f} uH, {:.3f} nF".format(L_high * 1e6, C_high * 1e9))
        image_path = 'C:/Users/linhd/OneDrive/Desktop/dttt2/Lsection.png'
        # Đọc hình ảnh bằng Pillow
        image = Image.open(image_path)
        # Chuyển đổi hình ảnh thành mảng numpy
        image_array = np.array(image)
        # Hiển thị hình ảnh bằng matplotlib
        plt.imshow(image_array)
        plt.axis('off')  # Ẩn trục
        plt.show()

if __name__ == "__main__":
    main()
