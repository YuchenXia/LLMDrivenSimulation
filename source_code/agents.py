from llm import gpt_model_call
import json

class SimpleDecisionAgent:
    def __init__(self):
        self.prompt_template = """You are a ball mixing machine operator. This machine mixes three types of balls—heavy, normal, and light—within a container. All balls are identical in size but differ in weight. The mixing process takes place in a two-dimensional container designed as a 10x10 matrix, allowing for 10 rows of 10 balls each.

Types of Balls:
- Heavy Ball: Weight of 3 units.
- Normal Ball: Weight of 2 units.
- Light Ball: Weight of 1 unit.

Container Specifications:
- The container is structured into a 10x10 matrix, accommodating up to 100 balls in 10 rows, with each row holding 10 balls.
- The container is filled from the bottom row to the top row.
- The container is represented as a 10x10 matrix, with each cell containing a number representing the weight of the ball in that position.
- '0' indicates an empty cell.
- '1' indicates a light ball.
- '2' indicates a normal ball.
- '3' indicates a heavy ball.
- Initially, the container is empty, and the container state has the following format:
row 10: [0 0 0 0 0 0 0 0 0 0]
row 9: [0 0 0 0 0 0 0 0 0 0]
row 8: [0 0 0 0 0 0 0 0 0 0]
row 7: [0 0 0 0 0 0 0 0 0 0]
row 6: [0 0 0 0 0 0 0 0 0 0]
row 5: [0 0 0 0 0 0 0 0 0 0]
row 4: [0 0 0 0 0 0 0 0 0 0]
row 3: [0 0 0 0 0 0 0 0 0 0]
row 2: [0 0 0 0 0 0 0 0 0 0]
row 1: [0 0 0 0 0 0 0 0 0 0]



Actions:
(1) Adding Balls:
- You can add one or more rows of balls, but exclusively of one type during each action.
- You can only add 1 row or 2 rows of balls in each action.
- You can perform the add action in this format: {"action": "add_balls", "parameters":{"row_number": "", "unit_of_weight": ""}}, row_number is an integer between 1 and 10, and unit_of_weight is an integer between 1 and 3.

(2) Shaking the Container:
- After each shake, gravity may cause heavier balls to switch positions with lighter balls immediately below them.
- The shaking action helps to mix the balls of different weights.
- You can perform the shake action in this format: {"action": "shake", "parameters":{}}.

(3) Stop:
- You terminate the process if the distribution of balls is well mixed and the container has 10 rows of balls.
- You can perform the stop action in this format: {"action": "stop", "parameters":{}}.

Objective:
The goal is to mix the balls of different weights by strategically adding rows and utilizing the shaking action to achieve a homogenous distribution of all types of balls within the container.
In total, you need add 4 rows of light balls, 3 rows of normal balls, and 3 rows of heavy balls to complete the process. The container must be filled with exactly 10 rows of balls by the end of the process.

You will receive the input of the current container state and need to provide an action to perform as action in output.
For example:
Input:
// 10 rows of balls with their weight number representing the current state of the container, the bottom row is at the bottom of the matrix.
Output:
{"action": "", "parameters": {}} //You should decide an action in JSON format.

You should now finish the output:
Input:
{{input_text}}
Output:"""


    def generate_output(self, input_text, model):
        self.prompt = self.prompt_template.replace("{{input_text}}", input_text)
        # print(input_text)
        print("***********************")
        print("Simple GPT Working")
        print("***********************")
        try:
            text_output = gpt_model_call(self.prompt, model=model)
        except Exception as e:
            print(f"Error: {e}")

            return None

        try:
            # Parse the text output into a JSON object
            result_json = json.loads(text_output)
        except json.JSONDecodeError as json_err:
            print(f"JSON Decode Error: {json_err}")
            return None

        # Write the JSON data to a file
        with open('simple_decision_agent.json', 'w') as file:
            json.dump(result_json, file, indent=4)
        print("Result:\n")
        print(text_output)
        return result_json


class SituationAnalysisAgent:
    def __init__(self):
        self.prompt_template = """You are a ball mixing machine operator. This machine mixes three types of balls—heavy, normal, and light—within a container. All balls are identical in size but differ in weight. The mixing process takes place in a two-dimensional container designed as a 10x10 matrix, allowing for 10 rows of 10 balls each.

Types of Balls:
- Heavy Ball: Weight of 3 units.
- Normal Ball: Weight of 2 units.
- Light Ball: Weight of 1 unit.

Container Specifications:
- The container is structured into a 10x10 matrix, accommodating up to 100 balls in 10 rows, with each row holding 10 balls.
- The container is filled from the bottom row to the top row.
- The container is represented as a 10x10 matrix, with each cell containing a number representing the weight of the ball in that position.
- '0' indicates an empty cell.
- '1' indicates a light ball.
- '2' indicates a normal ball.
- '3' indicates a heavy ball.
- Initially, the container is empty, and the container state has the following format:
row 10: [0 0 0 0 0 0 0 0 0 0]
row 9: [0 0 0 0 0 0 0 0 0 0]
row 8: [0 0 0 0 0 0 0 0 0 0]
row 7: [0 0 0 0 0 0 0 0 0 0]
row 6: [0 0 0 0 0 0 0 0 0 0]
row 5: [0 0 0 0 0 0 0 0 0 0]
row 4: [0 0 0 0 0 0 0 0 0 0]
row 3: [0 0 0 0 0 0 0 0 0 0]
row 2: [0 0 0 0 0 0 0 0 0 0]
row 1: [0 0 0 0 0 0 0 0 0 0]


Actions:
(1) Adding Balls:
- You can add one or more rows of balls, but exclusively of one type during each action.
- You can only add 1 row or 2 rows of balls in each action.
- You can perform the add action in this format: {"action": "add_balls", "parameters":{"row_number": "", "unit_of_weight": ""}}, row_number is an integer between 1 and 10, and unit_of_weight is an integer between 1 and 3.

(2) Shaking the Container:
- After each shake, gravity may cause heavier balls to switch positions with lighter balls immediately below them.
- The shaking action helps to mix the balls of different weights.
- You can perform the shake action in this format: {"action": "shake", "parameters":{}}.

(3) Stop:
- You terminate the process if the distribution of balls is well mixed and the container has 10 rows of balls.
- You can perform the stop action in this format: {"action": "stop", "parameters":{}}.

Objective:
The goal is to mix the balls of 3 different weights by strategically adding rows and utilizing the shaking action to achieve a homogenous distribution of all types of balls within the container.
In total, you need add 4 rows of light balls, 3 rows of normal balls, and 3 rows of heavy balls to complete the process. The container must be filled with exactly 10 rows of balls by the end of the process.

You will receive the input of the current container state and please concisely describe the current situation in terms of:
- The current state of the container.
- The number of rows filled and how many more rows are required to complete the process.
- Describing the 2-dimensional distribution of the different types of balls in the container.
- Make an conclusion about whether the types of the balls are well mixed or not.
- Highlight one important aspects of the current situation to achieve the objective described above.

For example, you provide the summarized description in this format after you receive the input:
Input:
// 10 rows of balls with their weight number representing the current state of the container, the bottom row is at the bottom of the matrix.
Output:
// Your summarized description of the current situation within 60 words.

You should now finish the output:
Input:
{{input_text}}
Output:"""


    def generate_output(self, input_text, model):
        self.prompt = self.prompt_template.replace("{{input_text}}", input_text)
        print("***********************")
        print("Analysis Agent Working")
        print("***********************")

        try:
            text_output = gpt_model_call(self.prompt, model=model)
        except Exception as e:
            print(f"Error: {e}")

            return None
        print("Result:\n")
        print(text_output)
        return text_output


class DecisionAgent:
    """the output of the decision agent is a JSON object that contains the action to be taken"""
    def __init__(self, agent_objective):
        self.agent_objective = agent_objective
        self.prompt_template = """You are a ball mixing machine operator. This machine mixes three types of balls—heavy, normal, and light—within a container. All balls are identical in size but differ in weight. The mixing process takes place in a two-dimensional container designed as a 10x10 matrix, allowing for 10 rows of 10 balls each.

Types of Balls:
- Heavy Ball: Weight of 3 units.
- Normal Ball: Weight of 2 units.
- Light Ball: Weight of 1 unit.

Container Specifications:
- The container is structured into a 10x10 matrix, accommodating up to 100 balls in 10 rows, with each row holding 10 balls.
- The container is filled from the bottom row to the top row.
- The container is represented as a 10x10 matrix, with each cell containing a number representing the weight of the ball in that position.
- '0' indicates an empty cell.
- '1' indicates a light ball.
- '2' indicates a normal ball.
- '3' indicates a heavy ball.
- Initially, the container is empty, and the container state has the following format:
row 10: [0 0 0 0 0 0 0 0 0 0]
row 9: [0 0 0 0 0 0 0 0 0 0]
row 8: [0 0 0 0 0 0 0 0 0 0]
row 7: [0 0 0 0 0 0 0 0 0 0]
row 6: [0 0 0 0 0 0 0 0 0 0]
row 5: [0 0 0 0 0 0 0 0 0 0]
row 4: [0 0 0 0 0 0 0 0 0 0]
row 3: [0 0 0 0 0 0 0 0 0 0]
row 2: [0 0 0 0 0 0 0 0 0 0]
row 1: [0 0 0 0 0 0 0 0 0 0]


Actions:
(1) Adding Balls:
- You can add one or more rows of balls, but exclusively of one type during each action.
- The container must be filled with exactly 10 rows of balls by the end of the process.
- You can only add 1 row or 2 rows of balls in each action.
- You can perform the add action in this format: {"action": "add_balls", "parameters":{"row_number": "", "unit_of_weight": ""}}, row_number is an integer between 1 and 10, and unit_of_weight is an integer between 1 and 3.

(2) Shaking the Container:
- After each shake, gravity may cause heavier balls to switch positions with lighter balls immediately below them.
- The shaking action helps to mix the balls of different weights.
- You can perform the shake action in this format: {"action": "shake", "parameters":{}}.

(3) Stop:
- You terminate the process if the distribution of balls is well mixed and the container has 10 rows of balls.
- You can perform the stop action in this format: {"action": "stop", "parameters":{}}.

Objective:
{{agent_objective}}

You shall pay attention to the following insights: {{analysis_insights}}

For example, you provide the output in this format after you receive the input:
Input:
// 10 rows of balls with their weight number representing the current state of the container, the bottom row is at the bottom of the matrix.
Output:
{"reason_for_an_action": "", "action": "", "parameters": {}} //You should decide an action in JSON format.

You should now finish the output, and only generate 1 action:
Input:
The container state is:
{{input_text}}
Output:"""

    def generate_output(self, input_text, analysis_insights, model):
        self.prompt = self.prompt_template.replace("{{input_text}}", input_text)
        self.prompt = self.prompt.replace("{{agent_objective}}", self.agent_objective)
        self.prompt = self.prompt.replace("{{analysis_insights}}", analysis_insights)
        print("***********************")
        print("Decision Agent Working")
        print("***********************")
        print("Input Decision Agent:\n")
        print("***********************")
        print(self.prompt)

        try:
            text_output = gpt_model_call(self.prompt, model=model)
        except Exception as e:
            print(f"Error: {e}")
            return None

        try:
            # Parse the text output into a JSON object
            result_json = json.loads(text_output)
        except json.JSONDecodeError as json_err:
            print(f"JSON Decode Error: {json_err}")
            return None

        # Write the JSON data to a file
        with open('decision.json', 'w') as file:
            json.dump(result_json, file, indent=4)
        print("Result:\n")
        print("***********************")
        print(text_output)
        return result_json


class ObservationAnalysisAgentWithTool:
    """the output of the observation analysis agent is a summarized observation of the current situation"""
    def __init__(self, agent_objective):
        self.agent_objective = agent_objective
        self.prompt_template = """You are a ball mixing machine operator. This machine mixes three types of balls—heavy, normal, and light—within a container. All balls are identical in size but differ in weight. The mixing process takes place in a two-dimensional container designed as a 10x10 matrix, allowing for 10 rows of 10 balls each.

Types of Balls:
- Heavy Ball: Weight of 3 units.
- Normal Ball: Weight of 2 units.
- Light Ball: Weight of 1 unit.

Container Specifications:
- The container is structured into a 10x10 matrix, accommodating up to 100 balls in 10 rows, with each row holding 10 balls.
- The container is filled from the bottom row to the top row.
- The container is represented as a 10x10 matrix, with each cell containing a number representing the weight of the ball in that position.
- '0' indicates an empty cell.
- '1' indicates a light ball.
- '2' indicates a normal ball.
- '3' indicates a heavy ball.
- Initially, the container is empty, and the container state has the following format:
row 10: [0 0 0 0 0 0 0 0 0 0]
row 9: [0 0 0 0 0 0 0 0 0 0]
row 8: [0 0 0 0 0 0 0 0 0 0]
row 7: [0 0 0 0 0 0 0 0 0 0]
row 6: [0 0 0 0 0 0 0 0 0 0]
row 5: [0 0 0 0 0 0 0 0 0 0]
row 4: [0 0 0 0 0 0 0 0 0 0]
row 3: [0 0 0 0 0 0 0 0 0 0]
row 2: [0 0 0 0 0 0 0 0 0 0]
row 1: [0 0 0 0 0 0 0 0 0 0]


Actions:
(1) Adding Balls:
- You can add one or more rows of balls, but exclusively of one type during each action.
- You can only add 1 row or 2 rows of balls in each action.
- You can perform the add action in this format: {"action": "add_balls", "parameters":{"row_number": "", "unit_of_weight": ""}}, row_number is an integer between 1 and 10, and unit_of_weight is an integer between 1 and 3.

(2) Shaking the Container:
- After each shake, gravity may cause heavier balls to switch positions with lighter balls immediately below them.
- The shaking action helps to mix the balls of different weights.
- You can perform the shake action in this format: {"action": "shake", "parameters":{}}.

(3) Stop:
- You terminate the process if the distribution of balls is well mixed and the container has 10 rows of balls.
- You can perform the stop action in this format: {"action": "stop", "parameters":{}}.

Objective:
{{agent_objective}}

You will receive the input of the current container state and please concisely describe the current situation within one sentence in terms of:
- The current state of the container.
- The number of rows filled and how many more rows of different types of balls are required to complete the process.
- Describe the 2-dimensional distribution of the different types of balls in the container.
- A mixing index is an indicator about how evenly distributed are the different types of balls. Review the change of the mixing index after the last shake action, and if the mixing index has been changed into negative value, stop.
- Highlight one important aspects of the current situation to achieve the objective described above.

For example, you provide the summarized description in this format after you receive the input:
Input:
// 10 rows of balls with their weight number representing the current state of the container, the bottom row is at the bottom of the matrix.
// The change of mixing index after the last shake action.
Output:
{"container_state": "", "rows_filled": "", "number_of_rows_required": {"light_ball": "", "normal_ball": "", "heavy_ball": ""}, "distribution": "", "change_of_mixing_index": "", "important_aspect": ""}

You should now finish the output:
Input:
The container state is: {{input_text}}
The change of mixing index after the last shake action is: {{delta_mixing_index}}
Output:"""


    def generate_output(self, input_text, delta_mixing_index, model):
        self.prompt = self.prompt_template.replace("{{agent_objective}}", self.agent_objective)
        self.prompt = self.prompt.replace("{{input_text}}", input_text)
        self.prompt = self.prompt.replace("{{delta_mixing_index}}", delta_mixing_index)
        print("\n\n***********************")
        print("Observation Agent Working (Using Tool)")
        print("***********************")
        print("Input Observation Agent:\n")
        print("***********************")
        print(self.prompt)
        try:
            text_output = gpt_model_call(self.prompt, model=model)

        except Exception as e:
            print(f"Error: {e}")

            return None
        print("Result:\n")
        print("***********************")
        print(text_output)
        return text_output



class LogSummarizationAgent:
    def __init__(self, agent_objective):
        self.agent_objective = agent_objective
        self.prompt_template = """You are a ball mixing machine operator. This machine mixes three types of balls—heavy, normal, and light—within a container. All balls are identical in size but differ in weight. The mixing process takes place in a two-dimensional container designed as a 10x10 matrix, allowing for 10 rows of 10 balls each.

Types of Balls:
- Heavy Ball: Weight of 3 units.
- Normal Ball: Weight of 2 units.
- Light Ball: Weight of 1 unit.

Container Specifications:
- The container is structured into a 10x10 matrix, accommodating up to 100 balls in 10 rows, with each row holding 10 balls.
- The container is filled from the bottom row to the top row.
- The container is represented as a 10x10 matrix, with each cell containing a number representing the weight of the ball in that position.
- '0' indicates an empty cell.
- '1' indicates a light ball.
- '2' indicates a normal ball.
- '3' indicates a heavy ball.
- Initially, the container is empty, and the container state has the following format:
row 10: [0 0 0 0 0 0 0 0 0 0]
row 9: [0 0 0 0 0 0 0 0 0 0]
row 8: [0 0 0 0 0 0 0 0 0 0]
row 7: [0 0 0 0 0 0 0 0 0 0]
row 6: [0 0 0 0 0 0 0 0 0 0]
row 5: [0 0 0 0 0 0 0 0 0 0]
row 4: [0 0 0 0 0 0 0 0 0 0]
row 3: [0 0 0 0 0 0 0 0 0 0]
row 2: [0 0 0 0 0 0 0 0 0 0]
row 1: [0 0 0 0 0 0 0 0 0 0]



Actions:
(1) Adding Balls:
- You can add one or more rows of balls, but exclusively of one type during each action.
- You can only add 1 row or 2 rows of balls in each action.
- You can perform the add action in this format: {"action": "add_balls", "parameters":{"row_number": "", "unit_of_weight": ""}}, row_number is an integer between 1 and 10, and unit_of_weight is an integer between 1 and 3.

(2) Shaking the Container:
- After each shake, gravity may cause heavier balls to switch positions with lighter balls immediately below them.
- The shaking action helps to mix the balls of different weights.
- You can perform the shake action in this format: {"action": "shake", "parameters":{}}.

(3) Stop:
- You terminate the process if the distribution of balls is well mixed and the container has 10 rows of balls.
- You can perform the stop action in this format: {"action": "stop", "parameters":{}}.

Objective:
{{agent_objective}}


You operated the machine and now need to summarize the actions taken during the mixing process concisely for each step. The detailed log of the actions taken by you during the mixing process, including the following information:
{{input_text}}

Now, please provide a summary of the actions taken in the log in a text report, summarizing each step with its main reason concisely within 8 words, in the following form:
{
    "step_summary": [
        {
            "step": ,
            "action": "",
            "summary": ""
            "change_of_mixing_index": ""
        }
        ...
    ]}
"""


    def generate_output(self,input_text, model):
        self.prompt = self.prompt_template.replace("{{input_text}}", str(input_text))
        self.prompt = self.prompt.replace("{{agent_objective}}", self.agent_objective)
        print("***********************")
        print("Summarization Agent Working")
        print("***********************")
        print("Input Summarization Agent:\n")
        print("***********************")
        print(self.prompt)
        try:
            text_output = gpt_model_call(self.prompt, model=model)
        except Exception as e:
            print(f"Error: {e}")

            return None
        print("Result:\n")
        print("***********************")
        print(text_output)
        return text_output
