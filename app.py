#Root application

import tkinter as tk

from models.bank_simulation import BankSimulation
from ui.simulation_ui import SimulationUI

if __name__ == "__main__":
    simulation = BankSimulation()
    root = tk.Tk()
    ui = SimulationUI(root, simulation)
    root.mainloop()
