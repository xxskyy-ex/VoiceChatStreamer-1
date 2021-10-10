# Voice Chat Streamer
_Userbot untuk memutar vidio maupun lagu

![GitHub Repo stars](https://img.shields.io/github/stars/Rifkiarisman/VoiceChatStreamer?color=green&logo=github)
![GitHub forks](https://img.shields.io/github/forks/Rifkiarisman/VoiceChatStreamer?color=green&logo=github)

_🎯 Follow me and star this repo for more telegram bots._

## 📌 Features
- Play youtube live streams.
- Radio playing.
- Play videos from youtube in audio and video formats
- Play via youtube search
- Telegram video/audio playing
- Admin control

## 📌 Deployment
- Deploy to **Heroku**

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Rifkiarisman/VoiceChatStreamer-1)


<details>
  <summary>How to get <code>API_ID</code> and <code>API_HASH</code></summary>
  Get <i>API_ID</i> and <i>API_HASH</i> from <a href="https://my.telegram.org/apps">here</a>. I think its easy.
</details>

<details>
  <summary>How to generate <code>SESSION</code>?</summary>
  <b>Step 1:</b> Go to <a href="https://replit.com/@AnjanaMadu/GenerateStringSession">here</a>.<br>
  <b>Step 2:</b> Click run button and wait.<br>
  <b>Step 3:</b> Not ask for option. Fill number 1.<br>
  <b>Step 4:</b> Now ask for API ID and API HASH. Fill them.<br>
  <b>Step 5:</b> Now ask for mobile fill it also.<br>
  <b>Final Step:</b> Now ask for confirmation. Fill it. TraLaa. Now check saved. String Session will be there.
</details>

### 🏷 Self Host

**For Linux (Ubuntu)**

- Updating package list and Install wget, git
  - `sudo apt-get update && sudo apt-get install wget git -y`
- Installing Docker
  - `wget https://get.docker.com -O get-docker.sh`
  - `sudo bash get-docker.sh`
  - `rm get-docker.sh`
- Cloning Repo and Go to dir
  - `git clone https://github.com/Rifkiarisman/VoiceChatStreamer bot`
  - `cd bot`
- _Now edit "config.py" with your values._
- Docker Build
  - `sudo docker build . -t vcstreamer`
- Start Bot
  - `sudo docker run vcstreamer`

