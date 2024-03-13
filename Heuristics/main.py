import streamlit as st
import numpy as np
import time
import pandas as pd
from utils.ui import *
from utils.heurstics import neh_algorithm, ham_heuristic, cds_heuristic, gupta_heuristic, run_palmer, PRSKE, special_heuristic
from utils.benchmarks import benchmarks
from utils.utils import generate_gantt_chart
# Placeholder for your algorithm execution function
# This should return a 1D array, execution time, and an image path


def run_algorithm(algo, input_data):
    start_time = time.perf_counter()
    output_data, makespan = algo["algo"](input_data)
    end_time = time.perf_counter()
    execution_time_micros = (end_time - start_time) * 1e3

    image_path = generate_gantt_chart(input_data.T, output_data)
    # Placeholder image path
    return output_data, execution_time_micros, makespan, image_path


def generate_statistics(benchmark_data):
    stats = []
    for algorithm in algorithms:
        output_data, execution_time, makespan, _ = run_algorithm(
            algorithm, benchmark_data)
        stats.append({
            "Algorithm": algorithm['name'],
            "Execution Time (ms)": execution_time,
            "Makespan": makespan
        })
    return pd.DataFrame(stats)


# Define your algorithms names
algorithms = [
    {
        "name": "NEH",
        "algo":  neh_algorithm
    },
    {
        "name": "Ham Heuristic",
        "algo":  ham_heuristic
    },
    {
        "name": "CDS Heuristic",
        "algo":  cds_heuristic
    },
    {
        "name": "Gupta Heuristic",
        "algo":  gupta_heuristic
    },
    {
        "name": "Run Palmer",
        "algo":  run_palmer
    },
    {
        "name": "PRSKE",
        "algo":  PRSKE
    },
    {
        "name": "Weighted CDS",
        "algo": special_heuristic
    }


]

# List of benchmarks for demonstration
benchmarks_list = {f"Benchmark {i+1}": b for i, b in enumerate(benchmarks)}


def main():
    st.title("Algorithm Showcase")

    # Algorithm selection
    st.header("Select an Algorithm")
    cols = st.columns(3)
    selected_algorithm = st.session_state.get('selected_algorithm', None)
    for index, algorithm in enumerate(algorithms):
        name, model = algorithm['name'], algorithm['algo']
        with cols[index % 3]:
            if st.button(name, key=name, args=(name,)):
                selected_algorithm = algorithm
                st.session_state['selected_algorithm'] = algorithm

    if selected_algorithm:
        st.header(f"Configurations for {selected_algorithm['name']}")
        option = st.radio(
            "Input Method", ["Benchmark", "Manual", "Generate Random",])

        if option == "Manual":
            num_jobs = st.number_input(
                "Number of Jobs (lines)", min_value=1, value=5, key='man_jobs')
            num_machines = st.number_input(
                "Number of Machines (columns)", min_value=1, value=5, key='man_machines')

            # Generate manual input grid
            input_data = generate_manual_input_grid(num_jobs, num_machines)

        elif option == "Generate Random":
            num_jobs = st.number_input(
                "Number of Jobs (lines)", min_value=1, value=5, key='rand_jobs')
            num_machines = st.number_input(
                "Number of Machines (columns)", min_value=1, value=5, key='rand_machines')
            input_data = np.random.randint(
                1, 100, size=(num_jobs, num_machines))
            display_matrix(input_data)

        elif option == "Benchmark":
            benchmark_selection = st.selectbox(
                "Choose a Benchmark", list(benchmarks.keys()))
            input_data = benchmarks[benchmark_selection]
            display_matrix(input_data)

        if st.button("Run Algorithm"):
            output_data, execution_time, count, image_path = run_algorithm(
                selected_algorithm, input_data)

            st.subheader("Results")
            # Displaying the output matrix directly
            st.write("Output Matrix:")
            st.write(output_data)
            st.write(f"Execution Time: {execution_time:.2f} seconds")
            st.write(f"Count: {count}")
            st.image(image_path, caption="Output Image")

    if st.button("📊 Show General Statistics", help="Click to view general statistics about the algorithms"):
        # Generate the statistics matrix
        statistics_df = generate_statistics_matrix()

        st.subheader("General Statistics")
        st.table(statistics_df)


if __name__ == "__main__":
    main()
