extends Area2D

func _draw() -> void:
	draw_circle(Vector2.ZERO, 30, Color("#65522e"))
	draw_arc(Vector2.ZERO, 24, 0, TAU, 48, Color("#f9bf58"), 2, true)
	draw_circle(Vector2.ZERO, 12, Color("#ffd578"))
