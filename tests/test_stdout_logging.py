from pathlib import Path

import convert
from convert import Stats, TreeNode, _convert_archive, log_event, main


def test_log_event_emits_key_value_line(capsys):
    log_event("stage_start", stage="extract_shcntx", note="has spaces")
    out = capsys.readouterr().out.strip()
    assert out.startswith("[hbk-to-md] ")
    assert "event=stage_start" in out
    assert "stage=extract_shcntx" in out
    assert "note=has_spaces" in out


def test_convert_archive_emits_sparse_progress_and_final(monkeypatch, tmp_path: Path, capsys):
    extracted_dir = tmp_path / "in"
    extracted_dir.mkdir()
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    html_paths = [extracted_dir / f"p{i}.html" for i in range(3)]
    for path in html_paths:
        path.write_text("<html></html>", encoding="utf-8")

    monkeypatch.setattr(convert, "PROGRESS_EVERY", 2)
    monkeypatch.setattr(convert, "iter_html", lambda _dir: html_paths)
    monkeypatch.setattr(convert, "convert_one", lambda **_kwargs: None)

    _convert_archive(
        extracted_dir=extracted_dir,
        out_dir=out_dir,
        prefix="",
        stage=convert.STAGE_CONVERT_SHCNTX,
        hbk_source=convert.SHCNTX_NAME,
        hbk_version="8.3",
        archive_index={},
        used_names=set(),
        logs={"truncated": [], "collisions": [], "unresolved": [], "errors": []},
        stats=Stats(),
        pages_meta={},
        archive_lookup_final={},
    )
    lines = [line for line in capsys.readouterr().out.splitlines() if "event=progress" in line]
    assert len(lines) == 2
    assert "done=2" in lines[0]
    assert "total=3" in lines[0]
    assert "done=3" in lines[1]
    assert "eta_sec=" in lines[1]


def test_main_emits_stage_and_run_end_events(monkeypatch, tmp_path: Path, capsys):
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    monkeypatch.setattr(convert, "prepare_output", lambda out, clean: out.mkdir(parents=True, exist_ok=True))
    monkeypatch.setattr(convert, "extract_hbk", lambda hbk, dest: dest.mkdir(parents=True, exist_ok=True))
    monkeypatch.setattr(convert, "quick_scan_titles", lambda _dir: {})
    monkeypatch.setattr(convert, "build_archive_index", lambda *_args, **_kwargs: {})
    monkeypatch.setattr(convert, "_convert_archive", lambda *args, **kwargs: None)
    monkeypatch.setattr(convert, "build_toc", lambda *args, **kwargs: (TreeNode(prefix="", segment=""), {}, 1))
    monkeypatch.setattr(convert, "inject_breadcrumbs", lambda *args, **kwargs: 0)

    def _fake_write_logs(_out, _logs, stats, _params):
        stats.finished_at = stats.started_at + 0.5

    monkeypatch.setattr(convert, "write_logs", _fake_write_logs)

    rc = main(["--hbk", str(tmp_path / "shcntx_ru.hbk"), "--out", str(out_dir), "--clean"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "event=stage_start stage=extract_shcntx" in out
    assert "event=stage_end stage=extract_shcntx" in out
    assert "event=stage_start stage=convert_shcntx" in out
    assert "event=stage_end stage=write_logs" in out
    assert "event=run_end" in out
