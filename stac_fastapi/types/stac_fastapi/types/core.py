"""Base clients."""
import abc
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Union
from urllib.parse import urljoin

import attr
from stac_pydantic.api import Search
from stac_pydantic.links import Relations
from stac_pydantic.shared import MimeTypes
from stac_pydantic.version import STAC_VERSION
from fastapi import Request

from stac_fastapi.types import stac as stac_types
from stac_fastapi.types.extension import ApiExtension

NumType = Union[float, int]
StacType = Dict[str, Any]


@attr.s  # type:ignore
class BaseTransactionsClient(abc.ABC):
    """Defines a pattern for implementing the STAC transaction extension."""

    @abc.abstractmethod
    def create_item(self, collection_id: str, item: stac_types.Item, request: Request) -> stac_types.Item:
        """Create a new item.

        Called with `POST /collections/{collection_id}/items`.

        Args:
            collection_id: ID of the collection to add item to.
            item: the item
            request: starlette request object

        Returns:
            The item that was created.

        """
        ...

    @abc.abstractmethod
    def update_item(self, collection_id: str,
                          item_id: str, item: stac_types.Item, request: Request
                          ) -> stac_types.Item:
        """Perform a complete update on an existing item.

        Called with `PUT /collections/{collection_id}/items/{item_id}`. It is expected that this item already exists.
        The update should do a diff against the saved item and perform any necessary updates.
        Partial updates are not supported by the transactions extension.

        Args:
            collection_id: the ID of the item's collection
            item_id: the ID of the item
            item: the item (must be complete)
            request: starlette request object

        Returns:
            The updated item.
        """
        ...

    @abc.abstractmethod
    def delete_item(
        self, item_id: str, collection_id: str, request: Request
    ) -> stac_types.Item:
        """Delete an item from a collection.

        Called with `DELETE /collections/{collection_id}/items/{item_id}`

        Args:
            item_id: id of the item.
            collection_id: id of the collection.
            request: starlette request object.

        Returns:
            The deleted item.
        """
        ...

    @abc.abstractmethod
    def create_collection(
        self, collection: stac_types.Collection, request: Request
    ) -> stac_types.Collection:
        """Create a new collection.

        Called with `POST /collections`.

        Args:
            collection: the collection
            request: starlette request object

        Returns:
            The collection that was created.
        """
        ...

    @abc.abstractmethod
    def update_collection(
        self, collection_id: str, collection: stac_types.Collection, request: Request,
    ) -> stac_types.Collection:
        """Perform a complete update on an existing collection.

        Called with `PUT /collections/{collection_id}`. It is expected that this item already exists.
        The update should do a diff against the saved collection and perform any necessary updates.
        Partial updates are not supported by the transactions extension.

        Args:
            collection_id: id of the collection
            collection: the collection (must be complete)
            request: starlette request object

        Returns:
            The updated collection.
        """
        ...

    @abc.abstractmethod
    def delete_collection(
        self, collection_id: str, request: Request
    ) -> stac_types.Collection:
        """Delete a collection.

        Called with `DELETE /collections/{collection_id}`

        Args:
            collection_id: id of the collection.
            request: starlette request object

        Returns:
            The deleted collection.
        """
        ...


@attr.s  # type:ignore
class AsyncBaseTransactionsClient(abc.ABC):
    """Defines a pattern for implementing the STAC transaction extension."""

    @abc.abstractmethod
    async def create_item(self, collection_id: str, item: stac_types.Item, request: Request) -> stac_types.Item:
        """Create a new item.

        Called with `POST /collections/{collection_id}/items`.

        Args:
            collection_id: ID of the collection to add item to.
            item: the item
            request: starlette request object

        Returns:
            The item that was created.

        """
        ...

    @abc.abstractmethod
    async def update_item(self, collection_id: str,
                          item_id: str, item: stac_types.Item, request: Request
                          ) -> stac_types.Item:
        """Perform a complete update on an existing item.

        Called with `PUT /collections/{collection_id}/items/{item_id}`. It is expected that this item already exists.
        The update should do a diff against the saved item and perform any necessary updates.
        Partial updates are not supported by the transactions extension.

        Args:
            collection_id: the ID of the item's collection
            item_id: the ID of the item
            item: the item (must be complete)
            request: starlette request object

        Returns:
            The updated item.
        """
        ...

    @abc.abstractmethod
    async def delete_item(
        self, item_id: str, collection_id: str, request: Request
    ) -> stac_types.Item:
        """Delete an item from a collection.

        Called with `DELETE /collections/{collection_id}/items/{item_id}`

        Args:
            item_id: id of the item.
            collection_id: id of the collection.
            request: starlette request object.

        Returns:
            The deleted item.
        """
        ...

    @abc.abstractmethod
    async def create_collection(
        self, collection: stac_types.Collection, request: Request
    ) -> stac_types.Collection:
        """Create a new collection.

        Called with `POST /collections`.

        Args:
            collection: the collection
            request: starlette request object

        Returns:
            The collection that was created.
        """
        ...

    @abc.abstractmethod
    async def update_collection(
        self, collection_id: str, collection: stac_types.Collection, request: Request,
    ) -> stac_types.Collection:
        """Perform a complete update on an existing collection.

        Called with `PUT /collections/{collection_id}`. It is expected that this item already exists.
        The update should do a diff against the saved collection and perform any necessary updates.
        Partial updates are not supported by the transactions extension.

        Args:
            collection_id: id of the collection
            collection: the collection (must be complete)
            request: starlette request object

        Returns:
            The updated collection.
        """
        ...

    @abc.abstractmethod
    async def delete_collection(
        self, collection_id: str, request: Request
    ) -> stac_types.Collection:
        """Delete a collection.

        Called with `DELETE /collections/{collection_id}`

        Args:
            collection_id: id of the collection.
            request: starlette request object

        Returns:
            The deleted collection.
        """
        ...


@attr.s
class LandingPageMixin:
    """Create a STAC landing page (GET /)."""

    stac_version: str = attr.ib(default=STAC_VERSION)
    landing_page_id: str = attr.ib(default="stac-fastapi")
    title: str = attr.ib(default="stac-fastapi")
    description: str = attr.ib(default="stac-fastapi")

    def _landing_page(self, base_url: str) -> stac_types.LandingPage:
        landing_page = stac_types.LandingPage(
            type="Catalog",
            id=self.landing_page_id,
            title=self.title,
            description=self.description,
            stac_version=self.stac_version,
            conformsTo=[
                "https://stacspec.org/STAC-api.html",
                "http://docs.opengeospatial.org/is/17-069r3/17-069r3.html#ats_geojson",
            ],
            links=[
                {
                    "rel": Relations.self.value,
                    "type": MimeTypes.json,
                    "href": base_url,
                },
                {
                    "rel": "data",
                    "type": MimeTypes.json,
                    "href": urljoin(base_url, "collections"),
                },
                {
                    "rel": Relations.docs.value,
                    "type": MimeTypes.json,
                    "title": "OpenAPI docs",
                    "href": urljoin(base_url, "docs"),
                },
                {
                    "rel": Relations.conformance.value,
                    "type": MimeTypes.json,
                    "title": "STAC/WFS3 conformance classes implemented by this server",
                    "href": urljoin(base_url, "conformance"),
                },
                {
                    "rel": Relations.search.value,
                    "type": MimeTypes.json,
                    "title": "STAC search",
                    "href": urljoin(base_url, "search"),
                },
            ],
            stac_extensions=[],
        )

        if self.extension_is_enabled("FilterExtension"):
            landing_page["links"].append(
                {
                    "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
                    "type": MimeTypes.geojson,
                    "title": "Filter Queryables",
                    "href": urljoin(str(base_url), "queryables"),
                }
            )

        return landing_page


@attr.s  # type:ignore
class BaseCoreClient(LandingPageMixin, abc.ABC):
    """Defines a pattern for implementing STAC api core endpoints.

    Attributes:
        extensions: list of registered api extensions.
    """

    extensions: List[ApiExtension] = attr.ib(default=attr.Factory(list))

    def extension_is_enabled(self, extension: str) -> bool:
        """Check if an api extension is enabled."""
        return any([type(ext).__name__ == extension for ext in self.extensions])

    def list_conformance_classes(self):
        """Return a list of conformance classes, including implemented extensions."""
        base_conformance = [
            "https://api.stacspec.org/v1.0.0-beta.2/core",
            "https://api.stacspec.org/v1.0.0-beta.2/ogcapi-features",
            "https://api.stacspec.org/v1.0.0-beta.2/item-search",
        ]

        for extension in self.extensions:
            extension_classes = getattr(extension, "conformance_classes", [])
            base_conformance.extend(extension_classes)

        return base_conformance

    def landing_page(self, **kwargs) -> stac_types.LandingPage:
        """Landing page.

        Called with `GET /`.

        Returns:
            API landing page, serving as an entry point to the API.
        """
        base_url = str(kwargs["request"].base_url)

        landing_page = self._landing_page(base_url=base_url)
        landing_page["conformsTo"] = self.list_conformance_classes()
        collections = self.all_collections(request=kwargs["request"])
        for collection in collections["collections"]:
            landing_page["links"].append(
                {
                    "rel": Relations.child.value,
                    "type": MimeTypes.json.value,
                    "title": collection.get("title") or collection.get("id"),
                    "href": urljoin(base_url, f"collections/{collection['id']}"),
                }
            )
        return landing_page

    @abc.abstractmethod
    def conformance(self, **kwargs) -> stac_types.Conformance:
        """Conformance classes.

        Called with `GET /conformance`.

        Returns:
            Conformance classes which the server conforms to.
        """
        ...

    @abc.abstractmethod
    def post_search(
        self, search_request: Search, **kwargs
    ) -> stac_types.ItemCollection:
        """Cross catalog search (POST).

        Called with `POST /search`.

        Args:
            search_request: search request parameters.

        Returns:
            ItemCollection containing items which match the search criteria.
        """
        ...

    @abc.abstractmethod
    def get_search(
        self,
        collections: Optional[List[str]] = None,
        ids: Optional[List[str]] = None,
        bbox: Optional[List[NumType]] = None,
        datetime: Optional[Union[str, datetime]] = None,
        limit: Optional[int] = 10,
        query: Optional[str] = None,
        token: Optional[str] = None,
        fields: Optional[List[str]] = None,
        sortby: Optional[str] = None,
        **kwargs,
    ) -> stac_types.ItemCollection:
        """Cross catalog search (GET).

        Called with `GET /search`.

        Returns:
            ItemCollection containing items which match the search criteria.
        """
        ...

    @abc.abstractmethod
    def get_item(self, item_id: str, collection_id: str, **kwargs) -> stac_types.Item:
        """Get item by id.

        Called with `GET /collections/{collectionId}/items/{itemId}`.

        Args:
            item_id: Id of the item.
            collection_id: Id of the collection.

        Returns:
            Item.
        """
        ...

    @abc.abstractmethod
    def all_collections(self, **kwargs) -> List[stac_types.Collection]:
        """Get all available collections.

        Called with `GET /collections`.

        Returns:
            A list of collections.
        """
        ...

    @abc.abstractmethod
    def get_collection(self, collection_id: str, **kwargs) -> stac_types.Collection:
        """Get collection by id.

        Called with `GET /collections/{collectionId}`.

        Args:
            collection_id: Id of the collection.

        Returns:
            Collection.
        """
        ...

    @abc.abstractmethod
    def item_collection(
        self, collection_id: str, limit: int = 10, token: str = None, **kwargs
    ) -> stac_types.ItemCollection:
        """Get all items from a specific collection.

        Called with `GET /collections/{collectionId}/items`

        Args:
            collection_id: id of the collection.
            limit: number of items to return.
            token: pagination token.

        Returns:
            An ItemCollection.
        """
        ...


@attr.s  # type:ignore
class AsyncBaseCoreClient(LandingPageMixin, abc.ABC):
    """Defines a pattern for implementing STAC api core endpoints.

    Attributes:
        extensions: list of registered api extensions.
    """

    extensions: List[ApiExtension] = attr.ib(default=attr.Factory(list))

    def extension_is_enabled(self, extension: Type[ApiExtension]) -> bool:
        """Check if an api extension is enabled."""
        return any([isinstance(ext, extension) for ext in self.extensions])

    async def landing_page(self, **kwargs) -> stac_types.LandingPage:
        """Landing page.

        Called with `GET /`.

        Returns:
            API landing page, serving as an entry point to the API.
        """
        base_url = str(kwargs["request"].base_url)
        landing_page = self._landing_page(base_url=base_url)
        collections = await self.all_collections(request=kwargs["request"])
        for collection in collections:
            landing_page["links"].append(
                {
                    "rel": Relations.child.value,
                    "type": MimeTypes.json.value,
                    "title": collection.get("title"),
                    "href": urljoin(base_url, f"collections/{collection['id']}"),
                }
            )
        return landing_page

    @abc.abstractmethod
    async def conformance(self, **kwargs) -> stac_types.Conformance:
        """Conformance classes.

        Called with `GET /conformance`.

        Returns:
            Conformance classes which the server conforms to.
        """
        ...

    @abc.abstractmethod
    async def post_search(
        self, search_request: Search, **kwargs
    ) -> stac_types.ItemCollection:
        """Cross catalog search (POST).

        Called with `POST /search`.

        Args:
            search_request: search request parameters.

        Returns:
            ItemCollection containing items which match the search criteria.
        """
        ...

    @abc.abstractmethod
    async def get_search(
        self,
        collections: Optional[List[str]] = None,
        ids: Optional[List[str]] = None,
        bbox: Optional[List[NumType]] = None,
        datetime: Optional[Union[str, datetime]] = None,
        limit: Optional[int] = 10,
        query: Optional[str] = None,
        token: Optional[str] = None,
        fields: Optional[List[str]] = None,
        sortby: Optional[str] = None,
        **kwargs,
    ) -> stac_types.ItemCollection:
        """Cross catalog search (GET).

        Called with `GET /search`.

        Returns:
            ItemCollection containing items which match the search criteria.
        """
        ...

    @abc.abstractmethod
    async def get_item(
        self, item_id: str, collection_id: str, **kwargs
    ) -> stac_types.Item:
        """Get item by id.

        Called with `GET /collections/{collectionId}/items/{itemId}`.

        Args:
            item_id: Id of the item.
            collection_id: Id of the collection.

        Returns:
            Item.
        """
        ...

    @abc.abstractmethod
    async def all_collections(self, **kwargs) -> List[stac_types.Collection]:
        """Get all available collections.

        Called with `GET /collections`.

        Returns:
            A list of collections.
        """
        ...

    @abc.abstractmethod
    async def get_collection(
        self, collection_id: str, **kwargs
    ) -> stac_types.Collection:
        """Get collection by id.

        Called with `GET /collections/{collectionId}`.

        Args:
            collection_id: Id of the collection.

        Returns:
            Collection.
        """
        ...

    @abc.abstractmethod
    async def item_collection(
        self, collection_id: str, limit: int = 10, token: str = None, **kwargs
    ) -> stac_types.ItemCollection:
        """Get all items from a specific collection.

        Called with `GET /collections/{collectionId}/items`

        Args:
            collection_id: id of the collection.
            limit: number of items to return.
            token: pagination token.

        Returns:
            An ItemCollection.
        """
        ...


@attr.s
class BaseFiltersClient(abc.ABC):
    """Defines a pattern for implementing the STAC filter extension."""

    def get_queryables(
        self, collection_id: Optional[str] = None, **kwargs
    ) -> Dict[str, Any]:
        """Get the queryables available for the given collection_id.

        If collection_id is None, returns the intersection of all
        queryables over all collections.

        This base implementation returns a blank queryable schema. This is not allowed
        under OGC CQL but it is allowed by the STAC API Filter Extension

        https://github.com/radiantearth/stac-api-spec/tree/master/fragments/filter#queryables
        """
        return {
            "$schema": "https://json-schema.org/draft/2019-09/schema",
            "$id": "https://example.org/queryables",
            "type": "object",
            "title": "Queryables for Example STAC API",
            "description": "Queryable names for the example STAC API Item Search filter.",
            "properties": {},
        }


@attr.s
class AsyncBaseFiltersClient(abc.ABC):
    """Defines a pattern for implementing the STAC filter extension."""

    async def get_queryables(
        self, collection_id: Optional[str] = None, **kwargs
    ) -> Dict[str, Any]:
        """Get the queryables available for the given collection_id.

        If collection_id is None, returns the intersection of all
        queryables over all collections.

        This base implementation returns a blank queryable schema. This is not allowed
        under OGC CQL but it is allowed by the STAC API Filter Extension

        https://github.com/radiantearth/stac-api-spec/tree/master/fragments/filter#queryables
        """
        return {
            "$schema": "https://json-schema.org/draft/2019-09/schema",
            "$id": "https://example.org/queryables",
            "type": "object",
            "title": "Queryables for Example STAC API",
            "description": "Queryable names for the example STAC API Item Search filter.",
            "properties": {},
        }
