extends SceneTree


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	var packed_scene := load("res://scenes/runtime_probe.tscn") as PackedScene
	if packed_scene == null:
		_fail("runtime probe scene could not be loaded")
		return

	var probe := packed_scene.instantiate()
	root.add_child(probe)
	await process_frame

	if not probe.is_in_group("gamemaker_watch"):
		_fail("runtime probe is missing the gamemaker_watch group")
		return

	var initial_state: Dictionary = probe._gamemaker_state()
	if initial_state.get("contract_version") != "0.1":
		_fail("unexpected contract version: %s" % JSON.stringify(initial_state))
		return

	var event := InputEventAction.new()
	event.action = &"verify_trigger"
	event.pressed = true
	probe._unhandled_input(event)

	var changed_state: Dictionary = probe._gamemaker_state()
	if changed_state.get("verification_value") != 10 or changed_state.get("trigger_count") != 1:
		_fail("unexpected state after verify_trigger: %s" % JSON.stringify(changed_state))
		return

	print("GAMEMAKER_PROBE_SMOKE_PASS ", JSON.stringify(changed_state))
	quit(0)


func _fail(message: String) -> void:
	push_error("GAMEMAKER_PROBE_SMOKE_FAIL " + message)
	quit(1)
