import 'dart:convert';
import 'dart:ui';

import 'package:chatbot/models/actionButtonModel.dart';
import 'package:chatbot/models/flightInfo.dart';
import 'package:chatbot/widgets/ActionButton.dart';
import 'package:chatbot/widgets/Command.dart';
import 'package:chatbot/widgets/FlightTable.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../models/messageModel.dart';
import '../utils.dart';
import 'package:geolocator/geolocator.dart';
import 'package:geocoding/geocoding.dart';
import '../widgets/Command.dart';
import 'package:carousel_slider/carousel_slider.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import '../constants.dart';

class ChatPage extends StatefulWidget {
  ChatPage({required int this.user_id});

  final int user_id;

  @override
  _ChatPageState createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  var user_id = 1;
  var _channel;
  var geolocation;
  @override
  void initState() {
    super.initState();
    user_id = widget.user_id;
    _channel = WebSocketChannel.connect(
      Uri.parse('$WS_BASE_URL/$user_id'),
    );
  }

  _ChatPageState() {
    determinePosition().then((value) {
      position = value;
      print(position);
      placemarkFromCoordinates(
        position.latitude,
        position.longitude,
      ).then((value) => {geolocation = value[0].administrativeArea});
    });
  }

  ScrollController _scrollController = ScrollController();

  _scrollToBottom() {
    _scrollController.jumpTo(_scrollController.position.maxScrollExtent);
  }

  /*
  ChatMessage(
        messageContent: "Hello, Will",
        messageContentType: "text",
        messageType: "receiver",
        messageTime: DateTime.now())
  */
  List<ChatMessage> messages = [];

  var position;
  double curr_rating = 3;
  bool rated = false;
  String talking_to = "Chatbot";
  bool _clear = false;

  final TextEditingController messageController = TextEditingController();

  @override
  void dispose() {
    // Clean up the controller when the widget is disposed.
    messageController.dispose();
    _channel.sink.close();
    super.dispose();
  }

  void addMessage(String message, String contentType) {
    if (contentType == "location") {
      _channel.sink.add(
          jsonEncode({"content": geolocation, "content_type": contentType}));
    } else if (contentType == "booking") {
      _channel.sink
          .add(jsonEncode({"content": message, "content_type": contentType}));
      message = "Book successfull";
    } else if (contentType == "help_accepted") {
      talking_to = message;
    } else {
      _channel.sink
          .add(jsonEncode({"content": message, "content_type": contentType}));
    }

    setState(() {
      talking_to = talking_to;
      messages.add(ChatMessage(
          messageContent: message,
          messageContentType: "text",
          messageType: "sender",
          messageTime: DateTime.now()));
    });
  }

  void filterMessage(snapshot) {
    var data = jsonDecode(snapshot.data);
    print(data);
    if (data["topic"] == "init") {
      for (var message in data["data"]) {
        messages.add(ChatMessage(
            messageContent: message["content"],
            messageContentType: message["content_type"],
            messageType: message["type"],
            messageTime: DateTime.parse(message["date"])));
      }
    } else if (data["topic"] == "receive") {
      var message = data["data"];
      for (var m in messages.reversed.toList()) {
        if (m.messageType == "receiver") {
          if (m.messageContent == message["content"]) {
            return;
          }
          break;
        }
      }
      messages.add(ChatMessage(
          messageContent: message["content"],
          messageContentType: message["content_type"],
          messageType: message["type"],
          messageTime: DateTime.parse(message["date"])));
    }
  }

  @override
  Widget build(BuildContext context) {
    return StreamBuilder(
        stream: _channel.stream,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            filterMessage(snapshot);
          }
          return (Scaffold(
            resizeToAvoidBottomInset: true,
            appBar: AppBar(
              elevation: 0,
              automaticallyImplyLeading: false,
              backgroundColor: Colors.white,
              flexibleSpace: SafeArea(
                child: Container(
                  padding: const EdgeInsets.only(right: 16),
                  child: Row(
                    children: <Widget>[
                      IconButton(
                        onPressed: () {
                          Navigator.pop(context);
                        },
                        icon: const Icon(
                          Icons.arrow_back,
                          color: Colors.black,
                        ),
                      ),
                      const SizedBox(
                        width: 2,
                      ),
                      const SizedBox(
                        width: 12,
                      ),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: <Widget>[
                            Text(
                              talking_to,
                              style: const TextStyle(
                                  fontSize: 18, fontWeight: FontWeight.w600),
                            ),
                          ],
                        ),
                      ),
                      GestureDetector(
                        child: const Icon(
                          Icons.handshake,
                          color: Colors.green,
                        ),
                        onTap: () {
                          addMessage("help", "help");
                        },
                      ),
                    ],
                  ),
                ),
              ),
            ),
            body: Stack(
              children: <Widget>[
                Padding(
                  padding: const EdgeInsets.only(bottom: 45),
                  child: ListView.builder(
                    controller: _scrollController,
                    itemCount: messages.length,
                    shrinkWrap: true,
                    padding: const EdgeInsets.only(top: 10, bottom: 10),
                    physics: const BouncingScrollPhysics(),
                    itemBuilder: (context, index) {
                      if (messages[index].messageContentType == "text") {
                        return Container(
                          padding: const EdgeInsets.only(
                              left: 14, right: 14, top: 10, bottom: 10),
                          child: Align(
                            alignment:
                                (messages[index].messageType == "receiver"
                                    ? Alignment.topLeft
                                    : Alignment.topRight),
                            child: Container(
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(20),
                                color:
                                    (messages[index].messageType == "receiver"
                                        ? (talking_to == "Chatbot"
                                            ? Colors.grey.shade200
                                            : Colors.green)
                                        : Colors.blue[200]),
                              ),
                              padding: const EdgeInsets.all(16),
                              child: Text(
                                messages[index].messageContent,
                                style: const TextStyle(fontSize: 15),
                              ),
                            ),
                          ),
                        );
                      } else if (messages[index].messageContentType ==
                          "buttons") {
                        // messages[index].messageContent

                        return Container(
                            child: CarouselSlider(
                          options: CarouselOptions(
                            height: 300,
                            enableInfiniteScroll: false,
                          ),
                          items: BOT_COMMANDS
                              .map((item) => Container(
                                      child: Command(
                                    buttonContent: item,
                                    onPressed: addMessage,
                                  )))
                              .toList(),
                        ));
                      } else if (messages[index].messageContentType ==
                          "search") {
                        var list = json.decode(messages[index].messageContent);
                        var flights = [];
                        for (var j in list) {
                          flights.add(FlightInfo.fromJson(j));
                        }

                        return Container(
                            child: CarouselSlider(
                          options: CarouselOptions(
                            height: 300,
                            enableInfiniteScroll: false,
                          ),
                          items: flights
                              .map((item) => Padding(
                                  padding: EdgeInsets.symmetric(horizontal: 4),
                                  child: FlightTable(
                                    info: item,
                                    onPressed: addMessage,
                                  )))
                              .toList(),
                        ));
                      } else if (messages[index].messageContentType ==
                          "feedback") {
                        if (!rated) {
                          return (Stack(children: [
                            RatingBar.builder(
                              initialRating: 3,
                              minRating: 1,
                              direction: Axis.horizontal,
                              allowHalfRating: false,
                              itemCount: 5,
                              itemPadding:
                                  const EdgeInsets.symmetric(horizontal: 4.0),
                              itemBuilder: (context, _) => const Icon(
                                Icons.star,
                                color: Colors.amber,
                              ),
                              onRatingUpdate: (rating) {
                                curr_rating = rating;
                              },
                            ),
                            Align(
                                alignment: Alignment.topRight,
                                child: Padding(
                                    padding: const EdgeInsets.only(right: 16),
                                    child: TextButton(
                                        style: TextButton.styleFrom(
                                          textStyle:
                                              const TextStyle(fontSize: 20),
                                        ),
                                        onPressed: (() {
                                          addMessage(
                                              "I rate this with ${curr_rating.round()}",
                                              "feedback");
                                          rated = true;
                                        }),
                                        child: const Text("Rate"))))
                          ]));
                        }
                        return Container();
                      } else if (messages[index].messageContentType ==
                          "location") {
                        return (Column(children: [
                          Container(
                            padding: const EdgeInsets.only(
                                left: 14, right: 14, top: 10, bottom: 10),
                            child: Align(
                              alignment:
                                  (messages[index].messageType == "receiver"
                                      ? Alignment.topLeft
                                      : Alignment.topRight),
                              child: Container(
                                decoration: BoxDecoration(
                                  borderRadius: BorderRadius.circular(20),
                                  color:
                                      (messages[index].messageType == "receiver"
                                          ? (talking_to == "Chatbot"
                                              ? Colors.grey.shade200
                                              : Colors.green)
                                          : Colors.blue[200]),
                                ),
                                padding: const EdgeInsets.all(16),
                                child: Text(
                                  messages[index].messageContent,
                                  style: const TextStyle(fontSize: 15),
                                ),
                              ),
                            ),
                          ),
                          ActionButton(
                            action: ActionButtonModel(
                                content: "My location",
                                content_type: "location"),
                            onPressed: addMessage,
                          ),
                        ]));
                      } else if (messages[index].messageContentType ==
                          "help_accepted") {
                        return (Align(
                          child: Text(
                            "Connected to Agent",
                            style:
                                TextStyle(backgroundColor: Colors.lightGreen),
                          ),
                          alignment: Alignment.topCenter,
                        ));
                      } else {
                        return (const Text("Error"));
                      }
                    },
                  ),
                ),
                Align(
                  alignment: Alignment.bottomLeft,
                  child: Container(
                    padding:
                        const EdgeInsets.only(left: 10, bottom: 10, top: 10),
                    height: 60,
                    width: double.infinity,
                    color: Colors.white,
                    child: Row(
                      children: <Widget>[
                        GestureDetector(
                          onTap: () {},
                          child: Container(
                            height: 30,
                            width: 30,
                            decoration: BoxDecoration(
                              color: Colors.lightBlue,
                              borderRadius: BorderRadius.circular(30),
                            ),
                            child: const Icon(
                              Icons.add,
                              color: Colors.white,
                              size: 20,
                            ),
                          ),
                        ),
                        const SizedBox(
                          width: 15,
                        ),
                        Expanded(
                          child: TextField(
                            controller: messageController,
                            decoration: const InputDecoration(
                                hintText: "Write message...",
                                hintStyle: TextStyle(color: Colors.black54),
                                border: InputBorder.none),
                          ),
                        ),
                        const SizedBox(
                          width: 15,
                        ),
                        FloatingActionButton(
                          onPressed: () {
                            addMessage(messageController.text, "text");
                            messageController.clear();
                          },
                          child: const Icon(
                            Icons.send,
                            color: Colors.white,
                            size: 18,
                          ),
                          backgroundColor: Colors.blue,
                          elevation: 0,
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ));
        });
  }
}
