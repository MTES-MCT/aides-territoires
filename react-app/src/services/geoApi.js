import axios from "axios";

const TERRITOIRE_TYPE_COMMUNE = "commune";
const TERRITOIRE_TYPE_DEPARTEMENT = "departement";
const TERRITOIRE_TYPE_REGION = "region";

/**
 * Get commune, département or region from insee code
 * @return {type} string : "commune", "departement", "region"
 * @param {string} codeInsee - Code Insee
 * @see https://geo.api.gouv.fr/docs/communes
 */
export const getTerritoireByTypeAndCodeInsee = (type, codeInsee) => {
  let result = null;
  if (type === TERRITOIRE_TYPE_COMMUNE) {
    result = axios.get(`https://geo.api.gouv.fr/communes/${codeInsee}`);
  }
  if (type === TERRITOIRE_TYPE_DEPARTEMENT) {
    result = axios.get(`https://geo.api.gouv.fr/departement/${codeInsee}`);
  }
  if (type === TERRITOIRE_TYPE_REGION) {
    result = axios.get(`https://geo.api.gouv.fr/region/${codeInsee}`);
  }
  return result;
};

/**
 * Get communes from a postal code
 * @param {string} postalCode
 * @return {array}
 * @see https://geo.api.gouv.fr/docs/communes
 */
export const getCommunesFromPostalCode = postalCode => {
  const result = axios.get(
    `https://geo.api.gouv.fr/communes?codePostal=${postalCode}&boost=population`
  );
  return result;
};

/**
 *
 * @param {sting} name - commune name
 */
export const getCommunesFromName = name => {
  const result = axios.get(
    `https://geo.api.gouv.fr/communes?nom=${name}&boost=population`
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
