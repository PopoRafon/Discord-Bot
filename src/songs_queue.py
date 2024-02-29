from typing import Any
import discord, requests, re, yt_dlp


class SongsQueue:
    def __init__(self) -> None:
        self.__queue: list[dict[str, str]] = []
        self.__ydl_opts: dict[str, str] = {'format': 'bestaudio/best'}
        self.__current_song: dict[str, str] = {}
        self.__repeat: bool = False

    def __extract_song(self, url: str) -> dict[str, Any]:
        """
        Extracts song from given url and returns info about that song.
        """
        response: requests.Response = requests.get(f'https://youtube.com/results?search_query={url}')
        content: str = response.content.decode()
        videos: list[str] = re.findall(r'/watch[?]v=([0-9a-zA-Z-_]*)', content)

        with yt_dlp.YoutubeDL(self.__ydl_opts) as ydl:
            return ydl.extract_info(videos[0], download=False)

    def play(self, voice_client: discord.VoiceClient) -> None:
        """
        Starts playing songs from queue one after another until queue is empty.
        """
        before_options: str = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"

        if self.__repeat and self.__current_song:
            voice_client.play(discord.FFmpegPCMAudio(self.__current_song['url'], before_options=before_options), after=lambda x: self.play(voice_client))
            return

        self.__current_song = {}

        if len(self.__queue) >= 1:
            self.__current_song = self.__queue.pop(0)

            voice_client.play(discord.FFmpegPCMAudio(self.__current_song['url'], before_options=before_options), after=lambda x: self.play(voice_client))

    def add(self, url: str) -> str | None:
        """
        Adds song from given url to queue.
        Returns `None` if song can't be added otherwise returns this song title.
        """
        song: dict[str, Any] = self.__extract_song(url)
        title: str = song.get('title')
        url: str = song.get('url')

        if url and title:
            self.__queue.append({'title': title, 'url': url})

            return title
        else:
            return None

    def move(self, from_index: int, to_index: int) -> None:
        """
        Swaps places of two songs from queue at given indexes.
        """
        self.__queue[from_index], self.__queue[to_index] = self.__queue[to_index], self.__queue[from_index]

    def remove(self, title: str) -> dict[str, str] | None:
        """
        Removes song from queue based on given song title.
        Returns `None` if song can't be found otherwise returns this song.
        """
        for song in self.__queue:
            if song['title'] == title:
                self.__queue.remove(song)
                return song

        return None

    def insert(self, url: str, index: int) -> str | None:
        """
        Inserts song into queue at provided index from given url.
        Returns `None` if song can't be inserted otherwise returns this song title.
        """
        song: dict[str, Any] = self.__extract_song(url)
        title: str = song.get('title')
        url: str = song.get('url')

        if url and title:
            self.__queue.insert(index, {'title': title, 'url': url})

            return title
        else:
            return None

    def get_queue(self) -> list[dict[str, str]]:
        """
        Gets and returns song queue.
        """
        return self.__queue

    def get_current_song(self) -> dict[str, str]:
        """
        Gets and returns current song.
        """
        return self.__current_song

    def clear(self) -> None:
        """
        Removes all songs from queue.
        """
        self.__queue.clear()

    def is_repeat_enabled(self) -> bool:
        """
        Returns if repeat is enabled or disabled.
        """
        return self.__repeat

    def set_repeat(self, repeat: bool) -> None:
        """
        Sets repeat.
        """
        self.__repeat = repeat
