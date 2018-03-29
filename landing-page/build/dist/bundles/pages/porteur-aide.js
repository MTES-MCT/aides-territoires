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
/******/ 	return __webpack_require__(__webpack_require__.s = 16);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports) {

module.exports = require("react");

/***/ }),
/* 1 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var Header = function (_React$Component) {
  _inherits(Header, _React$Component);

  function Header() {
    _classCallCheck(this, Header);

    return _possibleConstructorReturn(this, (Header.__proto__ || Object.getPrototypeOf(Header)).apply(this, arguments));
  }

  _createClass(Header, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "section",
        { id: "aides-territoires", className: "hero " },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "header",
          { className: "header " },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "header-overlay " },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "hero-body " },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "container " },
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "h1",
                  { className: "title " },
                  "UN OUTIL POUR LES COLLECTIVIT\xC9S"
                ),
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "h2",
                  { className: "subtitle " },
                  __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                    "p",
                    null,
                    "Identifiez en quelques clics toutes les aides disponibles sur votre territoire pour vos projets d'am\xE9nagements durables.",
                    __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("br", null),
                    __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("br", null),
                    " Un service actuellement exp\xE9riment\xE9 pour les projets de quartiers durables, dont les EcoQuartiers."
                  )
                ),
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "div",
                  { className: "button is-large is-primary " },
                  __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                    "a",
                    {
                      className: "button-lancez-la-recherche js-scrollTo ",
                      href: "#inscription"
                    },
                    "Lancez votre recherche"
                  )
                )
              )
            )
          )
        )
      );
    }
  }]);

  return Header;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (Header);

/***/ }),
/* 2 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";

// EXTERNAL MODULE: external "react"
var external__react_ = __webpack_require__(0);
var external__react__default = /*#__PURE__*/__webpack_require__.n(external__react_);

// CONCATENATED MODULE: ./components/Navigation.js
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var Navigation_Navigation = function (_React$Component) {
  _inherits(Navigation, _React$Component);

  function Navigation(props) {
    _classCallCheck(this, Navigation);

    var _this = _possibleConstructorReturn(this, (Navigation.__proto__ || Object.getPrototypeOf(Navigation)).call(this, props));

    _this.handleClick = function () {
      _this.setState({
        mobileMenuIsActive: !_this.state.mobileMenuIsActive
      });
    };

    _this.state = {
      mobileMenuIsActive: false
    };
    return _this;
  }

  _createClass(Navigation, [{
    key: "render",
    value: function render() {
      return external__react__default.a.createElement(
        "nav",
        {
          className: "navbar is-fixed-top app-main-menu",
          role: "navigation",
          "aria-label": "main navigation"
        },
        external__react__default.a.createElement(
          "div",
          { className: "navbar-brand" },
          external__react__default.a.createElement(
            "a",
            { className: "navbar-item js-scrollTo", href: "#aides-territoires" },
            external__react__default.a.createElement("img", { src: "/static/images/logo.png " }),
            external__react__default.a.createElement(
              "p",
              { className: "app-name " },
              "Aides-territoires"
            )
          ),
          external__react__default.a.createElement(
            "div",
            {
              className: this.state.mobileMenuIsActive ? "navbar-burger is-active" : "navbar-burger",
              "data-target": "navMenu",
              onClick: this.handleClick
            },
            external__react__default.a.createElement("span", null),
            external__react__default.a.createElement("span", null),
            external__react__default.a.createElement("span", null)
          )
        ),
        external__react__default.a.createElement(
          "div",
          {
            className: this.state.mobileMenuIsActive ? "navbar-menu is-active" : "navbar-menu",
            id: "navMenu "
          },
          external__react__default.a.createElement(
            "div",
            { className: "navbar-end" },
            external__react__default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#aides-territoires" },
              "Aides-territoires"
            ),
            external__react__default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#comment-ca-marche" },
              "Le service"
            ),
            external__react__default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#inscription" },
              "Inscription"
            ),
            external__react__default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/porteur-aide" },
              "Porteur d'aide"
            ),
            external__react__default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#contact" },
              "Contact"
            )
          )
        )
      );
    }
  }]);

  return Navigation;
}(external__react__default.a.Component);

/* harmony default export */ var components_Navigation = (Navigation_Navigation);
// EXTERNAL MODULE: external "next/head"
var head_ = __webpack_require__(3);
var head__default = /*#__PURE__*/__webpack_require__.n(head_);

// EXTERNAL MODULE: ./components/Header.js
var Header = __webpack_require__(1);

// CONCATENATED MODULE: ./components/DefaultLayout.js
var DefaultLayout__createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function DefaultLayout__classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function DefaultLayout__possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function DefaultLayout__inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }






var DefaultLayout_DefaultLayout = function (_React$Component) {
  DefaultLayout__inherits(DefaultLayout, _React$Component);

  function DefaultLayout() {
    DefaultLayout__classCallCheck(this, DefaultLayout);

    return DefaultLayout__possibleConstructorReturn(this, (DefaultLayout.__proto__ || Object.getPrototypeOf(DefaultLayout)).apply(this, arguments));
  }

  DefaultLayout__createClass(DefaultLayout, [{
    key: "render",
    value: function render() {
      return external__react__default.a.createElement(
        "div",
        { className: "default-layout" },
        external__react__default.a.createElement(
          head__default.a,
          null,
          external__react__default.a.createElement("meta", {
            name: "viewport",
            content: "initial-scale=1.0, width=device-width"
          }),
          external__react__default.a.createElement("link", { rel: "stylesheet", href: "/static/css/bulma.css" }),
          external__react__default.a.createElement("link", { rel: "stylesheet", href: "/static/css/style.css" })
        ),
        external__react__default.a.createElement(components_Navigation, null),
        this.props.children
      );
    }
  }]);

  return DefaultLayout;
}(external__react__default.a.Component);

/* harmony default export */ var components_DefaultLayout = __webpack_exports__["a"] = (DefaultLayout_DefaultLayout);

/***/ }),
/* 3 */
/***/ (function(module, exports) {

module.exports = require("next/head");

/***/ }),
/* 4 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SectionCommentCaMarche = function (_React$Component) {
  _inherits(SectionCommentCaMarche, _React$Component);

  function SectionCommentCaMarche() {
    _classCallCheck(this, SectionCommentCaMarche);

    return _possibleConstructorReturn(this, (SectionCommentCaMarche.__proto__ || Object.getPrototypeOf(SectionCommentCaMarche)).apply(this, arguments));
  }

  _createClass(SectionCommentCaMarche, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "section",
        { id: "comment-ca-marche", className: "section" },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "container " },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "h2",
            { className: "section-title title is-3" },
            "Comment \xE7a marche ?"
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "columns" },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "column" },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "numero" },
                "1"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "h3",
                { className: "title is-4" },
                "Un territoire, un projet"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "p",
                null,
                "Donnez nous votre localisation et votre projet "
              )
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "column" },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "numero" },
                "2"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "h3",
                { className: "title is-4" },
                "Des aides"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "p",
                null,
                "Nous vous aidons \xE0 identifier les meilleures aides publiques mobilisables"
              )
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "column" },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "numero" },
                "3"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "h3",
                { className: "title is-4" },
                "Du temps gagn\xE9"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "p",
                null,
                "passez plus de temps sur votre projet en activant les aides pertinentes au bon moment"
              )
            )
          )
        )
      );
    }
  }]);

  return SectionCommentCaMarche;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (SectionCommentCaMarche);

/***/ }),
/* 5 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SectionChronophage = function (_React$Component) {
  _inherits(SectionChronophage, _React$Component);

  function SectionChronophage() {
    _classCallCheck(this, SectionChronophage);

    return _possibleConstructorReturn(this, (SectionChronophage.__proto__ || Object.getPrototypeOf(SectionChronophage)).apply(this, arguments));
  }

  _createClass(SectionChronophage, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "section",
        { id: "chronophage", className: "section " },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "container " },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "p",
            null,
            "L'acc\xE8s aux aides publiques disponibles et pertinentes pour vos projets est trop souvent synonyme de veille chronophage au d\xE9triment du temps pass\xE9 sur le projet en lui-m\xEAme."
          )
        )
      );
    }
  }]);

  return SectionChronophage;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (SectionChronophage);

/***/ }),
/* 6 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SectionBenefices = function (_React$Component) {
  _inherits(SectionBenefices, _React$Component);

  function SectionBenefices() {
    _classCallCheck(this, SectionBenefices);

    return _possibleConstructorReturn(this, (SectionBenefices.__proto__ || Object.getPrototypeOf(SectionBenefices)).apply(this, arguments));
  }

  _createClass(SectionBenefices, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "section",
        { id: "benefices", className: "section " },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "container" },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "content " },
            "Avec Aides-territoires :",
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "ul",
              null,
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "li",
                null,
                " ",
                "Gagnez du temps dans votre recherche d'aides, de l'accompagnement au financement"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "li",
                null,
                " ",
                "Ne passez plus \xE0 c\xF4t\xE9 des aides qui correspondent \xE0 votre projet"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "li",
                null,
                "B\xE9n\xE9ficiez d'une s\xE9lection pertinente \xE0 chaque \xE9tape de votre projet"
              )
            )
          )
        )
      );
    }
  }]);

  return SectionBenefices;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (SectionBenefices);

/***/ }),
/* 7 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SectionTypeAides = function (_React$Component) {
  _inherits(SectionTypeAides, _React$Component);

  function SectionTypeAides() {
    _classCallCheck(this, SectionTypeAides);

    return _possibleConstructorReturn(this, (SectionTypeAides.__proto__ || Object.getPrototypeOf(SectionTypeAides)).apply(this, arguments));
  }

  _createClass(SectionTypeAides, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "section",
        { id: "types-aides", className: "section" },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "container" },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "p",
            { className: "text" },
            "Quelque soit le stade d'avancement de votre projet d'\xC9coQuartier, Aides-territoires vous permet d'identifier les aides pertinentes:"
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "content " },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "columns" },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "column" },
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "div",
                  { className: "aides-icon" },
                  __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("img", { src: "/static/images/icon-compas.png" })
                ),
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "h2",
                  { className: "title is-4" },
                  "Ing\xE9nierie"
                )
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "column" },
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "div",
                  { className: "aides-icon" },
                  __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("img", { src: "/static/images/icon-financement.png" })
                ),
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "h2",
                  { className: "title is-4" },
                  "Financement"
                )
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "column" },
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "div",
                  { className: "aides-icon" },
                  __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("img", { src: "/static/images/icon-journal.png" })
                ),
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "h2",
                  { className: "title is-4" },
                  "Appels \xE0 projet"
                )
              )
            )
          )
        )
      );
    }
  }]);

  return SectionTypeAides;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (SectionTypeAides);

/***/ }),
/* 8 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SendInBlueInscrivezVous = function (_React$Component) {
  _inherits(SendInBlueInscrivezVous, _React$Component);

  function SendInBlueInscrivezVous() {
    _classCallCheck(this, SendInBlueInscrivezVous);

    return _possibleConstructorReturn(this, (SendInBlueInscrivezVous.__proto__ || Object.getPrototypeOf(SendInBlueInscrivezVous)).apply(this, arguments));
  }

  _createClass(SendInBlueInscrivezVous, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "section",
        { id: "inscription", className: "section lancez-votre-recherche" },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("iframe", {
          width: "100%",
          height: "850",
          src: "https://my.sendinblue.com/users/subscribe/js_id/35zg8/id/1",
          frameBorder: "0",
          scrolling: "auto",
          allowFullScreen: true,
          style: {
            background: "transparent",
            display: "block",
            marginLeft: "auto",
            marginRight: "auto",
            maxWidth: "100%"
          }
        })
      );
    }
  }]);

  return SendInBlueInscrivezVous;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (SendInBlueInscrivezVous);

/***/ }),
/* 9 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_graphql_request__ = __webpack_require__(10);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_graphql_request___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_graphql_request__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_config__ = __webpack_require__(11);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_config___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_next_config__);
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }





var _getConfig = __WEBPACK_IMPORTED_MODULE_2_next_config___default()(),
    publicRuntimeConfig = _getConfig.publicRuntimeConfig;

var EMAIL_SENDING_STATUS_NOT_STARTED = "not_started";
var EMAIL_SENDING_STATUS_PENDING = "pending";
var EMAIL_SENDING_STATUS_SENT = "sent";
var EMAIL_SENDING_STATUS_ERROR = "error";

var ContactForm = function (_React$Component) {
  _inherits(ContactForm, _React$Component);

  function ContactForm(props) {
    _classCallCheck(this, ContactForm);

    var _this = _possibleConstructorReturn(this, (ContactForm.__proto__ || Object.getPrototypeOf(ContactForm)).call(this, props));

    _this.handleSubmit = function (event) {
      event.preventDefault();
      _this.setState({
        emailSendingStatus: EMAIL_SENDING_STATUS_PENDING
      });
      _this.sendEmail().then(function (r) {
        _this.setState({
          emailSendingStatus: EMAIL_SENDING_STATUS_SENT
        });
      }).catch(function (e) {
        _this.setState({
          emailSendingStatus: EMAIL_SENDING_STATUS_ERROR
        });
      });
    };

    _this.onEmailChange = function (event) {
      _this.setState({ email: event.target.value });
    };

    _this.onMessageChange = function (event) {
      _this.setState({ message: event.target.value });
    };

    _this.state = {
      email: "",
      message: "",
      emailSendingStatus: EMAIL_SENDING_STATUS_NOT_STARTED
    };
    return _this;
  }

  _createClass(ContactForm, [{
    key: "sendEmail",
    value: function sendEmail() {
      var query = "\n    mutation sendContactFormEmail($from:String!,$text:String!) {\n      sendContactFormEmail(from: $from, text:$text) {\n        from\n        text\n      }\n    }";
      var variables = {
        from: this.state.email,
        text: this.state.message
      };
      return Object(__WEBPACK_IMPORTED_MODULE_1_graphql_request__["request"])(publicRuntimeConfig.GRAPHQL_URL, query, variables);
    }
  }, {
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "div",
        null,
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "p",
          { className: "text" },
          "Vous avez encore des questions ? des suggestions ? N'h\xE9sitez pas, nous sommes \xE0 votre disposition et serons ravis d'\xE9changer avec vous : laissez-nous un message !",
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("br", null),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("br", null)
        ),
        this.state.emailSendingStatus === EMAIL_SENDING_STATUS_ERROR && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          null,
          "D\xE9sol\xE9 nous avons rencontr\xE9 une erreur lors de l'envoi de l'email. Vous pouvez nous contacter \xE0 l'addresse suivante :",
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "strong",
            null,
            "contact@aides-territoires.beta.gouv.fr"
          ),
          " ou",
          " ",
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "strong",
            null,
            "elise.marion@beta.gouv.fr"
          )
        ),
        this.state.emailSendingStatus === EMAIL_SENDING_STATUS_SENT && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "section message is-success" },
          "Merci! Votre message a bien \xE9t\xE9 envoy\xE9."
        ),
        this.state.emailSendingStatus !== EMAIL_SENDING_STATUS_ERROR && this.state.emailSendingStatus !== EMAIL_SENDING_STATUS_SENT && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "form",
          { id: "contact-form", onSubmit: this.handleSubmit },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "field" },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "label",
              { className: "label" },
              "Votre email*"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "control" },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("input", {
                id: "email",
                onChange: this.onEmailChange,
                className: "input is-large",
                type: "text",
                placeholder: "Email",
                required: true
              })
            )
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "field" },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "label",
              { className: "label" },
              "Votre message"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "control" },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("textarea", {
                onChange: this.onMessageChange,
                id: "message",
                className: "textarea",
                placeholder: "Votre message"
              })
            )
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "field is-grouped is-grouped-right" },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "control" },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("input", {
                type: "submit",
                value: "envoyer",
                className: "button is-link is-large is-primary"
              })
            )
          )
        )
      );
    }
  }]);

  return ContactForm;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (ContactForm);

/***/ }),
/* 10 */
/***/ (function(module, exports) {

module.exports = require("graphql-request");

/***/ }),
/* 11 */
/***/ (function(module, exports) {

module.exports = require("next/config");

/***/ }),
/* 12 */,
/* 13 */,
/* 14 */,
/* 15 */,
/* 16 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(17);


/***/ }),
/* 17 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });

// EXTERNAL MODULE: external "react"
var external__react_ = __webpack_require__(0);
var external__react__default = /*#__PURE__*/__webpack_require__.n(external__react_);

// EXTERNAL MODULE: ./components/DefaultLayout.js + 1 modules
var DefaultLayout = __webpack_require__(2);

// CONCATENATED MODULE: ./components/HeaderPorteurAide.js
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var HeaderPorteurAide_HeaderPorteurAide = function (_React$Component) {
  _inherits(HeaderPorteurAide, _React$Component);

  function HeaderPorteurAide() {
    _classCallCheck(this, HeaderPorteurAide);

    return _possibleConstructorReturn(this, (HeaderPorteurAide.__proto__ || Object.getPrototypeOf(HeaderPorteurAide)).apply(this, arguments));
  }

  _createClass(HeaderPorteurAide, [{
    key: "render",
    value: function render() {
      return external__react__default.a.createElement(
        "section",
        { id: "aides-territoires", className: "hero" },
        external__react__default.a.createElement(
          "header",
          { className: "header" },
          external__react__default.a.createElement(
            "div",
            { className: "header-overlay" },
            external__react__default.a.createElement(
              "div",
              { className: "hero-body" },
              external__react__default.a.createElement(
                "div",
                { className: "container" },
                external__react__default.a.createElement(
                  "h1",
                  { className: "title" },
                  "Porteur d'aides"
                ),
                external__react__default.a.createElement(
                  "h2",
                  { className: "subtitle" },
                  external__react__default.a.createElement(
                    "p",
                    null,
                    "Vous portez des aides publiques ou des appels \xE0 projet en faveur de l'am\xE9nagement durable ?",
                    external__react__default.a.createElement("br", null)
                  )
                )
              )
            )
          )
        )
      );
    }
  }]);

  return HeaderPorteurAide;
}(external__react__default.a.Component);

/* harmony default export */ var components_HeaderPorteurAide = (HeaderPorteurAide_HeaderPorteurAide);
// EXTERNAL MODULE: ./components/SectionCommentCaMarche.js
var SectionCommentCaMarche = __webpack_require__(4);

// EXTERNAL MODULE: ./components/SectionChronophage.js
var SectionChronophage = __webpack_require__(5);

// EXTERNAL MODULE: ./components/SectionBenefices.js
var SectionBenefices = __webpack_require__(6);

// EXTERNAL MODULE: ./components/SectionTypesAides.js
var SectionTypesAides = __webpack_require__(7);

// CONCATENATED MODULE: ./components/SectionPorteurAideDescription.js
var SectionPorteurAideDescription__createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function SectionPorteurAideDescription__classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function SectionPorteurAideDescription__possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function SectionPorteurAideDescription__inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SectionPorteurAideDescription_SectionPorteurAideDescription = function (_React$Component) {
  SectionPorteurAideDescription__inherits(SectionPorteurAideDescription, _React$Component);

  function SectionPorteurAideDescription() {
    SectionPorteurAideDescription__classCallCheck(this, SectionPorteurAideDescription);

    return SectionPorteurAideDescription__possibleConstructorReturn(this, (SectionPorteurAideDescription.__proto__ || Object.getPrototypeOf(SectionPorteurAideDescription)).apply(this, arguments));
  }

  SectionPorteurAideDescription__createClass(SectionPorteurAideDescription, [{
    key: "render",
    value: function render() {
      return external__react__default.a.createElement(
        "section",
        { id: "description", className: "section" },
        external__react__default.a.createElement(
          "div",
          { className: "container" },
          external__react__default.a.createElement(
            "div",
            { className: "text" },
            external__react__default.a.createElement(
              "p",
              null,
              "Aides-territoires propose aux porteurs de projets de quartiers durables un service leur permettant d'identifier les aides mobilisables quelles qu'en soient la forme (financement, ing\xE9nierie, y compris les appels \xE0 projets et manifestation d'int\xE9r\xEAt), en fonction de leur territoire et de l'\xE9tat d'avancement de leur projet.",
              " "
            ),
            external__react__default.a.createElement(
              "p",
              null,
              external__react__default.a.createElement(
                "strong",
                null,
                "Vous portez une telle aide ? R\xE9f\xE9rencez-la en moins de 10 minutes et elle sera visible par vos cibles potentielles utilisant le service Aides-territoires."
              ),
              external__react__default.a.createElement("br", null),
              external__react__default.a.createElement("br", null)
            )
          ),
          external__react__default.a.createElement(
            "div",
            { className: "has-text-centered" },
            external__react__default.a.createElement(
              "a",
              {
                href: "https://goo.gl/forms/lVd7CcukMQU7Ral82",
                className: "button is-primary is-large"
              },
              "D\xE9posez votre aide"
            )
          )
        )
      );
    }
  }]);

  return SectionPorteurAideDescription;
}(external__react__default.a.Component);

/* harmony default export */ var components_SectionPorteurAideDescription = (SectionPorteurAideDescription_SectionPorteurAideDescription);
// EXTERNAL MODULE: ./components/SendInBlueInscrivezVous.js
var SendInBlueInscrivezVous = __webpack_require__(8);

// EXTERNAL MODULE: ./components/SendInBlueContactForm.js
var SendInBlueContactForm = __webpack_require__(9);

// CONCATENATED MODULE: ./pages/porteur-aide.js
var porteur_aide__createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function porteur_aide__classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function porteur_aide__possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function porteur_aide__inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }












var porteur_aide_porteurAidePage = function (_React$Component) {
  porteur_aide__inherits(porteurAidePage, _React$Component);

  function porteurAidePage() {
    porteur_aide__classCallCheck(this, porteurAidePage);

    return porteur_aide__possibleConstructorReturn(this, (porteurAidePage.__proto__ || Object.getPrototypeOf(porteurAidePage)).apply(this, arguments));
  }

  porteur_aide__createClass(porteurAidePage, [{
    key: "render",
    value: function render() {
      return external__react__default.a.createElement(
        DefaultLayout["a" /* default */],
        null,
        external__react__default.a.createElement(components_HeaderPorteurAide, null),
        external__react__default.a.createElement(components_SectionPorteurAideDescription, null)
      );
    }
  }]);

  return porteurAidePage;
}(external__react__default.a.Component);

/* harmony default export */ var porteur_aide = __webpack_exports__["default"] = (porteur_aide_porteurAidePage);

/***/ })
/******/ ]);