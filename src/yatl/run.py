import sys
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from requests import Response

from .colors import (
    error,
    header,
    info,
    skipped,
    success,
)
from .extractor import DataExtractor
from .interface import IReporter, ITemplateRenderer
from .render import TemplateRenderer
from .reporter import Reporter
from .step_executor import execute_step
from .utils import create_context, is_skipped, load_test_yaml, search_files
from .validator import ResponseValidator


def run_tests_concurrently(runner, test_path: str = ".", max_workers: int = 10) -> None:
    """Runs all tests in parallel.

    Args:
        runner: Runner instance with a run_test method.
        test_path: Path to directory containing test files.
        max_workers: Maximum number of worker threads, default 10.
    """
    files = search_files(test_path)
    if not files:
        print(skipped(f"No .yatl.yaml files found in {test_path}"))
        return

    print(info(f"Found {len(files)} test file(s)"))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(runner.run_test, file): file for file in files}
        error_messages = []
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                error_messages.append(f"Test {futures[future]} failed with error: {e}")

        if error_messages:
            print(error(f"{len(error_messages)} test(s) failed"))
            for message in error_messages:
                print(error(message))
            sys.exit(1)


def run_test_not_concurrently(runner, test_path: str = ".") -> None:
    """Runs all tests one by one.

    Args:
        runner: Runner instance with a run_test method.
        test_path: Path to directory containing test files.
    """
    files = search_files(test_path)
    error_messages = []

    if not files:
        print(skipped(f"No .yatl.yaml files found in {test_path}"))
        return

    print(info(f"Found {len(files)} test file(s)"))

    for file in files:
        try:
            runner.run_test(file)
        except Exception as e:
            error_messages.append(f"Test {file} failed with error: {e}")

    if error_messages:
        print(error(f"{len(error_messages)} test(s) failed"))
        for message in error_messages:
            print(error(message))
        sys.exit(1)


class Runner:
    """Orchestrates the execution of YAML-based test suites.

    Loads test specifications from YAML files, runs each step sequentially,
    and maintains a context that is passed between steps.
    """

    def __init__(
        self,
        data_extractor: DataExtractor,
        template_renderer: ITemplateRenderer,
        response_validator_factory: Callable[
            [Response, dict[str, Any]], Any
        ] = ResponseValidator,
        reporter_factory: Callable[[], IReporter] = Reporter,
    ):
        """Initializes the runner with required services.

        Args:
            data_extractor: Used to extract values from responses.
            template_renderer: Used to render templates in the step.
            response_validator_factory: Factory function that creates a validator instance
                from a response and expectation dictionary.
            reporter_factory: Factory function that creates a reporter instance.
        """
        self.data_extractor = data_extractor
        self.template_renderer = template_renderer
        self.response_validator_factory = response_validator_factory
        self.reporter_factory = reporter_factory

    def _process_step(
        self,
        step_number: int,
        step: dict,
        context: dict,
        reporter: IReporter,
        is_parametrize_step: bool = False,
        data: tuple = None,
    ) -> dict[Any, Any]:
        """Execute a single step.

        Args:
            step_number: Step number in the test.
            step: Parsed YAML dictionary.
            context: Current context dictionary.
            reporter: Reporter instance for logging.

        Returns:
            Updated context dictionary.
        """

        if step is None:
            return context

        if is_skipped(step):
            reporter.add_info(
                skipped(f"Step {step_number}: {step.get('name', '')} skipped")
            )
            return context

        elif is_parametrize_step:
            reporter.add_info(info(f"Step {step_number}, params: {data}"))

            return execute_step(
                step,
                context,
                self.data_extractor,
                self.template_renderer,
                self.response_validator_factory,
            )

        else:
            reporter.add_info(info(f"Step {step_number}: {step.get('name', '')}"))

            if step.get("description"):
                reporter.add_info(info(f"description: {step['description']}"))

            return execute_step(
                step,
                context,
                self.data_extractor,
                self.template_renderer,
                self.response_validator_factory,
            )

    def run_test(self, yaml_path: str) -> None:
        """Executes a single test file.

        Loads the test, creates the initial context, runs each step in order,
        and prints progress messages. The context is updated after each step
        with extracted values.

        Args:
            yaml_path: Path to the test YAML file.
        """
        test_specification = load_test_yaml(yaml_path)
        if test_specification is None:
            return

        context = create_context(test_specification)
        reporter = self.reporter_factory()

        # Use filename as fallback when name is not specified
        test_name = test_specification.get("name") or Path(yaml_path).name

        if is_skipped(test_specification):
            reporter.add_info(skipped(f"Test {test_name} skipped"))
            reporter.print_info()
            return

        reporter.add_info(header("-" * 10))
        reporter.add_info(header(f"Run test: {test_name}"))
        steps: list[dict] = test_specification.get("steps", [])
        step_number = 1

        for step in steps:
            parametrize = step.get("parametrize", None)
            if parametrize:
                for param in parametrize:
                    data = tuple(v for v in param.values())
                    for k, v in param.items():
                        context[k] = v
                    context = self._process_step(
                        step_number,
                        step,
                        context,
                        reporter,
                        is_parametrize_step=True,
                        data=data,
                    )
                    step_number += 1
            else:
                context = self._process_step(step_number, step, context, reporter)
                step_number += 1

        reporter.add_info(success("Test passed"))
        reporter.print_info()


if __name__ == "__main__":
    runner = Runner(DataExtractor(), TemplateRenderer(), ResponseValidator, Reporter)
    run_tests_concurrently(runner, max_workers=10)
