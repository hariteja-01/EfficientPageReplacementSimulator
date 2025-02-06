import matplotlib.pyplot as plt

# Read the results file
with open("results.txt", "r") as file:
    data = file.readlines()

# Process data
algorithms = []
faults = []
for line in data:
    algo, fault_count = line.split()
    algorithms.append(algo)
    faults.append(int(fault_count))

# Create a bar chart
fig, ax = plt.subplots()
bars = ax.bar(algorithms, faults, color=['orange', 'violet', 'green'])

# Labeling the chart
plt.xlabel("Page Replacement Algorithms")
plt.ylabel("Total Page Faults")
plt.title("Comparison of Page Replacement Algorithms")

# Add an annotation (empty for now)
annot = ax.annotate("", xy=(0,0), xytext=(10,10), textcoords="offset points",
                    ha="center", va="bottom",
                    bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"),
                    fontsize=10, color="black", weight="bold",
                    arrowprops=dict(arrowstyle="wedge,tail_width=0.5", facecolor="black"))

annot.set_visible(False)  # Initially hidden

# Function to update annotation position and text
def update_annot(bar):
    x = bar.get_x() + bar.get_width() / 2
    y = bar.get_height()
    annot.xy = (x, y)
    annot.set_text(f"{int(y)}")  # Show exact page fault value
    annot.set_visible(True)

# Function to check if mouse is hovering over a bar
def on_hover(event):
    vis = annot.get_visible()
    for bar in bars:
        if bar.contains(event)[0]:  # If mouse is over a bar
            update_annot(bar)
            fig.canvas.draw_idle()
            return
    if vis:
        annot.set_visible(False)
        fig.canvas.draw_idle()

# Connect the hover event to the figure
fig.canvas.mpl_connect("motion_notify_event", on_hover)

# Show the plot
plt.show()
