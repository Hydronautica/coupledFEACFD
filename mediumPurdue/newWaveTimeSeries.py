import re
import numpy as np
import matplotlib.pyplot as plt

def parse_wave_data(content):
    # Regular expressions to find all instances of data
    amplitude_regex = r'amplitude\s+nonuniform List<scalar>\s+\d+\s+\((.*?)\);'
    frequency_regex = r'frequency\s+nonuniform List<scalar>\s+\d+\s+\((.*?)\);'
    phase_regex = r'phaselag\s+nonuniform List<scalar>\s+\d+\s+\((.*?)\);'
    wavenumber_regex = r'waveNumber\s+nonuniform List<vector>\s+\d+\s+\((.*?)\);'

    # Finding all matches
    amplitude_matches = re.findall(amplitude_regex, content, re.DOTALL)
    frequency_matches = re.findall(frequency_regex, content, re.DOTALL)
    phase_matches = re.findall(phase_regex, content, re.DOTALL)
    wavenumber_matches = re.findall(wavenumber_regex, content, re.DOTALL)

    # Function to parse individual matches
    def parse_match(match):
        return np.array(list(map(float, match.split())))

    # Parsing each match
    amplitudes = [parse_match(match) for match in amplitude_matches]
    frequencies = [parse_match(match) for match in frequency_matches]
    phases = [parse_match(match) for match in phase_matches]
    wavenumbers = [np.array([float(w.split()[0].strip('(')) for w in match.split(')')[:-1]]) for match in wavenumber_matches]

    return amplitudes, frequencies, phases, wavenumbers
def flatten_data(data):
    """Flatten a list of arrays into a single array."""
    return np.concatenate(data)

def calculate_wave_elevation(amplitudes, frequencies, phases, wavenumbers, time, x=None):
    if x is not None:
        # Calculate wave elevation for a spatial snapshot at a specific time
        wave_elevation = np.zeros(len(x))
        for a, f, p, k in zip(amplitudes, frequencies, phases, wavenumbers):
            wave_elevation += a * np.cos(2 * np.pi * f * time + p - k * x)
        return wave_elevation
    else:
        # Calculate wave elevation over time (original functionality)
        wave_elevation = np.zeros_like(time)
        for a, f, p in zip(amplitudes, frequencies, phases):
            wave_elevation += a * np.cos(2 * np.pi * f * time + p)
        return wave_elevation


def reconstruct_wave_elevation(frequencies, real_parts, imag_parts, time):
    reconstructed_wave = np.zeros_like(time)
    for f, cr, ci in zip(frequencies, real_parts, imag_parts):
        reconstructed_wave += cr * np.cos(2 * np.pi * f * time) - ci * np.sin(2 * np.pi * f * time)
    return reconstructed_wave
def save_wave_elevation_to_file(wave_elevation, time, file_name='wave_elevation.txt'):
    # Calculate time step and round to the third decimal place
    dt = round(time[1] - time[0], 3)

    # Write data to file
    with open(file_name, 'w') as file:
        file.write("# An externally specified irregular wave time series for OW3D\n")
        file.write(f"{dt:.3e}  <- dt\n")

        for zeta in wave_elevation:
            file.write(f"{zeta:.16e}\n")

    print(f"Wave elevation data saved to {file_name}")

def main():
    # Read and parse waveProperties
    with open('constant/waveProperties', 'r') as file:
        content = file.read()
    amplitudes, frequencies, phases, wavenumbers = parse_wave_data(content)

    # Generate wave elevation time series from original values
    time = np.linspace(-100, 100, 4000)  # Example time array
     # Flatten the data
    flat_amplitudes = flatten_data(amplitudes)
    flat_frequencies = flatten_data(frequencies)
    flat_phases = flatten_data(phases)
    flat_wavenumbers = flatten_data(wavenumbers)

    # Define spatial coordinates
    x_max = 200  # maximum x-coordinate
    x = np.linspace(-x_max, x_max, 1000)  # spatial points to evaluate the wave
    original_wave_elevation = calculate_wave_elevation(flat_amplitudes, flat_frequencies, flat_phases, flat_wavenumbers,time)
    # Specific time for the spatial snapshot
    specific_time = 5  # or any other specific time of interest
    specific_wave_elevation = calculate_wave_elevation(flat_amplitudes,  flat_frequencies, flat_phases, flat_wavenumbers, specific_time, x)
    # Plotting the original time series wave elevation
    plt.figure(figsize=(12, 6))
    plt.plot(time, original_wave_elevation, label='Original Wave Elevation')
    plt.xlabel('Time (s)')
    plt.ylabel('Wave Elevation (m)')
    plt.title('Temporal Wave Elevation Time Series')
    plt.legend()
    plt.show()

    # Plotting the spatial snapshot
    plt.figure(figsize=(12, 6))
    plt.plot(x, specific_wave_elevation, label=f'Wave Elevation at t = {specific_time}s')
    plt.xlabel('Spatial Coordinate x (m)')
    plt.show()


if __name__ == "__main__":
    main()

