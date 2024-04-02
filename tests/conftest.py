import pytest
import yaml
from typing import List
from openscenario_msgs import GlobalAction, Entities, Position, LanePosition, WorldPosition, TransitionDynamics, AbsoluteTargetSpeed, RelativeTargetSpeed, FollowingMode, Properties, Property, Controller, ControllerAction, AssignControllerAction, TeleportAction, Waypoint, Route, Trajectory, ReferenceContext, TimeReference, Timing, Action
from openscenario_msgs.common_pb2 import InfrastructureAction, EntityAction, LaneChangeAction, UserDefinedAction, PrivateAction, SpeedTargetValueType, SpeedAction
from scenario_transfer.builder.story_board.global_action_builder import GlobalActionBuilder
from scenario_transfer.builder.story_board.user_defined_action_builder import UserDefinedActionBuilder
from scenario_transfer.builder.entities_builder import EntityType, EntitiesBuilder
from scenario_transfer.openscenario.openscenario_coder import OpenScenarioDecoder

@pytest.fixture
def entities() -> Entities:
    builder = EntitiesBuilder(entities=[
        EntityType.NPC, EntityType.NPC, EntityType.EGO, EntityType.PEDESTRIAN,
        EntityType.NPC
    ])
    return builder.get_result()


@pytest.fixture
def ego_name(entities) -> str:
    return entities.scenarioObjects[0].name


@pytest.fixture
def transition_dynamics() -> TransitionDynamics:
    return TransitionDynamics(
        dynamicsDimension=TransitionDynamics.DynamicsDimension.RATE,
        dynamicsShape=TransitionDynamics.DynamicsShape.LINEAR,
        followingMode=FollowingMode.FOLLOWINGMODE_FOLLOW,
        value=1.0)


@pytest.fixture
def properties() -> Properties:
    return Properties(properties=[
        Property(name="isEgo", value="true"),
        Property(name="maxSpeed", value="50")
    ])


@pytest.fixture
def controller(properties) -> Controller:
    return Controller(name="controller",
                      properties=properties,
                      parameterDeclarations=[])


@pytest.fixture
def lane_position() -> LanePosition:
    return LanePosition(laneId="154", s=10.9835, offset=-0.5042)


@pytest.fixture
def world_position() -> WorldPosition:
    return WorldPosition(x=37.416880423172465, y=-122.01593194093681, z=0.0)


@pytest.fixture
def waypoints() -> List[Waypoint]:
    with open("tests/data/openscenario_route.yaml", "r") as file:
        input = file.read()

    dict = yaml.safe_load(input)
    openscenario_route = OpenScenarioDecoder.decode_yaml_to_pyobject(
        yaml_dict=dict, type_=Route, exclude_top_level_key=True)

    return openscenario_route.waypoints


@pytest.fixture
def trajectory() -> Trajectory:
    with open("tests/data/openscenario_trajectory.yaml", "r") as file:
        input = file.read()

    dict = yaml.safe_load(input)
    trajectory = OpenScenarioDecoder.decode_yaml_to_pyobject(
        yaml_dict=dict, type_=Trajectory, exclude_top_level_key=True)
    return trajectory


@pytest.fixture
def time_reference() -> TimeReference:
    return TimeReference(timing=Timing(
        domainAbsoluteRelative=ReferenceContext.REFERENCECONTEXT_RELATIVE,
        offset=0.0,
        scale=1))