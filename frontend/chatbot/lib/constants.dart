import 'package:chatbot/models/actionButtonModel.dart';

const API_BASE_URL = 'http://192.168.45.207:8000';
const WS_BASE_URL = 'ws://192.168.45.207:8000/ws';

// TODO: add command buttons
final BOT_COMMANDS = [
  ActionButtonModel(content: "Search Flights", content_type: "text"),
  ActionButtonModel(
      content: "Connect me to a real agent", content_type: "help"),
];
