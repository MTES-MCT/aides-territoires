import React from "react";
import PropTypes from "prop-types";

/**
 * Ce composant est entièrement controlé par le parent, qui doit lui implémenter
 * onChange pour faire un setState de la valeur et la lui repasser en props.
 *
 * Cela permet d'implémenter plus facilement la liste de suggestion
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
  placeholder: PropTypes.placeholder,
  onChange: PropTypes.func.isRequired
};

export default SearchForm;
