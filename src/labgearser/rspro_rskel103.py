import pyvisa

class RSProRSKEL103:

    MODES = ("CC", "CV", "CW", "CR")

    def __init__(self, resource, baudrate=9600, timeout=1000):
        rm = pyvisa.ResourceManager("@py")
        self.inst = rm.open_resource(
            resource,
            baud_rate         = baudrate,
            data_bits         = 8,
            parity            = pyvisa.constants.Parity.none,
            stop_bits         = pyvisa.constants.StopBits.one,
            read_termination  = "\n",
            write_termination = "\n",
            timeout           = timeout,
        )
        self.idn = self.identify()


    # =========================================================================
    # Comunicazione di base.
    # =========================================================================

    # --- Invio e lettura comandi ---------------------------------------------
    def write(self, cmd):
        self.inst.write(cmd)

    def query(self, cmd):
        return self.inst.query(cmd).strip()

    # --- Return product information -----------------------------------------------------
    def identify(self):
        idn = self.query("*IDN?")
        if not idn:
            raise RuntimeError(
                f"Nessuna risposta da {self.inst.resource_name}."
            )
        return idn

    # =========================================================================
    # Gestione modalità carico.
    # =========================================================================

    # --- Set the query of the device ON ---------------------------------------------------
    def load_on(self):
        self.write(":INPut ON")

    # --- Set the query of the device OFF --------------------------------------------------
    def load_off(self):
        self.write(":INPut OFF")

    # --- Set the mode of the device: voltage, current, resistor and power -----
    def set_mode(self, mode):
        if mode not in self.MODES:
            raise ValueError(
                f"Modalita' non valida: {mode!r}. Valori ammessi: {self.MODES}"
            )
        self.write(f":FUNCtion {mode}")

    # --- Legge la modalita' di carico attuale -----------------------------------
    def get_mode(self):
        return self.query(":FUNCtion?")


    # =========================================================================
    # Tensione.
    # =========================================================================

    # --- Set CV voltage ----------------------------------------
    def set_voltage(self, value):
        self.write(f":VOLTage {value}V")

    # --- Query CV voltage ------------------------------------------------
    def get_voltage(self):
        return float(self.query(":VOLTage?").rstrip("V"))

    # --- Query the max/min voltage of the device -----------------------------
    def get_max_voltage(self):
        return float(self.query(":VOLTage:UPPer?").rstrip("V"))

    def get_min_voltage(self):
        return float(self.query(":VOLTage:LOWer?").rstrip("V"))

    # --- Return the load voltage. Unit V ----------------------------------------------------
    def measure_voltage(self):
        return float(self.query(":MEASure:VOLTage?").rstrip("V"))


    # =========================================================================
    # Corrente.
    # =========================================================================

    # --- Set the CC current ----------------------------------------
    def set_current(self, value):
        self.write(f":CURRent {value}A")

    # --- Query the CC current ------------------------------------------------
    def get_current(self):
        return float(self.query(":CURRent?").rstrip("A"))

    # --- Query the max/min current --------------------------
    def get_max_current(self):
        return float(self.query(":CURRent:UPPer?").rstrip("A"))

    def get_min_current(self):
        return float(self.query(":CURRent:LOWer?").rstrip("A"))

    # --- Return the load current. Unit A ----------------------------------------------------
    def measure_current(self):
        return float(self.query(":MEASure:CURRent?").rstrip("A"))


    # =========================================================================
    # Resistenza.
    # =========================================================================

    # --- Set the CR resistor ---------------------------------------
    def set_resistance(self, value):
        self.write(f":RESistance {value}OHM")

    # --- Query the CR resistor -----------------------------------------------
    def get_resistance(self):
        return float(self.query(":RESistance?").rstrip("OHM"))

    # --- Query the max/min resistor of the device -------------------------
    def get_max_resistance(self):
        return float(self.query(":RESistance:UPPer?").rstrip("OHM"))

    def get_min_resistance(self):
        return float(self.query(":RESistance:LOWer?").rstrip("OHM"))


    # =========================================================================
    # Potenza.
    # =========================================================================

    # --- Set the CW power -----------------------------------------
    def set_power(self, value):
        self.write(f":POWer {value}W")

    # --- Query the CW power --------------------------------------------------
    def get_power(self):
        return float(self.query(":POWer?").rstrip("W"))

    # --- Query the max/min power of the device ----------------------------
    def get_max_power(self):
        return float(self.query(":POWer:UPPer?").rstrip("W"))

    def get_min_power(self):
        return float(self.query(":POWer:LOWer?").rstrip("W"))

    # --- Return the load power. Unit W -------------------------------------------------------
    def measure_power(self):
        return float(self.query(":MEASure:POWer?").rstrip("W"))


    # =========================================================================
    # Chiusura comunicazione.
    # =========================================================================

    # --- Chiude la comunicazione ---------------------------------------------
    def close(self):
        self.inst.close()


    # =========================================================================
    # Context manager.
    # =========================================================================

    # --- Ingresso nel blocco `with` ------------------------------------------
    def __enter__(self):
        return self

    # --- Uscita dal blocco `with`: rilascia sempre lo strumento --------------
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()