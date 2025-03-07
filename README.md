# Efficient Page Replacement Algorithm Simulator

## 📌 About the Project
This project implements **three page replacement algorithms**:
- **FIFO (First In First Out)**
- **LRU (Least Recently Used)**
- **Optimal Page Replacement**

It helps users understand how different memory management techniques perform by computing **total page faults**.

---
## ⚙️ Features
✅ Implements **FIFO, LRU, and Optimal** algorithms  
✅ Accepts **user input for frames and page references**  
✅ Calculates **total page faults** for each algorithm  
✅ Generates **visualization using Python Matplotlib**  
✅ Easy-to-understand **C++ implementation**  
✅ Well-structured **GitHub commits for version control**

---
## 🔧 How to Run the Code
### **1️⃣ Clone the Repository**
To get started, clone this repository using:
```bash
git clone https://github.com/hariteja-01/EfficientPageReplacementSimulator.git
cd EfficientPageReplacementSimulator
```
### **2️⃣ Compile the C++ Program**
Ensure you have **g++** installed (Windows users need MinGW).
To compile the program, run:
```bash
g++ page_replacement.cpp -o simulator
```
### **3️⃣ Run the C++ Program**
Execute the compiled file:
```bash
./simulator  # For Linux/macOS
simulator.exe  # For Windows
```
### **4️⃣ Install Python Dependencies**
To generate the bar chart visualization, install Matplotlib:
```bash
pip install matplotlib
```
### **5️⃣ Run the Python Visualization Script**
Execute the Python script to generate a bar chart comparing the algorithms:
```bash
python3 visualize.py   # For Linux/macOS
python visualize.py    # For Windows
```
### **6️⃣ Source Code Files**
Click on the file names to view the respective code:
- 📄 [C++ Code](page_replacement.cpp) → C++ implementation of FIFO, LRU, and Optimal page replacement algorithms.
- 📄 [Python Code](visualize.py) → Python script for visualization using Matplotlib.
- 📄 [Text File](results.txt) → Auto-generated file containing the number of page faults after running the C++ program.

---
## Flow Chart
<img src="https://github.com/hariteja-01/EfficientPageReplacementSimulator/blob/main/_-%20visual%20selection.png" alt="flowchart" width="500"/>

## 📊 Example Visualization Output
After running the Python script, you will see a **bar chart** like this:  

📊 **Page Replacement Algorithm Comparison**  
- 🔴 FIFO: **no. of page faults**  
- 🔵 LRU: **no. of page faults**  
- 🟢 Optimal: **no. of page faults**  

📌 **This graph helps visualize which algorithm is more efficient based on page faults.**  

---

## 📜 License  
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🚀 Author  
👤 **Hari Teja Patnala**  
🔗 GitHub Link: [hariteja-01](https://github.com/hariteja-01)  

