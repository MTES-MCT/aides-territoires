module.exports =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		var threw = true;
/******/ 		try {
/******/ 			modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 			threw = false;
/******/ 		} finally {
/******/ 			if(threw) delete installedModules[moduleId];
/******/ 		}
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 3);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./components/ui/ButtonLink.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_react_jss__ = __webpack_require__("react-jss");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_react_jss___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_react_jss__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__ui_config__ = __webpack_require__("./ui.config.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_next_link__ = __webpack_require__("next/link");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_next_link___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3_next_link__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_prop_types__ = __webpack_require__("prop-types");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_prop_types___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4_prop_types__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/ButtonLink.js";

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }







var ButtonLink = function ButtonLink(_ref) {
  var classes = _ref.classes,
      children = _ref.children,
      href = _ref.href;
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_3_next_link___default.a, {
    href: href,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 9
    }
  }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("a", {
    className: classes.a,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 10
    }
  }, children));
};

ButtonLink.propTypes = {
  href: __WEBPACK_IMPORTED_MODULE_4_prop_types___default.a.string.isRequired,
  type: __WEBPACK_IMPORTED_MODULE_4_prop_types___default.a.oneOf(["primary", "secondary"])
};
ButtonLink.defaultProps = {
  type: "primary"
};
var styles = {
  a: _defineProperty({
    textDecoration: "none",
    borderRadius: "5px",
    color: "white",
    fontSize: "24px",
    display: "inline-block",
    padding: "1.5rem 1.5rem",
    background: function background(_ref2) {
      var type = _ref2.type;
      var color = __WEBPACK_IMPORTED_MODULE_2__ui_config__["a" /* default */].colors.primaryLight;

      if (type === "secondary") {
        color = __WEBPACK_IMPORTED_MODULE_2__ui_config__["a" /* default */].colors.secondary;
      }

      return color;
    }
  }, "color", function color(_ref3) {
    var type = _ref3.type;
    var color = __WEBPACK_IMPORTED_MODULE_2__ui_config__["a" /* default */].colors.primary;

    if (type === "primary") {
      color = __WEBPACK_IMPORTED_MODULE_2__ui_config__["a" /* default */].colors.secondary;
    }

    return color;
  })
};
/* harmony default export */ __webpack_exports__["a"] = (__WEBPACK_IMPORTED_MODULE_1_react_jss___default()(styles)(ButtonLink));

/***/ }),

/***/ "./components/ui/Container.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_link__ = __webpack_require__("next/link");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_link___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_next_link__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_react_jss__ = __webpack_require__("react-jss");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_react_jss___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_react_jss__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_prop_types__ = __webpack_require__("prop-types");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_prop_types___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3_prop_types__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Container.js";





var Container = function Container(_ref) {
  var children = _ref.children,
      classes = _ref.classes;
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
    className: classes.root,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 7
    }
  }, children);
};

/* unused harmony default export */ var _unused_webpack_default_export = (__WEBPACK_IMPORTED_MODULE_2_react_jss___default()({
  root: {
    maxWidth: "940px",
    margin: "auto"
  }
})(Container));

/***/ }),

/***/ "./components/ui/Header.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_link__ = __webpack_require__("next/link");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_link___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_next_link__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__ui_ButtonLink__ = __webpack_require__("./components/ui/ButtonLink.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_prop_types__ = __webpack_require__("prop-types");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_prop_types___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3_prop_types__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_react_jss__ = __webpack_require__("react-jss");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_react_jss___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4_react_jss__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__ui_config__ = __webpack_require__("./ui.config.js");
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Header.js";

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }








var Header = function Header(_ref) {
  var classes = _ref.classes,
      title = _ref.title,
      subtitle = _ref.subtitle,
      callToActionText = _ref.callToActionText,
      callToActionLink = _ref.callToActionLink;
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("header", {
    className: classes.header,
    id: "aides-territoires",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 16
    }
  }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
    className: classes.headerOverlay,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 17
    }
  }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
    className: classes.content,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 18
    }
  }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("h1", {
    className: classes.title,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 19
    }
  }, title), __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("h2", {
    className: classes.subtitle,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 20
    }
  }, subtitle), callToActionText && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_2__ui_ButtonLink__["a" /* default */], {
    href: callToActionLink,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 22
    }
  }, callToActionText))));
};

Header.propTypes = {
  title: __WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.string.isRequired,
  backgroundImageUrl: __WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.string,
  subtitle: __WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.oneOfType([__WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.string, __WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.element]),
  callToActionText: __WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.string,
  callToActionLink: __WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.string
};

var styles = _defineProperty({
  header: {
    color: "white",
    position: "relative",
    backgroundImage: function backgroundImage(_ref2) {
      var backgroundImageUrl = _ref2.backgroundImageUrl;
      return "url(".concat(backgroundImageUrl, ")");
    },
    backgroundSize: "cover",
    backgroundPosition: "bottom",
    textAlign: "center",
    height: "400px"
  },
  content: {
    padding: "1rem"
  },
  headerOverlay: {
    display: "flex",
    flexDirection: "column",
    position: "absolute",
    justifyContent: "center",
    alignItems: "center",
    top: 0,
    left: 0,
    height: "100%",
    width: "100%",
    background: "rgba(20, 20, 20, 0.4)"
  }
}, __WEBPACK_IMPORTED_MODULE_5__ui_config__["a" /* default */].breakpoints.smallScreen, {
  content: {
    fontSize: "14px"
  }
  /*
  subtitle: { color: "white", fontSize: "1rem" },
  button: { color: "white" }
  */

});

/* harmony default export */ __webpack_exports__["a"] = (__WEBPACK_IMPORTED_MODULE_4_react_jss___default()(styles)(Header));

/***/ }),

/***/ "./components/ui/Layout.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__Navigation__ = __webpack_require__("./components/ui/Navigation.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_head__ = __webpack_require__("next/head");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_head___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_next_head__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_react_jss__ = __webpack_require__("react-jss");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_react_jss___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3_react_jss__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__content_config_md__ = __webpack_require__("./content/_config.md");
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Layout.js";






var Layout = function Layout(_ref) {
  var children = _ref.children;
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
    __source: {
      fileName: _jsxFileName,
      lineNumber: 9
    }
  }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_2_next_head___default.a, {
    __source: {
      fileName: _jsxFileName,
      lineNumber: 10
    }
  }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("meta", {
    name: "viewport",
    content: "initial-scale=1.0, width=device-width",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 11
    }
  }), __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("link", {
    rel: "icon",
    type: "image/png",
    href: "/static/images/favicon.png",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 12
    }
  }), __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("link", {
    rel: "stylesheet",
    href: "/static/css/global.css",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 13
    }
  })), __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_1__Navigation__["a" /* default */], {
    links: __WEBPACK_IMPORTED_MODULE_4__content_config_md__["a" /* meta */].navigationLinks,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 15
    }
  }), children);
};

var styles = {
  "@global": {
    border: "solid red 1px"
  }
};
/* harmony default export */ __webpack_exports__["a"] = (__WEBPACK_IMPORTED_MODULE_3_react_jss___default()(styles)(Layout));

/***/ }),

/***/ "./components/ui/Navigation.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_link__ = __webpack_require__("next/link");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_link___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_next_link__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_prop_types__ = __webpack_require__("prop-types");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_prop_types___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_prop_types__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__Container__ = __webpack_require__("./components/ui/Container.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__static_images_logo_aides_territoires_png__ = __webpack_require__("./static/images/logo-aides-territoires.png");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__static_images_logo_aides_territoires_png___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4__static_images_logo_aides_territoires_png__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__static_images_logo_fabrique_numerique_svg__ = __webpack_require__("./static/images/logo-fabrique-numerique.svg");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__static_images_logo_fabrique_numerique_svg___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_5__static_images_logo_fabrique_numerique_svg__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_react_jss__ = __webpack_require__("react-jss");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_react_jss___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_6_react_jss__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__ui_config__ = __webpack_require__("./ui.config.js");
var _class,
    _temp2,
    _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Navigation.js";

function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }









var Navigation = (_temp2 = _class =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Navigation, _React$Component);

  function Navigation() {
    var _ref;

    var _temp, _this;

    _classCallCheck(this, Navigation);

    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return _possibleConstructorReturn(_this, (_temp = _this = _possibleConstructorReturn(this, (_ref = Navigation.__proto__ || Object.getPrototypeOf(Navigation)).call.apply(_ref, [this].concat(args))), Object.defineProperty(_assertThisInitialized(_this), "state", {
      configurable: true,
      enumerable: true,
      writable: true,
      value: {
        mobileMenuOpened: false
      }
    }), _temp));
  }

  _createClass(Navigation, [{
    key: "render",
    value: function render() {
      var _props = this.props,
          classes = _props.classes,
          links = _props.links;
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
        className: classes.root,
        __source: {
          fileName: _jsxFileName,
          lineNumber: 25
        }
      }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
        className: classes.regionLogos,
        __source: {
          fileName: _jsxFileName,
          lineNumber: 26
        }
      }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(MenuLogoAidesTerritoires, {
        __source: {
          fileName: _jsxFileName,
          lineNumber: 27
        }
      }), __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(MenuLogoFabriqueNumerique, {
        __source: {
          fileName: _jsxFileName,
          lineNumber: 28
        }
      })), __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
        className: classes.regionLinks,
        __source: {
          fileName: _jsxFileName,
          lineNumber: 30
        }
      }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(MenuRight, {
        links: links,
        __source: {
          fileName: _jsxFileName,
          lineNumber: 31
        }
      })));
    }
  }]);

  return Navigation;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component), Object.defineProperty(_class, "propTypes", {
  configurable: true,
  enumerable: true,
  writable: true,
  value: {
    links: __WEBPACK_IMPORTED_MODULE_2_prop_types___default.a.arrayOf(__WEBPACK_IMPORTED_MODULE_2_prop_types___default.a.shape({
      to: __WEBPACK_IMPORTED_MODULE_2_prop_types___default.a.string.isRequired,
      title: __WEBPACK_IMPORTED_MODULE_2_prop_types___default.a.string.isRequired
    }).isRequired)
  }
}), _temp2);
Navigation = __WEBPACK_IMPORTED_MODULE_6_react_jss___default()(_defineProperty({
  root: {
    padding: "1rem 0",
    display: "flex",
    justifyContent: "space-between",
    position: "relative"
  }
}, __WEBPACK_IMPORTED_MODULE_7__ui_config__["a" /* default */].breakpoints.smallScreen, {
  root: {
    display: "block",
    textAlign: "center"
  },
  navigationContainer: {
    display: "block"
  }
}))(Navigation);
/**
 * MenuRight
 */

var MenuRight = function MenuRight(_ref2) {
  var links = _ref2.links,
      classes = _ref2.classes;
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
    className: classes.root,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 59
    }
  }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("ul", {
    className: classes.linksUl,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 60
    }
  }, links.map(function (link) {
    return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("li", {
      key: link.to,
      className: classes.linksLi,
      __source: {
        fileName: _jsxFileName,
        lineNumber: 62
      }
    }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_1_next_link___default.a, {
      href: link.to,
      __source: {
        fileName: _jsxFileName,
        lineNumber: 63
      }
    }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("a", {
      className: classes.a,
      __source: {
        fileName: _jsxFileName,
        lineNumber: 64
      }
    }, link.title)));
  })));
};

MenuRight = __WEBPACK_IMPORTED_MODULE_6_react_jss___default()(_defineProperty({
  linksUl: {
    margin: 0,
    padding: 0,
    paddingTop: "1rem",
    listStyleType: "none",
    display: "flex",
    justifyContent: "space-around"
  },
  a: {
    color: "black",
    textDecoration: "none",
    padding: "1rem",
    fontSize: "18px",
    "&:hover": {
      background: "rgb(240, 240, 240)"
    }
  }
}, __WEBPACK_IMPORTED_MODULE_7__ui_config__["a" /* default */].breakpoints.smallScreen, {
  a: {
    display: "block",
    padding: "0.5rem 0",
    margin: 0
  },
  linksUl: {
    // disable flex
    display: "block"
  },
  linksLi: {
    display: "block",
    textAlign: "center"
  }
}))(MenuRight);

var MenuLogoAidesTerritoires = function MenuLogoAidesTerritoires(_ref3) {
  var _React$createElement;

  var classes = _ref3.classes;
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("img", (_React$createElement = {
    alt: "Logo aides territoires",
    className: classes.image
  }, _defineProperty(_React$createElement, "alt", "logo"), _defineProperty(_React$createElement, "src", __WEBPACK_IMPORTED_MODULE_4__static_images_logo_aides_territoires_png___default.a), _defineProperty(_React$createElement, "__source", {
    fileName: _jsxFileName,
    lineNumber: 108
  }), _React$createElement));
};

MenuLogoAidesTerritoires = __WEBPACK_IMPORTED_MODULE_6_react_jss___default()(_defineProperty({
  image: {
    height: "50px"
  }
}, __WEBPACK_IMPORTED_MODULE_7__ui_config__["a" /* default */].breakpoints.smallScreen, {
  image: {
    display: "Block",
    margin: "auto",
    height: "30px"
  }
}))(MenuLogoAidesTerritoires);

var MenuLogoFabriqueNumerique = function MenuLogoFabriqueNumerique(_ref4) {
  var classes = _ref4.classes;
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("img", {
    className: classes.image,
    alt: "logo",
    src: __WEBPACK_IMPORTED_MODULE_5__static_images_logo_fabrique_numerique_svg___default.a,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 131
    }
  });
};

MenuLogoFabriqueNumerique = __WEBPACK_IMPORTED_MODULE_6_react_jss___default()(_defineProperty({
  image: {
    width: "50px",
    paddingLeft: "2rem"
  }
}, __WEBPACK_IMPORTED_MODULE_7__ui_config__["a" /* default */].breakpoints.smallScreen, {
  image: {
    display: "Block",
    margin: "auto",
    width: "90px"
  }
}))(MenuLogoFabriqueNumerique);
/* harmony default export */ __webpack_exports__["a"] = (Navigation);

/***/ }),

/***/ "./components/ui/Section.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_react_jss__ = __webpack_require__("react-jss");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_react_jss___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_react_jss__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__ui_config__ = __webpack_require__("./ui.config.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_prop_types__ = __webpack_require__("prop-types");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_prop_types___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3_prop_types__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Section.js";





var Section = function Section(_ref) {
  var classes = _ref.classes,
      children = _ref.children;
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
    className: classes.root,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 7
    }
  }, children);
};

var styles = {
  root: {
    padding: "4rem",
    background: function background(_ref2) {
      var type = _ref2.type;
      var color = __WEBPACK_IMPORTED_MODULE_2__ui_config__["a" /* default */].colors.primary;

      if (type === "secondary") {
        color = __WEBPACK_IMPORTED_MODULE_2__ui_config__["a" /* default */].colors.secondary;
      }

      return color;
    }
  }
};
Section.propTypes = {
  type: __WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.oneOf(["primary", "secondary"])
};
/* harmony default export */ __webpack_exports__["a"] = (__WEBPACK_IMPORTED_MODULE_1_react_jss___default()(styles)(Section));

/***/ }),

/***/ "./content/_config.md":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return meta; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);

/* unused harmony default export */ var _unused_webpack_default_export = (function (_ref) {
  var _ref$factories = _ref.factories,
      factories = _ref$factories === void 0 ? {} : _ref$factories;
  var _factories$wrapper = factories.wrapper,
      wrapper = _factories$wrapper === void 0 ? Object(__WEBPACK_IMPORTED_MODULE_0_react__["createFactory"])('div') : _factories$wrapper;
  return wrapper({});
});
var meta = {
  "navigationLinks": [{
    "title": "Aides Territoires",
    "to": "/"
  }, {
    "title": "À propos",
    "to": "/a-propos"
  }]
};

/***/ }),

/***/ "./content/index.md":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return meta; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);

/* unused harmony default export */ var _unused_webpack_default_export = (function (_ref) {
  var _ref$factories = _ref.factories,
      factories = _ref$factories === void 0 ? {} : _ref$factories;
  var _factories$wrapper = factories.wrapper,
      wrapper = _factories$wrapper === void 0 ? Object(__WEBPACK_IMPORTED_MODULE_0_react__["createFactory"])('div') : _factories$wrapper;
  return wrapper({});
});
var meta = {
  "header": {
    "title": "Un outil pour les collectivités",
    "subtitle": "Identifiez en quelques clics toutes les aides disponibles sur votre territoire pour vos projets d'aménagement durable",
    "callToAction": {
      "text": "Lancer la recherche",
      "link": "https://recherche.aides-territoires.beta.gouv.fr"
    }
  },
  "SectionCommentCaMarche": {
    "title": "Comment ça marche",
    "points": [{
      "title": "Un territoire, un projet",
      "description": "Indiquez-nous où est situé votre projet"
    }, {
      "title": "Des aides",
      "description": "Nous vous aidons à identifier les meilleures aides publiques mobilisables"
    }, {
      "title": "Du temps gagné",
      "description": "Gagnez du temps sur la recherche des aides pertinentes, au profit de votre projet"
    }]
  },
  "SectionPainPoint": {
    "title": "75% des porteurs de projets se plaignent du temps passé à rechercher les aides publiques disponibles et pertinentes pour leurs projets",
    "question": "Vous aussi, vous partagez ce constat ?"
  },
  "SectionBenefices": {
    "title": "Avec Aides-territoires",
    "points": ["Gagnez du temps dans votre recherche d'aides, de l'accompagnement au financement", "Ne passez plus à côté des aides qui correspondent à votre projet", "Bénéficiez d'une sélection pertinente à chaque étape de votre projet"]
  }
};

/***/ }),

/***/ "./pages/index.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__content_index_md__ = __webpack_require__("./content/index.md");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__components_ui_Header__ = __webpack_require__("./components/ui/Header.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__components_ui_ButtonLink__ = __webpack_require__("./components/ui/ButtonLink.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__components_ui_Section__ = __webpack_require__("./components/ui/Section.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__static_images_header_png__ = __webpack_require__("./static/images/header.png");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__static_images_header_png___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_5__static_images_header_png__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__components_ui_Layout__ = __webpack_require__("./components/ui/Layout.js");
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/pages/index.js";







/* harmony default export */ __webpack_exports__["default"] = (function () {
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_6__components_ui_Layout__["a" /* default */], {
    __source: {
      fileName: _jsxFileName,
      lineNumber: 10
    }
  }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_2__components_ui_Header__["a" /* default */], {
    backgroundImageUrl: __WEBPACK_IMPORTED_MODULE_5__static_images_header_png___default.a,
    title: __WEBPACK_IMPORTED_MODULE_1__content_index_md__["a" /* meta */].header.title,
    subtitle: __WEBPACK_IMPORTED_MODULE_1__content_index_md__["a" /* meta */].header.subtitle,
    callToActionText: __WEBPACK_IMPORTED_MODULE_1__content_index_md__["a" /* meta */].header.callToAction.text,
    callToActionLink: __WEBPACK_IMPORTED_MODULE_1__content_index_md__["a" /* meta */].header.callToAction.link,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 11
    }
  }), __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_4__components_ui_Section__["a" /* default */], {
    type: "primary",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 18
    }
  }, "Hello section !"));
});

/***/ }),

/***/ "./static/images/header.png":
/***/ (function(module, exports) {

module.exports = "/_next/static/images/header-e435320c7f184724b0cedbe446dc63dc.png";

/***/ }),

/***/ "./static/images/logo-aides-territoires.png":
/***/ (function(module, exports) {

module.exports = "/_next/static/images/logo-aides-territoires-009fcf69b8f18651cf55a2a1deb392ab.png";

/***/ }),

/***/ "./static/images/logo-fabrique-numerique.svg":
/***/ (function(module, exports) {

module.exports = "/_next/static/images/logo-fabrique-numerique-7a41e0b5605ad0d01869d2d807c1adb8.svg";

/***/ }),

/***/ "./ui.config.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony default export */ __webpack_exports__["a"] = ({
  // interactive elements
  colors: {
    primary: "#a1d273",
    primaryLight: "#a6e14c",
    secondary: "white",
    secondaryDark: "rgb(240, 240, 240)"
  },
  breakpoints: {
    smallScreen: "@media (max-width: 1000px)"
  }
});
/*
  --primary-color-text: #8c2;
  --primary-color-background: #a1d273;
  --primary-color-button: rgb(136, 204, 34);
  --primary-color-button-dark: #6ba01b;
  --primary-color-button-light: #a6e14c;
  --menu-height: 50px;
  --paragraph-font-size: 24px;
  */

/***/ }),

/***/ 3:
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__("./pages/index.js");


/***/ }),

/***/ "next/head":
/***/ (function(module, exports) {

module.exports = require("next/head");

/***/ }),

/***/ "next/link":
/***/ (function(module, exports) {

module.exports = require("next/link");

/***/ }),

/***/ "prop-types":
/***/ (function(module, exports) {

module.exports = require("prop-types");

/***/ }),

/***/ "react":
/***/ (function(module, exports) {

module.exports = require("react");

/***/ }),

/***/ "react-jss":
/***/ (function(module, exports) {

module.exports = require("react-jss");

/***/ })

/******/ });
//# sourceMappingURL=index.js.map