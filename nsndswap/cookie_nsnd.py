#!/usr/bin/env python3
# nsndswap/cookie_nsnd.py
# copyright 2017 ViKomprenas, 2-clause BSD license (LICENSE.md)

# Okay, a quick overview of how cookie's nsnd is structured:
# The first row is a header, which Word (wtf cookie) neglects to mark,
# so we'll just skip it automatically. Then, the next row is the first song!
# First cell in the row is the track number, skip that. Then the title,
# then the musician and album artist, then the references. If there is more than
# one row to the same song, we need to skip the first _four_ slots rather than
# Lambda's _one_ slot. We can safely ignore the <span>s and <b>s and <i>s
# scattered everywhere, but we _do_ need to watch for cell end tags, unlike
# in Lambda's. That's because occasionally Word decides to split one contiguous
# phrase into two (or more!) separate data regions, probably an artifact of the
# formatting being applied badly. Anyway, that's... relatively straightforward.

# Addendum 2017-05-30: Not all albums have art. Shit.

import html.parser
import enum
import nsndswap.util


@enum.unique
class ParseStates(enum.Enum):
    SEEKING_ALBUM = enum.auto()
    READING_ALBUM_HEADER = enum.auto()
    SEEKING_SONG = enum.auto()
    SKIPPING_TRACK_NUM = enum.auto()
    EATING_TITLE = enum.auto()
    SKIPPING_ARTIST = enum.auto()
    SKIPPING_ALBUM_ARTIST = enum.auto()
    SEEKING_REFERENCE = enum.auto()
    EATING_REFERENCE = enum.auto()
    RESUMING = enum.auto()
    SKIPPING_BLANK_TITLE_IN_RESUME = enum.auto()
    DONE = enum.auto()


@enum.unique
class Benchmarks(enum.IntEnum):
    NONE = 0
    PARTWAY_THROUGH_CANV5 = 1  # there are two tracks ON THE SAME DAMN ALBUM WITH THE SAME DAMN NAME
    IN_THE_BEGINNING = 2
    GAMESCANTE = 3


class CookieParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.state = ParseStates.SEEKING_ALBUM
        self.active_song = None
        self.all_songs = []
        self.got_new_this_round = False
        self.benchmark = Benchmarks.NONE
        self.current_album_has_art = False

    def _finish_song(self):
        if self.active_song is not None:
            if self.active_song.title != "":
                self.active_song.title = self._check_benchmarks(self.active_song.title.strip())
                print(f'Finished "{self.active_song.title}"')
                self.all_songs.append(self.active_song)
                self.active_song = None

    def _check_benchmarks(self, title, *, is_ref=False, update_benchmark=True):
        val = self._check_benchmarks_inner(title, is_ref=is_ref, update_benchmark=update_benchmark)
        if val != title:
            print(f'[W] Disambiguated "{title}" to "{val}"')
        return val

    def _check_benchmarks_inner(self, title, *, is_ref=False, update_benchmark=True):
        # Check
        title = title.replace('\n', '').replace('  ', ' ')
        if title == 'Moondoctor':
            if self.benchmark < Benchmarks.PARTWAY_THROUGH_CANV5:
                return 'Moondoctor (Difarem)'
            else:
                return 'Moondoctor (Shwan)'
        elif title == 'Showup':
            if self.benchmark < Benchmarks.IN_THE_BEGINNING:
                return 'Showup (loading)'
            else:
                return 'Showup (Viridian)'
        elif title == 'Three in the Morning (4 1/3 Hours Late Remix)':
            if self.benchmark < Benchmarks.PARTWAY_THROUGH_CANV5:
                return 'Three in the Morning (4 1/3 Hours Late Remix) (voulem. 1)'
            else:
                return 'Three in the Morning (4 1/3 Hours Late Remix) (Greatest Hits)'
        elif title == 'Fake Fruit Fiesta':
            if self.benchmark < Benchmarks.PARTWAY_THROUGH_CANV5:
                return 'Fake Fruit Fiesta (Volume 2)'
            else:
                return 'Fake Fruit Fiesta (Greatest Hits)'
        elif title == 'Ruses':
            if self.benchmark < Benchmarks.IN_THE_BEGINNING:
                return 'Ruses (CANWC Sound Test)'
            else:
                return 'Ruses (Median)'
        elif title == 'Downwards':
            if self.benchmark < Benchmarks.GAMESCANTE:
                return 'Downwards (9)'
            else:
                return 'Downwards (Greatest Hits 2)'
        elif title == 'Midnight':
            if self.benchmark < Benchmarks.GAMESCANTE:
                return 'Midnight (Intermishin)'
            else:
                return 'Midnight (Greatest Hits 2)'
        elif title.strip().replace('  ', ' ') == 'Meme Voyage':
            if self.benchmark < Benchmarks.GAMESCANTE:
                return 'Meme Voyage (vol. s*x)'
            else:
                return 'Meme Voyage (Greatest Hits 2)'
        elif title == 'Vegetal Colina':
            if self.benchmark < Benchmarks.GAMESCANTE:
                return 'Vegetal Colina (CANH2)'
            else:
                return 'Vegetal Colina (Greatest Hits 2)'
        elif title == 'Enter with Caliborn: Destruction Adventure':
            if self.benchmark < Benchmarks.GAMESCANTE:
                return 'Enter with Caliborn: Destruction Adventure (CANH2)'
            else:
                return 'Enter with Caliborn: Destruction Adventure (Greatest Hits 2)'
        elif title == '“Libera me” from Bowman' or title == '"Libera me" from Bowman':
            if self.benchmark < Benchmarks.GAMESCANTE:
                return '"Libera me" from Bowman (Bowmania)'
            else:
                return '"Libera me" from Bowman (Greatest Hits 2)'
        elif title == 'Fighting Spirit ~Double Ascended Form~':
            if self.benchmark < Benchmarks.GAMESCANTE:
                return 'Fighting Spirit ~Double Ascended Form~ (vol. 8)'
            else:
                return 'Fighting Spirit ~Double Ascended Form~ (Greatest Hits 2)'
        elif title == '1 Through 15':
            if self.benchmark < Benchmarks.GAMESCANTE:
                return '1 Through 15 (Intermishin)'
            else:
                return '1 Throgh 15 (Greatest Hits 2)'
        elif title == '72.0x SHOWDOWN COMBO':
            if self.benchmark < Benchmarks.GAMESCANTE:
                return '72.0x SHOWDOWN COMBO (CANH2)'
            else:
                return '72.0x SHOWDOWN COMBO (Greatest Hits 2)'
        elif title == 'Welcome to Flavortown (Battle Against a Bodacious Foe)':
            if self.benchmark < Benchmarks.GAMESCANTE:
                return 'Welcome to Flavortown (locomotif)'
            else:
                return 'Welcome to Flavortown (Greatest Hits 2)'
        elif title == 'you have got to be SHITTONG me (temp title)':
            if self.benchmark < Benchmarks.GAMESCANTE:
                return 'you have got to be SHITTONG me (9)'
            else:
                return 'you have got to be SHITTONG me (Greatest Hits 2)'
        elif title == 'Meldey':
            if self.benchmark < Benchmarks.GAMESCANTE:
                return 'Meldey (Basement Tale)'
            else:
                return 'Meldey (Rain)'
        elif title == 'Sunset':
            # two here and one in makin_nsnd
            if self.benchmark < Benchmarks.GAMESCANTE:
                return 'Sunset (CANWC)'
            else:
                return 'Sunset (Cerulean)'
        elif title == '==>':
            # There's one of these in makin_nsnd and one here
            return '==> (CANWC)'
        elif title == 'Checkmate' and not is_ref:
            # as above
            return 'Checkmate (CANWC)'
        elif title == 'Light':
            # as above
            return 'Light (CANWC)'
        elif title == 'Sunrise':
            # as above
            return 'Sunrise (CANWC)'
        elif title == 'Strife Mayhem':
            # as above
            return 'Strife Mayhem (CANWC)'
        elif title == 'Explored':
            # as above
            return 'Explored (CANWC)'
        elif title == 'Anticipation':
            # as above
            return 'Anticipation (CANWC)'
        elif title == 'Rain':
            # as above
            return 'Rain (CANWC)'
        elif title == 'Starsetter':
            # as above
            return 'Starsetter (CANWC)'
        elif title == 'Fanfare':
            # HA HA HA HA HA HA HA
            return 'Showtime (Imp Strife Mix)'
        elif title == 'Roundabout':
            # goddammit yaz I hope nobody references your song
            return 'Roundabout (yazshu)'

        # Update
        if update_benchmark:
            if title == 'Dogtor (get it?)' and self.benchmark < Benchmarks.PARTWAY_THROUGH_CANV5:
                print('Reached benchmark: PARTWAY_THROUGH_CANV5')
                self.benchmark = Benchmarks.PARTWAY_THROUGH_CANV5
            elif title == 'In the Beginning' and self.benchmark < Benchmarks.IN_THE_BEGINNING:
                print('Reached benchmark: IN_THE_BEGINNING')
                self.benchmark = Benchmarks.IN_THE_BEGINNING
            elif title == 'Gamescante' and self.benchmark < Benchmarks.GAMESCANTE:
                print('Reached benchmark: GAMESCANTE')
                self.benchmark = Benchmarks.GAMESCANTE

        return title

    def handle_starttag(self, tag, attrs):
        if self.state == ParseStates.DONE:
            return
        attrs = nsndswap.util.split_attrs(attrs)
        if self.state == ParseStates.SEEKING_ALBUM and tag == "tr":
            self.state = ParseStates.READING_ALBUM_HEADER
        elif self.state == ParseStates.SEEKING_SONG and tag == "tr" and 'class' in attrs.keys() and 'no-sep' in attrs['class']:
            self.state = ParseStates.RESUMING
        elif self.state != ParseStates.READING_ALBUM_HEADER and tag == "td":
            self.state = {
                ParseStates.SEEKING_SONG: ParseStates.SKIPPING_TRACK_NUM,
                ParseStates.SKIPPING_TRACK_NUM: ParseStates.EATING_TITLE,
                ParseStates.EATING_TITLE: ParseStates.SKIPPING_ARTIST,
                ParseStates.RESUMING: ParseStates.SKIPPING_BLANK_TITLE_IN_RESUME,
                ParseStates.SKIPPING_BLANK_TITLE_IN_RESUME: ParseStates.SKIPPING_ARTIST,
                ParseStates.SKIPPING_ARTIST: ParseStates.SKIPPING_ALBUM_ARTIST if self.current_album_has_art else ParseStates.SEEKING_REFERENCE,
                ParseStates.SKIPPING_ALBUM_ARTIST: ParseStates.SEEKING_REFERENCE,
                ParseStates.SEEKING_REFERENCE: ParseStates.EATING_REFERENCE,
                ParseStates.EATING_REFERENCE: ParseStates.EATING_REFERENCE,
            }[self.state]
            if self.state in (ParseStates.EATING_TITLE, ParseStates.SKIPPING_TRACK_NUM):  # ???
                self._finish_song()
                self.active_song = nsndswap.util.Track("")

    def handle_endtag(self, tag):
        if self.state == ParseStates.DONE:
            return
        if self.state in (ParseStates.READING_ALBUM_HEADER, ParseStates.SEEKING_REFERENCE) and tag == "tr":
            self.state = ParseStates.SEEKING_SONG
        elif tag == "td":
            if self.state == ParseStates.EATING_REFERENCE:
                self.state = ParseStates.SEEKING_REFERENCE
                if len(self.active_song.references) > 0 and self.active_song.references[-1] != "":
                    print(f'Got a reference from "{self.active_song.title}" to "{self.active_song.references[-1]}"')
                self.got_new_this_round = False
            elif self.state == ParseStates.EATING_TITLE:
                self.state = ParseStates.SKIPPING_ARTIST
                if self.active_song.title == "":
                    self.active_song = self.all_songs.pop()
                    print(f'Resuming "{self.active_song.title}"')
                else:
                    print(f'Scanning "{self.active_song.title}"')
        elif tag == "table":
            self.current_album_has_art = False
            if self.state != ParseStates.SEEKING_REFERENCE:
                print(f'[W] Reached unexpected end of album in state {self.state}')
                self._finish_song()
                self.state = ParseStates.SEEKING_ALBUM

    def handle_data(self, data):
        if self.state == ParseStates.DONE:
            return
        if data == 'Non-Homestuck music (Homestuck and CANWC musicians only)':
            print('Ending cookie_nsnd at non-homestuck section')
            self.state = ParseStates.DONE
        elif self.state == ParseStates.READING_ALBUM_HEADER and data.strip().startswith('T'):
            print('Noticed that this album has art')
            self.current_album_has_art = True
        elif self.state == ParseStates.READING_ALBUM_HEADER and data.strip().startswith('Album'):
            print('Noticed that this has an album column, pretending it\'s art')
            self.current_album_has_art = True
        elif self.state == ParseStates.EATING_TITLE:
            self.active_song.title += data
        elif self.state == ParseStates.EATING_REFERENCE:
            assert self.active_song.title != ""
            if len(self.active_song.references) is 0 or not self.got_new_this_round:
                self.active_song.references.append("")
                self.got_new_this_round = True
            self.active_song.references[-1] += data


def parse(nsnd):
    parser = CookieParser()
    parser.feed(nsnd)
    return parser.all_songs
