import py_compile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = sorted(ROOT.glob("s[0-9][0-9]_*"))


def test_every_chapter_keeps_only_the_chinese_readme() -> None:
    assert len(CHAPTERS) == 17

    for chapter in CHAPTERS:
        readme = chapter / "README.zh.md"
        assert readme.is_file()
        assert not (chapter / "README.md").exists()
        assert not (chapter / "README.ja.md").exists()
        assert not (chapter / "README.en.md").exists()
        text = readme.read_text(encoding="utf-8")
        assert "[English](README.md)" not in text
        assert "README.ja.md" not in text
        assert not list((chapter / "images").glob("*.en.svg"))
        assert not list((chapter / "images").glob("*.ja.svg"))


def test_every_chapter_script_compiles_on_python_311() -> None:
    for chapter in CHAPTERS:
        _ = py_compile.compile(str(chapter / "code.py"), doraise=True)
