# -*- coding: utf-8 -*-
# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2023 Tonje, Sougata / NMBU

"""
Test set for Fauna super class interface, in addition to child classes Herbivore and Carnivore
interface.
"""
import random

import pytest

from biosim.model.fauna import Herbivore, Carnivore

"""Random seed for tests"""
SEED = 123456
"""Significance level for statistical tests"""
ALPHA = 0.01


# TODO: Unsure about this, may be removed.
def reset_animal_params_():
    """ Reset the animal parameters before running the tests."""
    yield
    Herbivore.set_animal_parameters(Herbivore.default_params)
    Carnivore.set_animal_parameters(Herbivore.default_params)


def test_init_animal():
    """Initialization of animal with set input of age and weight."""
    random.seed(20)
    cycles = 20
    age = random.randint(0, 10)
    weight = random.randint(1, 50)
    for _ in range(1, cycles):
        herb = Herbivore(age, weight)
        carn = Carnivore(age, weight)


def test_age_carn_herb():
    """ Test that the default age for an instance of an Herbivore or Carnivore is equal to 0. """
    herb = Herbivore()
    carn = Carnivore()
    herb_set = Herbivore(5, 20)
    carn_set = Carnivore(6, 24)

    assert herb.age == 0
    assert carn.age == 0

    assert herb_set.age == 5
    assert carn_set.age == 6


def test_get_older_carn_herb():
    """ Test that the age of an animal increases by one when get_older() is used."""
    herb = Herbivore()
    carn = Carnivore()
    herb_set = Herbivore(5, 20)
    carn_set = Carnivore(6, 24)

    no_years = 10
    for _ in range(no_years):
        herb.get_older()
        herb_set.get_older()
        carn.get_older()
        carn_set.get_older()
    assert herb.age == no_years
    assert herb_set.age == no_years + 5
    assert carn.age == no_years
    assert carn_set.age == no_years + 6


def test_init_weight():
    """The initialized weight of an animal has to be greater than 0."""
    herb = Herbivore()
    carn = Carnivore()
    assert herb.weight != 0
    assert carn.weight != 0

    year = 10
    weight = random.randint(1, 10)
    for age in range(1, year):
        herb = Herbivore(age, weight)
        assert herb.weight != 0


def test_eat_and_gain_weight_herb():
    """ Test that a Herbivore that has eaten an F amount of fodder gains weight according to the
    formula beta*F, where beta = 0.9 for Herbivores."""
    herb = Herbivore()

    amount_fodder = 10
    beta = 0.9
    w_increase = amount_fodder * beta  # Formula for the increase of weight when a Herbivore eats
    w_before = herb.weight  # Weight of the Herbivore before feeding
    no_cycles = 10

    for _ in range(no_cycles):
        herb.feed_and_gain_weight(amount_fodder)
        assert herb.weight == pytest.approx(w_before + w_increase)
        w_before += w_increase


def test_eat_and_gain_weight_carn():
    """Carnivore eating and gaining weight. Weight gain is Fodder*beta, where beta = 0.75"""
    herb = Herbivore()
    carn = Carnivore()
    herb_set = Herbivore(5, 20)
    carn_set = Carnivore(6, 24)

    carn.set_animal_parameters(params={'DeltaPhiMax': 0.01})
    herbs = [herb, herb_set]
    assert carn_set.weight == 24
    carn_set.feed_on_herbivores_and_gain_weight(herbs)
    assert carn_set.weight > 24


# TODO: This does _not_ raise a ValueError, is going to be fixed asap.
@pytest.mark.parametrize('bad_age, bad_weight', [(-1, -1)])
def test_grow_old_herb_carn(bad_age, bad_weight):
    """It should not be possible to initialize a negative age and/or weight when instantiating a
    new Herbivore and/or Carnivore."""
    with pytest.raises(ValueError):
        Herbivore(bad_age, bad_weight)
        Carnivore(bad_age, bad_weight)


def test_weight_of_newborns_z_test():
    """This test is a probability test: executes procreate() N number of times.  We have that the
    number n of "successes", where procreate() returns an offspring, should be according to the log
    normal distribution ln(X) ~ N(mu, sigma^2). Here, the parameters are
    the mean mu = w_birth and variance sigma^2= (sigma_birth)^2.

    We have
    Z = (sum of X - mean) / standard deviation

    """

    random.seed(SEED)
    # no_trials = 100

    herb = Herbivore()
    herb.set_animal_parameters
