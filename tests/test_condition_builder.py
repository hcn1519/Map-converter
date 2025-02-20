from openscenario_msgs import Rule, LanePosition, Position, DirectionalDimension, RelativeDistanceType, CoordinateSystem, RoutingAlgorithm, StoryboardElementStateCondition
from openscenario_msgs.parameter_pb2 import ParameterDeclaration, ParameterType
from ads_scenario_transformer.builder.storyboard.by_entity_condition_builder import ByEntityConditionBuilder
from ads_scenario_transformer.builder.storyboard.by_value_condition_builder import ByValueConditionBuilder
from ads_scenario_transformer.builder.storyboard.condition_builder import ConditionBuilder

# Entity Condition


def test_entity_condition_builder_collision(entities, ego_name):

    colliding_npc_name = entities.scenarioObjects[1].name

    builder = ByEntityConditionBuilder(triggering_entity=ego_name)
    builder.make_collision_condition(colliding_entity_name=colliding_npc_name)
    by_entity_condition = builder.get_result()

    assert by_entity_condition is not None
    assert by_entity_condition.triggeringEntities.entityRefs[
        0].entityRef == "ego"
    assert by_entity_condition.entityCondition.collisionCondition is not None
    assert by_entity_condition.entityCondition.collisionCondition.entityRef.entityRef == "car_1"


def test_entity_condition_builder_acceleration(ego_name):
    builder = ByEntityConditionBuilder(triggering_entity=ego_name)
    builder.make_acceleration_condition(value_in_ms=10, rule=Rule.GREATER_THAN)
    by_entity_condition = builder.get_result()

    assert by_entity_condition is not None
    assert by_entity_condition.triggeringEntities.entityRefs[
        0].entityRef == "ego"
    assert by_entity_condition.entityCondition.accelerationCondition.value == 10.0
    assert by_entity_condition.entityCondition.accelerationCondition.rule == Rule.GREATER_THAN


def test_entity_condition_builder_speed(ego_name):

    builder = ByEntityConditionBuilder(triggering_entity=ego_name)
    builder.make_speed_condition(
        direction=DirectionalDimension.DIRECTIONALDIMENSION_LONGITUDINAL,
        value_in_ms=0.001,
        rule=Rule.GREATER_THAN)
    by_entity_condition = builder.get_result()

    assert by_entity_condition is not None
    assert by_entity_condition.triggeringEntities.entityRefs[
        0].entityRef == "ego"

    speed_condition = by_entity_condition.entityCondition.speedCondition
    assert speed_condition.value == 0.001
    assert speed_condition.rule == Rule.GREATER_THAN
    assert speed_condition.direction == DirectionalDimension.DIRECTIONALDIMENSION_LONGITUDINAL


def test_entity_condition_builder_stand_still(ego_name):

    builder = ByEntityConditionBuilder(triggering_entity=ego_name)
    builder.make_stand_still_condition(duration_in_sec=3)
    by_entity_condition = builder.get_result()

    assert by_entity_condition is not None
    assert by_entity_condition.triggeringEntities.entityRefs[
        0].entityRef == "ego"
    assert by_entity_condition.entityCondition.standStillCondition.duration == 3


def test_entity_condition_builder_reach_position(ego_name):

    lane_position = LanePosition(laneId="154", s=10.9835, offset=-0.5042)

    builder = ByEntityConditionBuilder(triggering_entity=ego_name)
    builder.make_reach_position_condition(
        tolerance=1, position=Position(lanePosition=lane_position))
    by_entity_condition = builder.get_result()

    assert by_entity_condition is not None
    assert by_entity_condition.triggeringEntities.entityRefs[
        0].entityRef == "ego"
    assert by_entity_condition.entityCondition.reachPositionCondition.position.lanePosition.laneId == "154"


def test_entity_condition_builder_distance(ego_name):
    lane_position = LanePosition(laneId="154", s=10.9835, offset=-0.5042)

    builder = ByEntityConditionBuilder(triggering_entity=ego_name)
    builder.make_distance_condition(
        coordinateSystem=CoordinateSystem.LANE,
        freespace=True,
        relativeDistanceType=RelativeDistanceType.RELATIVEDISTANCETYPE_LATERAL,
        routingAlgorithm=RoutingAlgorithm.SHORTEST,
        value_in_meter=5,
        rule=Rule.LESS_THAN,
        position=Position(lanePosition=lane_position))
    by_entity_condition = builder.get_result()

    assert by_entity_condition is not None
    assert by_entity_condition.triggeringEntities.entityRefs[
        0].entityRef == "ego"
    assert by_entity_condition.entityCondition.distanceCondition.position.lanePosition.laneId == "154"
    assert by_entity_condition.entityCondition.distanceCondition.value == 5


def test_entity_condition_builder_time_headway(entities, ego_name):

    headway_npc_name = entities.scenarioObjects[1].name

    builder = ByEntityConditionBuilder(triggering_entity=ego_name)
    builder.make_time_headway_condition(
        coordinateSystem=CoordinateSystem.LANE,
        entity_name=headway_npc_name,
        relativeDistanceType=RelativeDistanceType.RELATIVEDISTANCETYPE_LATERAL,
        rule=Rule.GREATER_THAN,
        value_in_sec=3)
    by_entity_condition = builder.get_result()

    assert by_entity_condition is not None
    assert by_entity_condition.triggeringEntities.entityRefs[
        0].entityRef == "ego"
    assert by_entity_condition.entityCondition.timeHeadwayCondition.value == 3
    assert by_entity_condition.entityCondition.timeHeadwayCondition.entityRef == headway_npc_name


def test_entity_condition_builder_relative_distance(entities, ego_name):

    target_npc_name = entities.scenarioObjects[1].name

    builder = ByEntityConditionBuilder(triggering_entity=ego_name)
    builder.make_relative_distance_condition(
        entity_name=target_npc_name,
        relativeDistanceType=RelativeDistanceType.RELATIVEDISTANCETYPE_LATERAL,
        value_in_meter=5,
        freespace=True,
        rule=Rule.GREATER_THAN)
    by_entity_condition = builder.get_result()

    assert by_entity_condition is not None
    assert by_entity_condition.triggeringEntities.entityRefs[
        0].entityRef == "ego"
    assert by_entity_condition.entityCondition.relativeDistanceCondition.value == 5
    assert by_entity_condition.entityCondition.relativeDistanceCondition.entityRef == target_npc_name


# Value Condition


def test_value_condition_builder_parameter(ego_name):

    builder = ByValueConditionBuilder()
    builder.make_parameter_condition(
        parameter_declaration=ParameterDeclaration(
            name="param",
            parameterType=ParameterType.PARAMETERTYPE_INT,
            value="1",
            constraintGroups=[]),
        rule=Rule.GREATER_THAN,
        value="condition_value")

    by_value_condition = builder.get_result()
    assert by_value_condition is not None

    declaration = by_value_condition.parameterCondition.parameterRef
    assert declaration.name == "param"
    assert declaration.parameterType == ParameterType.PARAMETERTYPE_INT


def test_value_condition_builder_simulation_time(ego_name):

    builder = ByValueConditionBuilder()
    builder.make_simulation_time_condition(rule=Rule.GREATER_THAN,
                                           value_in_sec=180)

    by_value_condition = builder.get_result()
    assert by_value_condition is not None
    assert by_value_condition.simulationTimeCondition.rule == Rule.GREATER_THAN
    assert by_value_condition.simulationTimeCondition.value == 180


def test_value_condition_builder_storyboard_element_state(ego_name):

    builder = ByValueConditionBuilder()
    builder.make_storyboard_element_state_condition(
        state=StoryboardElementStateCondition.State.COMPLETE_STATE,
        element_name="act_ego_testspeed_check",
        type=StoryboardElementStateCondition.Type.MANEUVER)

    by_value_condition = builder.get_result()
    assert by_value_condition is not None
    assert by_value_condition.storyboardElementStateCondition.state == StoryboardElementStateCondition.State.COMPLETE_STATE
    assert by_value_condition.storyboardElementStateCondition.storyboardElementRef == "act_ego_testspeed_check"
    assert by_value_condition.storyboardElementStateCondition.storyboardElementType == StoryboardElementStateCondition.Type.MANEUVER


def test_value_condition_builder_user_defined_value_condition(ego_name):
    builder = ByValueConditionBuilder()
    builder.make_user_defined_value_condition(name="test_name",
                                              rule=Rule.GREATER_THAN,
                                              value="test_value")
    by_value_condition = builder.get_result()

    assert by_value_condition is not None
    assert by_value_condition.userDefinedValueCondition.name == "test_name"
    assert by_value_condition.userDefinedValueCondition.rule == Rule.GREATER_THAN
    assert by_value_condition.userDefinedValueCondition.value == "test_value"


def test_value_condition_builder_traffic_signal_condition(ego_name):
    builder = ByValueConditionBuilder()
    builder.make_traffic_signal_condition(name="test_name", state="test_state")
    by_value_condition = builder.get_result()

    assert by_value_condition is not None
    assert by_value_condition.trafficSignalCondition.name == "test_name"
    assert by_value_condition.trafficSignalCondition.state == "test_state"


def test_value_condition_builder_traffic_signal_controller_condition(ego_name):

    builder = ByValueConditionBuilder()
    builder.make_traffic_signal_controller_condition(
        phase="test_phase", traffic_signal_controller_name="StraghtSignal")

    by_value_condition = builder.get_result()

    assert by_value_condition is not None
    assert by_value_condition.trafficSignalControllerCondition.phase == "test_phase"
    assert by_value_condition.trafficSignalControllerCondition.trafficSignalControllerRef == "StraghtSignal"


def test_condtion_builder_by_entity_condition(ego_name, entities):
    builder = ConditionBuilder()

    colliding_npc_name = entities.scenarioObjects[1].name

    by_entity_condition_builder = ByEntityConditionBuilder(
        triggering_entity=ego_name)
    by_entity_condition_builder.make_collision_condition(
        colliding_entity_name=colliding_npc_name)

    builder.make_by_entity_condition(
        by_entity_condition=by_entity_condition_builder.get_result())
    condition = builder.get_result()

    by_entity_condition = condition.byEntityCondition
    assert by_entity_condition is not None
    assert by_entity_condition.triggeringEntities.entityRefs[
        0].entityRef == "ego"
    assert by_entity_condition.entityCondition.collisionCondition is not None
    assert by_entity_condition.entityCondition.collisionCondition.entityRef.entityRef == "car_1"


def test_condtion_builder_by_value_condition(ego_name):
    builder = ConditionBuilder()

    by_value_condition_builder = ByValueConditionBuilder()
    by_value_condition_builder.make_traffic_signal_controller_condition(
        phase="test_phase", traffic_signal_controller_name="StraghtSignal")
    builder.make_by_value_condition(
        by_value_condition=by_value_condition_builder.get_result())
    condition = builder.get_result()
    by_value_condition = condition.byValueCondition
    assert by_value_condition is not None
    assert by_value_condition.trafficSignalControllerCondition.phase == "test_phase"
    assert by_value_condition.trafficSignalControllerCondition.trafficSignalControllerRef == "StraghtSignal"
