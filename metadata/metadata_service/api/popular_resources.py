# Copyright Contributors to the Amundsen project.
# SPDX-License-Identifier: Apache-2.0

from http import HTTPStatus
from typing import Dict, Iterable, List, Mapping, Optional, Union

from amundsen_common.entity.resource_type import ResourceType
from amundsen_common.models.dashboard import DashboardSummarySchema
from amundsen_common.models.table import TableSummarySchema
from flasgger import swag_from
from flask import request
from flask_restful import Resource

from metadata_service.proxy import get_proxy_client


class PopularResourcesAPI(Resource):
    """
    PopularResources API
    """

    def __init__(self) -> None:
        self.client = get_proxy_client()

    @swag_from('swagger_doc/popular_resources_get.yml')
    def get(self, user_id: Optional[str] = None) -> Iterable[Union[Mapping, int, None]]:
        limit = request.args.get('limit', 10, type=int)
        resource_types = request.args.get('types', 'table', type=str)
        resource_types = resource_types.split(',')
        popular_resources: Dict[str, List] = self.client.get_popular_resources(
            num_entries=limit,
            resource_types=resource_types,
            user_id=user_id)

        response: dict = dict()
        response[ResourceType.Table.name] = TableSummarySchema().dump(
            popular_resources.get(ResourceType.Table.name),
            many=True
        )
        response[ResourceType.Dashboard.name] = DashboardSummarySchema().dump(
            popular_resources.get(ResourceType.Dashboard.name),
            many=True
        )
        return response, HTTPStatus.OK
