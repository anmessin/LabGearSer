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

    # --- Identificazione -----------------------------------------------------
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

    # --- Attiva il carico (ingresso ON) --------------------------------------
    def load_on(self):
        self.write(":INPut ON")

    # --- Disattiva il carico (ingresso OFF) ----------------------------------
    def load_off(self):
        self.write(":INPut OFF")

    # --- Imposta la modalità di carico (CC, CV, CW, CR) ----------------------
    def set_mode(self, mode):
        if mode not in self.MODES:
            raise ValueError(
                f"Modalità non valida: {mode!r}. Valori ammessi: {self.MODES}"
            )
        self.write(f":FUNCtion {mode}")

    # --- Legge la modalità di carico attuale ---------------------------------
    def get_mode(self):
        return self.query(":FUNCtion?")


    # =========================================================================
    # Tensione.
    # =========================================================================

    # --- Imposta tensione (modalità CV) --------------------------------------
    def set_voltage(self, value):
        self.write(f":VOLTage {value}V")

    # --- Legge tensione impostata (modalità CV) ------------------------------
    def get_voltage(self):
        return float(self.query(":VOLTage?").rstrip("V"))

    # --- Legge la tensione massima/minima impostabile ------------------------
    def get_max_voltage(self):
        return float(self.query(":VOLTage:UPPer?").rstrip("V"))

    def get_min_voltage(self):
        return float(self.query(":VOLTage:LOWer?").rstrip("V"))

    # --- Misura tensione reale (V) -------------------------------------------
    def measure_voltage(self):
        return float(self.query(":MEASure:VOLTage?").rstrip("V"))


    # =========================================================================
    # Corrente.
    # =========================================================================

    # --- Imposta corrente (modalità CC) --------------------------------------
    def set_current(self, value):
        self.write(f":CURRent {value}A")

    # --- Legge corrente impostata (modalità CC) ------------------------------
    def get_current(self):
        return float(self.query(":CURRent?").rstrip("A"))

    # --- Legge la corrente massima/minima impostabile ------------------------
    def get_max_current(self):
        return float(self.query(":CURRent:UPPer?").rstrip("A"))

    def get_min_current(self):
        return float(self.query(":CURRent:LOWer?").rstrip("A"))

    # --- Misura corrente reale (A) -------------------------------------------
    def measure_current(self):
        return float(self.query(":MEASure:CURRent?").rstrip("A"))


    # =========================================================================
    # Resistenza.
    # =========================================================================

    # --- Imposta resistenza (modalità CR) ------------------------------------
    def set_resistance(self, value):
        self.write(f":RESistance {value}OHM")

    # --- Legge resistenza impostata (modalità CR) ----------------------------
    def get_resistance(self):
        return float(self.query(":RESistance?").rstrip("OHM"))

    # --- Legge la resistenza massima/minima impostabile ----------------------
    def get_max_resistance(self):
        return float(self.query(":RESistance:UPPer?").rstrip("OHM"))

    def get_min_resistance(self):
        return float(self.query(":RESistance:LOWer?").rstrip("OHM"))


    # =========================================================================
    # Potenza.
    # =========================================================================

    # --- Imposta potenza (modalità CW) ---------------------------------------
    def set_power(self, value):
        self.write(f":POWer {value}W")

    # --- Legge potenza impostata (modalità CW) -------------------------------
    def get_power(self):
        return float(self.query(":POWer?").rstrip("W"))

    # --- Legge la potenza massima/minima impostabile -------------------------
    def get_max_power(self):
        return float(self.query(":POWer:UPPer?").rstrip("W"))

    def get_min_power(self):
        return float(self.query(":POWer:LOWer?").rstrip("W"))

    # --- Misura potenza reale (W) --------------------------------------------
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