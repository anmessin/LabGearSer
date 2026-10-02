from labgearser import AgilentE3631A
from labgearser import RSProRSKEL103
from labgearser import Keysight34460A

# --- CONFIGURAZIONE RS-232 (Agilent E3631A) -----------------------------------
PSU_PORT = "ASRL3::INSTR"
PSU_BAUDRATE = 9600
PSU_TIMEOUT = 1000

# --- CONFIGURAZIONE USB-seriale (RS-KEL103) ------------------------------------
LOAD_PORT = "ASRL4::INSTR"
LOAD_BAUDRATE = 9600
LOAD_TIMEOUT = 1000

# --- CONFIGURAZIONE USBTMC (Keysight 34460A) -----------------------------------
MULT_PORT = "USB0::0x2A8D::0x1601::MY53101442::0::INSTR"
MULT_TIMEOUT = 1000

if __name__ == "__main__":

    psu = AgilentE3631A(PSU_PORT, PSU_BAUDRATE, PSU_TIMEOUT)
    load = RSProRSKEL103(LOAD_PORT, LOAD_BAUDRATE, LOAD_TIMEOUT)
    mult = Keysight34460A(MULT_PORT, MULT_TIMEOUT)
    
    print(f"Connesso: {psu.idn}")
    print(f"Connesso: {load.idn}")
    print(f"Connesso: {mult.idn}")
