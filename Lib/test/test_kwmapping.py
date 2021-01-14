import unittest


class TestKwMapping(unittest.TestCase):
    def test_kw_item(self):
        results = []

        class KwItem:
            def __getitem__(self, index, kw1, kw2):
                return index, kw1, kw2
            def __setitem__(self, index, value, kw1, kw2):
                results.append((index, value, kw1, kw2))
            def __delitem__(self, index, kw1, kw2):
                results.append((index, kw1, kw2))

        # Getitem testing
        k = KwItem()
        self.assertEqual(k[1, kw1="hello", kw2="hi"], (1, "hello", "hi"))
        self.assertEqual(k[1, kw2="hi", kw1="hello"], (1, "hello", "hi"))
        self.assertEqual(
            k[1, 2, kw1="hello", kw2="hi"],
            ((1, 2), "hello", "hi"))

        # FIXME segfaulting
        kws = {"kw1": "hello", "kw2": "hi"}
        self.assertEqual(
           k[1, 2, **kws],
           ((1, 2), "hello", "hi"))
        idx = (1, 2)
        self.assertEqual(
            k[*idx, kw1="hello", kw2="hi"], ((1, 2), "hello", "hi"))

        # FIXME check if this should give 1 or (1, ) in the pep
        #idx = (1,)
        #self.assertEqual(
        #    k[*idx, kw1="hello", kw2="hi"], (1, "hello", "hi"))

        self.assertEqual(
            k[kw1="hello", kw2="hi"], ((), "hello", "hi"))

        with self.assertRaisesRegex(
            TypeError,
            "missing 1 required positional argument:"):
                k[kw1="hello"]

        with self.assertRaisesRegex(
            TypeError,
            "missing 2 required positional arguments:"):
                k[3]

        # Setitem testing
        k[1, kw1="hello", kw2="hi"] = 5
        self.assertEqual(results[-1], (1, 5, "hello", "hi"))

        k[1, 2, kw1="hello", kw2="hi"] = 5
        self.assertEqual(results[-1], ((1, 2), 5, "hello", "hi"))

        k[1, 2, kw2="hi", kw1="hello"] = 5
        self.assertEqual(results[-1], ((1, 2), 5, "hello", "hi"))

        k[kw1="hello", kw2="hi"] = 5
        self.assertEqual(results[-1], ((), 5, "hello", "hi"))

        # FIXME segfaulting
        # kws = {"kw1": "hello", "kw2": "hi"}
        # k[1, 2, **kws] = 5
        # self.assertEqual(results[-1], ((1, 2), "hello", "hi"))
        #
        #idx = (1, 2)
        #self.assertEqual(
        #    k[*idx, kw1="hello", kw2="hi"], ((1, 2), "hello", "hi"))

        # FIXME check if this should give 1 or (1, ) in the pep
        #idx = (1,)
        #self.assertEqual(
        #    k[*idx, kw1="hello", kw2="hi"], (1, "hello", "hi"))

        # Delitem testing
        del k[1, kw1="hello", kw2="hi"]
        self.assertEqual(results[-1], (1, "hello", "hi"))

        del k[1, 2, kw1="hello", kw2="hi"]
        self.assertEqual(results[-1], ((1, 2), "hello", "hi"))

        del k[1, 2, kw2="hi", kw1="hello"]
        self.assertEqual(results[-1], ((1, 2), "hello", "hi"))

        del k[kw1="hello", kw2="hi"]
        self.assertEqual(results[-1], ((), "hello", "hi"))

        # FIXME segfaulting
        # kws = {"kw1": "hello", "kw2": "hi"}
        # k[1, 2, **kws] = 5
        # self.assertEqual(results[-1], ((1, 2), "hello", "hi"))
        #
        #idx = (1, 2)
        #self.assertEqual(
        #    k[*idx, kw1="hello", kw2="hi"], ((1, 2), "hello", "hi"))

        # FIXME check if this should give 1 or (1, ) in the pep
        #idx = (1,)
        #self.assertEqual(
        #    k[*idx, kw1="hello", kw2="hi"], (1, "hello", "hi"))

    def test_defaults(self):
        results = []
        class KwItem:
            def __getitem__(self, index, kw1="kw1def", kw2="kw2def"):
                return index, kw1, kw2
            def __setitem__(self, index, value, kw1="kw1def", kw2="kw2def"):
                results.append((index, value, kw1, kw2))
            def __delitem__(self, index, kw1="kw1def", kw2="kw2def"):
                results.append((index, kw1, kw2))

        k = KwItem()
        # getitem
        self.assertEqual(k[1, 2], ((1, 2), "kw1def", "kw2def"))
        self.assertEqual(k[1, 2, kw2="hello"], ((1, 2), "kw1def", "hello"))

        # setitem
        k[1,2] = 5
        self.assertEqual(results[-1], ((1, 2), 5, "kw1def", "kw2def"))

        k[1,2, kw2="hello"] = 5
        self.assertEqual(results[-1], ((1, 2), 5, "kw1def", "hello"))

        # delitem
        del k[1,2]
        self.assertEqual(results[-1], ((1, 2), "kw1def", "kw2def"))

        del k[1,2, kw2="hello"]
        self.assertEqual(results[-1], ((1, 2), "kw1def", "hello"))


if __name__ == "__main__":
    unittest.main()
