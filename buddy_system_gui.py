import logging
from tkinter import messagebox
import tkinter as tk
from datetime import datetime

DEFAULT_TOTAL_MEMORY = 128  # MB

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


class BuddySystem:
    def __init__(self, total_memory, log_callback):
        self.total_memory = total_memory
        self.free_blocks = {}
        self.allocated_blocks = []
        self.log_callback = log_callback
        self._initialize_free_blocks()
        self.log(f"Initialized Buddy System with {total_memory} MB of memory.")

    def log(self, message):
        gui_message = f"{datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')} - {message}"
        logging.info(message)
        if self.log_callback:
            self.log_callback(gui_message)

    def _initialize_free_blocks(self):
        self.free_blocks = {self.total_memory: [0]}
        size = self.total_memory // 2
        while size >= 1:
            self.free_blocks[size] = []
            size //= 2

    def allocate(self, size, process_name):
        block_size = self._find_block_size(size)
        self.log(f"Attempting to allocate {size} MB ({
                 block_size} MB block) for process '{process_name}'.")

        if not self._ensure_block_available(block_size):
            self.log(f"Allocation failed for process '{
                     process_name}' with size {size} MB. Not enough memory.")
            return None

        address = self.free_blocks[block_size].pop(0)
        self.allocated_blocks.append((process_name, address, block_size, size))
        self.log(f"Allocated {size} MB to process '{
                 process_name}' at address {address}.")
        return address

    def _ensure_block_available(self, block_size):
        if block_size in self.free_blocks and self.free_blocks[block_size]:
            return True

        larger_block_size = block_size * 2
        if larger_block_size <= self.total_memory and self._ensure_block_available(larger_block_size):
            self._split_block(larger_block_size)
            return True

        return False

    def _split_block(self, larger_block_size):
        if larger_block_size not in self.free_blocks or not self.free_blocks[larger_block_size]:
            self.log(f"Cannot split: No larger block of size {
                     larger_block_size} MB available.")
            return False

        address = self.free_blocks[larger_block_size].pop(0)
        smaller_block_size = larger_block_size // 2
        self.free_blocks[smaller_block_size].append(address)
        self.free_blocks[smaller_block_size].append(
            address + smaller_block_size)
        self.log(f"Split block of size {larger_block_size} MB into two blocks of size {
                 smaller_block_size} MB.")
        return True

    def deallocate(self, process_name):
        for block in self.allocated_blocks:
            if block[0] == process_name:
                address, block_size = block[1], block[2]
                self.allocated_blocks.remove(block)
                if block_size not in self.free_blocks:
                    self.free_blocks[block_size] = []
                self.free_blocks[block_size].append(address)
                self.free_blocks[block_size].sort()
                self.log(f"Deallocated memory of process '{
                         process_name}' at address {address}.")

                while block_size < self.total_memory:
                    buddy_address = self._find_buddy(address, block_size)
                    if buddy_address in self.free_blocks[block_size]:
                        self.free_blocks[block_size].remove(address)
                        self.free_blocks[block_size].remove(buddy_address)
                        address = min(address, buddy_address)
                        block_size *= 2
                        self.free_blocks[block_size].append(address)
                        self.log(f"Merged block at address {
                                 address} into size {block_size} MB.")
                    else:
                        break
                return True
        self.log(f"Deallocate failed: No process named '{
                 process_name}' found.")
        return False

    def _find_block_size(self, size):
        block_size = 1
        while block_size < size:
            block_size *= 2
        return block_size

    def _find_buddy(self, address, block_size):
        return address ^ block_size

    def calculate_stats(self):
        allocated_space = sum(block[3] for block in self.allocated_blocks)
        free_space = sum(size * len(blocks)
                         for size, blocks in self.free_blocks.items())
        internal_fragmentation = sum(
            block[2] - block[3] for block in self.allocated_blocks)
        return allocated_space, free_space, internal_fragmentation


def create_gui():
    root = tk.Tk()
    root.title("Buddy System Memory Manager")

    # Configure main layout
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    # Header
    header_frame = tk.Frame(root, bg="#f0f0f0")
    header_frame.grid(row=0, column=0, sticky="ew")
    header_label = tk.Label(header_frame, text="Buddy System Memory Allocation Algorithm",
                            font=("Arial", 16, "bold"), bg="#f0f0f0")
    header_label.pack(pady=10)

    # Main content frame
    content_frame = tk.Frame(root)
    content_frame.grid(row=1, column=0, sticky="nsew")
    content_frame.columnconfigure(0, weight=1)
    content_frame.rowconfigure(0, weight=1)

    main_frame = tk.Frame(content_frame)
    main_frame.grid(row=0, column=0, sticky="nsew")
    content_frame.rowconfigure(0, weight=1)
    content_frame.columnconfigure(0, weight=1)

    main_frame.columnconfigure(0, weight=1)  # first column
    main_frame.columnconfigure(1, weight=1)  # second column
    main_frame.columnconfigure(2, weight=1)  # third column
    main_frame.rowconfigure(0, weight=0)
    main_frame.rowconfigure(1, weight=1)

    # Log area
    log_frame = tk.Frame(main_frame)
    log_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    log_frame.rowconfigure(0, weight=1)
    log_frame.columnconfigure(0, weight=1)

    log_scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL)
    log_scrollbar.grid(row=0, column=1, sticky="ns")

    log_box = tk.Text(log_frame, wrap=tk.WORD,
                      yscrollcommand=log_scrollbar.set)
    log_box.grid(row=0, column=0, sticky="nsew")
    log_box.tag_config("latest", background="yellow")
    log_scrollbar.config(command=log_box.yview)

    def log_callback(message):
        log_box.tag_remove("latest", "1.0", tk.END)
        log_box.insert(tk.END, message + "\n", "latest")
        log_box.see(tk.END)

    system = BuddySystem(DEFAULT_TOTAL_MEMORY, log_callback)

    # Memory visualization canvas
    canvas = tk.Canvas(main_frame, bg="white")
    canvas.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=10, pady=10)

    # Controls (top-left)
    input_frame = tk.Frame(main_frame)
    input_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    input_frame.columnconfigure(0, weight=0)
    input_frame.columnconfigure(1, weight=1)

    total_label = tk.Label(input_frame, text=f"Total Memory: {
                           system.total_memory} MB", font=("Arial", 12))
    total_label.grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky="w")

    total_memory_frame = tk.Frame(input_frame)
    total_memory_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
    total_memory_frame.columnconfigure(1, weight=1)
    tk.Label(total_memory_frame, text="Set Total Memory (MB):").grid(
        row=0, column=0, sticky="e", padx=5)
    total_memory_entry = tk.Entry(total_memory_frame)
    total_memory_entry.grid(row=0, column=1, sticky="ew", padx=5)
    total_memory_entry.insert(0, "128")  # Default
    update_memory_button = tk.Button(
        total_memory_frame, text="Update Memory", bg="lightgrey")
    update_memory_button.grid(row=0, column=2, padx=5)

    process_count = 1

    tk.Label(input_frame, text="Process Name:").grid(
        row=2, column=0, sticky="e", padx=5, pady=2)
    process_name_entry = tk.Entry(input_frame)
    process_name_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
    process_name_entry.insert(0, f"Process-{process_count}")

    tk.Label(input_frame, text="Memory Size (MB):").grid(
        row=3, column=0, sticky="e", padx=5, pady=2)
    memory_entry = tk.Entry(input_frame)
    memory_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=2)
    memory_entry.insert(0, "16")

    add_button = tk.Button(input_frame, text="Add Process", bg="lightgrey")
    add_button.grid(row=4, column=0, columnspan=2, pady=5)

    # Process list (bottom-left)
    process_frame = tk.Frame(main_frame)
    process_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    process_frame.columnconfigure(0, weight=1)
    process_frame.rowconfigure(1, weight=1)

    active_processes_label = tk.Label(process_frame, text="Active Processes:")
    active_processes_label.grid(row=0, column=0, sticky="w")

    # Scrollable process list
    process_list_frame = tk.Frame(process_frame)
    process_list_frame.grid(row=1, column=0, sticky="nsew", pady=2)
    process_list_frame.rowconfigure(0, weight=1)
    process_list_frame.columnconfigure(0, weight=1)

    process_scrollbar = tk.Scrollbar(process_list_frame, orient=tk.VERTICAL)
    process_scrollbar.grid(row=0, column=1, sticky="ns")

    active_processes = tk.Listbox(
        process_list_frame, width=50, yscrollcommand=process_scrollbar.set)
    active_processes.grid(row=0, column=0, sticky="nsew")
    process_scrollbar.config(command=active_processes.yview)

    remove_button = tk.Button(
        process_frame, text="Remove Process", bg="lightgrey", width=12, font=("Arial", 9))
    remove_button.grid(row=2, column=0, pady=5, sticky="ew")

    # Stats (top-middle)
    stats_canvas = tk.Canvas(main_frame, width=300,
                             height=100, bg="white", highlightthickness=0)
    stats_canvas.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    def update_memory_view():
        canvas.delete("all")
        height = int(canvas.winfo_height())
        if height < 100:
            height = 500
        total_height = height - 100
        start_y = 50
        x = 80

        # Free memory
        for block_size, blocks in system.free_blocks.items():
            for block in blocks:
                block_height = (
                    block_size / system.total_memory) * total_height
                block_start = start_y + \
                    (1 - (block + block_size) / system.total_memory) * total_height
                canvas.create_rectangle(
                    x, block_start, x + 30, block_start + block_height, fill="green", outline="black"
                )
                canvas.create_text(
                    x + 50, block_start, text=f"Addr: {block}", anchor=tk.W, font=("Arial", 8)
                )

        # Highlight selected process
        selected = active_processes.curselection()
        highlighted_process = active_processes.get(selected[0]).split(":")[
            0] if selected else None

        # Allocated memory
        for block in system.allocated_blocks:
            address, block_size, _, size = block[1], block[2], block[3], block[3]
            block_height = (block_size / system.total_memory) * total_height
            block_start = start_y + \
                (1 - (address + block_size) / system.total_memory) * total_height
            allocated_height = (size / system.total_memory) * total_height

            color = "blue" if block[0] == highlighted_process else "red"
            canvas.create_rectangle(
                x, block_start, x + 30, block_start + allocated_height, fill=color, outline="black"
            )

            if allocated_height < block_height:
                canvas.create_rectangle(
                    x, block_start + allocated_height, x + 30, block_start + block_height, fill="black", outline="black"
                )

        allocated_space, free_space, internal_fragmentation = system.calculate_stats()
        stats_canvas.delete("all")
        stats_canvas.create_rectangle(
            10, 10, 30, 30, fill="red", outline="black")
        stats_canvas.create_text(40, 20, text=f"Allocated: {
                                 allocated_space} MB", anchor="w", font=("Arial", 10), fill="black")
        stats_canvas.create_rectangle(
            10, 40, 30, 60, fill="green", outline="black")
        stats_canvas.create_text(40, 50, text=f"Free: {
                                 free_space} MB", anchor="w", font=("Arial", 10), fill="black")
        stats_canvas.create_rectangle(
            10, 70, 30, 90, fill="black", outline="black")
        stats_canvas.create_text(40, 80, text=f"Internal Fragmentation: {
                                 internal_fragmentation} MB", anchor="w", font=("Arial", 10), fill="black")

    def add_process():
        nonlocal process_count
        process_name = process_name_entry.get()
        try:
            size = int(memory_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Memory size must be an integer.")
            return

        if process_name and size > 0:
            address = system.allocate(size, process_name)
            if address is None:
                messagebox.showerror(
                    "Error", "Allocation failed. Not enough memory.")
            else:
                active_processes.insert(tk.END, f"{process_name}: {size} MB")
                update_memory_view()
                process_count += 1
                process_name_entry.delete(0, tk.END)
                process_name_entry.insert(0, f"Process-{process_count}")
        else:
            messagebox.showerror(
                "Error", "Invalid process name or memory size.")

    def remove_process_func():
        selected = active_processes.curselection()
        if selected:
            selected_index = selected[0]
            process_info = active_processes.get(selected_index)
            process_name = process_info.split(":")[0]
            if system.deallocate(process_name):
                active_processes.delete(selected_index)
                update_memory_view()

                # Try to select next process
                if active_processes.size() > 0:
                    if selected_index < active_processes.size():
                        active_processes.selection_set(selected_index)
                    else:
                        active_processes.selection_set(
                            active_processes.size() - 1)
            else:
                messagebox.showerror("Error", "Deallocation failed.")
        else:
            messagebox.showerror("Error", "No process selected.")

    def update_total_memory():
        try:
            new_memory = int(total_memory_entry.get())
            if new_memory > 0:
                nonlocal system
                system = BuddySystem(new_memory, log_callback)
                total_label.config(text=f"Total Memory: {
                                   system.total_memory} MB")
                update_memory_view()
                log_callback(f"Total memory updated to {new_memory} MB.")
            else:
                messagebox.showerror(
                    "Error", "Total memory must be a positive integer.")
        except ValueError:
            messagebox.showerror("Error", "Total memory must be an integer.")

    add_button.config(command=add_process)
    remove_button.config(command=remove_process_func)
    update_memory_button.config(command=update_total_memory)

    active_processes.bind("<<ListboxSelect>>", lambda _: update_memory_view())

    main_frame.rowconfigure(1, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.columnconfigure(2, weight=1)

    process_frame.rowconfigure(1, weight=1)
    log_frame.rowconfigure(0, weight=1)
    process_list_frame.rowconfigure(0, weight=1)
    process_list_frame.columnconfigure(0, weight=1)

    root.bind("<Configure>", lambda event: update_memory_view())

    update_memory_view()

    # Footer (centered)
    footer_frame = tk.Frame(root, bg="#f0f0f0")
    footer_frame.grid(row=2, column=0, sticky="ew")
    footer_frame.columnconfigure(0, weight=1)

    footer_content = tk.Frame(footer_frame, bg="#f0f0f0")
    footer_content.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    footer_content.columnconfigure(0, weight=1)

    tk.Label(footer_content, text="Department of Electrical and Computer Engineering",
             bg="#f0f0f0", font=("Arial", 10), anchor="center").pack(anchor="center")
    tk.Label(footer_content, text="The Open University of Sri Lanka",
             bg="#f0f0f0", font=("Arial", 10), anchor="center").pack(anchor="center")

    root.mainloop()


if __name__ == "__main__":
    create_gui()
