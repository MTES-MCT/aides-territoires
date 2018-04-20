import React from "react";
import classNames from "classnames";

export default props => {
  return (
    <div className="field">
      <input
        className={classNames("button", props.className)}
        type="submit"
        value={props.value}
        disabled={props.disabled}
      />
    </div>
  );
};
