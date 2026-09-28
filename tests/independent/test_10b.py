import sqlite3
import pytest

def test_backup_restores_data_to_new_database(assignment,tmp_path):
    source=tmp_path/'source.db';target=tmp_path/'restored.db'
    with sqlite3.connect(source) as db:
        db.execute('CREATE TABLE records(cents INTEGER)');db.executemany('INSERT INTO records VALUES(?)',[(10,),(25,)])
    assert tuple(assignment.restore_copy(source,target))==(2,35)
    with sqlite3.connect(target) as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert db.execute('SELECT cents FROM records ORDER BY cents').fetchall()==[(10,),(25,)]

def test_existing_restore_destination_is_preserved(assignment,tmp_path):
    existing=tmp_path/'keep.db';existing.write_bytes(b'do not overwrite')
    with pytest.raises(FileExistsError):assignment.restore_copy(tmp_path/'source.db',existing)
    assert existing.read_bytes()==b'do not overwrite'
