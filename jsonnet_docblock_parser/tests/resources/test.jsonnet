{
  /**
   * Returns whether the string a is prefixed by the string b.
   *
   * Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut venenatis ex tellus, ac
   * consectetur libero pretium in. Donec vehicula est nec odio cursus, non condimentum
   * est cursus. Integer dui sapien, tincidunt non velit non, bibendum facilisis mi. Morbi
   *
   * @param a The input string.
   * @param b (optional) The prefix.
   * @return bool true if string a is prefixed by the string b or false otherwise.
   */
  startsWith(a, b):
    if std.length(a) < std.length(b) then
      false
    else
      std.substr(a, 0, std.length(b)) == b,
}
