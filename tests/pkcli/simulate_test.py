# -*- coding: utf-8 -*-

import pytest
from bnlcrl.pkcli import simulate

verbose = False

_EPSILON = 1e-7


def test_calc_ideal_focus1():
    delta = simulate.find_delta(9000, calc_delta=True)["characteristic_value"]
    d = simulate.calc_ideal_focus(radius=1.5e-3, n=20, delta=delta, p0=20.0)
    _eq(8.924966829362239, d["ideal_focus"])
    _eq(16.11727331530564, d["p1_ideal"])
    _eq(36.11727331530564, d["p1_ideal_from_source"])


def test_calc_ideal_focus1s():
    delta = simulate.find_delta(9000, calc_delta=True)["characteristic_value"]
    d = simulate.calc_ideal_focus(radius="1.5e-3", n="20", delta=str(delta), p0="20.0")
    _eq(8.924966829362239, d["ideal_focus"])
    _eq(16.11727331530564, d["p1_ideal"])
    _eq(36.11727331530564, d["p1_ideal_from_source"])


def test_calc_ideal_focus0():
    delta = simulate.find_delta(9000, calc_delta=True)["characteristic_value"]
    with pytest.raises(AssertionError):
        simulate.calc_ideal_focus(radius=1.5e-3, n=0, delta=delta, p0=20.0)


def test_crl_simulator1():
    d = simulate.simulate_crl(
        ["2", "4", "6", "7", "8"], 21500, p0=6.52, verbose=verbose
    )
    _eq(0.00120167289264, d["d"])
    _eq(-0.0661303590822, d["d_ideal"])
    _eq(1.0480597835, d["f"])
    _eq(6.52, d["p0"])
    _eq(1.24879832711, d["p1"])
    _eq(1.31613035908, d["p1_ideal"])


def test_crl_simulator1s():
    d = simulate.simulate_crl(
        ["2", "4", "6", "7", "8"], "21500", p0="6.52", verbose=verbose
    )
    _eq(0.00120167289264, d["d"])
    _eq(-0.0661303590822, d["d_ideal"])
    _eq(1.0480597835, d["f"])
    _eq(6.52, d["p0"])
    _eq(1.24879832711, d["p1"])
    _eq(1.31613035908, d["p1_ideal"])


def test_crl_simulator1n():
    d = simulate.simulate_crl(
        ["2", "4", "6", "7", "8"], 21500, p0=6.52, verbose=verbose, use_numpy=True
    )
    _eq(0.00120167289264, d["d"])
    _eq(-0.0661303590822, d["d_ideal"])
    _eq(1.0480597835, d["f"])
    _eq(6.52, d["p0"])
    _eq(1.24879832711, d["p1"])
    _eq(1.31613035908, d["p1_ideal"])


def test_crl_simulator2():
    d = simulate.simulate_crl([], 24000)
    assert 0 == d["d"]
    assert 0 == d["d_ideal"]
    assert 0 == d["f"]
    _eq(6.2, d["p0"])
    assert 0 == d["p1"]
    assert 0 == d["p1_ideal"]


def test_crl_simulator2s():
    d = simulate.simulate_crl([], "24000")
    assert 0 == d["d"]
    assert 0 == d["d_ideal"]
    assert 0 == d["f"]
    _eq(6.2, d["p0"])
    assert 0 == d["p1"]
    assert 0 == d["p1_ideal"]


# TODO: add tests for different data formats (csv, json, plain text)


def test_delta_finder1():
    d = simulate.find_delta(
        24000, precise=True, data_file="Be_delta.dat", verbose=verbose
    )
    _eq(5.91145636e-07, d["characteristic_value"])
    _eq(24001.0234, d["closest_energy"])
    assert "file" == d["method"]


def test_delta_finder1s():
    d = simulate.find_delta(
        "24000", precise=True, data_file="Be_delta.dat", verbose=verbose
    )
    _eq(5.91145636e-07, d["characteristic_value"])
    _eq(24001.0234, d["closest_energy"])
    assert "file" == d["method"]


def test_delta_finder1n():
    d = simulate.find_delta(
        24000, precise=True, data_file="Be_delta.dat", verbose=verbose, use_numpy=True
    )
    _eq(5.91145636e-07, d["characteristic_value"])
    _eq(24001.0234, d["closest_energy"])
    assert "file" == d["method"]


def test_delta_finder2():
    d = simulate.find_delta(24000, precise=True, verbose=verbose)
    _eq(5.91196169e-07, d["characteristic_value"])
    _eq(23999.998, d["closest_energy"])
    assert "server" == d["method"]


def test_delta_finder2s():
    d = simulate.find_delta("24000", precise=True, verbose=verbose)
    _eq(5.91196169e-07, d["characteristic_value"])
    _eq(23999.998, d["closest_energy"])
    assert "server" == d["method"]


def test_delta_finder3():
    d = simulate.find_delta(24000, calc_delta=True, verbose=verbose)
    _eq(5.908635405401086e-07, d["characteristic_value"])
    _eq(24000, d["closest_energy"])
    assert "calculation" == d["method"]


def test_delta_finder3s():
    d = simulate.find_delta("24000", calc_delta=True, verbose=verbose)
    _eq(5.908635405401086e-07, d["characteristic_value"])
    _eq(24000, d["closest_energy"])
    assert "calculation", d["method"]


def test_atten_finder1():
    d = simulate.find_delta(
        24000,
        precise=True,
        data_file="Be_atten.dat",
        characteristic="atten",
        verbose=verbose,
    )
    _eq(0.0312459, d["characteristic_value"])
    _eq(24003.0, d["closest_energy"])


def test_atten_finder1():
    d = simulate.find_delta(
        "24000",
        precise=True,
        data_file="Be_atten.dat",
        characteristic="atten",
        verbose=verbose,
    )
    _eq(0.0312459, d["characteristic_value"])
    _eq(24003.0, d["closest_energy"])


def test_atten_finder1n():
    d = simulate.find_delta(
        24000,
        precise=True,
        data_file="Be_atten.dat",
        characteristic="atten",
        verbose=verbose,
        use_numpy=True,
    )
    _eq(0.0312459, d["characteristic_value"])
    _eq(24003.0, d["closest_energy"])


def test_atten_finder2():
    d = simulate.find_delta(
        24000, precise=True, characteristic="atten", verbose=verbose
    )
    _eq(0.0312442, d["characteristic_value"])
    _eq(24000.0, d["closest_energy"])


def _eq(a, b):
    assert abs(a - b) < _EPSILON
