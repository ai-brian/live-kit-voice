from dotenv import load_dotenv

import asyncio
from livekit import agents
from livekit import rtc
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    noise_cancellation,
)

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        # brian: instructions are a required field
        super().__init__(instructions="You are a helpful voice AI assistant.")


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()
    
    session = AgentSession(
        #brian: comment out the llm to make this a dumb agent so we can handle 
        # connecting, loading routines/tools, and handle messages
        
        #llm=openai.realtime.RealtimeModel(voice="ash"),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )
    # brian: code from https://docs.livekit.io/agents/build/media/#receiving-tracks
    # for getting the audio from the SIP Call
    @ctx.room.on("track_subscribed")
    def on_track_subscribed(
        track: rtc.Track,
        publication: rtc.TrackPublication,
        participant: rtc.RemoteParticipant,
    ):
        if track.kind == rtc.TrackKind.KIND_AUDIO:
            asyncio.create_task(handle_caller_audio(track))

    #await session.generate_reply(instructions="Greet the user and offer your assistance.")


async def handle_caller_audio(track: rtc.Track):
    if track.kind == rtc.TrackKind.KIND_AUDIO:
        audio_stream = rtc.AudioStream(track)
        async for event in audio_stream:
            # Do something here to process event.frame
            # The PCM audio bytes are already here so can be sent to openai as is
            frame = event.frame
            pcm_bytes = frame.data.tobytes()
            pass
        await audio_stream.aclose()


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
