from labgearser import AgilentE3631A
from labgearser import RSProRSKEL103
from labgearser import Keysight34460A

# --- CONFIGURAZIONE RS-232 (Agilent E3631A) -----------------------------------
PSU_PORT = "ASRL3::INSTR"
PSU_BAUDRATE = 9600
PSU_TIMEOUT = 5000

# --- CONFIGURAZIONE USB-seriale (RS-KEL103) ------------------------------------
ELD_PORT = "ASRL4::INSTR"
ELD_BAUDRATE = 9600
ELD_TIMEOUT = 5000

# --- CONFIGURAZIONE USBTMC (Keysight 34460A) -----------------------------------
DMM_PORT_1 = "USB0::0x2A8D::0x1601::MY53101442::0::INSTR"
DMM_PORT_2 = "USB0::0x2A8D::0x1701::MY57100432::0::INSTR"
DMM_TIMEOUT = 5000

if __name__ == "__main__":

    psu = AgilentE3631A(PSU_PORT, PSU_BAUDRATE, PSU_TIMEOUT)
    eld = RSProRSKEL103(ELD_PORT, ELD_BAUDRATE, ELD_TIMEOUT)
    dmm = Keysight34460A(DMM_PORT_1, DMM_TIMEOUT)
    # dmm_2 = Keysight34460A(DMM_PORT_2, DMM_TIMEOUT)