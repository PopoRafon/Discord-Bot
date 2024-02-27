import discord, requests, re, yt_dlp


class SongsQueue:
    def __init__(self) -> None:
        self._queue: list[dict[str, str]] = []
        self._ydl_opts: dict[str, str] = {'format': 'bestaudio/best'}

    def play(self, voice_client: discord.VoiceClient) -> None:
        if len(self._queue) >= 1:
            song: dict[str, str] = self._queue.pop(0)
            before_options: str = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            voice_client.play(discord.FFmpegPCMAudio(song['url'], before_options=before_options), after=lambda x: self.play(voice_client))

    def add(self, url: str) -> str:
        response: requests.Response = requests.get(f'https://youtube.com/results?search_query={url}')
        content: str = response.content.decode()
        videos: list[str] = re.findall(r'/watch[?]v=([0-9a-zA-Z-_]*)', content)

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
