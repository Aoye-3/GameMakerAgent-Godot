extends Node2D

var items_collected: int = 0

func _ready() -> void:
	$Target.body_entered.connect(_on_target_body_entered)
	print("TRIAL_READY items_collected=0 speed=", $Player.speed)

func _on_target_body_entered(body: Node2D) -> void:
	if body == $Player and items_collected == 0:
		items_collected = 1
		$Target.queue_free()
		queue_redraw()
		print("TRIAL_COLLECTED items_collected=1")

func _draw() -> void:
	draw_rect(Rect2(0, 0, 800, 560), Color("#101c28"))
	draw_rect(Rect2(32, 164, 736, 324), Color("#182b37"))
	for x in range(48, 760, 32):
		for y in range(180, 480, 32):
			draw_circle(Vector2(x, y), 1, Color("#34515c"))
	var font := ThemeDB.fallback_font
	draw_string(font, Vector2(36, 44), "GAMEMAKER / LIVE MCP TRIAL", HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Color("#61d7cf"))
	draw_string(font, Vector2(36, 100), "Move. Touch. Collect.", HORIZONTAL_ALIGNMENT_LEFT, -1, 36, Color("#edf6f5"))
	draw_string(font, Vector2(36, 136), "WASD or arrow keys  /  Reach the gold beacon", HORIZONTAL_ALIGNMENT_LEFT, -1, 18, Color("#a7bdc5"))
	var status := "COLLECTED  1 / 1" if items_collected == 1 else "COLLECTED  0 / 1"
	draw_string(font, Vector2(36, 528), status, HORIZONTAL_ALIGNMENT_LEFT, -1, 22, Color("#61d7cf"))
	draw_string(font, Vector2(422, 528), "Generated sprite / native Godot", HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Color("#a7bdc5"))
