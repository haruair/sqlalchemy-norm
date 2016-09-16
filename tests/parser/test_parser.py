import pytest
from sqlalchemy_norm import parse

class TestDotNotationParser():
    def test_convert_to_node_simple(self):
        content = [
            "name",
            "username"
        ]

        result = parse(content)
        expected = {
            "property": {"name", "username"}
        }

        assert result == expected

    def test_convert_to_single_depth(self):
        content = [
            "addresses",
            "addresses.city",
            "addresses.state",
            "addresses.country",
        ]

        result = parse(content)
        expected = {
            "property": {"addresses"},
            "legacy": {
                "addresses": {"city", "state", "country"}
            }
        }

        assert result == expected

    def test_convert_to_multiple_depth(self):
        content = [
            "courses",
            "courses.subject",
            "courses.lecturer",
            "courses.lecturer.name",
            "courses.lecturer.major",
            "courses.lecturer.addresses",
            "courses.lecturer.addresses.city"
        ]

        result = parse(content)
        expected = {
            "property": {"courses"},
            "legacy": {
                "courses": {
                    "subject",
                    "lecturer",
                    "lecturer.name",
                    "lecturer.major",
                    "lecturer.addresses",
                    "lecturer.addresses.city"
                }
            }
        }

        assert result == expected
