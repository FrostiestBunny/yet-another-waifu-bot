from date import DateBuilder
import pytest


@pytest.fixture
def builder():
    return DateBuilder("dates.json")


class TestDateBuilders:

    def test_date_start(self, builder):
        start = "You go on a date with {waifu.name}"
        builder.start_build("test date", start)
        date = builder.get_date("test date")
        assert start == date.main_text
    
    def test_date_choices(self, builder):
        start = "You go on a date with {waifu.name}. You get a choice: [Do this?|Yes|No]"
        builder.start_build("test date", start)
        date = builder.get_date("test date")
        assert 1 == len(date.choices)

