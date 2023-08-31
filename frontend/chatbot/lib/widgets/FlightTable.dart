import 'dart:convert';

import 'package:chatbot/models/actionButtonModel.dart';
import 'package:chatbot/models/flightInfo.dart';
import 'package:flutter/material.dart';
import '../models/flightInfo.dart';
import 'ActionButton.dart';

class FlightTable extends StatelessWidget {
  final FlightInfo info;
  final Function(String, String) onPressed;

  FlightTable({required this.info, required this.onPressed});

  _getBackgroundDecoration() {
    return BoxDecoration(
      borderRadius: BorderRadius.circular(10.0),
      color: Colors.white,
    );
  }

  TextStyle get bodyTextStyle =>
      TextStyle(color: Color(0xFF083e64), fontSize: 13, fontFamily: 'Oswald');

  Widget _buildTicketHeader(context) {
    var headerStyle = TextStyle(
        fontFamily: 'OpenSans',
        fontWeight: FontWeight.bold,
        fontSize: 11,
        color: Colors.redAccent);
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: <Widget>[
        Text("#${info.flightNumber} ${info.airline}", style: headerStyle),
      ],
    );
  }

  Widget _buildTicketOrigin() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: <Widget>[
        Text(
          info.cityFrom.toUpperCase(),
          textAlign: TextAlign.left,
          style: bodyTextStyle.copyWith(fontSize: 22),
        ),
        Text(
            "${info.departure.hour.toString()}:${info.departure.minute.toString()} ${info.departure.day.toString()}/${info.departure.month.toString()}/${info.departure.year.toString()}",
            style: bodyTextStyle.copyWith(color: Color(0xFF838383))),
      ],
    );
  }

  Widget _buildTicketDuration() {
    String planeRoutePath = 'assets/images/planeroute_blue.png';

    return Container(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: <Widget>[
          Container(
            width: 100,
            height: 120,
            child: Stack(
              alignment: Alignment.center,
              children: <Widget>[
                Image.asset(planeRoutePath, fit: BoxFit.cover),
                Image.asset('assets/images/airplane_blue.png',
                    height: 20, fit: BoxFit.contain),
              ],
            ),
          ),
          Text("Price: ${info.price.toString()}€",
              textAlign: TextAlign.center, style: bodyTextStyle),
        ],
      ),
    );
  }

  Widget _buildTicketDestination() {
    return Column(
      children: <Widget>[
        Text(
          info.cityTo.toUpperCase(),
          textAlign: TextAlign.right,
          style: bodyTextStyle.copyWith(fontSize: 22),
        ),
        Text(
          "${info.arrival.hour.toString()}:${info.arrival.minute.toString()} ${info.arrival.day.toString()}/${info.arrival.month.toString()}/${info.arrival.year.toString()}",
          style: bodyTextStyle.copyWith(color: Color(0xFF838383)),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: _getBackgroundDecoration(),
      width: double.infinity,
      height: double.infinity,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 1),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: <Widget>[
            _buildTicketHeader(context),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 10.0),
              child: Stack(
                children: <Widget>[
                  Align(
                      alignment: Alignment.centerLeft,
                      child: _buildTicketOrigin()),
                  Align(
                      alignment: Alignment.center,
                      child: _buildTicketDuration()),
                  Align(
                      alignment: Alignment.centerRight,
                      child: _buildTicketDestination())
                ],
              ),
            ),
            TextButton(
                onPressed: () {
                  onPressed(jsonEncode(info), "booking");
                },
                child: Text("Book"))
          ],
        ),
      ),
    );
  }
}
