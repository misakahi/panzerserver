import copy
import yaml

DEFAULT_CONFIG = {
    "components": {
        "left_wheel": [16, 19, 13],
        "right_wheel": [26, 20, 21],
        "turret": [
            25, 5, 6,               # motor
            18, 0.001, 0.05, 0.06    # servo
        ],
    },
    "watch_threshold": 200
}


def overrides_dict(d, overrides):
    res = copy.deepcopy(d)
    if isinstance(d, dict):
        for k, v in overrides.items():
            v = copy.deepcopy(v)
            if isinstance(v, dict):
                if k in d:
                    res[k] = overrides_dict(res[k], v)
                else:
                    res[k] = v
            else:
                res[k] = v
    return res


def get_default():
    return copy.deepcopy(DEFAULT_CONFIG)


def load_config(file):
    with open(file, "r") as f:
        overrides = yaml.load(f)
    return overrides_dict(get_default(), overrides)


def _test():
    # testing overrides_dict
    d = {
        "a": [1, 2],
        "b": {
            "c": 1
        },
        "d": 1
    }
    o = {
        "a": [3, 4],
        "b": {
            "c": 2,
            "d": 1,
        }
    }
    print(overrides_dict(d, o))


if __name__ == '__main__':
    _test()
