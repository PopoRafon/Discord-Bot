import discord, requests, re, yt_dlp

class SongsQueue:
    def __init__(self) -> None:
        self._queue: list[dict[str, str]] = []
        self._ydl_opts = {'format': 'bestaudio/best'}

    def play(self, voice_client: discord.VoiceClient) -> None:
        if len(self._queue) >= 1:
            song = self._queue.pop(0)
            before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            voice_client.play(discord.FFmpegPCMAudio(song['url'], before_options=before_options), after=lambda x: self.play(voice_client))

    def add(self, url: str) -> str:
        response = requests.get(f'https://youtube.com/results?search_query={url}')
        content = response.content.decode()
        videos = re.findall(r'/watch[?]v=([0-9a-zA-Z-_]*)', content)

        with yt_dlp.YoutubeDL(self._ydl_opts) as ydl:
            info = ydl.extract_info(videos[0], download=False)
            self._queue.append({'title': info['title'], 'url': info['url']})
            return info['title']

    def remove(self, song: dict[str, str]) -> dict[str, str]:
        return self._queue.remove(song)

    def get(self) -> list[dict[str, str]]:
        return self._queue

    def clear(self) -> None:
        self._queue.clear()
