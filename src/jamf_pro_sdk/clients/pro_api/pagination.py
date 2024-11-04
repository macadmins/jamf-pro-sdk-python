from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Iterable, Iterator, List, Optional, Type, Union

from pydantic import BaseModel

if TYPE_CHECKING:
    from . import ProApi


# QUERY FILTERING


@dataclass
class FilterEntry:
    name: str
    op: str
    value: str


class FilterExpression:
    def __init__(self, filter_expression: str, fields: List[FilterEntry]):
        self.filter_expression = filter_expression
        self.fields = fields

    def __str__(self):
        return self.filter_expression

    def _compose(self, expression: FilterExpression, sep: str):
        return FilterExpression(
            filter_expression=f"{self}{sep}{expression.filter_expression}",
            fields=self.fields + expression.fields,
        )

    def __and__(self, expression: FilterExpression):
        return self._compose(expression=expression, sep=";")

    def __or__(self, expression: FilterExpression):
        return self._compose(expression=expression, sep=",")

    def validate(self, allowed_fields: List[str]):
        if not all([i.name in allowed_fields for i in self.fields]):
            raise ValueError(
                f"A field is not in allowed filter fields: {', '.join(allowed_fields)}"
            )


class FilterField:
    def __init__(self, name: str):
        self.name = name

    def _return_expression(self, operator: str, value: Union[bool, int, str]) -> FilterExpression:
        return FilterExpression(
            filter_expression=f"{self.name}{operator}{value}",
            fields=[FilterEntry(name=self.name, op=operator, value=str(value))],
        )

    def eq(self, value: Union[bool, int, str]) -> FilterExpression:
        return self._return_expression("==", value)

    def ne(self, value: Union[bool, int, str]) -> FilterExpression:
        return self._return_expression("!=", value)

    def lt(self, value: Union[bool, int, str]) -> FilterExpression:
        return self._return_expression("<", value)

    def lte(self, value: Union[bool, int, str]) -> FilterExpression:
        return self._return_expression("<=", value)

    def gt(self, value: Union[bool, int, str]) -> FilterExpression:
        return self._return_expression(">", value)

    def gte(self, value: Union[bool, int, str]) -> FilterExpression:
        return self._return_expression(">=", value)

    @staticmethod
    def _iter_to_str(iterable: Iterable):
        return ",".join([str(i) for i in iterable])

    def is_in(self, value: Iterable[Union[bool, int, str]]) -> FilterExpression:
        return self._return_expression("=in=", f"({self._iter_to_str(value)})")

    def not_in(self, value: Iterable[Union[bool, int, str]]) -> FilterExpression:
        return self._return_expression("=out=", f"({self._iter_to_str(value)})")


def filter_group(expression: FilterExpression) -> FilterExpression:
    return FilterExpression(
        filter_expression=f"({expression.filter_expression})",
        fields=expression.fields,
    )


# QUERY SORTING


class SortExpression:
    def __init__(self, sort_expression: str, fields: List[str]):
        self.sort_expression = sort_expression
        self.fields = fields

    def __str__(self):
        return self.sort_expression

    def __and__(self, expression: SortExpression) -> SortExpression:
        return SortExpression(
            sort_expression=f"{self},{expression.sort_expression}",
            fields=self.fields + expression.fields,
        )

    def validate(self, allowed_fields: List[str]):
        if not all([i in allowed_fields for i in self.fields]):
            raise ValueError(f"A field is not in allowed sort fields: {', '.join(allowed_fields)}")


class SortField:
    def __init__(self, field: str):
        self.field = field

    def _return_expression(self, order: str) -> SortExpression:
        return SortExpression(sort_expression=f"{self.field}:{order}", fields=[self.field])

    def asc(self) -> SortExpression:
        return self._return_expression("asc")

    def desc(self) -> SortExpression:
        return self._return_expression("desc")


# PAGINATION


class Page(BaseModel):
    """A page result from a Pro API paginator."""

    page: int
    page_count: int
    total_count: int
    results: list


class Paginator:
    def __init__(
        self,
        api_client: ProApi,
        resource_path: str,
        return_model: Type[BaseModel],
        start_page: int = 0,
        end_page: Optional[int] = None,
        page_size: int = 100,
        sort_expression: Optional[SortExpression] = None,
        filter_expression: Optional[FilterExpression] = None,
        extra_params: Optional[Dict[str, str]] = None,
    ):
        """A paginator for the Jamf Pro API. A paginator automatically iterates over an API if
        multiple unreturned pages are detected in the response. Paginated requests are performed
        concurrently.

        :param api_client: A Jamf Pro API client.
        :type api_client: ProApi

        :param resource_path: The API resource path the paginator will make requests to. This path
            should begin with the API version and not the ``/api`` base path.
        :type resource_path: str

        :param return_model: A Pydantic model to parse the results of the request as. If not set
            the raw JSON response is returned.
        :type return_model: Type[BaseModel]

        :param start_page: (optional) The page to begin returning results from. Generally this value
            should be left at the default (``0``).

            .. note::

                Pages in the Pro API are zero-indexed. In a response that includes 10 pages the first
                page is ``0`` and the last page is ``9``.

        :type start_page: int

        :param end_page: (optional) The page number to stop pagination on. The ``end_page`` argument
            allows for retrieving page ranges (e.g. 2 - 4) or a single page result by using the same
            number for both start and end values.
        :type start_page: int

        :param page_size: (optional) The number of results to include in each requested page. The
            default value is ``100`` and the maximum value is ``2000``.
        :type page_size: int

        :param sort_expression: (optional) The sort fields to apply to the request. See the
            documentation for :ref:`Pro API Sorting` for more information.
        :type sort_expression: SortExpression

        :param filter_expression: (optional) The filter expression to apply to the request. See the
            documentation for :ref:`Pro API Filtering` for more information.
        :type filter_expression: FilterExpression

        :param extra_params: (optional) A dictionary of key-value pairs that will be added to the
            query string parameters of the requests.
        :type extra_params: Dict[str, str]

        """
        self._api_client = api_client
        self.resource_path = resource_path
        self.return_model = return_model
        self.start_page = start_page
        self.end_page = end_page
        self.page_size = page_size
        self.sort_expression = sort_expression
        self.filter_expression = filter_expression
        self.extra_params = extra_params

    def _paginated_request(self, page: int) -> Page:
        query_params: dict = {"page": page, "page-size": self.page_size}
        if self.sort_expression:
            query_params["sort"] = str(self.sort_expression)
        if self.filter_expression:
            query_params["filter"] = str(self.filter_expression)
        if self.extra_params:
            query_params.update(self.extra_params)

        response = self._api_client.api_request(
            method="get", resource_path=self.resource_path, query_params=query_params
        ).json()

        return Page(
            page=page,
            page_count=len(response["results"]),
            total_count=response["totalCount"],
            results=(
                [self.return_model.model_validate(i) for i in response["results"]]
                if self.return_model
                else response["results"]
            ),
        )

    def _request(self) -> Iterator[Page]:
        first_page = self._paginated_request(page=self.start_page)
        yield first_page

        total_count = (
            min(first_page.total_count, (self.end_page + 1) * self.page_size)
            if self.end_page
            else first_page.total_count
        )

        if total_count > (results_count := len(first_page.results)):
            for page in self._api_client.concurrent_api_requests(
                self._paginated_request,
                [
                    {"page": i}
                    for i in range(
                        self.start_page + 1,
                        math.ceil((total_count - results_count) / self.page_size) + 1,
                    )
                ],
            ):
                yield page

    def __call__(self, return_generator: bool = True) -> Union[List, Iterator[Page]]:
        """Call the instantiated paginator to return results.

        :param return_generator: If ``True`` a generator is returned to iterate over pages. If
            ``False`` the results for all pages will be returned in a single list response.
        :type return_generator: bool

        :return: An iterator that yields :class:`~Page` objects, or a list of responses if
            ``return_generator`` is ``False``.
        :rtype: Union[List, Iterator[Page]]
        """
        generator = self._request()
        if return_generator:
            return generator
        else:
            results = []
            for i in sorted([p for p in generator], key=lambda x: x.page):
                results.extend(i.results)

            return results
