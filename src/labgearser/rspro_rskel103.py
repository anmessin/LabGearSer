import pyvisa

class RSProRSKEL103:

    # --- Modalità di carico disponibili --------------------------------------
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
    # COMUNICAZIONE DI BASE
    # =========================================================================

    # --- Invio comando -------------------------------------------------------
    def write(self, cmd):
        self.inst.write(cmd)

    # --- Invio comando e lettura della risposta ------------------------------
    def query(self, cmd):
        return self.inst.query(cmd).strip()


    # =========================================================================
    # PRIMITIVE SCPI
    # =========================================================================

    # -------------------------------------------------------------------------
    # Metodi di sistema.
    # -------------------------------------------------------------------------

    # --- Identificazione -----------------------------------------------------
    def identify(self):
        idn = self.query("*IDN?")
        self._check_idn(idn)
        return idn

    # --- Abilita il BEEP!!! --------------------------------------------------
    def beeper_on(self):
        self.write(":SYSTem:BEEP ON")

    # --- Disabilita il BEEP!!! -----------------------------------------------
    def beeper_off(self):
        self.write(":SYSTem:BEEP OFF")

    # --- Stato del BEEP!!! ---------------------------------------------------
    def get_beeper_state(self):
        return self.query(":SYSTem:BEEP?")

    # --- Stato del dispositivo (buzzer, baud rate, ...) ----------------------
    def get_status(self):
        return self.query(":STATus?")

    # -------------------------------------------------------------------------
    # Gestione carico.
    # -------------------------------------------------------------------------

    # --- Attiva il carico (ingresso ON) --------------------------------------
    def load_on(self):
        self.write(":INPut ON")

    # --- Disattiva il carico (ingresso OFF) ----------------------------------
    def load_off(self):
        self.write(":INPut OFF")

    # --- Stato del carico (da verificare) ------------------------------------
    def get_load_state(self):
        return self.query(":INPut?")

    # --- Imposta la modalità di carico ---------------------------------------
    def set_mode(self, mode):
        self._check_mode(mode)
        self.write(f":FUNCtion {mode}")

    # --- Legge la modalità di carico attuale ---------------------------------
    def get_mode(self):
        return self.query(":FUNCtion?")

    # -------------------------------------------------------------------------
    # Gestione Tensione.
    # -------------------------------------------------------------------------

    # --- Imposta tensione (modalità CV) --------------------------------------
    def set_voltage(self, voltage):
        self.write(f":VOLTage {voltage}V")

    # --- Legge tensione impostata (modalità CV) ------------------------------
    def get_voltage(self):
        return self.query(":VOLTage?")

    # --- Legge la tensione massima impostabile -------------------------------
    def get_max_voltage(self):
        return self.query(":VOLTage:UPPer?")

    # --- Legge la tensione minima impostabile --------------------------------
    def get_min_voltage(self):
        return self.query(":VOLTage:LOWer?")

    # --- Misura tensione reale -----------------------------------------------
    def measure_voltage(self):
        return self.query(":MEASure:VOLTage?")

    # -------------------------------------------------------------------------
    # Gestione Corrente.
    # -------------------------------------------------------------------------

    # --- Imposta corrente (modalità CC) --------------------------------------
    def set_current(self, current):
        self.write(f":CURRent {current}A")

    # --- Legge corrente impostata (modalità CC) ------------------------------
    def get_current(self):
        return self.query(":CURRent?")

    # --- Legge la corrente massima impostabile -------------------------------
    def get_max_current(self):
        return self.query(":CURRent:UPPer?")

    # --- Legge la corrente minima impostabile --------------------------------
    def get_min_current(self):
        return self.query(":CURRent:LOWer?")

    # --- Misura corrente reale -----------------------------------------------
    def measure_current(self):
        return self.query(":MEASure:CURRent?")

    # -------------------------------------------------------------------------
    # Gestione Resistenza.
    # -------------------------------------------------------------------------

    # --- Imposta resistenza (modalità CR) ------------------------------------
    def set_resistance(self, resistance):
        self.write(f":RESistance {resistance}OHM")

    # --- Legge resistenza impostata (modalità CR) ----------------------------
    def get_resistance(self):
        return self.query(":RESistance?")

    # --- Legge la resistenza massima impostabile -----------------------------
    def get_max_resistance(self):
        return self.query(":RESistance:UPPer?")

    # --- Legge la resistenza minima impostabile ------------------------------
    def get_min_resistance(self):
        return self.query(":RESistance:LOWer?")

    # -------------------------------------------------------------------------
    # Gestione Potenza.
    # -------------------------------------------------------------------------

    # --- Imposta potenza (modalità CW) ---------------------------------------
    def set_power(self, power):
        self.write(f":POWer {power}W")

    # --- Legge potenza impostata (modalità CW) -------------------------------
    def get_power(self):
        return self.query(":POWer?")

    # --- Legge la potenza massima impostabile --------------------------------
    def get_max_power(self):
        return self.query(":POWer:UPPer?")

    # --- Legge la potenza minima impostabile ---------------------------------
    def get_min_power(self):
        return self.query(":POWer:LOWer?")

    # --- Misura potenza reale ------------------------------------------------
    def measure_power(self):
        return self.query(":MEASure:POWer?")


    # =========================================================================
    # COMPOSITI E LOGICHE
    # =========================================================================

    # --- Chiude la comunicazione ---------------------------------------------
    def close(self):
        self.inst.close()


    # =========================================================================
    # METODI INTERNI
    # =========================================================================

    # --- Verifica dello stato di identificazione -----------------------------
    def _check_idn(self, idn):
        if not idn:
            raise RuntimeError(
                f"Nessuna risposta da {self.inst.resource_name}."
            )

    # --- Validazione della modalità di carico --------------------------------
    def _check_mode(self, mode):
        if mode not in self.MODES:
            raise ValueError(
                f"Modalità non valida: {mode}. Valori ammessi: {self.MODES}."
            )


    # =========================================================================
    # CONTEXT MANAGER
    # =========================================================================

    # --- Ingresso nel blocco `with` ------------------------------------------
    def __enter__(self):
        return self

    # --- Uscita dal blocco `with`: rilascia sempre lo strumento --------------
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
