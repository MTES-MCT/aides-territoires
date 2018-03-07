import axios from "axios";

/**
 * Get postal code from
 * @param {string} postalCode
 * @return {array}
 * @see https://geo.api.gouv.fr/docs/communes
 */
export const getCommunesFromPostalCode = postalCode => {
  const result = axios.get(
    `https://geo.api.gouv.fr/communes?codePostal=${postalCode}`
  );
  return result;
};
