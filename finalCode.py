import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import deque

class PageReplacementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Algorithm Simulator")
        self.root.geometry("1000x800") 
        
        
        self.input_frame = ttk.Frame(root, padding="10")
        self.input_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.result_frame = ttk.Frame(root, padding="10")
        self.result_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.root.grid_rowconfigure(1, weight=1)  
        self.root.grid_rowconfigure(0, weight=0)  
        self.root.grid_columnconfigure(0, weight=1)

        # Input Section
        ttk.Label(self.input_frame, text="Page Reference String (comma-separated):").grid(row=0, column=0, padx=5, pady=5)
        self.page_entry = ttk.Entry(self.input_frame, width=50)
        self.page_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.input_frame, text="Frame Size:").grid(row=1, column=0, padx=5, pady=5)
        self.frame_size = ttk.Entry(self.input_frame, width=10)
        self.frame_size.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Button(self.input_frame, text="Simulate", command=self.run_simulation).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Results Section
        self.notebook = ttk.Notebook(self.result_frame)
        self.notebook.pack(fill="both", expand=True)
        
        self.tabs = {}
        for algo in ["FIFO", "LRU", "Optimal"]:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=algo)
            self.tabs[algo] = frame
# this code implements fifo algo.
    def fifo_algorithm(self, pages, frame_size):
        frames = []
        page_faults = 0
        steps = []
        
        for page in pages:
            current = frames.copy()
            if page not in frames:
                if len(frames) < frame_size:
                    frames.append(page)
                else:
                    frames.pop(0)
                    frames.append(page)
                page_faults += 1
            steps.append((current, page, page_faults))
        return steps, page_faults
# this code implements lru algo. 
    def lru_algorithm(self, pages, frame_size):
        frames = []
        page_faults = 0
        steps = []
        recent = []
        
        for page in pages:
            current = frames.copy()
            if page not in frames:
                if len(frames) < frame_size:
                    frames.append(page)
                    recent.append(page)
                else:
                    lru_page = recent.pop(0)
                    frames[frames.index(lru_page)] = page
                    recent.append(page)
                page_faults += 1
            else:
                recent.remove(page)
                recent.append(page)
            steps.append((current, page, page_faults))
        return steps, page_faults
# this implements optimal algo. 
    def optimal_algorithm(self, pages, frame_size):
        frames = []
        page_faults = 0
        steps = []
        
        for i, page in enumerate(pages):
            current = frames.copy()
            if page not in frames:
                if len(frames) < frame_size:
                    frames.append(page)
                else:
                    future = pages[i+1:]
                    replace_idx = self.find_optimal_replace(frames, future)
                    frames[replace_idx] = page
                page_faults += 1
            steps.append((current, page, page_faults))
        return steps, page_faults

    def find_optimal_replace(self, frames, future):
        distances = []
        for frame in frames:
            try:
                distances.append(future.index(frame))
            except ValueError:
                return frames.index(frame)
        return np.argmax(distances)

    def create_visualization(self, algo, steps, total_faults, pages, frame_size):
        for widget in self.tabs[algo].winfo_children():
            widget.destroy()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), height_ratios=[1, 1])  # Adjusted figure size
        
        # Memory state matrix
        states = np.zeros((frame_size, len(pages)))
        for i, (current, page, _) in enumerate(steps):
            for j in range(min(frame_size, len(current))):
                states[j, i] = current[j] if current[j] else 0
        
        cax = ax1.matshow(states, cmap='viridis')
        fig.colorbar(cax, ax=ax1)
        ax1.set_title(f"{algo} - Memory States")
        ax1.set_xlabel("Reference Number")
        ax1.set_ylabel("Frame Number")
        
        # Page Faults Plot with Metrics
        faults = [step[2] for step in steps]
        ax2.plot(faults, 'r.-', label='Page Faults')
        #ax2.set_title(f"Page Faults Over Time (Total: {total_faults})")
        ax2.set_xlabel("Reference Number")
        ax2.set_ylabel("Fault Count")
        ax2.legend()
        
        # Step 4: Performance Metrics
        hit_ratio = 1 - (total_faults / len(pages))
        miss_ratio = 1 - hit_ratio
        metrics_text = (f"Hit Ratio: {hit_ratio:.2%}\n"
                       f"Miss Ratio: {miss_ratio:.2%}\n"
                       f"Total Faults: {total_faults}")
        ax2.text(0.02, 0.98, metrics_text, transform=ax2.transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout(pad=3.0)  # Increased padding to prevent overlap
        canvas = FigureCanvasTkAgg(fig, master=self.tabs[algo])
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def run_simulation(self):
        try:
            pages = [int(x.strip()) for x in self.page_entry.get().split(',')]
            frame_size = int(self.frame_size.get())
            
            if frame_size <= 0 or not pages:
                raise ValueError("Invalid input")
            
            fifo_steps, fifo_faults = self.fifo_algorithm(pages, frame_size)
            lru_steps, lru_faults = self.lru_algorithm(pages, frame_size)
            opt_steps, opt_faults = self.optimal_algorithm(pages, frame_size)
            
            self.create_visualization("FIFO", fifo_steps, fifo_faults, pages, frame_size)
            self.create_visualization("LRU", lru_steps, lru_faults, pages, frame_size)
            self.create_visualization("Optimal", opt_steps, opt_faults, pages, frame_size)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementSimulator(root)
    root.mainloop()