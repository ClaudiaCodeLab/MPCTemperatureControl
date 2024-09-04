# Temperature Control with Model Predictive Control (MPC)

This project implements a Model Predictive Control (MPC) algorithm for temperature control in a simulated environment. It uses Streamlit to create an interactive web application that allows users to adjust parameters and visualize the control system's response.

## Features

- Interactive Streamlit web application
- Model Predictive Control (MPC) implementation for temperature regulation
- Visualization of room temperature, ambient temperature, and heating power over time

## Installation

Clone this repository:

  bash

      git clone https://github.com/yourusername/temperature-control-mpc.git
      cd temperature-control-mpc

Install the required packages:

  bash
  
      pip install -r requirements.txt


## Usage

Run the Streamlit app:

bash

    streamlit run src/temperature_control_mpc.py

Then, open your web browser and go to the URL displayed in the terminal (usually http://localhost:8501).

Use the sliders in the sidebar to adjust the current temperature and desired setpoint temperature. The graph will update in real-time to show the system's response.

##Dependencies

- streamlit
- numpy
- cvxpy
- matplotlib

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## How It Works
The Model Predictive Control (MPC) algorithm works as follows:


- It takes the current room temperature and desired setpoint as inputs.
- It predicts the system's behavior over a finite time horizon.
- It calculates the optimal control inputs to minimize the difference between the predicted temperature and the setpoint.
- It applies the first control input and repeats the process at the next time step.

The simulation also includes a varying ambient temperature to make the scenario more realistic.

## Future Improvements

Add more customizable parameters in the Streamlit interface
Implement different control strategies for comparison
Add unit tests to ensure reliability of the core functions

## Contact
If you have any questions or suggestions, please open an issue on this repository.
