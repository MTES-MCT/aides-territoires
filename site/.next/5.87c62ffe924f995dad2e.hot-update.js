webpackHotUpdate(5,{

/***/ "./components/ui/Navigation.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_link__ = __webpack_require__("./node_modules/next/link.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_link___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_next_link__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_prop_types__ = __webpack_require__("./node_modules/next/node_modules/prop-types/index.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_prop_types___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_prop_types__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__Container__ = __webpack_require__("./components/ui/Container.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__static_images_logo_aides_territoires_png__ = __webpack_require__("./static/images/logo-aides-territoires.png");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__static_images_logo_aides_territoires_png___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4__static_images_logo_aides_territoires_png__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__static_images_logo_fabrique_numerique_svg__ = __webpack_require__("./static/images/logo-fabrique-numerique.svg");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__static_images_logo_fabrique_numerique_svg___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_5__static_images_logo_fabrique_numerique_svg__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_react_jss__ = __webpack_require__("./node_modules/react-jss/lib/index.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_react_jss___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_6_react_jss__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__ui_config__ = __webpack_require__("./ui.config.js");
var _class,
    _temp2,
    _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Navigation.js";

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();

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
  }, {
    key: "__reactstandin__regenerateByEval",
    // @ts-ignore
    value: function __reactstandin__regenerateByEval(key, code) {
      // @ts-ignore
      this[key] = eval(code);
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
var _default = Navigation;
/* harmony default export */ __webpack_exports__["a"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(Navigation, "Navigation", "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Navigation.js");
  reactHotLoader.register(MenuRight, "MenuRight", "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Navigation.js");
  reactHotLoader.register(MenuLogoAidesTerritoires, "MenuLogoAidesTerritoires", "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Navigation.js");
  reactHotLoader.register(MenuLogoFabriqueNumerique, "MenuLogoFabriqueNumerique", "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Navigation.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Navigation.js");
  leaveModule(module);
})();

;
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ })

})
//# sourceMappingURL=5.87c62ffe924f995dad2e.hot-update.js.map