@tool
extends VBoxContainer

const INDEX_PATH := "res://.vibegame/gamemaker/index.json"

var heading := Label.new()
var summary := RichTextLabel.new()
var last_modified := 0
var refresh_elapsed := 0.0


func _ready() -> void:
	name = "GameMaker Context"
	heading.text = "GameMaker Context · read only"
	summary.fit_content = true
	summary.custom_minimum_size = Vector2(300, 240)
	add_child(heading)
	add_child(summary)
	reload_index()
	set_process(true)


func _process(delta: float) -> void:
	refresh_elapsed += delta
	if refresh_elapsed >= 2.0:
		refresh_elapsed = 0.0
		reload_index()


func reload_index() -> void:
	last_modified = FileAccess.get_modified_time(INDEX_PATH)
	if not FileAccess.file_exists(INDEX_PATH):
		summary.text = "No .vibegame/gamemaker/index.json record found."
		return
	var parsed := read_record(INDEX_PATH)
	if parsed.is_empty():
		summary.text = "The GameMaker work index is invalid JSON."
		return
	var expected = parsed.get("source_files", {})
	var current := source_hashes("res://")
	var fresh: bool = not expected.is_empty() and expected == current
	var lines: Array[String] = ["Source: %s" % ("CURRENT" if fresh else "STALE / UNVERIFIED")]
	var environment := read_record("res://.vibegame/gamemaker/environment.json")
	lines.append("Provider (last recorded): %s" % environment.get("provider_status", "not recorded"))
	for work in parsed.get("works", []):
		if not work is Dictionary:
			continue
		var base := "res://" + str(work.get("path", "")) + "/"
		var production := read_record(base + "production-card.json")
		var decision := read_record(base + "decision-card.json")
		var assets := read_record(base + "normalized-assets.json")
		var implementation := read_record(base + "implementation.json")
		var evidence := read_record(base + "evidence/evidence-bundle.json")
		var intact := evidence_intact(evidence)
		var same_revision: bool = implementation.get("source_revision", "") == parsed.get("project_revision", "unknown")
		var verdict := str(work.get("verdict", "insufficient_evidence")).to_upper()
		var recorded: Dictionary = work.get("record_files", {})
		var records_current: bool = not recorded.is_empty() and recorded == record_hashes(base)
		if not fresh or not intact or not same_revision or not records_current:
			verdict = "INSUFFICIENT_EVIDENCE"
		lines.append("\n%s · %s" % [work.get("work_id", "unknown"), verdict])
		lines.append("Goal: %s" % production.get("player_outcome", "missing"))
		lines.append("Decision / style: %s" % decision.get("decision", "missing"))
		for asset in assets.get("assets", []):
			lines.append("Asset: %s → %s (normalized)" % [asset.get("asset_id", "?"), asset.get("path", "?")])
		lines.append("Change: %s" % implementation.get("summary", "missing"))
		for path in implementation.get("files", []):
			lines.append("  %s" % path)
		lines.append("Evidence: %s · %s" % [evidence.get("evidence_id", "missing"), "hashes verified" if intact else "missing / changed"])
	summary.text = "\n".join(lines)


func read_record(path: String) -> Dictionary:
	if not path.begins_with("res://.vibegame/gamemaker/") or ".." in path:
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


func evidence_intact(evidence: Dictionary) -> bool:
	if evidence.get("runtime", {}).get("run_id", "").is_empty() or evidence.get("assertions", []).is_empty():
		return false
	var has_screenshot := false
	for artifact in evidence.get("artifacts", []):
		var path := str(artifact.get("path", "")).trim_prefix("res://")
		if not path.begins_with(".vibegame/gamemaker/artifacts/") or ".." in path:
			return false
		if artifact.get("stale_frame", false) or FileAccess.get_sha256("res://" + path) != artifact.get("sha256", "missing"):
			return false
		has_screenshot = has_screenshot or artifact.get("kind") == "screenshot"
	return has_screenshot


func source_hashes(folder: String) -> Dictionary:
	var result := {}
	var directory := DirAccess.open(folder)
	if directory == null:
		return result
	for name in directory.get_directories():
		if name.begins_with(".") or (folder == "res://addons/" and name in ["godot_ai", "gamemaker_context"]):
			continue
		if not directory.is_link(name):
			result.merge(source_hashes(folder + name + "/"))
	for name in directory.get_files():
		if name.get_extension().to_lower() in ["gd", "godot", "tres", "tscn", "png", "svg", "import", "uid"]:
			result[(folder + name).trim_prefix("res://")] = FileAccess.get_sha256(folder + name)
	return result


func record_hashes(folder: String) -> Dictionary:
	var result := {}
	if not folder.begins_with("res://.vibegame/gamemaker/work/") or ".." in folder:
		return result
	var directory := DirAccess.open(folder)
	if directory == null:
		return result
	for name in directory.get_directories():
		if not directory.is_link(name):
			result.merge(record_hashes(folder + name + "/"))
	for name in directory.get_files():
		if name.get_extension() in ["json", "md"]:
			result[(folder + name).trim_prefix("res://")] = FileAccess.get_sha256(folder + name)
	return result
