"""
Airport Baggage Handling System (Educational Demo) — White + Teal Theme
-----------------------------------------------------------------------
GUI: Tkinter (custom styled)
Data Structures:
    - Linked List → Conveyor Belt
    - Dictionaries → Flight Metadata + Flight Bins
"""

import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import Optional, Any, Dict, List

# ----------------------------
# Data Models & Structures
# ----------------------------

@dataclass
class Bag:
    bag_id: str
    passenger: str
    weight: float
    flight_code: str

class Node:
    def __init__(self, value: Bag):
        self.value: Bag = value
        self.next: Optional["Node"] = None

class SinglyLinkedList:
    """Simple FIFO queue behavior using a linked list."""
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0

    def __len__(self):
        return self._size

    def is_empty(self) -> bool:
        return self.head is None

    def append(self, value: Bag) -> None:
        node = Node(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def popleft(self) -> Bag:
        if self.head is None:
            raise IndexError("Conveyor is empty")
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return node.value

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.value
            cur = cur.next

# ----------------------------
# Core System
# ----------------------------

class BaggageSystem:
    def __init__(self):
        self.conveyor = SinglyLinkedList()
        self.current_bag: Optional[Bag] = None

        self.flights: Dict[str, Dict[str, Any]] = {
            "AI201": {"airline": "Air India", "gate": "A4", "dest": "DEL"},
            "6E512": {"airline": "IndiGo", "gate": "B2", "dest": "HYD"},
            "UK709": {"airline": "Vistara", "gate": "C1", "dest": "BLR"},
            "SG431": {"airline": "SpiceJet", "gate": "D3", "dest": "CCU"},
        }
        self.flight_bins: Dict[str, List[Bag]] = {code: [] for code in self.flights}

    def add_bag(self, bag: Bag) -> None:
        if bag.flight_code not in self.flights:
            raise ValueError(f"Unknown flight code: {bag.flight_code}")
        if bag.weight <= 0:
            raise ValueError("Weight must be positive")
        if self._bag_id_exists(bag.bag_id):
            raise ValueError(f"Bag ID '{bag.bag_id}' already exists")
        self.conveyor.append(bag)

    def _bag_id_exists(self, bag_id: str) -> bool:
        if self.current_bag and self.current_bag.bag_id == bag_id:
            return True
        for b in self.conveyor:
            if b.bag_id == bag_id:
                return True
        for bags in self.flight_bins.values():
            for b in bags:
                if b.bag_id == bag_id:
                    return True
        return False

    def move_conveyor(self) -> Optional[Bag]:
        if self.current_bag is not None:
            raise RuntimeError("Sorter is busy. Sort current bag first.")
        if self.conveyor.is_empty():
            return None
        self.current_bag = self.conveyor.popleft()
        return self.current_bag

    def sort_current_bag(self) -> Optional[Bag]:
        if self.current_bag is None:
            return None
        bag = self.current_bag
        self.flight_bins[bag.flight_code].append(bag)
        self.current_bag = None
        return bag

    def fast_sort_all(self) -> int:
        count = 0
        while not self.conveyor.is_empty():
            if self.current_bag is not None:
                self.sort_current_bag()
            self.current_bag = self.conveyor.popleft()
            self.sort_current_bag()
            count += 1
        return count

# ----------------------------
# GUI (White + Teal Theme)
# ----------------------------

class BaggageGUI(tk.Tk):
    def __init__(self, system: BaggageSystem):
        super().__init__()
        self.title("✈️ Airport Baggage Handling System")
        self.geometry("1150x700")
        self.configure(bg="white")
        self.system = system

        # Apply theme styling
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", font=("Segoe UI", 10))
        style.configure("TLabelframe", background="white", font=("Segoe UI", 11, "bold"), foreground="#008080")
        style.configure("TButton", background="#008080", foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#006666")])
        style.configure("Treeview", background="white", fieldbackground="white", foreground="black", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#008080", foreground="white", font=("Segoe UI", 10, "bold"))

        self._build_inputs()
        self._build_conveyor_view()
        self._build_sorter_view()
        self._build_bins_view()
        self._build_log()
        self._refresh_all()

    # --- UI Builders ---
    def _build_inputs(self):
        frm = ttk.LabelFrame(self, text="Add Bag (Enqueue to Conveyor)")
        frm.pack(fill="x", padx=12, pady=8)

        ttk.Label(frm, text="Bag ID").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.var_bagid = tk.StringVar()
        ttk.Entry(frm, textvariable=self.var_bagid, width=16).grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(frm, text="Passenger").grid(row=0, column=2, padx=6, pady=6, sticky="w")
        self.var_passenger = tk.StringVar()
        ttk.Entry(frm, textvariable=self.var_passenger, width=22).grid(row=0, column=3, padx=6, pady=6)

        ttk.Label(frm, text="Weight (kg)").grid(row=0, column=4, padx=6, pady=6, sticky="w")
        self.var_weight = tk.StringVar()
        ttk.Entry(frm, textvariable=self.var_weight, width=10).grid(row=0, column=5, padx=6, pady=6)

        ttk.Label(frm, text="Flight Code").grid(row=0, column=6, padx=6, pady=6, sticky="w")
        self.var_flight = tk.StringVar(value=list(self.system.flights.keys())[0])
        ttk.Combobox(frm, textvariable=self.var_flight, values=list(self.system.flights.keys()), width=10, state="readonly").grid(row=0, column=7, padx=6, pady=6)

        ttk.Button(frm, text="Add to Conveyor", command=self.on_add_bag).grid(row=0, column=8, padx=8, pady=6)
        ttk.Button(frm, text="Fast-Sort All", command=self.on_fast_sort).grid(row=0, column=9, padx=8, pady=6)

    def _build_conveyor_view(self):
        frm = ttk.LabelFrame(self, text="Conveyor (Linked List Queue)")
        frm.pack(fill="both", expand=True, padx=12, pady=8)

        cols = ("bag_id", "passenger", "weight", "flight")
        self.tree_conveyor = ttk.Treeview(frm, columns=cols, show="headings", height=8)
        for c, text in zip(cols, ["Bag ID", "Passenger", "Weight(kg)", "Flight"]):
            self.tree_conveyor.heading(c, text=text)
            self.tree_conveyor.column(c, anchor="center", width=120)
        self.tree_conveyor.pack(fill="both", expand=True, side="left", padx=6, pady=6)

        btns = ttk.Frame(frm)
        btns.pack(side="left", fill="y", padx=6)
        ttk.Button(btns, text="Move Conveyor → Sorter", command=self.on_move_conveyor).pack(pady=6, fill="x")

    def _build_sorter_view(self):
        frm = ttk.LabelFrame(self, text="Sorter")
        frm.pack(fill="x", padx=12, pady=4)
        self.lbl_current = ttk.Label(frm, text="Current Bag: —", font=("Segoe UI", 11, "bold"), foreground="#008080")
        self.lbl_current.pack(side="left", padx=8, pady=6)
        ttk.Button(frm, text="Sort Current Bag into Bin", command=self.on_sort_current).pack(side="left", padx=8)

    def _build_bins_view(self):
        frm = ttk.LabelFrame(self, text="Flight Bins (Dictionaries)")
        frm.pack(fill="both", expand=True, padx=12, pady=8)

        self.notebook = ttk.Notebook(frm)
        self.notebook.pack(fill="both", expand=True)
        self.bin_trees: Dict[str, ttk.Treeview] = {}

        for code, meta in self.system.flights.items():
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=f"{code}")

            header = ttk.Frame(tab)
            header.pack(fill="x", padx=6, pady=4)
            ttk.Label(header, text=f"Airline: {meta['airline']}  |  Dest: {meta['dest']}  |  Gate: {meta['gate']}", foreground="#006666", font=("Segoe UI", 10, "bold")).pack(side="left")

            cols = ("bag_id", "passenger", "weight")
            tree = ttk.Treeview(tab, columns=cols, show="headings", height=6)
            for c, text in zip(cols, ["Bag ID", "Passenger", "Weight(kg)"]):
                tree.heading(c, text=text)
                tree.column(c, anchor="center", width=140)
            tree.pack(fill="both", expand=True, padx=6, pady=6)
            self.bin_trees[code] = tree

    def _build_log(self):
        frm = ttk.LabelFrame(self, text="Activity Log")
        frm.pack(fill="both", expand=True, padx=12, pady=8)
        self.txt_log = tk.Text(frm, height=6, state="disabled", background="white", foreground="#004c4c", font=("Consolas", 10))
        self.txt_log.pack(fill="both", expand=True, padx=6, pady=6)

    # --- Actions ---
    def on_add_bag(self):
        try:
            bag_id = self.var_bagid.get().strip()
            passenger = self.var_passenger.get().strip()
            weight_str = self.var_weight.get().strip()
            flight = self.var_flight.get().strip()

            if not bag_id or not passenger or not weight_str:
                raise ValueError("All fields are required")
            weight = float(weight_str)

            bag = Bag(bag_id, passenger, weight, flight)
            self.system.add_bag(bag)
            self._log(f"Enqueued bag {bag_id} for flight {flight}")
            self._clear_inputs()
            self._refresh_conveyor()
        except Exception as e:
            messagebox.showerror("Add Bag Failed", str(e))

    def on_move_conveyor(self):
        try:
            bag = self.system.move_conveyor()
            if bag is None:
                messagebox.showinfo("Move Conveyor", "Conveyor is empty")
                return
            self._log(f"Moved bag {bag.bag_id} to sorter")
            self._refresh_sorter()
            self._refresh_conveyor()
        except Exception as e:
            messagebox.showerror("Move Conveyor Failed", str(e))

    def on_sort_current(self):
        bag = self.system.sort_current_bag()
        if bag is None:
            messagebox.showinfo("Sorter", "No bag at sorter")
            return
        self._log(f"Sorted bag {bag.bag_id} into bin {bag.flight_code}")
        self._refresh_sorter()
        self._refresh_bins()

    def on_fast_sort(self):
        n = self.system.fast_sort_all()
        self._log(f"Fast-sorted {n} bag(s) from conveyor to bins")
        self._refresh_all()

    # --- Helpers ---
    def _clear_inputs(self):
        self.var_bagid.set("")
        self.var_passenger.set("")
        self.var_weight.set("")

    def _refresh_conveyor(self):
        self.tree_conveyor.delete(*self.tree_conveyor.get_children())
        for bag in self.system.conveyor:
            self.tree_conveyor.insert("", "end", values=(bag.bag_id, bag.passenger, f"{bag.weight:.1f}", bag.flight_code))

    def _refresh_sorter(self):
        if self.system.current_bag:
            b = self.system.current_bag
            self.lbl_current.config(text=f"Current Bag: {b.bag_id} | {b.passenger} | {b.weight:.1f}kg | {b.flight_code}")
        else:
            self.lbl_current.config(text="Current Bag: —")

    def _refresh_bins(self):
        for code, tree in self.bin_trees.items():
            tree.delete(*tree.get_children())
            for bag in self.system.flight_bins.get(code, []):
                tree.insert("", "end", values=(bag.bag_id, bag.passenger, f"{bag.weight:.1f}"))

    def _refresh_all(self):
        self._refresh_conveyor()
        self._refresh_sorter()
        self._refresh_bins()

    def _log(self, msg: str):
        self.txt_log.configure(state="normal")
        self.txt_log.insert("end", f"• {msg}\n")
        self.txt_log.configure(state="disabled")
        self.txt_log.see("end")

# ----------------------------
# Entry Point
# ----------------------------

def main():
    system = BaggageSystem()
    app = BaggageGUI(system)
    app.mainloop()

if __name__ == "__main__":
    main()
