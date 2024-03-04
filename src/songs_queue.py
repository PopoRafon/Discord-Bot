from typing import Any
import discord, requests, re, yt_dlp


class SongsQueue:
    def __init__(self) -> None:
        self.__queue: list[dict[str, str]] = []
        self.__current_song: dict[str, str] = {}
        self.__repeat: bool = False
        self.__ydl_opts: dict[str, str] = {
            'format': 'bestaudio/best',
            'ignoreerrors': True,
            'abort_on_unavailable_fragments': True
        }

    def __extract_song(self, track: str) -> dict[str, Any]:
        """
        Extracts song from given track name or url.
        Returns info about that song.
        """
        if track.startswith('https://www.youtube.com/watch?v='):
            url: str = track
        else:
            response: requests.Response = requests.get(f'https://youtube.com/results?search_query={track}')
            content: str = response.content.decode()
            videos: list[str] = re.findall(r'/watch\?v=([\w-]*)', content)
            url: str = videos[0]

        with yt_dlp.YoutubeDL(self.__ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    def __extract_playlist(self, playlist: str) -> dict[str, Any]:
        """
        Extracts all songs from given playlist url.
        Returns info about that playlist.
        """
        with yt_dlp.YoutubeDL(self.__ydl_opts) as ydl:
            return ydl.extract_info(playlist, download=False)

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

    def add(self, track: str) -> str:
        """
        Adds song from given track url or title to queue.
        Returns this song title.
        """
        if re.match(r'(https:\/\/w{3}\.|w{3}\.|)youtube.com/.*list=', track):
            playlist: dict[str, Any] = self.__extract_playlist(track)

            for song in playlist['entries']:
                self.__queue.append({'title': song['title'], 'url': song['url']})

            return playlist['title']
        else:
            song: dict[str, Any] = self.__extract_song(track)
            self.__queue.append({'title': song['title'], 'url': song['url']})

            return song['title']

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

    def insert(self, track: str, index: int) -> str:
        """
        Inserts song into queue at provided index from given track name or url.
        Returns this song title.
        """
        if re.match(r'(https:\/\/w{3}\.|w{3}\.|)youtube.com/.*list=', track):
            playlist: dict[str, Any] = self.__extract_playlist(track)

            for song in playlist['entries'][::-1]:
                self.__queue.insert(index, {'title': song['title'], 'url': song['url']})

            return playlist['title']
        else:
            song: dict[str, Any] = self.__extract_song(track)
            self.__queue.insert(index, {'title': song['title'], 'url': song['url']})

            return song['title']

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
