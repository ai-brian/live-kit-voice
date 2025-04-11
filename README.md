# live-kit-sip

### What is this?
This a is an exploration of using [LiveKit](https://github.com/livekit/livekit) and [LiveKit SIP](https://github.com/livekit/sip) to bring SIP audio into Distyl Voice Server.

main.py - is a scratch pad of implementation that would be added into Voice Server. 
See the comments in the code for reference. 

LiveKit provides a lot of abrstraction to interfacing with models, including OAI realtime-api. I don't think we want that as it would change much of what we currently do with Voice Server. main.py removes some of that abstraction. 

### Demo setup
We can setup a demo environment using Twilio SIP trunks and LiveKit Cloud to host the LiveKit services. We have a Twilio number (888-901-9823) configured to point to a LiveKit cloud project and we can easily run this locally or deployed to our infrastructure.

### Installation
1. create an .env file with:

    LIVEKIT_API_KEY=(ask Brian)
    LIVEKIT_API_SECRET=(ask Brian)
    LIVEKIT_URL=wss://voice-dm3jqtxb.livekit.cloud
    OPENAI_AIP_KEY=(your key)
2. run `python main.py dev` this will connect to the LiveKit cloud server and create an agent. The pseudo code in there now won't run but can be played with
3. Call 888-901-9823

### Why LiveKit?

 - It's modern, well documented, developer friendly, and works. Other Python SIP libraries are old, not well documented and extremely hard to configure
 - It should be easy to deploy. The LiveKit and SIP servers are containerized and need no development. All the code to interface with the service can be done in Python within Voice Server


