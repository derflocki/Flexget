from tests import FlexGetBase
import os
import shutil
class TestOutputNfo(FlexGetBase):
    __yaml__ = """
        presets:
          global:
            make_nfo: "{{movedone}}/{{content_filename}}.nfo"
            thetvdb_lookup: yes
            imdb_lookup: yes
            tmdb_lookup: yes
        tasks:
          movies:
            mock: 
              - {title: 'Taken[2008]DvDrip[Eng]-FOO', imdb_url: 'http://www.imdb.com/title/tt0936501/'}
            set:
              content_filename: "{{ imdb_name }} ({{imdb_year}})"
              movedone: "/tmp/make_nfo/Movies"
            accept_all: yes
          shows:
            mock:
              - {title: 'House.S01E02.HDTV.XViD-FlexGet'}
              - {title: 'Doctor.Who.2005.S02E03.PDTV.XViD-FlexGet'}
            set:
              content_filename: "{{ series_name }} - {{ series_id|replace('S0','')|replace('E','x') }} - {{ tvdb_ep_name|default('',True)|replace('/','-') }}" 
              movedone: "/tmp/make_nfo/Shows/{{series_name|title}}/{{series_name|title}} Season {{series_season}}"
            accept_all: yes
            all_series:
              upgrade: yes
    """

    def test_shows(self):
        self.execute_task('shows')
        for entry in self.task.entries:
            nfo = entry.get('nfo_outfile')
            print nfo
            assert os.path.exists(nfo), 'nfo present'
            os.remove(nfo)
        shutil.rmtree('/tmp/make_nfo')
    def test_movies(self):
        self.execute_task('movies')
        #self.execute_task('shows')
        for entry in self.task.entries:
            nfo = entry.get('nfo_outfile')
            print nfo
            assert os.path.exists(nfo), 'nfo present'
            os.remove(nfo)
        shutil.rmtree('/tmp/make_nfo')
