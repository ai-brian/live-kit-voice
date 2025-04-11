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
        super().__init__(instructions="You are a helpful voice AI assistant.")


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    # brian: 
    # code from: https://docs.livekit.io/agents/build/media/#publishing
    # to setup audio publishing from OpenAI 
    source = rtc.AudioSource(SAMPLE_RATE, NUM_CHANNELS)
    
    # brian: change this to rtc.RemoteAudioTrack? 
    track = rtc.LocalAudioTrack.create_audio_track("example-track", source)
    
    # since the agent is a participant, our audio I/O is its "microphone"
    # brian: ?????
    options = rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE)
    # ctx.agent is an alias for ctx.room.local_participant
    publication = await ctx.agent.publish_track(track, options)

    frequency = 440
    async def _sinewave():
        audio_frame = rtc.AudioFrame.create(SAMPLE_RATE, NUM_CHANNELS, SAMPLES_PER_CHANNEL)
        audio_data = np.frombuffer(audio_frame.data, dtype=np.int16)

        time = np.arange(SAMPLES_PER_CHANNEL) / SAMPLE_RATE
        total_samples = 0
        while True:
            time = (total_samples + np.arange(SAMPLES_PER_CHANNEL)) / SAMPLE_RATE
            sinewave = (AMPLITUDE * np.sin(2 * np.pi * frequency * time)).astype(np.int16)
            np.copyto(audio_data, sinewave)

            # send this frame to the track
            await source.capture_frame(frame)
            total_samples += samples_per_channel

    # end audio publishing
    
    session = AgentSession(
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
            # Decode the Opus to PCM here and send to OpenAI Realtime
            pass
        await audio_stream.aclose()


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
