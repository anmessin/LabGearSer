import pyvisa

class Keysight34460A:

    def __init__(self, resource, timeout=1000):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(
            resource,
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

    # --- Reset a stato noto (non svuota la coda errori) -----------------------
    def reset(self):
        self.write("*RST")


    # =========================================================================
    # Tensione.
    # =========================================================================

    # --- Misura tensione DC (rng=None: autorange) ------------------------------
    def measure_voltage(self, rng=None):
        if rng is None:
            cmd = "MEASure:VOLTage:DC?"
        else:
            cmd = f"MEASure:VOLTage:DC? {rng}"
        return float(self.query(cmd))

    # --- Imposta il tempo di integrazione (NPLC) per la tensione DC -----------
    def set_voltage_nplc(self, value):
        self.write(f"VOLTage:DC:NPLC {value}")

    # --- Legge il tempo di integrazione (NPLC) impostato per la tensione DC ---
    def get_voltage_nplc(self):
        return float(self.query("VOLTage:DC:NPLC?"))


    # =========================================================================
    # Corrente.
    # =========================================================================

    # --- Misura corrente DC (rng=None: autorange) -------------------------------
    def measure_current(self, rng=None):
        if rng is None:
            cmd = "MEASure:CURRent:DC?"
        else:
            cmd = f"MEASure:CURRent:DC? {rng}"
        return float(self.query(cmd))

    # --- Imposta il tempo di integrazione (NPLC) per la corrente DC -----------
    def set_current_nplc(self, value):
        self.write(f"CURRent:DC:NPLC {value}")

    # --- Legge il tempo di integrazione (NPLC) impostato per la corrente DC ---
    def get_current_nplc(self):
        return float(self.query("CURRent:DC:NPLC?"))


    # =========================================================================
    # Resistenza.
    # =========================================================================

    # --- Misura resistenza a 2 fili (rng=None: autorange) -----------------------
    def measure_resistance(self, rng=None):
        if rng is None:
            cmd = "MEASure:RESistance?"
        else:
            cmd = f"MEASure:RESistance? {rng}"
        return float(self.query(cmd))

    # --- Misura resistenza a 4 fili, Kelvin (rng=None: autorange) ---------------
    def measure_resistance_4w(self, rng=None):
        if rng is None:
            cmd = "MEASure:FRESistance?"
        else:
            cmd = f"MEASure:FRESistance? {rng}"
        return float(self.query(cmd))

    # --- Imposta il tempo di integrazione (NPLC) per la resistenza a 4 fili ---
    def set_resistance_4w_nplc(self, value):
        self.write(f"FRESistance:NPLC {value}")

    # --- Legge il tempo di integrazione (NPLC) impostato per la resistenza a 4 fili ---
    def get_resistance_4w_nplc(self):
        return float(self.query("FRESistance:NPLC?"))


    # =========================================================================
    # Test di continuità e diodo.
    # =========================================================================

    # --- Test di continuità (range fisso 1 kOhm, beep sotto i 10 Ohm) ---------
    def measure_continuity(self):
        return float(self.query("MEASure:CONTinuity?"))

    # --- Test diodo (sorgente fissa 1 mA, range 1 V) ---------------------------
    def measure_diode(self):
        return float(self.query("MEASure:DIODe?"))


    # =========================================================================
    # Gestione errori.
    # =========================================================================

    # --- Legge il prossimo errore dalla coda (FIFO) --------------------------
    def get_error(self):
        return self.query("SYSTem:ERRor?")


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