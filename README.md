# AI Bash One-liner Generator

AI Bash One-liner Generator is a web application that uses OpenAI's GPT-4 AI model and Langchain Libraries to transform requests in any language into Bash one-liner commands for Linux systems. It also provides a risk assessment, ranking the potential harm the command could cause.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Screenshots](#screenshots)
4. [Contributing](#contributing)
5. [License](#license)

## Installation

To set up the AI Bash One-liner Generator, follow these steps:

1. Clone the repository:


2. Install the required packages:

pip install -r requirements.txt

3. Run the web application:

python app.py

4. Open your web browser and navigate to `http://localhost:9922`.

## Usage

1. Enter your request in the input field, for example: "Find the 3 largest files in /tmp and archive them".
2. Press the "Submit" button.
3. Review the generated Bash one-liner command and the associated harm potential.
4. Use the generated command with caution, always review it for accuracy and potential risks before executing it on your system.

## Screenshots

![screenshot1](https://github.com/jasona7/ai_bash_oneliner_generator/blob/main/screenshots/screenshot1.png?raw=true)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](./LICENSE)
