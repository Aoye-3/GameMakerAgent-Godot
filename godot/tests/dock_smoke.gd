extends SceneTree


func _init() -> void:
	var dock = preload("res://addons/gamemaker_context/read_only_dock.gd").new()
	root.add_child(dock)
	await process_frame
	if FileAccess.file_exists("res://.vibegame/gamemaker/index.json"):
		push_error("Dock smoke fixture must not create a work index")
		quit(1)
		return
	print("GAMEMAKER_DOCK_READ_ONLY_PASS")
	quit(0)
