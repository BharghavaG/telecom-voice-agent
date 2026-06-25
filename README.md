# Telecom Voice Support Agent

Telecom Voice Support Agent is an AI-powered real-time customer support voicebot built using LiveKit. The system is designed to handle telecom customer interactions such as billing queries, recharge assistance, internet troubleshooting, and general support through natural voice conversations.

The agent uses speech-to-text, large language models, and text-to-speech technologies to provide a seamless conversational support experience.

---

## Features

- **Real-Time Voice Conversations**: Supports live two-way voice communication with customers.
- **Intent Detection**: Identifies customer intents such as billing issues, recharge requests, and technical problems.
- **AI-Powered Responses**: Generates intelligent and context-aware support responses using LLMs.
- **Automatic Call Handling**:
  - Greets users when they join the room
  - Detects user inactivity
  - Ends calls gracefully when the conversation is complete
- **Voice Activity Detection (VAD)**: Uses Silero VAD to detect speech and silence.
- **Noise Cancellation**: Improves voice quality using background voice cancellation.
- **Room Event Handling**:
  - Detects participant join/leave events
  - Handles audio track subscriptions
- **End Call Tool Integration**: Automatically disconnects calls when users say goodbye or remain inactive.

---

## Technology Stack
- **Programming Language**: Python
- **Framework**: LiveKit Agents SDK
- **Speech-to-Text (STT)**: AssemblyAI Streaming API
- **Large Language Model (LLM)**: OpenAI GPT-4.1 Mini
- **Text-to-Speech (TTS)**: Cartesia Sonic-3
- **Voice Activity Detection**: Silero VAD
- **Noise Cancellation**: LiveKit BVC
- **Environment Management**: UV and dotenv

---

## Installation and Setup:
1. This project was built using uv package. Make sure you have uv package installed.
2. This project requires python version>=13. Not using the right verison can cause errors.
3. Clone the repository:
   ```bash
   https://github.com/BharghavaG/telecom-voice-agent.git
   ```
5. Initializing uv:
   ```bash
   uv init telecom-agent --bare
   ```
6. Install the required dependencies:
   ```bash
   uv add -r requirements.txt
   ```
7. Create a .env file and fill the details. You can find your API key after creating a free account on [Livekit](https://livekit.com). The API key is FREE. Create a new project.
8. Open the terminal venv and run the following command this will install required models:
   ```bash
   python -m livekit.agents download-files
   ```
9. After downloading run the following command to run the agent in the console:
   ```bash
   uv run agent.py console
   ```
10. If you want to see the list or change the input, output devices you use the following commands:
    ```bash
    uv run agent.py console --list-devices
    uv run agent.py console --input-device "device name or ID"
    uv run agent.py console --ouptut-device "device name or ID"
    ```
11. To deploy the model to the livekit cloud download the livekit cli:
- windows
    ```bash
    winget install LiveKit.LiveKitCLI
    ```
- MAC
  ```bash
  brew install livekit-cli
  ```
11. Authotize your livekit account from the cli and select the project:
    ```bash
    lk cloud auth
    ```
12. Deplot your agent using the following command:
    ```bash
    lk agent create
    ```
    Now you can view and test your model in the console.
13. To connect to a room other than the playground you can use [LivekitMeet](https://meet.livekit.io/) and select custom.
14. In the terminal use the following command to run the agent:
    ```bash
    uv run agent.py dev
    ```
15. To generate the token and the url needed use the following command:
    ```bash
    lk token create --join --room <room-name> --identity <user-name> --valid-for <duration>
    ```
16. Now you can interact with your agent. You can view the agent logs in your terminal and view analytics on the livekit console.
---

## Usage
- Start the voice agent.
- Join the LiveKit room from a client application.
- The agent greets the customer automatically.
- Customers can ask about:
  - Billing issues
  - Recharge plans
  - Internet problems
  - Technical support
- The agent responds conversationally using voice.
- Calls are automatically ended when:
  - The customer says goodbye or wants to cuts the call
  - The customer remains inactive for a configured timeout period

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments
- LiveKit for the real-time communication framework
- OpenAI for language models
- AssemblyAI for speech recognition
- Cartesia for speech synthesis

---

## If you like this project
Consider starring the repository to support the project.

---

## Contact
For any questions or suggestions, please open an issue or contact us at goudibharghava@gmail.com.
