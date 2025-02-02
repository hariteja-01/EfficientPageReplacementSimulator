# Efficient Page Replacement Algorithm Simulator

## 📌 About the Project
This project implements **three page replacement algorithms**:
- **FIFO (First In First Out)**
- **LRU (Least Recently Used)**
- **Optimal Page Replacement**

It helps users understand how different memory management techniques perform by computing **total page faults**.

## ⚙️ Features
✅ Implements **FIFO, LRU, and Optimal** algorithms  
✅ Accepts **user input for frames and page references**  
✅ Calculates **total page faults** for each algorithm  
✅ Generates **visualization using Python Matplotlib**  
✅ Easy-to-understand **C++ implementation**  
✅ Well-structured **GitHub commits for version control** 

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


