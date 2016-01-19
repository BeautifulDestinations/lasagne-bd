import pytest
import numpy as np
import theano.tensor as T


class TestNonlinearities(object):
    def linear(self, x):
        return x

    def rectify(self, x):
        return x * (x > 0)

    def leaky_rectify(self, x):
        return x * (x > 0) + 0.01 * x * (x < 0)

    def leaky_rectify_0(self, x):
        return self.rectify(x)

    def softplus(self, x):
        return np.log1p(np.exp(x))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def tanh(self, x):
        return np.tanh(x)

    def scaled_tanh(self, x):
        return np.tanh(x)

    def scaled_tanh_p(self, x):
        return 2.27 * np.tanh(0.5 * x)

    def softmax(self, x):
        return (np.exp(x).T / np.exp(x).sum(-1)).T

    @pytest.mark.parametrize('nonlinearity',
                             ['linear', 'rectify',
                              'leaky_rectify', 'sigmoid',
                              'tanh', 'scaled_tanh',
                              'softmax', 'leaky_rectify_0',
                              'scaled_tanh_p', 'softplus'])
    def test_nonlinearity(self, nonlinearity):
        import lasagne.nonlinearities

        if nonlinearity == 'leaky_rectify_0':
            from lasagne.nonlinearities import LeakyRectify
            theano_nonlinearity = LeakyRectify(leakiness=0)
        elif nonlinearity == 'scaled_tanh':
            from lasagne.nonlinearities import ScaledTanH
            theano_nonlinearity = ScaledTanH()
        elif nonlinearity == 'scaled_tanh_p':
            from lasagne.nonlinearities import ScaledTanH
            theano_nonlinearity = ScaledTanH(scale_in=0.5, scale_out=2.27)
        else:
            theano_nonlinearity = getattr(lasagne.nonlinearities,
                                          nonlinearity)
        np_nonlinearity = getattr(self, nonlinearity)

        X = T.matrix()
        X0 = lasagne.utils.floatX(np.random.uniform(-3, 3, (10, 10)))

        theano_result = theano_nonlinearity(X).eval({X: X0})
        np_result = np_nonlinearity(X0)

        assert np.allclose(theano_result, np_result)
