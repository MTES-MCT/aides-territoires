import React from "react";
import PropTypes from "prop-types";

/**
 * Ce composant est entièrement controlé par le parent, qui maintient
 * l'état de la variable value et la repasse en props à ce composant.
 *
 * Cela permet d'implémenter plus facilement la liste de suggestion et de se
 * passer d'une implémentation de getDerivedStateFromProps dans ce composant.
 * @param {*} param0
 */
const SearchForm = ({ onChange, onSubmit, value, placeholder = "" }) => {
  return (
    <form onSubmit={onSubmit}>
      <div className="field has-addons">
        <div className="control is-expanded">
          <input
            onChange={onChange}
            className="input is-large"
            type="text"
            value={value}
            placeholder={placeholder}
          />
        </div>
        <div className="control">
          <input
            type="submit"
            value="Chercher"
            className="button is-info is-large"
          />
        </div>
      </div>
    </form>
  );
};

SearchForm.propTypes = {
  onSubmit: PropTypes.func,
  value: PropTypes.string,
  placeholder: PropTypes.string,
  onChange: PropTypes.func.isRequired
};

export default SearchForm;
