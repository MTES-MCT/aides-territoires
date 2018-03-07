import axios from "axios";

/**
 * Get communes from a postal code
 * @param {string} postalCode
 * @return {array}
 * @see https://geo.api.gouv.fr/docs/communes
 */
export const getCommunesFromPostalCode = postalCode => {
  const result = axios.get(
    `https://geo.api.gouv.fr/communes?codePostal=${postalCode}&fields=nom&boost=population`
  );
  return result;
};

/**
 *
 * @param {sting} name - commune name
 */
export const getCommunesFromName = name => {
  const result = axios.get(
    `https://geo.api.gouv.fr/communes?nom=${name}&fields=nom&boost=population`
  );
  return result;
};

export const getDepartementsByName = name => {
  const result = axios.get(`https://geo.api.gouv.fr/departements?nom=${name}`);
  return result;
};

export const getRegionsByName = name => {
  const result = axios.get(`https://geo.api.gouv.fr/regions?nom=${name}`);
  return result;
};
