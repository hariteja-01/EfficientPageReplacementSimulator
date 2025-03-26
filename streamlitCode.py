import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import time

# -------------------------
# Page Replacement Functions
# -------------------------
def fifo_page_replacement(pages, capacity):
    frame = []
    page_faults = 0
    steps = []
    hit_miss = []
    response_times = []
    
    start_time = time.time()
    for page in pages:
        req_time = time.time()
        if page not in frame:
            if len(frame) < capacity:
                frame.append(page)
            else:
                frame.pop(0)
                frame.append(page)
            page_faults += 1
            hit_miss.append("Miss")
        else:
            hit_miss.append("Hit")
        steps.append(list(frame))
        response_times.append(time.time() - req_time)
    
    execution_time = time.time() - start_time
    memory_utilization = (len(set(pages)) / capacity) * 100
    return page_faults, steps, hit_miss, execution_time, response_times, memory_utilization

def lru_page_replacement(pages, capacity):
    frame = []
    page_faults = 0
    steps = []
    hit_miss = []
    response_times = []
    
    start_time = time.time()
    for page in pages:
        req_time = time.time()
        if page not in frame:
            if len(frame) < capacity:
                frame.append(page)
            else:
                frame.pop(0)
                frame.append(page)
            page_faults += 1
            hit_miss.append("Miss")
        else:
            frame.remove(page)
            frame.append(page)
            hit_miss.append("Hit")
        steps.append(list(frame))
        response_times.append(time.time() - req_time)
    
    execution_time = time.time() - start_time
    memory_utilization = (len(set(pages)) / capacity) * 100
    return page_faults, steps, hit_miss, execution_time, response_times, memory_utilization

def optimal_page_replacement(pages, capacity):
    frame = []
    page_faults = 0
    steps = []
    hit_miss = []
    response_times = []
    
    start_time = time.time()
    for i, page in enumerate(pages):
        req_time = time.time()
        if page not in frame:
            if len(frame) < capacity:
                frame.append(page)
            else:
                future_pages = pages[i+1:]
                farthest = -1
                index_to_replace = 0
                for index, f_page in enumerate(frame):
                    if f_page in future_pages:
                        next_use = future_pages.index(f_page)
                        if next_use > farthest:
                            farthest = next_use
                            index_to_replace = index
                    else:
                        index_to_replace = index
                        break
                frame[index_to_replace] = page
            page_faults += 1
            hit_miss.append("Miss")
        else:
            hit_miss.append("Hit")
        steps.append(list(frame))
        response_times.append(time.time() - req_time)
    
    execution_time = time.time() - start_time
    memory_utilization = (len(set(pages)) / capacity) * 100
    return page_faults, steps, hit_miss, execution_time, response_times, memory_utilization

# -------------------------
# Concepts Explanation Function
# -------------------------
def generate_concepts_explanation(algorithm, pages, capacity, faults):
    explanation = f"## Concepts Covered: {algorithm} Page Replacement Algorithm\n\n"
    explanation += "### Algorithm Overview\n"
    explanation += f"The simulation used a page reference string of {len(pages)} pages with a frame capacity of {capacity}.\n\n"
    
    if algorithm == "FIFO":
        explanation += """
#### First-In-First-Out (FIFO) Page Replacement

FIFO is the simplest page replacement algorithm:
- New pages are added to the end of the frame
- When frames are full, the oldest page (first one added) is removed
- Works like a queue: first page in is the first to be replaced

**Key Characteristics:**
- Simple to implement
- Doesn't consider page usage frequency
- Can suffer from Belady's anomaly (more frames can increase page faults)
"""
    
    elif algorithm == "LRU":
        explanation += """
#### Least Recently Used (LRU) Page Replacement

LRU tracks the order of page usage more intelligently:
- Most recently used page moves to the end of the frame list
- When frames are full, the least recently used page is removed
- Assumes recently used pages are more likely to be used again

**Key Characteristics:**
- More adaptive than FIFO
- Considers recent page access patterns
- Requires tracking page usage order
"""
    
    elif algorithm == "Optimal":
        explanation += """
#### Optimal Page Replacement

Optimal algorithm makes the most theoretically efficient replacement:
- Replaces the page that won't be used for the longest time in the future
- Looks ahead in the page reference string to make the best replacement decision
- Impossible to implement perfectly in real systems, but serves as a theoretical benchmark

**Key Characteristics:**
- Minimizes page faults
- Requires future knowledge of page references
- Used as a theoretical ideal for comparing other algorithms
"""
    
    total_pages = len(pages)
    unique_pages = len(set(pages))
    fault_percentage = (faults / total_pages) * 100
    hit_percentage = 100 - fault_percentage
    
    explanation += f"\n### Performance Insights\n"
    explanation += f"""
- **Total Pages Processed:** {total_pages}
- **Unique Pages in Reference String:** {unique_pages}
- **Frame Capacity:** {capacity}
- **Page Fault Rate:** {fault_percentage:.2f}%
- **Page Hit Rate:** {hit_percentage:.2f}%

### Interpretation
The performance depends on:
1. Page reference string pattern
2. Number of available frames
3. Chosen replacement algorithm

A lower page fault rate indicates more efficient memory management.
"""
    return explanation

# -------------------------
# Individual Animation Function
# -------------------------
def create_algorithm_animation(algo_name, pages, capacity):
    # Simulate the chosen algorithm
    if algo_name == "FIFO":
        faults, steps, hit_miss, exec_time, response_times, mem_util = fifo_page_replacement(pages, capacity)
    elif algo_name == "LRU":
        faults, steps, hit_miss, exec_time, response_times, mem_util = lru_page_replacement(pages, capacity)
    elif algo_name == "Optimal":
        faults, steps, hit_miss, exec_time, response_times, mem_util = optimal_page_replacement(pages, capacity)
    else:
        raise ValueError("Invalid algorithm")
    
    # Compute cumulative page faults
    cumulative_faults = np.cumsum([1 if hm == "Miss" else 0 for hm in hit_miss])
    color_map = {"FIFO": "red", "LRU": "blue", "Optimal": "green"}
    
    # Create figure with enhanced styling
    fig = go.Figure()
    
    # Annotations for step tracking
    annotations = []
    
    # Create animation frames
    frames = []
    for i in range(1, len(pages) + 1):
        # Create frame trace
        frame_trace = go.Scatter(
            x=list(range(i)),
            y=cumulative_faults[:i],
            mode='lines+markers',
            name=algo_name,
            line=dict(color=color_map[algo_name], width=3),
            marker=dict(
                size=8,
                color=color_map[algo_name],
                line=dict(width=2, color='white')
            ),
            hovertemplate=
                "<b>%{fullData.name}</b><br>" +
                "Page Request: %{x}<br>" +
                "Cumulative Page Faults: %{y}<extra></extra>"
        )
        
        # Create annotation for current page request
        page_annotation = {
            "xref": "x",
            "yref": "y",
            "x": i-1,
            "y": cumulative_faults[i-1],
            "text": f"Page: {pages[i-1]}",
            "showarrow": True,
            "arrowhead": 1,
            "ax": 0,
            "ay": -40
        }
        
        frames.append(go.Frame(
            data=[frame_trace],
            name=f'frame_{i}',
            layout={'annotations': [page_annotation]}
        ))
    
    # Initial trace
    fig.add_trace(
        go.Scatter(
            x=list(range(len(pages))),
            y=cumulative_faults,
            mode='lines+markers',
            name=algo_name,
            line=dict(color=color_map[algo_name], width=3),
            marker=dict(
                size=8,
                color=color_map[algo_name],
                line=dict(width=2, color='white')
            ),
            hovertemplate=
                "<b>%{fullData.name}</b><br>" +
                "Page Request: %{x}<br>" +
                "Cumulative Page Faults: %{y}<extra></extra>"
        )
    )
    
    # Enhanced layout
    fig.update_layout(
        title={
            'text': f"{algo_name} Algorithm: Cumulative Page Faults",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=16)
        },
        xaxis_title="Page Requests",
        yaxis_title="Cumulative Page Faults",
        
        # Responsive sizing
        autosize=True,
        height=450,  # Fixed height for consistency
        
        # Axis configurations
        xaxis=dict(
            range=[-1, len(pages)],
            dtick=1,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            range=[0, max(cumulative_faults) + 1],
            showgrid=False,
            zeroline=False
        ),
        
        # Dark theme styling
        plot_bgcolor='rgba(0,0,0,0.1)',
        paper_bgcolor='rgba(0,0,0,0)',
        
        # Animation controls
        updatemenus=[
            {
                "type": "buttons",
                "direction": "left",
                "showactive": False,
                "x": 0.1,
                "y": -0.2,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {
                            "frame": {"duration": 300, "redraw": True},
                            "transition": {"duration": 100},
                            "fromcurrent": True,
                            "mode": "immediate"
                        }]
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }]
                    }
                ]
            }
        ]
    )
    
    # Set the frames
    fig.frames = frames
    
    return fig, faults, hit_miss, exec_time, response_times, mem_util

# -------------------------
# Streamlit UI Code
# -------------------------
st.title("Advanced Page Replacement Algorithm Simulator")

# Input methods
page_string = st.text_input("Enter reference string (comma-separated numbers):", "7, 0, 1, 2, 0, 3, 4, 2, 3, 0, 3, 2")
capacity = st.slider("Number of frames:", min_value=1, max_value=10, value=3)
algorithm = st.selectbox("Select Algorithm for Detailed Metrics:", ["FIFO", "LRU", "Optimal"])

if st.button("Run Advanced Simulation", key="run_advanced_simulation_button"):
    # Convert input string to list of integers
    pages = list(map(int, page_string.split(',')))
    
    # Run simulation for the selected algorithm for detailed metrics
    if algorithm == "FIFO":
        faults, steps, hit_miss, exec_time, response_times, mem_util = fifo_page_replacement(pages, capacity)
    elif algorithm == "LRU":
        faults, steps, hit_miss, exec_time, response_times, mem_util = lru_page_replacement(pages, capacity)
    else:
        faults, steps, hit_miss, exec_time, response_times, mem_util = optimal_page_replacement(pages, capacity)
    
    hit_rate = ((len(pages) - faults) / len(pages)) * 100
    fault_rate = (faults / len(pages)) * 100
    avg_response_time = np.mean(response_times) * 1000  # in milliseconds
    
    # Display Results
    st.subheader("Simulation Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Page Faults", faults)
    with col2:
        st.metric("Page Hit Rate", f"{hit_rate:.2f}%")
    with col3:
        st.metric("Page Miss Rate", f"{fault_rate:.2f}%")
    
    # -------------------------
    # Independent Animation Plots for All Algorithms
    # -------------------------
    st.subheader("Algorithm Performance Animations")
    # Create three columns for independent figures
    col_fifo, col_lru, col_opt = st.columns(3)
    
    # FIFO Animation
    with col_fifo:
        fig_fifo, faults_fifo, hit_miss_fifo, exec_time_fifo, response_times_fifo, mem_util_fifo = create_algorithm_animation("FIFO", pages, capacity)
        st.plotly_chart(fig_fifo, use_container_width=True)
    
    # LRU Animation
    with col_lru:
        fig_lru, faults_lru, hit_miss_lru, exec_time_lru, response_times_lru, mem_util_lru = create_algorithm_animation("LRU", pages, capacity)
        st.plotly_chart(fig_lru, use_container_width=True)
    
    # Optimal Animation
    with col_opt:
        fig_opt, faults_opt, hit_miss_opt, exec_time_opt, response_times_opt, mem_util_opt = create_algorithm_animation("Optimal", pages, capacity)
        st.plotly_chart(fig_opt, use_container_width=True)
    
    # Detailed Metrics Table for the selected algorithm
    metrics_df = pd.DataFrame([
        {
            "Algorithm": algorithm, 
            "Page Faults": faults, 
            "Hit Rate": f"{hit_rate:.2f}%", 
            "Fault Rate": f"{fault_rate:.2f}%", 
            #"Memory Utilization": f"{mem_util:.2f}%", 
            "Execution Time": f"{exec_time:.6f} s",
            "Avg Response Time": f"{avg_response_time:.4f} ms"
        }
    ])
    
    st.dataframe(metrics_df)
    
    st.download_button(
        "Download as CSV", 
        metrics_df.to_csv(index=False), 
        "page_replacement_results.csv", 
        "text/csv"
    )
    
    # Algorithm Concepts Explanation
    st.markdown(generate_concepts_explanation(algorithm, pages, capacity, faults), unsafe_allow_html=True)
