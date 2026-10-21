import pyvisa

class Keysight34460A:

    UNIT_TEMP = ("C", "K", "F")

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

    # --- Reset dello strumento -----------------------------------------------
    def reset(self):
        self.write("*RST")

    # --- Legge il prossimo errore dalla FIFO ---------------------------------
    def get_error(self):
        return self.query("SYSTem:ERRor?")

    # --- Fa fare BEEP allo strumento!!! --------------------------------------
    def beep(self):
        self.write("SYSTem:BEEPer")

    # --- Abilita il BEEP!!! --------------------------------------------------
    def beeper_on(self):
        self.write("SYSTem:BEEPer:STATe ON")

    # --- Disabilita il BEEP!!! -----------------------------------------------
    def beeper_off(self):
        self.write("SYSTem:BEEPer:STATe OFF")

    # --- Stato del BEEP!!! ---------------------------------------------------
    def get_beeper_state(self):
        return self.query("SYSTem:BEEPer:STATe?")

    # -------------------------------------------------------------------------
    # Gestione Tensione.
    # -------------------------------------------------------------------------

    # --- Misura tensione DC --------------------------------------------------
    def measure_voltage(self, rng=None, res=None):
        self._check_resolution(rng, res)
        cmd = self._build_measure_cmd("MEASure:VOLTage:DC?", rng, res)
        return self.query(cmd)

    # --- Legge il range attuale per la tensione DC ---------------------------
    def get_voltage_range(self):
        return self.query("VOLTage:DC:RANGe?")

    # -------------------------------------------------------------------------
    # Gestione Corrente.
    # -------------------------------------------------------------------------

    # --- Misura corrente DC --------------------------------------------------
    def measure_current(self, rng=None, res=None):
        self._check_resolution(rng, res)
        cmd = self._build_measure_cmd("MEASure:CURRent:DC?", rng, res)
        return self.query(cmd)

    # --- Legge il range attuale per la corrente DC ---------------------------
    def get_current_range(self):
        return self.query("CURRent:DC:RANGe?")

    # -------------------------------------------------------------------------
    # Gestione Resistenza.
    # -------------------------------------------------------------------------

    # --- Misura resistenza a 2 fili ------------------------------------------
    def measure_resistance(self, rng=None, res=None):
        self._check_resolution(rng, res)
        cmd = self._build_measure_cmd("MEASure:RESistance?", rng, res)
        return self.query(cmd)

    # --- Misura resistenza a 4 fili, Kelvin ----------------------------------
    def measure_resistance_4w(self, rng=None, res=None):
        self._check_resolution(rng, res)
        cmd = self._build_measure_cmd("MEASure:FRESistance?", rng, res)
        return self.query(cmd)

    # --- Legge il range attuale per la resistenza a 2 fili -------------------
    def get_resistance_range(self):
        return self.query("RESistance:RANGe?")

    # --- Legge il range attuale per la resistenza a 4 fili -------------------
    def get_resistance_4w_range(self):
        return self.query("FRESistance:RANGe?")

    # -------------------------------------------------------------------------
    # Test di continuità e diodo.
    # -------------------------------------------------------------------------

    # --- Test di continuità (range fisso 1 kOhm, beep sotto i 10 Ohm) --------
    def measure_continuity(self):
        return self.query("MEASure:CONTinuity?")

    # --- Test diodo (sorgente fissa 1 mA, range 1 V) -------------------------
    def measure_diode(self):
        return self.query("MEASure:DIODe?")

    # -------------------------------------------------------------------------
    # Gestione Temperatura.
    # -------------------------------------------------------------------------

    # --- Imposta l'unità della temperatura -----------------------------------
    def set_unit_temperature(self, unit):
        self._check_temperature_unit(unit)
        self.write(f"UNIT:TEMPerature {unit}")

    # --- Legge l'unità della temperatura impostata ---------------------------
    def get_unit_temperature(self):
        return self.query(f"UNIT:TEMPerature?")

    # --- Misura temperatura con PT100 a 2 fili -------------------------------
    def measure_temperature(self):
        return self.query("MEASure:TEMPerature? RTD,85")


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

    # --- Validazione dei parametri rng e res per measure ---------------------
    def _check_resolution(self, rng, res):
        if rng is None and res is not None:
            raise ValueError("Non si può dare res senza rng.")

    # --- Costruisce il comando per i metodi measure_* con rng e res ----------
    def _build_measure_cmd(self, header, *params):
        params = [str(p) for p in params if p is not None]
        if not params:
            return header
        return f"{header} {','.join(params)}"

    # --- Validazione dell'unità di temperatura -------------------------------
    def _check_temperature_unit(self, unit):
        if unit not in self.UNIT_TEMP:
            raise ValueError(
                f"Unità non valida: {unit}. Valori ammessi: {self.UNIT_TEMP}."
            )