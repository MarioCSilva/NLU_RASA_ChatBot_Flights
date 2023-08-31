import 'dart:ffi';

class FlightInfo {
  final String cityFrom;
  final String cityTo;
  final DateTime departure;
  final DateTime arrival;
  final double price;
  final String flightNumber;
  final String airline;
  final String flightIcao;

  FlightInfo(
      {required this.cityFrom,
      required this.cityTo,
      required this.departure,
      required this.arrival,
      required this.price,
      required this.flightNumber,
      required this.airline,
      required this.flightIcao});

  Map toJson() => {
        'departure_iata': cityFrom,
        'arrival_iata': cityTo,
        'departure_time': departure.toIso8601String(),
        'arrival_time': arrival.toIso8601String(),
        'price': price,
        'flight_number': flightNumber,
        'airline_name': airline,
        'flight_icao': flightIcao
      };

  factory FlightInfo.fromJson(Map<String, dynamic> json) {
    return FlightInfo(
      airline: json['airline_name'] as String,
      flightNumber: json['flight_number'] as String,
      departure: DateTime.parse(json['departure_time']) as DateTime,
      cityFrom: json['departure_iata'] as String,
      cityTo: json['arrival_iata'] as String,
      arrival: DateTime.parse(json['arrival_time']) as DateTime,
      price: json['price'] as double,
      flightIcao: json['flight_icao'] as String,
    );
  }
}
