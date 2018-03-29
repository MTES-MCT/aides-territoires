webpackHotUpdate(3,{

/***/ "./components/Navigation.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/Navigation.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var Navigation = function (_React$Component) {
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
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "nav",
        {
          className: "navbar is-fixed-top app-main-menu",
          role: "navigation",
          "aria-label": "main navigation",
          __source: {
            fileName: _jsxFileName,
            lineNumber: 17
          }
        },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "navbar-brand", __source: {
              fileName: _jsxFileName,
              lineNumber: 22
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "a",
            { className: "navbar-item js-scrollTo", href: "#aides-territoires", __source: {
                fileName: _jsxFileName,
                lineNumber: 23
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("img", { src: "/static/images/logo.png ", __source: {
                fileName: _jsxFileName,
                lineNumber: 24
              }
            }),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "p",
              { className: "app-name ", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 25
                }
              },
              "Aides-territoires"
            )
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            {
              className: this.state.mobileMenuIsActive ? "navbar-burger is-active" : "navbar-burger",
              "data-target": "navMenu",
              onClick: this.handleClick,
              __source: {
                fileName: _jsxFileName,
                lineNumber: 27
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("span", {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 36
              }
            }),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("span", {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 37
              }
            }),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("span", {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 38
              }
            })
          )
        ),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          {
            className: this.state.mobileMenuIsActive ? "navbar-menu is-active" : "navbar-menu",
            id: "navMenu ",
            __source: {
              fileName: _jsxFileName,
              lineNumber: 41
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "navbar-end", __source: {
                fileName: _jsxFileName,
                lineNumber: 49
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#aides-territoires", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 50
                }
              },
              "Aides-territoires"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#comment-ca-marche", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 53
                }
              },
              "Le service"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#inscription", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 56
                }
              },
              "Inscription"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/porteur-aide", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 59
                }
              },
              "Contact"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#contact", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 62
                }
              },
              "Contact"
            )
          )
        )
      );
    }
  }, {
    key: "__reactstandin__regenerateByEval",
    value: function __reactstandin__regenerateByEval(key, code) {
      this[key] = eval(code);
    }
  }]);

  return Navigation;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

var _default = Navigation;


/* harmony default export */ __webpack_exports__["a"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(Navigation, "Navigation", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/Navigation.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/Navigation.js");
  leaveModule(module);
})();

;
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ })

})
//# sourceMappingURL=3.790e3028819e4190c61b.hot-update.js.map