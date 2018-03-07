/**
 * Determine if string looks like a postal code, suitable
 * to launch a search on postal code API
 *
 * @param {!string} string
 * @return {boolean} - true if string seems to be a postal code
 */
export const isPostalCode = string => {
  // remove all spaces
  const newString = string.replace(" ", "");
  // check string contains only digit
  const isNumeric = /^\d+$/.test(string);
  if (isNumeric) {
    return true;
  }
  return false;
};
