"""The recovered stdout/stderr labels follow the natural language (#745).

The two labels were hard-coded in Dutch in ``tested/judge/evaluation.py``
whatever the submission's natural language. They are i18n strings now, like
every other message.
"""

from pathlib import Path

import pytest
import yaml

_INTERNATIONALIZATION = Path(__file__).resolve().parent.parent / "tested" / "internationalization"


def _recovered_keys(locale: str) -> dict:
    data = yaml.safe_load((_INTERNATIONALIZATION / f"{locale}.yaml").read_text())
    return data[locale]["judge"]["evaluation"]["recovered"]


class TestRecoveredLabelsInTranslationFiles:
    @pytest.mark.parametrize("locale", ["en", "nl", "es"])
    def test_every_locale_defines_the_recovered_labels(self, locale):
        keys = _recovered_keys(locale)
        assert keys["stdout"].endswith("%{output}")
        assert keys["stderr"].endswith("%{output}")

    def test_english_labels(self):
        assert _recovered_keys("en")["stdout"] == "Standard output was:\n%{output}"
        assert _recovered_keys("en")["stderr"] == "Standard error was:\n%{output}"

    def test_dutch_labels_keep_the_historical_text(self):
        assert _recovered_keys("nl")["stdout"] == "Standaarduitvoer was:\n%{output}"
        assert _recovered_keys("nl")["stderr"] == "Standaardfout was:\n%{output}"


class TestRecoveredLabelsFollowTheLocale:
    def test_labels_are_translated_per_locale(self):
        i18n = pytest.importorskip("i18n")  # needs the i18n package
        from tested.internationalization import get_i18n_string, set_locale

        try:
            assert get_i18n_string(
                "judge.evaluation.recovered.stdout", output="x"
            ) == "Standard output was:\nx"
            set_locale("nl")
            assert get_i18n_string(
                "judge.evaluation.recovered.stdout", output="x"
            ) == "Standaarduitvoer was:\nx"
            set_locale("es")
            assert get_i18n_string(
                "judge.evaluation.recovered.stderr", output="y"
            ) == "El error estándar fue:\ny"
        finally:
            set_locale("en")
