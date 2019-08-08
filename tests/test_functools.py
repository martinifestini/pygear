from pygear import func


def test_lazy_property():
    class A:
        @func.lazy_property
        def myfunc(_self):  # pylint: disable=no-self-argument
            return 1
    a = A()
    assert not hasattr(a, "_myfunc")
    result = a.myfunc
    assert result == 1
    assert getattr(a, "_myfunc") == 1