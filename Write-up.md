STT-LLM-TTS Pipeline:



**Voice Activity Detection (VAD)**

Silero VAD is used to detect when the customer starts and stops speaking. This improves conversational turn-taking and allows the system to detect inactivity and silence. This prevents the agent wasting money on silence, this also helps the agent understand when the user is interupting



**Speech-to-Text (STT)**

The customer’s voice input is streamed through LiveKit audio tracks and sent to AssemblyAI’s streaming speech recognition service. The STT engine continuously converts the user’s speech into text in real time.



**Large Language Model (LLM)**

The transcribed text is passed to OpenAI GPT-4.1 Mini, which acts as the conversational reasoning engine. The LLM identifies the user’s intent (billing, recharge, internet issue, etc.), maintains conversation context, and generates appropriate telecom support responses.



**Text-to-Speech (TTS)**

The generated response is then sent to Cartesia Sonic-3 for speech synthesis. The TTS engine converts the AI-generated response into natural-sounding audio and streams it back to the customer through the LiveKit room.



VAD --> STT --> LLM --> TTS --> VAD



Handling LiveKit room events:



The participant joining and leaving are handled by attaching listeners to the room object. Using the participant\_connected and participant\_disconnected events we can determine participant join/leave.



The track subscriptions are handled using the track\_subscribed and track\_unsubscribed events. They provide information about when a user subscribed and unsubscribed an audio track.



Improvements for going into production:



&#x20;- Adding an MCP to the tool set so that the llm has access to information about the company and can give context-oriented responses.

&#x20;- Escalating the issues to a human if needed.

&#x20;- Using opentelemetry for better analytics and error tracing.

&#x20;- Sending a transcript of the conversation to the user. 



