"""Parser that converts raw YAML dictionaries into domain objects."""

from typing import Any

from yatl.domains.domain import ExpectSpec, ExtractSpec, TestSpecification, TestStep
from yatl.domains.http import (
    Body,
    BodyExpectation,
    ContentFormat,
    FilesBody,
    FormBody,
    HttpRequest,
    JsonBody,
    TextBody,
    XmlBody,
)


def parse_test_specification(raw: dict[str, Any]) -> TestSpecification:
    """Parses a raw YAML dictionary into a TestSpecification domain object.

    Args:
        raw: The raw dictionary loaded from a YAML file.

    Returns:
        A TestSpecification domain object.
    """
    name = raw.get("name")
    description = raw.get("description")
    skip = raw.get("skip", False)

    raw_steps: list[dict[str, Any]] = raw.get("steps", [])
    steps = [parse_step(s) for s in raw_steps]

    return TestSpecification(
        name=name,
        description=description,
        steps=steps,
        skip=skip,
    )


def parse_step(raw: dict[str, Any]) -> TestStep:
    """Parses a raw step dictionary into a Step domain object.

    Args:
        raw: The raw step dictionary from YAML.

    Returns:
        A Step domain object.
    """
    name = raw.get("name")
    description = raw.get("description")
    skip = raw.get("skip", False)
    parametrize: list[dict] | None = raw.get("parametrize")

    request = parse_request(raw.get("request", {}))
    expect = parse_expect_spec(raw.get("expect"))
    extract = parse_extract_spec(raw.get("extract"))

    return TestStep(
        name=name,
        description=description,
        request=request,
        expect=expect,
        extract=extract,
        parametrize=parametrize,
        skip=skip,
    )


def parse_request(raw: dict[str, Any]) -> HttpRequest:
    """Parses a raw request dictionary into a Request domain object.

    Args:
        raw: The raw request dictionary from YAML.

    Returns:
        A Request domain object.
    """
    method = str(raw.get("method", "GET")).upper()
    url: str = raw.get("url", "")
    headers: dict[str, str] = raw.get("headers", {})
    params: dict[str, str] = raw.get("params", {})
    cookies: dict[str, str] = raw.get("cookies", {})
    timeout: float | None = raw.get("timeout", None)
    body = parse_body(raw.get("body"))

    return HttpRequest(
        method=method,
        url=url,
        headers=headers,
        params=params,
        cookies=cookies,
        timeout=timeout,
        body=body,
    )


def parse_body(raw: Any) -> Body | None:
    """Parses a raw body value into a Body domain object.

    Args:
        raw: The raw body value from YAML (dict with format key, or string).

    Returns:
        A Body domain object, or None if no body is provided.
    """
    if raw is None:
        return None

    if isinstance(raw, str):
        return TextBody(data=raw)

    if isinstance(raw, dict):
        if "json" in raw:
            return JsonBody(data=raw["json"])
        elif "xml" in raw:
            return XmlBody(data=str(raw["xml"]))
        elif "form" in raw:
            return FormBody(data=raw["form"])
        elif "files" in raw:
            return FilesBody(data=raw["files"])
        elif "text" in raw:
            return TextBody(data=str(raw["text"]))

    # Fallback: treat the entire dict as JSON body
    return JsonBody(data=raw)


def parse_expect_spec(raw: Any) -> ExpectSpec | None:
    """Parses a raw expect dictionary into an ExpectSpec domain object.

    Args:
        raw: The raw expect dictionary from YAML.

    Returns:
        An ExpectSpec domain object, or None if no expect block is provided.
    """
    if raw is None:
        return None

    status: int | None = raw.get("status")
    headers: dict[str, str] | None = raw.get("headers")
    body = _parse_body_expectation(raw.get("body"))

    return ExpectSpec(
        status=status,
        headers=headers,
        body=body,
    )


def _parse_body_expectation(raw: Any) -> BodyExpectation | None:
    """Parses a raw body expectation into a BodyExpectation domain object.

    Args:
        raw: The raw body expectation from YAML (e.g., {"json": {...}}).

    Returns:
        A BodyExpectation domain object, or None.
    """
    if raw is None:
        return None

    if isinstance(raw, dict):
        for fmt in ContentFormat:
            if fmt in raw:
                return BodyExpectation(format=fmt, spec=raw[fmt])

    raise ValueError(
        f"Body spec must be a dict with one of {list(ContentFormat)} keys, "
        f"got: {type(raw).__name__}"
    )


def parse_extract_spec(raw: Any) -> ExtractSpec | None:
    """Parses a raw extract dictionary into an ExtractSpec domain object.

    Args:
        raw: The raw extract dictionary from YAML.

    Returns:
        An ExtractSpec domain object, or None if no extract block is provided.
    """
    if raw is None:
        return None

    return ExtractSpec(mappings=raw)
