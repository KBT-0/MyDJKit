"""Read-only Rekordbox access: playlists with BPM/key per track."""
import urllib.request
from pathlib import Path
from pyrekordbox.__main__ import KEY_SOURCES
from sqlcipher3 import dbapi2 as sql
def connect():
    key=None
    for s in KEY_SOURCES:
        try:
            m=s['regex'].match(urllib.request.urlopen(s['url'],timeout=20).read().decode())
            if m:key=m.group('dp');break
        except Exception:continue
    assert key
    p=Path.home()/'Library/Pioneer/rekordbox/master.db'
    db=sql.connect(f'file:{p}?mode=ro',uri=True);db.execute("PRAGMA key='"+key.replace("'","''")+"'");db.row_factory=sql.Row
    return db
Q="SELECT c.ID,c.Title,c.FolderPath,c.BPM,c.Length,k.ScaleName KeyName,a.Name ArtistName FROM djmdContent c LEFT JOIN djmdKey k ON c.KeyID=k.ID LEFT JOIN djmdArtist a ON c.ArtistID=a.ID"
def playlist(db,pid):
    return [dict(r) for r in db.execute(Q+" JOIN djmdSongPlaylist s ON s.ContentID=c.ID WHERE s.PlaylistID=? AND s.rb_local_deleted=0 ORDER BY s.TrackNo",(pid,))]
