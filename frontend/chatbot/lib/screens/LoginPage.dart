import 'dart:convert';

import 'package:chatbot/models/userModel.dart';
import 'package:flutter/material.dart';
import 'ChatPage.dart';
import 'package:http/http.dart' as http;
import '../constants.dart';

Future<http.Response> register(String username) {
  return http.post(Uri.parse('$API_BASE_URL/users/register'),
      headers: {
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode({"username": username, "is_real_agent": false}));
}

Future<http.Response> login(String username) {
  return http.post(Uri.parse('$API_BASE_URL/users/login'),
      headers: {
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode({"username": username}));
}

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final usernameController = TextEditingController();

  bool isAgent = false;

  Future userLogin() async {
    var response = await register(usernameController.text);
    if (response.statusCode == 200) {
      dynamic body = jsonDecode(response.body);
      UserModel user = UserModel.fromJson(body["data"]);
      Navigator.push(context,
          MaterialPageRoute(builder: (_) => ChatPage(user_id: user.id)));
    } else {
      response = await login(usernameController.text);
      if (response.statusCode == 200) {
        dynamic body = jsonDecode(response.body);
        UserModel user = UserModel.fromJson(body["data"]);
        Navigator.push(context,
            MaterialPageRoute(builder: (_) => ChatPage(user_id: user.id)));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text("Login Page"),
      ),
      body: SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            const SizedBox(
              height: 300,
            ),
            Padding(
              //padding: const EdgeInsets.only(left:15.0,right: 15.0,top:0,bottom: 0),
              padding: const EdgeInsets.symmetric(horizontal: 15),
              child: TextField(
                controller: usernameController,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'Username',
                ),
              ),
            ),
            const SizedBox(
              height: 30,
            ),
            Container(
              height: 50,
              width: 250,
              decoration: BoxDecoration(
                  color: Colors.blue, borderRadius: BorderRadius.circular(20)),
              child: TextButton(
                onPressed: userLogin,
                child: const Text(
                  'Login',
                  style: TextStyle(color: Colors.white, fontSize: 25),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
