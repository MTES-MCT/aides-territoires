// https://gist.github.com/getify/3667624
// escape double quotes, if they are not already escaped
export function escapeDoubleQuotes(str) {
  return str.replace(/\\([\s\S])|(")/g, "\\$1$2"); // thanks @slevithan!
}

export function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

export function graphQLEscapeString(text, replaceLineBreakBy = "") {
  let escapedText = escapeDoubleQuotes(text);
  escapedText = text.replace(/(?:\r\n|\r|\n)/g, replaceLineBreakBy);
  return escapedText;
}
