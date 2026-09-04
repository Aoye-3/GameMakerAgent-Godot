extends SceneTree


func _init() -> void:
	var before := hashes("res://")
	var dock = load("res://addons/gamemaker_context/read_only_dock.gd").new()
	root.add_child(dock)
	await process_frame
	dock.reload_index()
	var after := hashes("res://")
	print(dock.summary.text)
	var ok: bool = before == after and "Source: CURRENT" in dock.summary.text and "· PASS" in dock.summary.text
	print("TRIAL_DOCK_READ_ONLY_PASS" if ok else "TRIAL_DOCK_CHECK_FAILED")
	quit(0 if ok else 1)


func hashes(folder: String) -> Dictionary:
	var result := {}
	var directory := DirAccess.open(folder)
	for name in directory.get_directories():
		if name in [".godot", ".git", "addons"] or directory.is_link(name):
			continue
		result.merge(hashes(folder + name + "/"))
	for name in directory.get_files():
		result[folder + name] = FileAccess.get_sha256(folder + name)
	return result
