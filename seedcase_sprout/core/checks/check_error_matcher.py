from dataclasses import dataclass

from seedcase_sprout.core.checks.check_error import CheckError


@dataclass
class CheckErrorMatcher:
    """A class that helps to filter `CheckError`s based on their attributes."""

    message: str | None = None
    json_path: str | None = None
    validator: str | None = None

    def matches(self, error: CheckError) -> bool:
        """Determines if this matcher matches the given `CheckError`.

        Args:
            error: The `CheckError` to match.

        Returns:
            If there was a match.
        """
        return (
            self.message_matches(error)
            and self.json_path_matches(error)
            and self.validator_matches(error)
        )

    def message_matches(self, error: CheckError) -> bool:
        """Determines if this matcher matches the message of the given `CheckError`.

        Args:
            error: The `CheckError` to match.

        Returns:
            If there was a match.
        """
        return self.message is None or self.message in error.message

    def json_path_matches(self, error: CheckError) -> bool:
        """Determines if this matcher matches the `json_path` of the given `CheckError`.

        Matching on the full `json_path` and matching on the field name are supported.

        Args:
            error: The `CheckError` to match.

        Returns:
            If there was a match.
        """
        if self.json_path is None:
            return True
        if self.json_path == "" or self.json_path.startswith("$"):
            return self.json_path == error.json_path
        return error.json_path.endswith(f".{self.json_path}")

    def validator_matches(self, error: CheckError) -> bool:
        """Determines if this matcher matches the validator of the given `CheckError`.

        Args:
            error: The `CheckError` to match.

        Returns:
            If there was a match.
        """
        return self.validator is None or self.validator == error.validator
