import io
import unittest
import urllib.error
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import lantern


class LoadConfigTest(unittest.TestCase):
    def test_defaults_when_file_is_missing(self):
        missing = Path("/tmp/lantern-missing.toml")
        self.assertEqual(lantern.load_config(missing), {"timeout": 5, "color": True})

    def test_reads_known_keys_and_ignores_the_rest(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "lantern.toml"
            path.write_text("timeout = 12\ncolor = false\nextra = 1\n", encoding="utf-8")
            self.assertEqual(lantern.load_config(path), {"timeout": 12.0, "color": False})


class CheckCommandTest(unittest.TestCase):
    def test_up_exits_zero(self):
        response = mock.Mock(status=200)
        response.__enter__ = mock.Mock(return_value=response)
        response.__exit__ = mock.Mock(return_value=False)
        buffer = io.StringIO()
        with mock.patch("lantern.urllib.request.urlopen", return_value=response):
            with redirect_stdout(buffer):
                code = lantern.main(["check", "https://example.com", "--no-color"])
        self.assertEqual(code, 0)
        self.assertEqual(buffer.getvalue(), "up 200\n")

    def test_timeout_flag_is_sent(self):
        response = mock.Mock(status=204)
        response.__enter__ = mock.Mock(return_value=response)
        response.__exit__ = mock.Mock(return_value=False)
        with mock.patch("lantern.urllib.request.urlopen", return_value=response) as urlopen:
            with redirect_stdout(io.StringIO()):
                lantern.main(["check", "https://example.com", "--timeout", "9"])
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 9.0)

    def test_http_error_is_down(self):
        error = urllib.error.HTTPError("https://example.com", 503, "nope", {}, None)
        buffer = io.StringIO()
        with mock.patch("lantern.urllib.request.urlopen", side_effect=error):
            with redirect_stdout(buffer):
                code = lantern.main(["check", "https://example.com"])
        self.assertEqual(code, 1)
        self.assertEqual(buffer.getvalue(), "down 503\n")

    def test_connection_failure_has_no_response(self):
        buffer = io.StringIO()
        with mock.patch(
            "lantern.urllib.request.urlopen",
            side_effect=urllib.error.URLError("refused"),
        ):
            with redirect_stdout(buffer):
                code = lantern.main(["check", "https://example.com"])
        self.assertEqual(code, 1)
        self.assertEqual(buffer.getvalue(), "down no response\n")


if __name__ == "__main__":
    unittest.main()
