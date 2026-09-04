@tool
extends McpTestSuite

func suite_name() -> String:
	return "trial"

func test_scene_has_player_visual_and_collision() -> void:
	var scene = track(load("res://scenes/mcp_trial.tscn").instantiate())
	assert_true(scene.has_node("Player/Visual"), "Player visual must exist")
	assert_true(scene.has_node("Player/Collision"), "Player collision must exist")
	assert_true(scene.has_node("Target/Collision"), "Target collision must exist")

func test_four_custom_actions_are_unique() -> void:
	for action in ["move_left", "move_right", "move_up", "move_down"]:
		assert_true(ProjectSettings.has_setting("input/" + action), action)
		if InputMap.has_action(action):
			assert_eq(InputMap.action_get_events(action).size(), 2, "WASD plus arrows only")

func test_no_duplicate_root_children() -> void:
	var scene = track(load("res://scenes/mcp_trial.tscn").instantiate())
	assert_eq(scene.get_child_count(), 2, "Exactly Player and Target")
	assert_eq(scene.get_node("Player").get_child_count(), 2, "Exactly visual and collision")

func test_dock_load_and_refresh_are_read_only() -> void:
	var dock = track(load("res://addons/gamemaker_context/read_only_dock.gd").new())
	var before = _hash_project("res://")
	dock._ready()
	dock.reload_index()
	var after = _hash_project("res://")
	assert_eq(after, before, "Dock must not change native files or records")

func _hash_project(folder: String) -> Dictionary:
	var result = {}
	var dir = DirAccess.open(folder)
	for name in dir.get_directories():
		if name in [".godot", ".git", "addons"]:
			continue
		result.merge(_hash_project(folder + name + "/"))
	for name in dir.get_files():
		result[folder + name] = FileAccess.get_sha256(folder + name)
	return result

