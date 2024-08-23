import 'package:fraud_detection/input_view.dart';

class AppRoute {
  AppRoute._();
  static const String homeRoute = '/';

  static getApplicationRoute() {
    return {
      // homeRoute: (context) => const SelectView(),
      // inputRoute: (context) => const InputView(),
      // uploadRoute: (context) => const UploadView(),
      homeRoute: (context) => UploadPage(),
      // inputResultRoute: (context) => const CreditView(),
    };
  }
}
