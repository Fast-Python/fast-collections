from typing import Any

import requests
from requests import Response, request

from yatl.exceptions import YATLRequestError


def send_request(context: dict[str, Any], resolved_step: dict[str, Any]) -> Response:
    """Builds and sends the HTTP request described by the step.

    Args:
        context: The current context (contains base_url, previous extracts, etc.)
        resolved_step: The step dictionary after template rendering.

    Returns:
        The HTTP response object.

    Raises:
        YATLRequestError: If a network-level error occurs (timeout or
            connection failure).
    """
    request_data = build_request_data(context, resolved_step)
    try:
        response = request(**request_data)
        return response
    except requests.exceptions.Timeout as e:
        timeout_value = request_data.get("timeout")
        if timeout_value is not None:
            msg = f"Request timed out after {timeout_value}s: {request_data['method']} {request_data['url']}"
        else:
            msg = f"Request timed out (no explicit timeout set): {request_data['method']} {request_data['url']}"
        raise YATLRequestError(msg) from e
    except requests.exceptions.ConnectionError as e:
        raise YATLRequestError(
            f"Connection failed: {request_data['method']} {request_data['url']}"
        ) from e


def build_request_data(
    context: dict[str, Any], resolved_step: dict[str, Any]
) -> dict[str, Any]:
    """Produces the keyword arguments for `requests.request`.

    Extracts method, URL, headers, parameters, cookies, timeout, and body
    from the step's `request` block. Automatically sets Content-Type headers
    based on the body format (JSON, XML, text, form-data, files).

    Returns:
        A dictionary that can be unpacked as `requests.request(**kwargs)`.

    Raises:
        ValueError: If the body has an unsupported type.
    """
    request_data: dict[str, Any] = resolved_step["request"]
    method, url, timeout, headers, params, cookies, body = extract_request_params(
        request_data
    )

    url = build_url(context.get("base_url", ""), url)

    kwargs: dict[str, Any] = {
        "method": method,
        "url": url,
        "timeout": timeout,
        "headers": headers,
        "params": params,
        "cookies": cookies,
    }

    if body is not None:
        process_body(body, headers, kwargs)

    kwargs["headers"] = headers
    return kwargs


def build_url(base_url: str, url: str) -> str:
    """Constructs a full URL by prepending the base URL from context.

    Args:
        base_url: The base URL from context (may be empty).
        url: The relative or absolute URL from the step.

    Returns:
        The absolute URL. If the context contains a `base_url`, it is
        prepended (with proper slash handling). If `url` is already absolute, the base URL is ignored
    """
    if url.startswith("http://") or url.startswith("https://"):
        return url

    if not base_url:
        return url

    if not base_url.startswith("http"):
        base_url = "https://" + base_url

    return base_url.rstrip("/") + "/" + url.lstrip("/")


def extract_request_params(
    request_data: dict[str, Any],
) -> tuple[str, str, Any, dict, dict, dict, Any]:
    """Extracts request parameters from the request data dictionary.

    Returns:
        tuple of (method, url, timeout, headers, params, cookies, body)
    """
    method = str(request_data.get("method", "GET")).upper()
    url: str = request_data.get("url", "")
    timeout = request_data.get("timeout", None)
    headers = request_data.get("headers", {})
    body: dict[str, Any] | str | None = request_data.get("body", None)
    params = request_data.get("params", {})
    cookies = request_data.get("cookies", {})

    return method, url, timeout, headers, params, cookies, body


def process_body(
    body: dict[str, Any] | str, headers: dict[str, str], kwargs: dict[str, Any]
) -> None:
    """Processes the request body and updates kwargs and headers accordingly.

    Args:
        body: The body from the request data.
        headers: The headers dictionary (may be modified).
        kwargs: The kwargs dictionary for requests.request (may be modified).

    Raises:
        ValueError: If the body has an unsupported type.
    """
    if isinstance(body, dict):
        for format, fmt, key in [
            ("json", "application/json", "json"),
            ("text", "text/plain", "data"),
            ("form", "application/x-www-form-urlencoded", "data"),
        ]:
            if format in body:
                kwargs[key] = body[format]
                _set_content_type(headers, fmt)

        if "xml" in body:
            xml_content = body["xml"]
            if isinstance(xml_content, str):
                kwargs["data"] = xml_content
                _set_content_type(headers, "application/xml")

        if "files" in body:
            kwargs["files"] = body["files"]

    elif isinstance(body, str):
        kwargs["data"] = body
        _set_content_type(headers, "text/plain")
    else:
        raise ValueError(f"Unsupported body type: {type(body)}")


def _set_content_type(headers: dict[str, str], content_type: str) -> None:
    """Sets the Content-Type header if not already present.

    Args:
        headers: The headers dictionary (modified in place).
        content_type: The content type to set.
    """
    if "Content-Type" not in headers:
        headers["Content-Type"] = content_type
