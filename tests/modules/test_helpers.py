
import xml.etree.ElementTree as XML
import yaml

import pytest

from jenkins_jobs.errors import InvalidAttributeError
from jenkins_jobs.errors import MissingAttributeError
from jenkins_jobs.errors import JenkinsJobsException
from jenkins_jobs.modules.helpers import (
    convert_mapping_to_xml,
    check_mutual_exclusive_data_args,
)


def test_convert_mapping_to_xml():
    """
    Tests the test_convert_mapping_to_xml_fail_required function
    """

    # Test default values
    default_root = XML.Element("testdefault")
    default_data = yaml.safe_load("string: hello")
    default_mappings = [("default-string", "defaultString", "default")]

    convert_mapping_to_xml(
        default_root, default_data, default_mappings, fail_required=True
    )
    result = default_root.find("defaultString").text
    result == "default"

    # Test user input
    user_input_root = XML.Element("testUserInput")
    user_input_data = yaml.safe_load("user-input-string: hello")
    user_input_mappings = [("user-input-string", "userInputString", "user-input")]

    convert_mapping_to_xml(
        user_input_root, user_input_data, user_input_mappings, fail_required=True
    )
    result = user_input_root.find("userInputString").text
    result == "hello"

    # Test missing required input
    required_root = XML.Element("testrequired")
    required_data = yaml.safe_load("string: hello")
    required_mappings = [("required-string", "requiredString", None)]

    with pytest.raises(MissingAttributeError):
        convert_mapping_to_xml(
            required_root,
            required_data,
            required_mappings,
            fail_required=True,
        )

    # Test invalid user input for list
    user_input_root = XML.Element("testUserInput")
    user_input_data = yaml.safe_load("user-input-string: bye")
    valid_inputs = ["hello"]
    user_input_mappings = [
        ("user-input-string", "userInputString", "user-input", valid_inputs)
    ]

    with pytest.raises(InvalidAttributeError):
        convert_mapping_to_xml(
            user_input_root,
            user_input_data,
            user_input_mappings,
        )

    # Test invalid user input for dict
    user_input_root = XML.Element("testUserInput")
    user_input_data = yaml.safe_load("user-input-string: later")
    valid_inputs = {"hello": "world"}
    user_input_mappings = [
        ("user-input-string", "userInputString", "user-input", valid_inputs)
    ]

    with pytest.raises(InvalidAttributeError):
        convert_mapping_to_xml(
            user_input_root,
            user_input_data,
            user_input_mappings,
        )

    # Test invalid key for dict
    user_input_root = XML.Element("testUserInput")
    user_input_data = yaml.safe_load("user-input-string: world")
    valid_inputs = {"hello": "world"}
    user_input_mappings = [
        ("user-input-string", "userInputString", "user-input", valid_inputs)
    ]

    with pytest.raises(InvalidAttributeError):
        convert_mapping_to_xml(
            user_input_root,
            user_input_data,
            user_input_mappings,
        )


def test_check_mutual_exclusive_data_args_no_mutual_exclusive():
    @check_mutual_exclusive_data_args(0, "foo", "bar")
    @check_mutual_exclusive_data_args(0, "foo", "baz")
    def func(data):
        pass

    func({"baz": "qaz", "bar": "qaz"})


def test_check_mutual_exclusive_data_args_mutual_exclusive():
    @check_mutual_exclusive_data_args(0, "foo", "bar")
    @check_mutual_exclusive_data_args(0, "foo", "baz")
    def func(data):
        pass

    with pytest.raises(JenkinsJobsException):
        func({"foo": "qaz", "bar": "qaz"})
