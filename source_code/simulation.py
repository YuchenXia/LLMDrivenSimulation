import base64
from io import BytesIO
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches


matplotlib.use('Agg')

class ContainerBallSimulation:
    def __init__(self, size=(10, 10)):
        self.size = size
        self.container_state = np.zeros(size, dtype=int)  # Initialize container with zeros
        self.colors = {0: 'white', 1: 'yellow', 2: 'red', 3: 'blue'}  # Colors for each weight
        self.step_log = []
        self.step_counter = 0

    def use_example(self, example_num):
        self.container_state = np.zeros(self.size, dtype=int)  # Reset container state

        # Mapping of examples to their configurations
        example_rows = {
            1: [(0, 4, 1), (4, 7, 2), (7, 10, 3)],
            2: [(0, 3, 1), (3, 6, 2), (6, 7, 1), (7, 10, 3)],
            3: [(0, 4, 1), (4, 6, 3), (6, 9, 2), (9, 10, 3)],
            4: [(0, 3, 1), (3, 5, 3), (5, 8, 2), (8, 9, 1), (9, 10, 3)],
            5: [(0, 10, 0)]
        }

        rows = example_rows.get(example_num, [])
        for start, end, weight in rows:
            self.container_state[start:end, :] = weight

    def draw_ball(self, ax, center, radius, color):
        """Draws a single ball on the ax."""
        circle = patches.Circle(center, radius, color=color, fill=True)
        ax.add_patch(circle)

    def visualize_container(self):
        """Visualizes the container with balls."""
        fig, ax = plt.subplots(figsize=(6, 6))
        offset = 0.5  # Offset to center the balls in the grid

        # Iterate through the container and draw the balls
        for i, row in enumerate(np.flipud(self.container_state.copy())):
            for j, weight in enumerate(row):

                center = (j + offset, self.size[0] - i - offset)
                self.draw_ball(ax, center, offset, self.colors[weight])

        ax.set_xlim(0, self.size[1])
        ax.set_ylim(0, self.size[0])
        ax.set_aspect('equal')
        ax.axis('off')  # Turn off the axes
        plt.show()

    def visualize_container_to_base64(self):
        fig, ax = plt.subplots(figsize=(6, 6))
        offset = 0.5  # Offset to center the balls in the grid

        # Iterate through the container and draw the balls
        for i, row in enumerate(np.flipud(self.container_state.copy())):
            for j, weight in enumerate(row):
                center = (j + offset, self.size[0] - i - offset)
                self.draw_ball(ax, center, offset, self.colors[weight])

        # Adding an arrow to indicate the direction of gravity
        ax.annotate('', xy=(self.size[1] + 1, self.size[0] / 2 - 1), xytext=(self.size[1] + 1, self.size[0] / 2 + 1),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))
        ax.text(self.size[1] + 1.5, self.size[0] / 2, 'Gravity', verticalalignment='center', fontsize=12)

        # Draw a border around the balls
        ax.add_patch(patches.Rectangle((0, 0), self.size[1], self.size[0], linewidth=2, edgecolor='black', facecolor='none'))

        # Set the axes limits
        ax.set_xlim(-1, self.size[1] + 2)
        ax.set_ylim(-1, self.size[0] + 1)

        ax.set_aspect('equal')
        plt.axis('off')


        # Convert plot to a PNG byte array
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        # Encode PNG image to base64 string
        base64_string = base64.b64encode(buf.getvalue()).decode('utf-8')
        return base64_string

    def add_balls(self, row_num, weight):
        """Add balls of a specific weight to the container, filling from the top."""
        added = 0
        row_num = int(row_num)
        for row in range(self.size[0]):
            if added >= row_num * self.size[1]:  # Stop after adding the specified number of rows
                break
            for col in range(self.size[1]):
                if self.container_state[row, col] == 0:  # Find the first empty spot
                    self.container_state[row, col] = weight
                    added += 1
                    if added >= row_num * self.size[1]:  # Stop after filling the required rows
                        break
        self.step_counter += 1
        step = {
            "step": self.step_counter,
            "action": "add_balls",
            "parameters": {
                "row_number": row_num,
                "unit_of_weight": weight
            },
            "container_state": self.get_container_state().tolist(),
            "mixing_index": self.calculate_mixing_index(self.get_container_state()),
            "delta_mixing_index": self.calculate_mixing_index(self.get_container_state()) - self.step_log[-1]["mixing_index"] if len(self.step_log) > 0 else self.calculate_mixing_index(self.get_container_state())
        }
        self.step_log.append(step)
        # print(self.get_step_log())


    def shake(self, shake_times):
        """Shake the container to potentially rearrange balls based on their weights."""
        for _ in range(shake_times):
            for row in range(1, self.size[0]):  # Start from the top row
                for col in range(self.size[1]):
                    # Ensure both current and the cell above are not empty and compare weights
                    if (self.container_state[row, col] > 0 and
                            self.container_state[row - 1, col] > 0 and
                            self.container_state[row, col] > self.container_state[row - 1, col]):
                        # Calculate the probability of a lighter ball switching with a heavier one
                        weight_light = self.container_state[row - 1, col]
                        weight_heavy = self.container_state[row, col]
                        probability = 1 - (weight_light / weight_heavy)

                        # Use the calculated probability to determine if a switch should occur
                        if np.random.random() < probability:
                            # Switch the positions of the two balls
                            self.container_state[row, col], self.container_state[row - 1, col] = self.container_state[row - 1, col], self.container_state[row, col]
        self.step_counter += 1
        step = {
            "step": self.step_counter,
            "action": "shake",
            "parameters": {
                "shake_times": shake_times
            },
            "container_state": self.get_container_state().tolist(),
            "mixing_index": self.calculate_mixing_index(self.get_container_state()),
            "delta_mixing_index": self.calculate_mixing_index(self.get_container_state()) - self.step_log[-1]["mixing_index"] if len(self.step_log) > 0 else self.calculate_mixing_index(self.get_container_state())
        }
        self.step_log.append(step)
        # print(self.get_step_log())

    def stop(self):
        """Stop the simulation."""
        self.step_counter += 1
        step = {
            "step": self.step_counter,
            "action": "stop",
            "parameters": {},
            "container_state": self.get_container_state().tolist(),
            "mixing_index": self.calculate_mixing_index(self.get_container_state()),
            "delta_mixing_index": self.calculate_mixing_index(self.get_container_state()) - self.step_log[-1]["mixing_index"] if len(self.step_log) > 0 else self.calculate_mixing_index(self.get_container_state())
        }
        self.step_log.append(step)
        # print(self.get_step_log())

    def execute_steps(self, steps):
        """Execute a series of steps that add balls and shake the container."""
        for row_num, weight, shake_times in steps:
            self.add_balls(row_num, weight)
            if shake_times:
                self.shake(shake_times)
        return self.container_state

    def get_container_state(self):
        """Return the current state of the container."""
        return np.flipud(self.container_state.copy())

    def get_container_state_in_text(self):
        """Return the current state of the container in text format."""
        modified_string = ' ' + str(np.flipud(self.container_state.copy()))[1:-1]
        rows = modified_string.strip().split('\n')
        formatted_rows = [f"row {10 - i}: {row.strip()}" for i, row in enumerate(rows)]
        formatted_string = '\n'.join(formatted_rows)
        return formatted_string

    def get_step_log(self):
        """Return the actions log."""
        return self.step_log

    def calculate_mixing_index(self,matrix):
        """Calculate the homogeneity of the mixture in the container."""
        # Initialize the count
        diversity_count = 0

        # Loop through each element in the matrix
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                current = matrix[i, j]
                # Initialize the count for local diversity
                local_diversity = 0
                # Check the 8 surrounding elements
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        # Make sure we don't go out of bounds
                        if 0 <= i + di < matrix.shape[0] and 0 <= j + dj < matrix.shape[1]:
                            # Check if the neighbor is different and not the element itself
                            if matrix[i + di, j + dj] != current and matrix[i + di, j + dj] != 0 and not (di == 0 and dj == 0):
                                local_diversity += 1
                # Accumulate the average diversity for this element
                diversity_count += local_diversity / 8.0  # The maximum number of different neighbors is 8

        # Calculate the overall average diversity
        average_diversity = diversity_count / (matrix.shape[0] * matrix.shape[1])

        # Normalize the mixing degree to a 0-1 range (considering the maximum diversity is for 3 different elements)
        normalized_mixing_index = average_diversity / 3

        return normalized_mixing_index


if __name__ == "__main__":
    sim = ContainerBallSimulation()

    sim.add_balls(2, 1)
    sim.add_balls(3, 2)
    sim.add_balls(2, 1)
    sim.add_balls(3, 3)
    print(sim.get_container_state())
    sim.shake(1)
    print(sim.get_container_state())
    sim.visualize_container()

