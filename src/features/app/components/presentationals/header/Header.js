import React from "react";

const style = {
  fontSize: "60px"
};

class Header extends React.Component {
  render() {
    return (
      <header className="container">
        <div style={style} className="title">
          Aide territoires
        </div>
      </header>
    );
  }
}

export default Header;
