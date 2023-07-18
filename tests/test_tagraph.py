import pytest

from tests.conftest import TagRepo

def test_load_file():
    with open("./tests/tags.yml") as f:
        TagRepo(f)


def test_name(repo: TagRepo):
    assert repo.query("funny") == ["funny"]


def test_wildcard(repo: TagRepo):
    assert repo.query("*") == ["funny", "science"]


def test_multi_level_wildcard(repo: TagRepo):
    assert repo.query("**") == [
        "funny",
        "science",
        "funny::fail",
        "funny::video",
        "funny::joke",
        "science::pop",
        "science::biology",
        "funny::fail::injury",
        "funny::joke::video",
        "funny::joke::knock-knock",
        "funny::joke::dad",
        "science::biology::micro",
        "science::biology::neuro",
        "funny::joke::dad::good",
        "funny::joke::dad::bad",
    ]


def test_nested__name_name(repo: TagRepo):
    assert repo.query("funny::joke") == ["funny::joke"]


def test_nested__name_wildcard(repo: TagRepo):
    assert repo.query("funny::*") == ["funny::fail", "funny::video", "funny::joke"]


def test_nested__name_multi_level_wildcard(repo: TagRepo):
    assert repo.query("funny::**") == [
        "funny::fail",
        "funny::video",
        "funny::joke",
        "funny::fail::injury",
        "funny::joke::video",
        "funny::joke::knock-knock",
        "funny::joke::dad",
        "funny::joke::dad::good",
        "funny::joke::dad::bad",
    ]


def test_nested__wildcard_name(repo: TagRepo):
    assert repo.query("*::joke") == ["funny::joke"]


def test_nested__wildcard_wildcard(repo: TagRepo):
    assert repo.query("*::*") == [
        "funny::fail",
        "funny::video",
        "funny::joke",
        "science::pop",
        "science::biology",
    ]


def test_nested__wildcard_multi_level_wildcard(repo: TagRepo):
    assert repo.query("*::**") == [
        "funny::fail",
        "funny::video",
        "funny::joke",
        "science::pop",
        "science::biology",
        "funny::fail::injury",
        "funny::joke::video",
        "funny::joke::knock-knock",
        "funny::joke::dad",
        "science::biology::micro",
        "science::biology::neuro",
        "funny::joke::dad::good",
        "funny::joke::dad::bad",
    ]


def test_nested__multi_level_wildcard_name(repo: TagRepo):
    assert repo.query("**::bad") == ["funny::joke::dad::bad"]


def test_nested__multi_level_wildcard_name_multiple_matches(repo: TagRepo):
    assert repo.query("**::video") == ["funny::video", "funny::joke::video"]


def test_nested__multi_level_wildcard_wildcard(repo: TagRepo):
    assert repo.query("**::*") == [
        "funny::fail",
        "funny::video",
        "funny::joke",
        "science::pop",
        "science::biology",
        "funny::fail::injury",
        "funny::joke::video",
        "funny::joke::knock-knock",
        "funny::joke::dad",
        "science::biology::micro",
        "science::biology::neuro",
        "funny::joke::dad::good",
        "funny::joke::dad::bad",
    ]


def test_nested__multi_level_wildcard_multi_level_wildcard(repo: TagRepo):
    assert repo.query("**::**") == [
        "funny::fail",
        "funny::video",
        "funny::joke",
        "science::pop",
        "science::biology",
        "funny::fail::injury",
        "funny::joke::video",
        "funny::joke::knock-knock",
        "funny::joke::dad",
        "science::biology::micro",
        "science::biology::neuro",
        "funny::joke::dad::good",
        "funny::joke::dad::bad",
    ]


def test_mpq(repo: TagRepo):
    assert repo.query("{funny}") == ["funny"]


def test_mpq__not(repo: TagRepo):
    assert repo.query("{!funny}") == ["science"]


def test_mpq__and(repo: TagRepo):
    assert repo.query("*::{!fail&!pop}") == [
        "funny::video",
        "funny::joke",
        "science::biology",
    ]


def test_mpq__or(repo: TagRepo):
    assert repo.query("*::{fail|pop}") == ["funny::fail", "science::pop"]
