import pyvisa

class AgilentE3631A:

    # --- Uscite disponibili --------------------------------------------------
    DC_OUTPUTS = ("P6V", "P25V", "N25V")

    # --- Limiti nominali per uscita (tensione/corrente) ----------------------
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

    # --- Passa in remoto (blocca il pannello frontale) -----------------------
    def remote(self):
        self.write("SYSTem:REMote")

    # --- Rilascia in locale (riabilita il pannello frontale) -----------------
    def local(self):
        self.write("SYSTem:LOCal")

    # -------------------------------------------------------------------------
    # Gestione uscite.
    # -------------------------------------------------------------------------

    # --- Selezione uscita ----------------------------------------------------
    def select_output(self, output):
        self._check_output(output)
        self.write(f"INSTrument:SELect {output}")

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

    # --- Attiva il tracking simmetrico P25V/N25V -----------------------------
    def track_on(self):
        self.write("OUTPut:TRACk:STATe ON")

    # --- Disattiva il tracking -----------------------------------------------
    def track_off(self):
        self.write("OUTPut:TRACk:STATe OFF")

    # --- Stato del tracking --------------------------------------------------
    def is_track_on(self):
        return bool(int(self.query("OUTPut:TRACk:STATe?")))

    # -------------------------------------------------------------------------
    # Gestione Tensione.
    # -------------------------------------------------------------------------

    # --- Imposta tensione ----------------------------------------------------
    def set_voltage(self, voltage):
        self.write(f"VOLTage {voltage}")

    # --- Lettura di setpoint in tensione -------------------------------------
    def get_voltage(self):
        return float(self.query("VOLTage?"))

    # --- Readback in tensione ------------------------------------------------
    def measure_voltage(self):
        return float(self.query("MEASure:VOLTage?"))

    # -------------------------------------------------------------------------
    # Gestione Corrente.
    # -------------------------------------------------------------------------

    # --- Imposta corrente ------------------------------------------------------
    def set_current(self, current):
        self.write(f"CURRent {current}")

    # --- Lettura di setpoint in corrente -------------------------------------
    def get_current(self):
        return float(self.query("CURRent?"))

    # --- Readback in corrente ------------------------------------------------
    def measure_current(self):
        return float(self.query("MEASure:CURRent?"))


    # =========================================================================
    # COMPOSITI E LOGICHE
    # =========================================================================

    # --- Chiude la comunicazione ---------------------------------------------
    def close(self):
        self.local()
        self.inst.close()


    # =========================================================================
    # VERIFICHE E VALIDAZIONI (metodi interni)
    # =========================================================================

    # --- Verifica dello stato di identificazione -----------------------------
    def _check_idn(self, idn):
        if not idn:
            raise RuntimeError(
                f"Nessuna risposta da {self.inst.resource_name}."
            )

    # --- Validazione dell'uscita selezionata ---------------------------------
    def _check_output(self, output):
        if output not in self.DC_OUTPUTS:
            raise ValueError(
                f"Uscita non valida: {output}. ValorI ammessi: {self.DC_OUTPUTS}."
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