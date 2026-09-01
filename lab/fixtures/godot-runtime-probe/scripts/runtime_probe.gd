extends Node2D

const STATE_CONTRACT_VERSION := "0.1"

var verification_value := 0
var trigger_count := 0

@onready var state_label: Label = $State


func _ready() -> void:
	_update_state_label()
	print("GAMEMAKER_PROBE_READY ", JSON.stringify(_gamemaker_state()))


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("verify_trigger"):
		apply_verification_trigger()


func apply_verification_trigger() -> void:
	trigger_count += 1
	verification_value += 10
	_update_state_label()
	print("GAMEMAKER_PROBE_CHANGED ", JSON.stringify(_gamemaker_state()))


func _gamemaker_state() -> Dictionary:
	return {
		"contract_version": STATE_CONTRACT_VERSION,
		"verification_value": verification_value,
		"trigger_count": trigger_count,
	}


func _update_state_label() -> void:
	state_label.text = "verification_value=%d trigger_count=%d" % [
		verification_value,
		trigger_count,
	]
