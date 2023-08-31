import 'package:chatbot/models/actionButtonModel.dart';
import 'package:flutter/material.dart';

class ActionButton extends StatelessWidget {
  final ActionButtonModel action;
  final Function(String, String) onPressed;

  ActionButton({required this.action, required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return TextButton(
      onPressed: () => onPressed(action.content, action.content_type),
      style: TextButton.styleFrom(
        textStyle: const TextStyle(fontSize: 20),
      ),
      child: Text(
        action.content.toUpperCase(),
        style: const TextStyle(fontSize: 15),
      ),
    );
  }
}
