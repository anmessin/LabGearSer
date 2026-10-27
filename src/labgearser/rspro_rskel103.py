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
        print(f"[INFO]: Connessione {self.idn}")


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

    # --- Stato del dispositivo (buzzer, baud rate, ...) ----------------------
    def get_status(self):
        return self.query(":STATus?")

    # --- Attiva il remote sense (non documentato nella guida v2.10) ----------
    def sense_on(self):
        self.write(":SYSTem:COMPensate ON")

    # --- Disattiva il remote sense -------------------------------------------
    def sense_off(self):
        self.write(":SYSTem:COMPensate OFF")

    # --- Stato del remote sense ----------------------------------------------
    def get_sense_state(self):
        return int(self.query(":SYSTem:COMPensate?") == "ON")

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
        return self._to_float(self.query(":VOLTage?"), "V")

    # --- Legge la tensione massima impostabile -------------------------------
    def get_max_voltage(self):
        return self._to_float(self.query(":VOLTage:UPPer?"), "V")

    # --- Legge la tensione minima impostabile --------------------------------
    def get_min_voltage(self):
        return self._to_float(self.query(":VOLTage:LOWer?"), "V")

    # --- Misura tensione reale -----------------------------------------------
    def measure_voltage(self):
        return self._to_float(self.query(":MEASure:VOLTage?"), "V")

    # -------------------------------------------------------------------------
    # Gestione Corrente.
    # -------------------------------------------------------------------------

    # --- Imposta corrente (modalità CC) --------------------------------------
    def set_current(self, current):
        self.write(f":CURRent {current}A")

    # --- Legge corrente impostata (modalità CC) ------------------------------
    def get_current(self):
        return self._to_float(self.query(":CURRent?"), "A")

    # --- Legge la corrente massima impostabile -------------------------------
    def get_max_current(self):
        return self._to_float(self.query(":CURRent:UPPer?"), "A")

    # --- Legge la corrente minima impostabile --------------------------------
    def get_min_current(self):
        return self._to_float(self.query(":CURRent:LOWer?"), "A")

    # --- Misura corrente reale -----------------------------------------------
    def measure_current(self):
        return self._to_float(self.query(":MEASure:CURRent?"), "A")

    # -------------------------------------------------------------------------
    # Gestione Resistenza.
    # -------------------------------------------------------------------------

    # --- Imposta resistenza (modalità CR) ------------------------------------
    def set_resistance(self, resistance):
        self.write(f":RESistance {resistance}OHM")

    # --- Legge resistenza impostata (modalità CR) ----------------------------
    def get_resistance(self):
        return self._to_float(self.query(":RESistance?"), "OHM")

    # --- Legge la resistenza massima impostabile -----------------------------
    def get_max_resistance(self):
        return self._to_float(self.query(":RESistance:UPPer?"), "OHM")

    # --- Legge la resistenza minima impostabile ------------------------------
    def get_min_resistance(self):
        return self._to_float(self.query(":RESistance:LOWer?"), "OHM")

    # -------------------------------------------------------------------------
    # Gestione Potenza.
    # -------------------------------------------------------------------------

    # --- Imposta potenza (modalità CW) ---------------------------------------
    def set_power(self, power):
        self.write(f":POWer {power}W")

    # --- Legge potenza impostata (modalità CW) -------------------------------
    def get_power(self):
        return self._to_float(self.query(":POWer?"), "W")

    # --- Legge la potenza massima impostabile --------------------------------
    def get_max_power(self):
        return self._to_float(self.query(":POWer:UPPer?"), "W")

    # --- Legge la potenza minima impostabile ---------------------------------
    def get_min_power(self):
        return self._to_float(self.query(":POWer:LOWer?"), "W")

    # --- Misura potenza reale ------------------------------------------------
    def measure_power(self):
        return self._to_float(self.query(":MEASure:POWer?"), "W")


    # =========================================================================
    # COMPOSITI E LOGICHE
    # =========================================================================

    # --- Porta lo strumento in uno stato noto --------------------------------
    def initialize(self):
        self.load_off()
        self.write(":CURRent MIN")
        self.write(":VOLTage MAX")
        self.write(":RESistance MAX")
        self.write(":POWer MIN")
        self.set_mode("CC")

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

    # --- Converte una risposta con unità in float ----------------------------
    def _to_float(self, response, unit):
        return float(response.rstrip(unit))


    # =========================================================================
    # CONTEXT MANAGER
    # =========================================================================

    # --- Ingresso nel blocco `with` ------------------------------------------
    def __enter__(self):
        return self

    # --- Uscita dal blocco `with`: rilascia sempre lo strumento --------------
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
