import pyvisa

class AgilentE3631A:

    # --- Uscite disponibili --------------------------------------------------
    DC_OUTPUTS = ("P6V", "P25V", "N25V")

    # --- Limiti rated per uscita (tensione/corrente) --------------------------
    LIMITS = {
        "P6V":  {"voltage": (0, 6),   "current": (0, 5)},
        "P25V": {"voltage": (0, 25),  "current": (0, 1)},
        "N25V": {"voltage": (-25, 0), "current": (0, 1)},
    }

    def __init__(self, resource, baudrate=9600, timeout=1000):
        rm = pyvisa.ResourceManager("@py")
        self.inst = rm.open_resource(
            resource,
            baud_rate         = baudrate,
            data_bits         = 8,
            parity            = pyvisa.constants.Parity.none,
            stop_bits         = pyvisa.constants.StopBits.two,
            flow_control      = pyvisa.constants.VI_ASRL_FLOW_DTR_DSR,
            read_termination  = "\n",
            write_termination = "\n",
            timeout           = timeout,
        )
        self.idn = self.identify()
        self._selected_output = self.get_selected_output()


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
    # Gestione uscite.
    # =========================================================================

    # --- Selezione uscita ----------------------------------------------------
    def select_output(self, output):
        if output not in self.DC_OUTPUTS:
            raise ValueError(
                f"Uscita non valida: {output!r}. Valori ammessi: {self.DC_OUTPUTS}"
            )
        self.write(f"INSTrument:SELect {output}")
        self._selected_output = output

    # --- Uscita selezionata --------------------------------------------------
    def get_selected_output(self):
        return self.query("INSTrument:SELect?")

    # --- Accensione uscita ---------------------------------------------------
    def output_on(self):
        self.write("OUTPut ON")

    # --- Spegnimento uscita --------------------------------------------------
    def output_off(self):
        self.write("OUTPut OFF")

    # --- Stato uscita --------------------------------------------------------
    def is_output_on(self):
        return bool(int(self.query("OUTPut?")))

    # --- Attiva il tracking simmetrico P25V/N25V ------------------------------
    def track_on(self):
        self.write("OUTPut:TRACk:STATe ON")

    # --- Disattiva il tracking -------------------------------------------------
    def track_off(self):
        self.write("OUTPut:TRACk:STATe OFF")

    # --- Stato del tracking ------------------------------------------------------
    def is_track_on(self):
        return bool(int(self.query("OUTPut:TRACk:STATe?")))


    # =========================================================================
    # Tensione.
    # =========================================================================

    # --- Imposta tensione ----------------------------------------------------
    def set_voltage(self, value):
        vmin, vmax = self.LIMITS[self._selected_output]["voltage"]
        if not (vmin <= value <= vmax):
            raise ValueError(
                f"Tensione {value} V fuori range per {self._selected_output}: "
                f"[{vmin},{vmax}] V"
            )
        self.write(f"VOLTage {value}")

    # --- Legge tensione impostata --------------------------------------------
    def get_voltage(self):
        return float(self.query("VOLTage?"))

    # --- Misura tensione reale ------------------------------------------------
    def measure_voltage(self):
        output = self.get_selected_output()
        return float(self.query(f"MEASure:VOLTage? {output}"))


    # =========================================================================
    # Corrente.
    # =========================================================================

    # --- Imposta corrente ----------------------------------------------------
    def set_current(self, value):
        imin, imax = self.LIMITS[self._selected_output]["current"]
        if not (imin <= value <= imax):
            raise ValueError(
                f"Corrente {value} A fuori range per {self._selected_output}: "
                f"[{imin},{imax}] A"
            )
        self.write(f"CURRent {value}")

    # --- Legge corrente impostata --------------------------------------------
    def get_current(self):
        return float(self.query("CURRent?"))

    # --- Misura corrente reale -----------------------------------------------
    def measure_current(self):
        output = self.get_selected_output()
        return float(self.query(f"MEASure:CURRent? {output}"))


    # =========================================================================
    # Gestione errori.
    # =========================================================================

    # --- Legge il prossimo errore dalla coda (FIFO) --------------------------
    def get_error(self):
        return self.query("SYSTem:ERRor?")


    # =========================================================================
    # Controllo remoto/locale.
    # =========================================================================

    # --- Passa in remoto (blocca il pannello frontale) -----------------------
    def remote(self):
        self.write("SYSTem:REMote")

    # --- Rilascia in locale (riabilita il pannello frontale) -----------------
    def local(self):
        self.write("SYSTem:LOCal")

    # --- Chiude la comunicazione ---------------------------------------------
    def close(self):
        self.local()
        self.inst.close()


    # =========================================================================
    # Stato dello strumento.
    # =========================================================================

    # --- Riproduce lo stato dello strumento -----------------
    def get_status(self):
        state = {
            "output_on":       self.is_output_on(),
            "track_on":        self.is_track_on(),
            "selected_output": self.get_selected_output(),
            "error":           self.get_error(),
        }
        for ch in self.DC_OUTPUTS:
            response = self.query(f"APPLy? {ch}").strip('"')
            voltage, current = response.split(",")
            state[ch] = {"voltage": float(voltage), "current": float(current)}
        return state


    # =========================================================================
    # Context manager.
    # =========================================================================

    # --- Ingresso nel blocco `with` ------------------------------------------
    def __enter__(self):
        return self

    # --- Uscita dal blocco `with`: rilascia sempre lo strumento --------------
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()