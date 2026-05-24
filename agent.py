import logging
import asyncio

from livekit import rtc
from dotenv import load_dotenv
from livekit import agents
from livekit.rtc import Room
from livekit.agents.beta.tools import EndCallTool
from livekit.agents import Agent, AgentServer, AgentSession, JobContext, room_io
from livekit.agents.voice.agent_session import UserStateChangedEvent, UserState
from livekit.plugins import noise_cancellation, silero
#from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv()


# Define your agent's behavior by extending the Agent class
class Assistant(Agent):
    def __init__(self, room: Room) -> None:
        super().__init__(
            instructions="""You are a telecom customer support voice agent from ABC Telecom.

Your responsibilities:
1. Speak polietly.
2. Ask the customer what they need help with.
3. Detect the customer's intent based on their response.
4. Respond with an appropriate scripted reply.
5. Try to solve the users problems. 
6. Answer only the queries related to the Telecom.

Example intents and responses(You can use your own intents and responses as well):

- Billing Issues:
  "I can help you with your bill. Can you tell me more about the problem?"

- Recharge / Top-up:
  "I can assist you with recharging your account. Are you looking for a prepaid plan or a top-up?"

- Technical / Internet Issues:
  "I am sorry you are experiencing issues. Let's troubleshoot your connection."

- Unknown Intent:
  "Could you please provide more details about the issue you are facing?"

If the customer says things like:
"bye", "thank you", "that's all", "goodbye", or indicates they want to end the call use the EndCallTool. Do not use this tool for any other reason.

""",
                tools=[EndCallTool(
                #extra_description="""end the call when the user says \"Bye, Goodbye, That's it thank you\" or other similar words. end the call if the user is inactive for 10 seconds.""",
                end_instructions="""end the call when the user says \"Bye, Goodbye, That's it thank you\" or other similar words. end the call if the user is inactive for 10 seconds.""",
                delete_room=False,
            )]  # System prompt for the LLM
        )
        self.room = room
        
    # @function_tool
    # async def end_call(self):
    #     """End the call gracefully."""
    #     logger.info("Ending call.")
    #     await self.room.disconnect()
    async def on_enter(self):
        await self.session.say(
            "Hi, thanks for calling ABC telecom support. how can i help you today?",
            allow_interruptions=False,
        )
    # async def on_user_away(self):
    #     await self.session.say("I could not hear anything for awhile. Ending the call now.",
    #     allow_interruptions=False,
    #     )
    #     await asyncio.sleep(2)
    #     await self.room.disconnect()
    # @session.on("user_state_changed")
    # async def on_user_state_changed(event: agent.UserstateChangedEvent):
    #     if event.new_state == UserState.AWAY:
    #         logging.info("User is away")
    #         await self.session.say("I could not hear anything for a while. Ending the call now.")
    #         self.session.close()

server = AgentServer()


# The entrypoint function runs when a participant joins the room
@server.rtc_session()
async def entrypoint(ctx: JobContext):
    await ctx.connect()
    logging.info(f"Connected to room:{ctx.room.name}")
    @ctx.room.on("track_subscribed")
    def on_track_subscribed(
        track: rtc.Track,
        publication: rtc.RemoteTrackPublication,
        participant: rtc.RemoteParticipant):

        if track.kind == rtc.TrackKind.KIND_AUDIO:
            logging.info(f"Audio Track Subscribed."
            f"User: {participant.identity}"
            f"Track ID: {publication.sid}")

    @ctx.room.on("track_unsubscribed")
    def on_track_unsubscribed(
        track: rtc.Track,
        publication: rtc.RemoteTrackPublication,
        participant: rtc.RemoteParticipant):

        if track.kind == rtc.TrackKind.KIND_AUDIO:
            logging.info(f"Audio Track Unsubscribed."
            f"User: {participant.identity}"
            f"Track ID: {publication.sid}")

    for identity, participant in ctx.room.remote_participants.items():
        for track_pub in participant.track_publications.values():
            if track_pub.subscribed and track_pub.kind == rtc.TrackKind.KIND_AUDIO:
                logger.info(
                    f" Existing Active Audio Track Found: "
                    f"User: {identity} | Track ID: {track_pub.sid}"
                )

    @ctx.room.on("participant_joined")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        print(f"Participant joined: {participant.identity}")
        logging.info(f"Participant joined: {participant.identity}")

    @ctx.room.on("participant_left")
    def on_participant_disconnected(participant: rtc.RemoteParticipant):
        print(f"Participant left: {participant.identity}")
        logging.info(f"Participant left: {participant.identity}")

    # Configure the voice pipeline with STT, LLM, TTS, and VAD providers
    session = AgentSession(
        stt="assemblyai/universal-streaming:en",  # Speech-to-text provider
        llm="openai/gpt-4.1-mini",                # Language model for responses
        tts="cartesia/sonic-3",                   # Text-to-speech voice
        vad=silero.VAD.load(),                    # Voice activity detection
        user_away_timeout = 10,                   # User inactivity
        #turn_handling=TurnHandlingOptions(user_away_timeout=10),
    )
    @session.on("user_state_changed")
    def on_user_state_changed(event: UserStateChangedEvent):
        if event.new_state == 'away':
            logging.info("User is away")
            async def handle_disconnect_async():
                await session.say("I could not hear anything for a while. Ending the call now.", allow_interruptions=False)
                session.shutdown()
            asyncio.create_task(handle_disconnect_async())
    # Start the session with noise cancellation enabled
    await session.start(
        agent=Assistant(ctx.room),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=noise_cancellation.BVC(),  # Background voice cancellation
            ),
        ),
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agents.cli.run_app(server)