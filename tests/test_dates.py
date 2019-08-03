from date import DateBuilder, Choice
import pytest


@pytest.fixture
def builder():
    return DateBuilder("dates.json")


class TestDateBuilder:

    def test_build_date(self, builder):
        builder.start_build("test date")
        date = builder.get_date("test date")
        assert date is not None
        assert "" == date.main_text

    def test_date_text(self, builder):
        start_text = "You go on a date with {waifu.name}"
        builder.start_build("test date")
        builder.add_text(start_text)
        date = builder.get_date("test date")
        assert start_text == date.main_text
    
    def test_add_empty_choice(self, builder):
        builder.start_build("test date")
        choice = Choice()
        builder.add_choice(choice)
        date = builder.get_date("test date")
        assert choice == date.choices[0]
    
    def test_add_choice(self, builder):
        builder.start_build("test date")
        choice = Choice()
        choice.add_prompt("You find some money on the ground. Do you pick it up?")
        choice.add_option("yes", "Yes.")
        choice.add_option("no", "No.")
        choice.add_outcome("yes", "You get 50 bucks.")
        choice.add_outcome("no", "You're a loser and get nothing.")
        builder.add_choice(choice)
