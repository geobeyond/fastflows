from fastflows.cli.utils import (
    process_parmas_as_a_string_with_dict,
    process_parmas_input_as_a_comma_separated_string,
    process_params_from_str,
    check_path_is_dir,
)
import pytest


@pytest.mark.parametrize(
    "input,result",
    (
        ["a=3,b=4", {"a": "3", "b": "4"}],
        [
            "'ma'='ba','ga'='ga'",
            {"'ga'": "'ga'", "'ma'": "'ba'"},
        ],
    ),
)
def test_process_parmas_input_as_a_comma_separated_string(input: str, result: dict):
    assert process_parmas_input_as_a_comma_separated_string(input) == result


@pytest.mark.parametrize(
    "input,result",
    (
        ["{'one': 'two', 'three': 'four'}", {"one": "two", "three": "four"}],
        ["{0:1, 2:3, 4:4}", {0: 1, 2: 3, 4: 4}],
    ),
)
def test_process_parmas_as_a_string_with_dict(input: str, result: dict):
    assert process_parmas_as_a_string_with_dict(input) == result


@pytest.mark.parametrize(
    "input,result",
    (
        ["{'one': 'two', 'three': 'four'}", {"one": "two", "three": "four"}],
        ["{0:1, 2:3, 4:4}", {0: 1, 2: 3, 4: 4}],
    ),
)
def test_process_params_from_str(input: str, result: dict):
    assert process_params_from_str(input) == result


@pytest.mark.parametrize(
    "path,result",
    (
        ["tests/test_data/flows", "tests/test_data/flows"],
        ["/not_exist", "Path '/not_exist' does not exist"],
        [
            "tests/test_data/flows/flow_with_params.py",
            "Path 'tests/test_data/flows/flow_with_params.py' is not a directory",
        ],
    ),
)
def test_check_path_is_dir(path: str, result: str):
    if "Path" in result:
        with pytest.raises(ValueError) as e:
            check_path_is_dir(path)
        assert result in e.value.args[0]
    else:
        assert check_path_is_dir(path) == result
