import os
import numpy as np
from protocols import bb84_protocol, b92_protocol, six_state_protocol
from simulation_manager import compare_protocols


def test_bb84_protocol_returns_three_values():
    qber, sifted, final_key = bb84_protocol(100, eve_present=False, noise_level=0.0)
    assert 0.0 <= qber <= 100.0
    assert isinstance(sifted, int)
    assert isinstance(final_key, int)
    assert sifted >= 0
    assert final_key >= 0


def test_b92_protocol_returns_three_values_no_errors():
    qber, sifted, final_key = b92_protocol(100, eve_present=False, noise_level=0.0)
    assert isinstance(qber, float)
    assert isinstance(sifted, int)
    assert isinstance(final_key, int)
    assert qber >= 0.0
    assert sifted >= 0
    assert final_key >= 0


def test_b92_protocol_returns_three_values_if_no_success():
    qber, sifted, final_key = b92_protocol(1, eve_present=False, noise_level=0.0)
    assert qber == 0.0 or (0.0 <= qber <= 100.0)
    assert isinstance(sifted, int)
    assert isinstance(final_key, int)


def test_six_state_protocol_basic():
    qber, sifted, final_key = six_state_protocol(100, eve_present=False, noise_level=0.0)
    assert 0.0 <= qber <= 100.0
    assert sifted >= 0
    assert final_key >= 0


def test_compare_protocols_creates_summary_file(tmp_path):
    cwd = os.getcwd()
    output_prefix = 'test_analysis'
    try:
        os.chdir(tmp_path)
        compare_protocols(['bb84'], 50, [0.0], 1, output_dir='.', output_prefix=output_prefix)
        assert os.path.exists(f'{output_prefix}.txt')
        assert os.path.exists(f'{output_prefix}.png')
    finally:
        os.chdir(cwd)
