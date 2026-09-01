@tool
extends VBoxContainer

const INDEX_PATH := "res://.vibegame/gamemaker/index.json"

var heading := Label.new()
var summary := RichTextLabel.new()
var last_modified := 0


func _ready() -> void:
	name = "GameMaker Context"
	heading.text = "GameMaker Context · read only"
	summary.fit_content = true
	summary.custom_minimum_size = Vector2(300, 240)
	add_child(heading)
	add_child(summary)
	reload_index()
	set_process(true)


func _process(_delta: float) -> void:
	var modified := FileAccess.get_modified_time(INDEX_PATH)
	if modified != last_modified:
		reload_index()


func reload_index() -> void:
	last_modified = FileAccess.get_modified_time(INDEX_PATH)
	if not FileAccess.file_exists(INDEX_PATH):
		summary.text = "No .vibegame/gamemaker/index.json record found."
		return
	var file := FileAccess.open(INDEX_PATH, FileAccess.READ)
	var parsed = JSON.parse_string(file.get_as_text())
	if not parsed is Dictionary:
		summary.text = "The GameMaker work index is invalid JSON."
		return
	var lines: Array[String] = ["Revision: %s" % parsed.get("project_revision", "unknown")]
	for work in parsed.get("works", []):
		lines.append("• %s · %s · %s" % [work.get("work_id", "unknown"), work.get("status", "unknown"), work.get("verdict", "unreviewed")])
	summary.text = "\n".join(lines)
