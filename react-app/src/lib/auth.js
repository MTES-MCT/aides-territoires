import decode from "jwt-decode";

const STORAGE_KEY = "auth";

/**
 *
 */

export function getToken() {
  let data = {};
  try {
    data = JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
  } catch (err) {}

  if (!data.token || isTokenExpired(data.token)) return null;
  return data.token;
}

/**
 *
 */

export function setToken(token) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ token }));
}

/**
 *
 */

function getTokenExpirationDate(token) {
  const decoded = decode(token);
  if (!decoded.exp) return null;

  const date = new Date(0); // The 0 here is the key, which sets the date to the epoch
  date.setUTCSeconds(decoded.exp);
  return date;
}

/**
 *
 */

function isTokenExpired(token) {
  const date = getTokenExpirationDate(token);
  if (date === null) return false;
  return date.valueOf() <= new Date().valueOf();
}
