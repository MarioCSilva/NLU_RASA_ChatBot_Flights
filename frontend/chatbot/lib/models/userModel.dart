class UserModel {
  final int id;
  final bool is_real_agent;
  final String username;

  UserModel(
      {required this.id, required this.is_real_agent, required this.username});

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as int,
      is_real_agent: json['is_real_agent'] as bool,
      username: json['username'] as String,
    );
  }
}
