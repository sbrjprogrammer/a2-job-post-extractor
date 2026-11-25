
import json
import unittest
from unittest.mock import Mock

from pydantic import ValidationError

from extract import extract_with_retry


class RetryTests(unittest.TestCase):

    def test_retry_after_invalid_response(self):
        client = Mock()

        invalid_response = Mock()
        invalid_response.text = json.dumps({
            "title": "Developer",
            "salary": "not-a-number",
            "skills": ["Python"]
        })

        valid_response = Mock()
        valid_response.text = json.dumps({
            "title": "Python Developer",
            "company": "ABC",
            "location": "Karachi",
            "salary": 150000,
            "currency": "PKR",
            "skills": ["Python"],
            "remote": True,
            "experience": "3 years"
        })

        client.models.generate_content.side_effect = [
            invalid_response,
            valid_response
        ]

        result = extract_with_retry(
            client,
            "test-model",
            "Extract job information.",
            "Python Developer required."
        )

        self.assertEqual(result.title, "Python Developer")
        self.assertEqual(
            client.models.generate_content.call_count, 2
        )

        second_call = client.models.generate_content.call_args_list[1]
        self.assertIn(
            "Validation error",
            second_call.kwargs["contents"]
        )

    def test_fails_after_three_invalid_responses(self):
        client = Mock()

        invalid_response = Mock()
        invalid_response.text = json.dumps({
            "title": "Developer",
            "salary": "invalid",
            "skills": ["Python"]
        })

        client.models.generate_content.side_effect = [
            invalid_response,
            invalid_response,
            invalid_response
        ]

        with self.assertRaises(RuntimeError):
            extract_with_retry(
                client,
                "test-model",
                "Extract job information.",
                "Developer required."
            )

        self.assertEqual(
            client.models.generate_content.call_count, 3
        )


if __name__ == "__main__":
    unittest.main()
