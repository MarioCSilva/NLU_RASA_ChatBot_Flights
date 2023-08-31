import 'package:chatbot/models/actionButtonModel.dart';
import 'package:flutter/material.dart';
import '../models/actionButtonModel.dart';
import 'ActionButton.dart';

class Command extends StatelessWidget {
  final ActionButtonModel buttonContent;
  final Function(String, String) onPressed;

  Command({required this.buttonContent, required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return Container(
      child: Column(
        children: [
          Image.asset(
              "assets/images/${buttonContent.content_type.toLowerCase()}.jpeg",
              fit: BoxFit.cover),
          ActionButton(action: buttonContent, onPressed: onPressed)
        ],
      ),
    );
  }
}
