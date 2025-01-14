from typing import List
from openscenario_msgs import ScenarioDefinition, ParameterDeclaration, RoadNetwork, Entities, Storyboard, TrafficSignalController
from ads_scenario_transformer.builder import Builder
from ads_scenario_transformer.builder.catalog_locations_builder import CatalogLocationsBuilder
from ads_scenario_transformer.builder.road_network_builder import RoadNetworkBuilder
from ads_scenario_transformer.builder.parameter_declarations_builder import ParameterDeclarationsBuilder, ParameterDeclarationBuilder


class ScenarioDefinitionBuilder(Builder):
    """
    message ScenarioDefinition {
        optional ParameterDeclarations parameterDeclarations = 1;  // 0..*
        required CatalogLocations catalogLocations = 2;           // 1..1
        required RoadNetwork roadNetwork = 3;                     // 1..1
        required Entities entities = 4;                           // 1..1
        required Storyboard storyboard = 5;                       // 1..1
    }
    """

    product: ScenarioDefinition
    parameter_declarations: List[ParameterDeclaration]
    road_network: RoadNetwork
    entities: Entities
    storyboard: Storyboard

    def __init__(self,
                 parameter_declarations: List[ParameterDeclaration] = []):

        params_builder = ParameterDeclarationsBuilder(
            parameterDeclarations=parameter_declarations)
        self.parameter_declarations = params_builder.get_result()
        self.entities = None

    def add_parameter_declaration(self, name: str, parameterType: int,
                                  value: str):
        param = ParameterDeclarationBuilder(name, parameterType,
                                            value).get_result()
        self.parameter_declarations.parameterDeclarations.append(param)

    def make_road_network(self,
                          lanelet_map_path: str,
                          road_network_pcd_map_path: str = "point_cloud.pcd",
                          trafficSignals: List[TrafficSignalController] = []):
        builder = RoadNetworkBuilder(lanelet_map_path, road_network_pcd_map_path,
                                     trafficSignals)
        self.road_network = builder.get_result()

    def make_entities(self, entities: Entities):
        self.entities = entities

    def make_storyboard(self, storyboard: Storyboard):
        self.storyboard = storyboard

    def get_result(self) -> ScenarioDefinition:
        assert self.road_network is not None
        assert self.entities is not None
        assert self.storyboard is not None

        self.product = ScenarioDefinition(
            parameterDeclarations=self.parameter_declarations,
            catalogLocations=CatalogLocationsBuilder().get_result(),
            roadNetwork=self.road_network,
            entities=self.entities,
            storyboard=self.storyboard)
        return self.product
