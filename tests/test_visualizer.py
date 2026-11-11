from connect4.visualizer.export import Visualizer


def test_visualizer_ascii_output(board_7x6):
    b = board_7x6
    b.drop_piece(0, 3, 1)
    b.drop_piece(0, 4, 2)

    ascii_out = Visualizer.to_ascii(b, use_unicode=True)
    assert "🔴" in ascii_out
    assert "🟡" in ascii_out
    assert "⚪" in ascii_out
    assert "1   2   3   4   5   6   7" in ascii_out

    plain_out = Visualizer.to_ascii(b, use_unicode=False)
    assert "X" in plain_out
    assert "O" in plain_out
    assert "." in plain_out


def test_visualizer_svg_output(board_7x6):
    b = board_7x6
    b.drop_piece(0, 3, 1)

    svg_str = Visualizer.to_svg(b)
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert 'fill="#EF4444"' in svg_str  # Red coin


def test_visualizer_dot_output(board_7x6):
    b = board_7x6
    b.drop_piece(0, 3, 1)

    dot_str = Visualizer.to_dot(b, title="TestConnectFour")
    assert "digraph TestConnectFour" in dot_str
    assert "cell_0_3" in dot_str
    assert "rankdir=TB" in dot_str


def test_visualizer_file_exports(board_7x6, tmp_path):
    svg_file = tmp_path / "board.svg"
    dot_file = tmp_path / "board.dot"

    Visualizer.save_svg(board_7x6, svg_file)
    Visualizer.save_dot(board_7x6, dot_file)

    assert svg_file.exists()
    assert dot_file.exists()
    assert len(svg_file.read_text()) > 50
    assert len(dot_file.read_text()) > 50
