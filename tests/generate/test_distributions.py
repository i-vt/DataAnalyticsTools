"""Tests for data_analytics_tools.generate.distributions."""

import numpy as np
import pytest

from data_analytics_tools.generate.distributions import bootstrap, generate_normal


class TestBootstrap:
    def test_basic(self):
        data = [1, 2, 3, 4, 5]
        result = bootstrap(data, 100, seed=0)
        assert len(result) == 100
        # All values should come from the original
        assert set(result.tolist()).issubset(set(data))

    def test_deterministic_with_seed(self):
        data = [10, 20, 30]
        a = bootstrap(data, 50, seed=42)
        b = bootstrap(data, 50, seed=42)
        np.testing.assert_array_equal(a, b)

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="empty"):
            bootstrap([], 10)

    def test_zero_samples_raises(self):
        with pytest.raises(ValueError, match="n_samples"):
            bootstrap([1], 0)

    def test_single_element(self):
        result = bootstrap([7], 50, seed=0)
        assert all(x == 7 for x in result)


class TestGenerateNormal:
    def test_shape(self):
        result = generate_normal(0, 1, 500, seed=0)
        assert len(result) == 500

    def test_deterministic(self):
        a = generate_normal(5, 2, 100, seed=1)
        b = generate_normal(5, 2, 100, seed=1)
        np.testing.assert_array_equal(a, b)

    def test_mean_approx(self):
        result = generate_normal(100, 1, 50_000, seed=0)
        assert abs(result.mean() - 100) < 0.1

    def test_std_approx(self):
        result = generate_normal(0, 5, 50_000, seed=0)
        assert abs(result.std() - 5) < 0.1

    def test_zero_std_raises(self):
        with pytest.raises(ValueError, match="positive"):
            generate_normal(0, 0, 10)

    def test_negative_std_raises(self):
        with pytest.raises(ValueError, match="positive"):
            generate_normal(0, -1, 10)

    def test_zero_samples_raises(self):
        with pytest.raises(ValueError, match="n_samples"):
            generate_normal(0, 1, 0)
