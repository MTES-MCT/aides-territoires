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
/******/ 	return __webpack_require__(__webpack_require__.s = 1);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports) {

module.exports = require("react");

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(2);


/***/ }),
/* 2 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });

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

// CONCATENATED MODULE: ./components/Header.js
var Header__createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function Header__classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function Header__possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function Header__inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var Header_Header = function (_React$Component) {
  Header__inherits(Header, _React$Component);

  function Header() {
    Header__classCallCheck(this, Header);

    return Header__possibleConstructorReturn(this, (Header.__proto__ || Object.getPrototypeOf(Header)).apply(this, arguments));
  }

  Header__createClass(Header, [{
    key: "render",
    value: function render() {
      return external__react__default.a.createElement(
        "section",
        { id: "aides-territoires", className: "hero " },
        external__react__default.a.createElement(
          "header",
          { className: "header " },
          external__react__default.a.createElement(
            "div",
            { className: "header-overlay " },
            external__react__default.a.createElement(
              "div",
              { className: "hero-body " },
              external__react__default.a.createElement(
                "div",
                { className: "container " },
                external__react__default.a.createElement(
                  "h1",
                  { className: "title " },
                  "UN OUTIL POUR LES COLLECTIVIT\xC9S"
                ),
                external__react__default.a.createElement(
                  "h2",
                  { className: "subtitle " },
                  external__react__default.a.createElement(
                    "p",
                    null,
                    "Identifiez en quelques clics toutes les aides disponibles sur votre territoire pour vos projets d'am\xE9nagements durables.",
                    external__react__default.a.createElement("br", null),
                    external__react__default.a.createElement("br", null),
                    " Un service actuellement exp\xE9riment\xE9 pour les projets de quartiers durables, dont les EcoQuartiers."
                  )
                ),
                external__react__default.a.createElement(
                  "div",
                  { className: "button is-large is-primary " },
                  external__react__default.a.createElement(
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
}(external__react__default.a.Component);

/* harmony default export */ var components_Header = (Header_Header);
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
        external__react__default.a.createElement(components_Header, null),
        this.props.children
      );
    }
  }]);

  return DefaultLayout;
}(external__react__default.a.Component);

/* harmony default export */ var components_DefaultLayout = (DefaultLayout_DefaultLayout);
// CONCATENATED MODULE: ./components/SectionCommentCaMarche.js
var SectionCommentCaMarche__createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function SectionCommentCaMarche__classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function SectionCommentCaMarche__possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function SectionCommentCaMarche__inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SectionCommentCaMarche_SectionCommentCaMarche = function (_React$Component) {
  SectionCommentCaMarche__inherits(SectionCommentCaMarche, _React$Component);

  function SectionCommentCaMarche() {
    SectionCommentCaMarche__classCallCheck(this, SectionCommentCaMarche);

    return SectionCommentCaMarche__possibleConstructorReturn(this, (SectionCommentCaMarche.__proto__ || Object.getPrototypeOf(SectionCommentCaMarche)).apply(this, arguments));
  }

  SectionCommentCaMarche__createClass(SectionCommentCaMarche, [{
    key: "render",
    value: function render() {
      return external__react__default.a.createElement(
        "section",
        { id: "comment-ca-marche", className: "section" },
        external__react__default.a.createElement(
          "div",
          { className: "container " },
          external__react__default.a.createElement(
            "h2",
            { className: "section-title title is-3" },
            "Comment \xE7a marche ?"
          ),
          external__react__default.a.createElement(
            "div",
            { className: "columns" },
            external__react__default.a.createElement(
              "div",
              { className: "column" },
              external__react__default.a.createElement(
                "div",
                { className: "numero" },
                "1"
              ),
              external__react__default.a.createElement(
                "h3",
                { className: "title is-4" },
                "Un territoire, un projet"
              ),
              external__react__default.a.createElement(
                "p",
                null,
                "Donnez nous votre localisation et votre projet "
              )
            ),
            external__react__default.a.createElement(
              "div",
              { className: "column" },
              external__react__default.a.createElement(
                "div",
                { className: "numero" },
                "2"
              ),
              external__react__default.a.createElement(
                "h3",
                { className: "title is-4" },
                "Des aides"
              ),
              external__react__default.a.createElement(
                "p",
                null,
                "Nous vous aidons \xE0 identifier les meilleures aides publiques mobilisables"
              )
            ),
            external__react__default.a.createElement(
              "div",
              { className: "column" },
              external__react__default.a.createElement(
                "div",
                { className: "numero" },
                "3"
              ),
              external__react__default.a.createElement(
                "h3",
                { className: "title is-4" },
                "Du temps gagn\xE9"
              ),
              external__react__default.a.createElement(
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
}(external__react__default.a.Component);

/* harmony default export */ var components_SectionCommentCaMarche = (SectionCommentCaMarche_SectionCommentCaMarche);
// CONCATENATED MODULE: ./components/SectionChronophage.js
var SectionChronophage__createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function SectionChronophage__classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function SectionChronophage__possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function SectionChronophage__inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SectionChronophage_SectionChronophage = function (_React$Component) {
  SectionChronophage__inherits(SectionChronophage, _React$Component);

  function SectionChronophage() {
    SectionChronophage__classCallCheck(this, SectionChronophage);

    return SectionChronophage__possibleConstructorReturn(this, (SectionChronophage.__proto__ || Object.getPrototypeOf(SectionChronophage)).apply(this, arguments));
  }

  SectionChronophage__createClass(SectionChronophage, [{
    key: "render",
    value: function render() {
      return external__react__default.a.createElement(
        "section",
        { id: "chronophage", className: "section " },
        external__react__default.a.createElement(
          "div",
          { className: "container " },
          external__react__default.a.createElement(
            "p",
            null,
            "L'acc\xE8s aux aides publiques disponibles et pertinentes pour vos projets est trop souvent synonyme de veille chronophage au d\xE9triment du temps pass\xE9 sur le projet en lui-m\xEAme."
          )
        )
      );
    }
  }]);

  return SectionChronophage;
}(external__react__default.a.Component);

/* harmony default export */ var components_SectionChronophage = (SectionChronophage_SectionChronophage);
// CONCATENATED MODULE: ./components/SectionBenefices.js
var SectionBenefices__createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function SectionBenefices__classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function SectionBenefices__possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function SectionBenefices__inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SectionBenefices_SectionBenefices = function (_React$Component) {
  SectionBenefices__inherits(SectionBenefices, _React$Component);

  function SectionBenefices() {
    SectionBenefices__classCallCheck(this, SectionBenefices);

    return SectionBenefices__possibleConstructorReturn(this, (SectionBenefices.__proto__ || Object.getPrototypeOf(SectionBenefices)).apply(this, arguments));
  }

  SectionBenefices__createClass(SectionBenefices, [{
    key: "render",
    value: function render() {
      return external__react__default.a.createElement(
        "section",
        { id: "benefices", className: "section " },
        external__react__default.a.createElement(
          "div",
          { className: "container" },
          external__react__default.a.createElement(
            "div",
            { className: "content " },
            "Avec Aides-territoires :",
            external__react__default.a.createElement(
              "ul",
              null,
              external__react__default.a.createElement(
                "li",
                null,
                " ",
                "Gagnez du temps dans votre recherche d'aides, de l'accompagnement au financement"
              ),
              external__react__default.a.createElement(
                "li",
                null,
                " ",
                "Ne passez plus \xE0 c\xF4t\xE9 des aides qui correspondent \xE0 votre projet"
              ),
              external__react__default.a.createElement(
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
}(external__react__default.a.Component);

/* harmony default export */ var components_SectionBenefices = (SectionBenefices_SectionBenefices);
// CONCATENATED MODULE: ./components/SectionTypesAides.js
var SectionTypesAides__createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function SectionTypesAides__classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function SectionTypesAides__possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function SectionTypesAides__inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SectionTypesAides_SectionTypeAides = function (_React$Component) {
  SectionTypesAides__inherits(SectionTypeAides, _React$Component);

  function SectionTypeAides() {
    SectionTypesAides__classCallCheck(this, SectionTypeAides);

    return SectionTypesAides__possibleConstructorReturn(this, (SectionTypeAides.__proto__ || Object.getPrototypeOf(SectionTypeAides)).apply(this, arguments));
  }

  SectionTypesAides__createClass(SectionTypeAides, [{
    key: "render",
    value: function render() {
      return external__react__default.a.createElement(
        "section",
        { id: "types-aides", className: "section" },
        external__react__default.a.createElement(
          "div",
          { className: "container" },
          external__react__default.a.createElement(
            "p",
            { className: "text" },
            "Quelque soit le stade d'avancement de votre projet d'\xC9coQuartier, Aides-territoires vous permet d'identifier les aides pertinentes:"
          ),
          external__react__default.a.createElement(
            "div",
            { className: "content " },
            external__react__default.a.createElement(
              "div",
              { className: "columns" },
              external__react__default.a.createElement(
                "div",
                { className: "column" },
                external__react__default.a.createElement(
                  "div",
                  { className: "aides-icon" },
                  external__react__default.a.createElement("img", { src: "/static/images/icon-compas.png" })
                ),
                external__react__default.a.createElement(
                  "h2",
                  { className: "title is-4" },
                  "Ing\xE9nierie"
                )
              ),
              external__react__default.a.createElement(
                "div",
                { className: "column" },
                external__react__default.a.createElement(
                  "div",
                  { className: "aides-icon" },
                  external__react__default.a.createElement("img", { src: "/static/images/icon-financement.png" })
                ),
                external__react__default.a.createElement(
                  "h2",
                  { className: "title is-4" },
                  "Financement"
                )
              ),
              external__react__default.a.createElement(
                "div",
                { className: "column" },
                external__react__default.a.createElement(
                  "div",
                  { className: "aides-icon" },
                  external__react__default.a.createElement("img", { src: "/static/images/icon-journal.png" })
                ),
                external__react__default.a.createElement(
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
}(external__react__default.a.Component);

/* harmony default export */ var SectionTypesAides = (SectionTypesAides_SectionTypeAides);
// CONCATENATED MODULE: ./components/SendInBlueInscrivezVous.js
var SendInBlueInscrivezVous__createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function SendInBlueInscrivezVous__classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function SendInBlueInscrivezVous__possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function SendInBlueInscrivezVous__inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SendInBlueInscrivezVous_SendInBlueInscrivezVous = function (_React$Component) {
  SendInBlueInscrivezVous__inherits(SendInBlueInscrivezVous, _React$Component);

  function SendInBlueInscrivezVous() {
    SendInBlueInscrivezVous__classCallCheck(this, SendInBlueInscrivezVous);

    return SendInBlueInscrivezVous__possibleConstructorReturn(this, (SendInBlueInscrivezVous.__proto__ || Object.getPrototypeOf(SendInBlueInscrivezVous)).apply(this, arguments));
  }

  SendInBlueInscrivezVous__createClass(SendInBlueInscrivezVous, [{
    key: "render",
    value: function render() {
      return external__react__default.a.createElement(
        "section",
        { id: "inscription", className: "section lancez-votre-recherche" },
        external__react__default.a.createElement("iframe", {
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
}(external__react__default.a.Component);

/* harmony default export */ var components_SendInBlueInscrivezVous = (SendInBlueInscrivezVous_SendInBlueInscrivezVous);
// EXTERNAL MODULE: external "graphql-request"
var external__graphql_request_ = __webpack_require__(4);
var external__graphql_request__default = /*#__PURE__*/__webpack_require__.n(external__graphql_request_);

// EXTERNAL MODULE: external "next/config"
var config_ = __webpack_require__(5);
var config__default = /*#__PURE__*/__webpack_require__.n(config_);

// CONCATENATED MODULE: ./components/SendInBlueContactForm.js
var SendInBlueContactForm__createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function SendInBlueContactForm__classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function SendInBlueContactForm__possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function SendInBlueContactForm__inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }





var _getConfig = config__default()(),
    publicRuntimeConfig = _getConfig.publicRuntimeConfig;

var EMAIL_SENDING_STATUS_NOT_STARTED = "not_started";
var EMAIL_SENDING_STATUS_PENDING = "pending";
var EMAIL_SENDING_STATUS_SENT = "sent";
var EMAIL_SENDING_STATUS_ERROR = "error";

var SendInBlueContactForm_ContactForm = function (_React$Component) {
  SendInBlueContactForm__inherits(ContactForm, _React$Component);

  function ContactForm(props) {
    SendInBlueContactForm__classCallCheck(this, ContactForm);

    var _this = SendInBlueContactForm__possibleConstructorReturn(this, (ContactForm.__proto__ || Object.getPrototypeOf(ContactForm)).call(this, props));

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

  SendInBlueContactForm__createClass(ContactForm, [{
    key: "sendEmail",
    value: function sendEmail() {
      var query = "\n    mutation sendContactFormEmail($from:String!,$text:String!) {\n      sendContactFormEmail(from: $from, text:$text) {\n        from\n        text\n      }\n    }";
      var variables = {
        from: this.state.email,
        text: this.state.message
      };
      return Object(external__graphql_request_["request"])(publicRuntimeConfig.GRAPHQL_URL, query, variables);
    }
  }, {
    key: "render",
    value: function render() {
      return external__react__default.a.createElement(
        "div",
        null,
        external__react__default.a.createElement(
          "p",
          { className: "text" },
          "Vous avez encore des questions ? des suggestions ? N'h\xE9sitez pas, nous sommes \xE0 votre disposition et serons ravis d'\xE9changer avec vous : laissez-nous un message !",
          external__react__default.a.createElement("br", null),
          external__react__default.a.createElement("br", null)
        ),
        this.state.emailSendingStatus === EMAIL_SENDING_STATUS_ERROR && external__react__default.a.createElement(
          "div",
          null,
          "D\xE9sol\xE9 nous avons rencontr\xE9 une erreur lors de l'envoi de l'email. Vous pouvez nous contacter \xE0 l'addresse suivante :",
          external__react__default.a.createElement(
            "strong",
            null,
            "contact@aides-territoires.beta.gouv.fr"
          ),
          " ou",
          " ",
          external__react__default.a.createElement(
            "strong",
            null,
            "elise.marion@beta.gouv.fr"
          )
        ),
        this.state.emailSendingStatus === EMAIL_SENDING_STATUS_SENT && external__react__default.a.createElement(
          "div",
          { className: "section message is-success" },
          "Merci! Votre message a bien \xE9t\xE9 envoy\xE9."
        ),
        this.state.emailSendingStatus !== EMAIL_SENDING_STATUS_ERROR && this.state.emailSendingStatus !== EMAIL_SENDING_STATUS_SENT && external__react__default.a.createElement(
          "form",
          { id: "contact-form", onSubmit: this.handleSubmit },
          external__react__default.a.createElement(
            "div",
            { className: "field" },
            external__react__default.a.createElement(
              "label",
              { className: "label" },
              "Votre email*"
            ),
            external__react__default.a.createElement(
              "div",
              { className: "control" },
              external__react__default.a.createElement("input", {
                id: "email",
                onChange: this.onEmailChange,
                className: "input is-large",
                type: "text",
                placeholder: "Email",
                required: true
              })
            )
          ),
          external__react__default.a.createElement(
            "div",
            { className: "field" },
            external__react__default.a.createElement(
              "label",
              { className: "label" },
              "Votre message"
            ),
            external__react__default.a.createElement(
              "div",
              { className: "control" },
              external__react__default.a.createElement("textarea", {
                onChange: this.onMessageChange,
                id: "message",
                className: "textarea",
                placeholder: "Votre message"
              })
            )
          ),
          external__react__default.a.createElement(
            "div",
            { className: "field is-grouped is-grouped-right" },
            external__react__default.a.createElement(
              "div",
              { className: "control" },
              external__react__default.a.createElement("input", {
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
}(external__react__default.a.Component);

/* harmony default export */ var SendInBlueContactForm = (SendInBlueContactForm_ContactForm);
// CONCATENATED MODULE: ./pages/index.js
var pages__createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function pages__classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function pages__possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function pages__inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }










var pages_HomePage = function (_React$Component) {
  pages__inherits(HomePage, _React$Component);

  function HomePage() {
    pages__classCallCheck(this, HomePage);

    return pages__possibleConstructorReturn(this, (HomePage.__proto__ || Object.getPrototypeOf(HomePage)).apply(this, arguments));
  }

  pages__createClass(HomePage, [{
    key: "render",
    value: function render() {
      return external__react__default.a.createElement(
        components_DefaultLayout,
        null,
        external__react__default.a.createElement(components_SectionCommentCaMarche, null),
        external__react__default.a.createElement(components_SectionChronophage, null),
        external__react__default.a.createElement(components_SectionBenefices, null),
        external__react__default.a.createElement("hr", null),
        external__react__default.a.createElement(SectionTypesAides, null),
        external__react__default.a.createElement(components_SendInBlueInscrivezVous, null),
        external__react__default.a.createElement(
          "section",
          { id: "contact", className: "section container" },
          external__react__default.a.createElement(SendInBlueContactForm, null)
        )
      );
    }
  }]);

  return HomePage;
}(external__react__default.a.Component);

/* harmony default export */ var pages = __webpack_exports__["default"] = (pages_HomePage);

/***/ }),
/* 3 */
/***/ (function(module, exports) {

module.exports = require("next/head");

/***/ }),
/* 4 */
/***/ (function(module, exports) {

module.exports = require("graphql-request");

/***/ }),
/* 5 */
/***/ (function(module, exports) {

module.exports = require("next/config");

/***/ })
/******/ ]);