from flask import Flask, render_template, request, send_from_directory, jsonify
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMBashChain
from langchain.llms import OpenAI
from collections import deque

app = Flask(__name__)
llm = OpenAI(temperature=0)

_PROMPT_TEMPLATE = """If someone asks you to perform a task, your job is to come up with a one-liner bash command that will perform the task. Make sure to supress any output except the actual command and a number that ranks the 'harm_level' indicating how much harm the command can cause, with 1 being the least harm, and 5 being the most harm, using this format:
Question: "copy the files in the directory named 'target' into a new directory at the same level as target called 'myNewDirectory'"
I need to take the following actions:
- List all files in the directory
- Create a new directory
- Copy the files from the first directory into the second directory
```bash
ls
mkdir myNewDirectory
cp -r target/* myNewDirectory
Do not use 'echo' when writing the script.
Determine how harmful a command is on a scale of 1-5, with 1 being the least harmful and 5 being the most harmful, save the result in 'harm_level'

That is the format. Begin!
Important: Do not use the 'echo' command in your answer.
Question: {question}
Please only provide the answer in the following format:

your_one_liner_command_here # harm_level
"""

PROMPT = PromptTemplate(input_variables=["question"], template=_PROMPT_TEMPLATE)
bash_chain = LLMBashChain(llm=llm, prompt=PROMPT, verbose=True)


recent_requests = deque(maxlen=5)  # Change maxlen to the number of recent results you want to store

def extract_harm_level(result):
    if "#" in result:
        try:
            harm_level = int(result.split("#")[-1].strip())
            command = result.rsplit("#", 1)[0].strip()
            return command, harm_level
        except ValueError:
            pass
    return result, None


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error_message = None
    question = None
    harm_level = None
    command_history = []

    if request.method == "POST":
        question = request.form["question"]

        try:
            #result = bash_chain.run(question)
            #result = bash_chain.run(question)
            #harm_level = extract_harm_level(result)
            result = bash_chain.run(question)
            result, harm_level = extract_harm_level(result)

            print(harm_level)
            #command_history.insert(0, result)
            command_history.insert(0, {"question": question, "result": result, "harm_level": harm_level})
            if len(command_history) > 5:
                command_history.pop()
            #recent_requests.appendleft({"question": question, "result": result})
            recent_requests.appendleft({"question": question, "result": result, "harm_level": harm_level})
        except ValueError as e:
            error_message = str(e)
            if error_message.startswith("unknown format from LLM"):
                result = error_message.split("LLM: ")[1]
                error_message = None
            else:
                result = None

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            #return jsonify(question=question, result=result, error_message=error_message)
            return jsonify(question=question, result=result, harm_level=harm_level, error_message=error_message)

    return render_template("index.html", result=result, error_message=error_message, recent_requests=recent_requests, command_history=command_history)

@app.route('/static/oneliner.png>')
def serve_image(filename):
    return send_from_directory('static', filename, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9922, debug=True)
