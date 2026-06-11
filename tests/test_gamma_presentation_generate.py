from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import gamma_presentation_generate as gamma


def test_gamma_request_defaults_to_chinese_and_preserves_english_key_terms():
    body = gamma.build_request_body("## 学习圈\n\nLearning Cycle 与 ABC。", "inputTextBreaks")

    assert body["textOptions"]["language"] == "zh-cn"
    assert "简体中文" in body["additionalInstructions"]
    assert "English key terms" in body["additionalInstructions"]


def test_long_page_profile_resolves_to_double_gamma_cards():
    assert gamma.resolve_num_cards(None, "long") == 28
    assert gamma.resolve_num_cards(None, "normal") is None
    assert gamma.resolve_num_cards(32, "long") == 32


if __name__ == "__main__":
    test_gamma_request_defaults_to_chinese_and_preserves_english_key_terms()
    test_long_page_profile_resolves_to_double_gamma_cards()
    print("ok")
