import { Controller } from '/static/@hotwired/stimulus/dist/stimulus.js'

export default class extends Controller {
  departments = {}
  communes = {}
  zoomFrance = 5.5
  centerFrance = [46.227, 2.213]
  defaultFillStyle = {
    weight: 2,
    opacity: 1,
    color: 'white',
    dashArray: '3',
    fillOpacity: 0.6,
  }
  defaultHoverStyle = {
    weight: 4,
    dashArray: '',
    fillOpacity: 0.7,
  }
  static targets = [
    'regions',
    'regionsOrgCount',
    'departments',
    'departmentsOrgCount',
    'communes',
    'communesWithOrg',
    'table',
  ]
  static values = {
    regionsOrgMax: Number,
    departmentsOrgMax: Number,
  }

  #_forwardRegularEvent(e) {
    // This is a hack because Leaflet does not dispatch regular events,
    // so we created that proxy to be able to bind them using Stimulus
    // from the HTML: `data-action="map:moveend->map#switchShapes"`.
    this.dispatch(e.type, { detail: e })
  }

  connect() {
    // Styles to retrieve colors from CSS variables (DesignSystem).
    this.styles = getComputedStyle(document.documentElement)
    this.defaultHoverStyle.color = this.styles.getPropertyValue(
      '--blue-france-sun-113-625'
    )
    // Counts/existence given the perimeter.
    this.regionsOrgCount = JSON.parse(this.regionsOrgCountTarget.textContent)
    this.departmentsOrgCount = JSON.parse(this.departmentsOrgCountTarget.textContent)
    this.communesWithOrg = JSON.parse(this.communesWithOrgTarget.textContent)
    // Compute density scales for map’s legend.
    this.scaleRegions = utils.generateScale(this.regionsOrgMaxValue, 7)
    this.scaleDepartments = utils.generateScale(this.departmentsOrgMaxValue, 7)
    // Only now can we create the map with correct data.
    this.map = this.#initMap()
    this.map.on('moveend', this.#_forwardRegularEvent, this)
  }

  switchShapes() {
    // These two values are empirical, on load, when you zoom in
    // then zoom out you should get back to the same shapes level.
    const zoomRegion = this.zoomFrance + 0.5
    const zoomDepartment = zoomRegion + 2.5
    const currentZoomLevel = this.map.getZoom()
    const regionLevel = currentZoomLevel <= zoomRegion
    const departmentLevel =
      currentZoomLevel > zoomRegion && currentZoomLevel < zoomDepartment
    const communeLevel = currentZoomLevel >= zoomDepartment
    if (regionLevel) {
      this.#switchToRegionLevel()
    } else if (departmentLevel) {
      this.#switchToDepartmentLevel()
    } else if (communeLevel) {
      this.#switchToCommuneLevel()
    }
  }

  #switchToRegionLevel() {
    this.map.hasLayer(this.departments) && this.map.removeLayer(this.departments)
    if (this.map.hasLayer(this.regions)) return
    this.map.addLayer(this.regions)
    this.legend.setContent(this.#generateLegendContent(this.scaleRegions))
    this.tableTarget.innerHTML = ''
  }

  #switchToDepartmentLevel() {
    this.map.hasLayer(this.regions) && this.map.removeLayer(this.regions)
    for (let commune of Object.values(this.communes)) {
      this.map.removeLayer(commune)
    }
    if (this.map.hasLayer(this.departments)) return
    if (this.departments.length) {
      this.map.addLayer(this.departments)
    } else {
      this.#getDepartments().then((departments) => {
        this.departments = departments
        this.map.addLayer(departments)
      })
    }
    this.legend.setContent(this.#generateLegendContent(this.scaleDepartments))
    this.tableTarget.innerHTML = ''
  }

  #switchToCommuneLevel() {
    this.map.hasLayer(this.regions) && this.map.removeLayer(this.regions)
    this.map.hasLayer(this.departments) && this.map.removeLayer(this.departments)

    // We determine the current department being the one at the center of the map.
    const insideLayers = mapUtils.pointInLayer(
      this.map.getCenter(),
      this.departments,
      true
    )
    if (!insideLayers.length) return
    const currentDepartmentCode = insideLayers[0].feature.properties.code

    if (this.communes[currentDepartmentCode]) {
      this.map.addLayer(this.communes[currentDepartmentCode])
    } else {
      this.#getCommunes(currentDepartmentCode).then(({ communes, data }) => {
        this.communes[currentDepartmentCode] = communes
        this.map.addLayer(communes)
        this.#updateTable(data)
      })
    }
    this.legend.setContent(`
      <i style="background:${this.#getAgeColor(3)};"></i> Ces 30 derniers jours<br>
      <i style="background:${this.#getAgeColor(2)};"></i> Dans le dernier trimestre<br>
      <i style="background:${this.#getAgeColor(1)};"></i> Inscription plus ancienne
    `)
  }

  #updateTable(data) {
    const correspondance = []
    for (const feature of data.features) {
      const key = `${feature.properties.code}-${feature.properties.nom}`
      if (Object.keys(this.communesWithOrg).includes(key)) {
        correspondance.push({
          nom: feature.properties.nom,
          organization_name: this.communesWithOrg[key].organization_name,
          date_created: this.communesWithOrg[key].date_created,
          projects_count: this.communesWithOrg[key].projects_count,
          users_count: this.communesWithOrg[key].users_count,
        })
      }
    }
    correspondance.sort((a, b) => b.date_created > a.date_created)
    this.tableTarget.innerHTML = `
      <table data-controller="table" class="fr-table">
        <caption>
          Communes et leurs organisations :
        </caption>
        <thead>
          <tr>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="text"
              >Commune</th>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="text"
              >Organisation</th>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              aria-sort="descending"
              data-type="date"
              >Date de création</th>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="number"
              >Nombre de projets</th>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="number"
              >Nombre de comptes</th>
          </tr>
        </thead>
        <tbody data-table-target="body">
          <tr data-table-target="row">
            ${correspondance
              .map(
                (item) =>
                  `
                  <td scope="row">${item.nom}</td>
                  <td>${item.organization_name}</td>
                  <td>${new Date(item.date_created).toLocaleDateString('fr-FR')}</td>
                  <td>${item.projects_count}</td>
                  <td>${item.users_count}</td>
                  `
              )
              .join('</tr><tr data-table-target="row">')}
          </tr>
        </tbody>
      </table>
    `
  }

  #initMap() {
    const map = this.#createMap()
    // Control that shows state info on hover.
    this.info = this.#createInfo()
    map.addControl(this.info)
    // Control that shows the legend for colors.
    this.legend = this.#createLegend()
    map.addControl(this.legend)
    this.regions = this.#getRegions()
    // By default, we load regions’ shapes.
    this.regions.addTo(map)
    return map
  }

  #createMap() {
    const map = L.map(this.element.querySelector('div')).setView(
      this.centerFrance,
      this.zoomFrance
    )
    map.attributionControl.addAttribution(
      'Contours &copy; <a href="https://github.com/etalab/contours-administratifs">Etalab</a>'
    )
    L.tileLayer('https://{s}.forte.tiles.quaidorsay.fr/fr{r}/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: `&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>
        et Quai d’Orsay`,
    }).addTo(map)
    return map
  }

  #createInfo() {
    L.HoverInfo = L.Control.extend({
      onAdd: function () {
        this._div = L.DomUtil.create('div', 'info')
        this.update(null, this.regionsOrgCount)
        return this._div
      },
      update: function (props, orgCount) {
        let message = '<h4>Organisations</h4>'
        if (!props) {
          message += 'Survoler une zone'
        } else {
          const count = orgCount[props.nom] || 0
          if (count) {
            message += `<b>${props.nom}</b><br>${count} organisations créées`
          } else {
            if (props.date_created) {
              message += `<b>${
                props.nom
              }</b><br>${props.date_created.toLocaleDateString('fr-FR')}`
            } else {
              message += `<b>${props.nom}</b>`
            }
          }
        }
        this._div.innerHTML = message
      },
    })
    return new L.HoverInfo()
  }

  #createLegend() {
    L.Legend = L.Control.extend({
      onAdd: function () {
        const container = document.createElement('div')
        container.classList.add('info', 'legend')
        if (this.options.content) {
          container.innerHTML = this.options.content
        }
        return container
      },
      setContent: function (str) {
        this.getContainer().innerHTML = str
      },
    })

    return new L.Legend({
      position: 'bottomleft',
      content: this.#generateLegendContent(this.scaleRegions),
    })
  }

  #generateLegendContent(scale) {
    const labels = []
    let from, to

    for (let i = 0; i < scale.length; i++) {
      from = scale[i]
      to = scale[i + 1]

      const color = this.#getDensityColor(from + 1, scale)
      labels.push(
        `<i style="background:${color};"></i> ${from} ${to ? '&ndash;' + to : '+'}`
      )
    }
    return labels.join('<br>')
  }

  #getRegions() {
    const regionsShapes = JSON.parse(this.regionsTarget.textContent)
    const regions = L.geoJson([regionsShapes], {
      style: (feature) => {
        const fillColor = {
          fillColor: this.#getDensityColor(
            this.regionsOrgCount[feature.properties.nom] || 0,
            this.scaleRegions
          ),
        }
        return { ...this.defaultFillStyle, ...fillColor }
      },
      onEachFeature: (_feature, layer) => {
        layer.on({
          mouseover: (e) => {
            const target = e.target
            target.setStyle(this.defaultHoverStyle)

            if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
              target.bringToFront()
            }

            this.info.update(target.feature.properties, this.regionsOrgCount)
          },
          mouseout: (e) => {
            regions.resetStyle(e.target)
            this.info.update(null, this.regionsOrgCount)
          },
          click: this.#fitMap.bind(this),
        })
      },
    })
    return regions
  }

  #getDepartments() {
    return fetch(this.departmentsTarget.dataset.src)
      .then(this.#checkResponse)
      .then((data) => {
        const departments = L.geoJson(data, {
          style: (feature) => {
            const fillColor = {
              fillColor: this.#getDensityColor(
                this.departmentsOrgCount[feature.properties.nom] || 0,
                this.scaleDepartments
              ),
            }
            return { ...this.defaultFillStyle, ...fillColor }
          },
          onEachFeature: (_feature, layer) => {
            layer.on({
              mouseover: (e) => {
                const target = e.target
                target.setStyle(this.defaultHoverStyle)

                if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                  target.bringToFront()
                }

                this.info.update(target.feature.properties, this.departmentsOrgCount)
              },
              mouseout: (e) => {
                departments.resetStyle(e.target)
                this.info.update(null, this.departmentsOrgCount)
              },
              click: this.#fitMap.bind(this),
            })
          },
        })
        return departments
      })
      .catch((ex) => {
        console.log('No available shapes for departments?', ex)
      })
  }

  #getCommunes(code) {
    return fetch(this.communesTarget.getAttribute(`data-src-${code}`))
      .then(this.#checkResponse)
      .then((data) => {
        const communes = L.geoJson(data, {
          style: (feature) => {
            const key = `${feature.properties.code}-${feature.properties.nom}`
            const age = Object.keys(this.communesWithOrg).includes(key)
              ? this.communesWithOrg[key].age
              : 0
            const fillColor = { fillColor: this.#getAgeColor(age) }
            return { ...this.defaultFillStyle, ...fillColor }
          },
          onEachFeature: (_feature, layer) => {
            layer.on({
              mouseover: (e) => {
                const target = e.target
                target.setStyle(this.defaultHoverStyle)

                if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                  target.bringToFront()
                }

                const properties = target.feature.properties
                const key = `${properties.code}-${properties.nom}`
                const communeHasOrg = Object.keys(this.communesWithOrg).includes(key)
                if (communeHasOrg) {
                  const communeProperties = this.communesWithOrg[key]
                  properties.date_created = new Date(communeProperties['date_created'])
                }
                this.info.update(properties, {})
              },
              mouseout: (e) => {
                communes.resetStyle(e.target)
                this.info.update(null, {})
              },
              click: this.#fitMap.bind(this),
            })
          },
        })
        return { communes, data }
      })
      .catch((ex) => {
        console.log(
          `No available communes shapes for that department code ${code}?`,
          ex
        )
      })
  }

  #checkResponse(response) {
    if (response.ok) {
      return response.json()
    }
    throw response.statusText
  }

  #fitMap(e) {
    this.map.fitBounds(e.target.getBounds())
  }

  // Get color depending on density value
  #getDensityColor(density, scale) {
    // Gradient of CSS colors from France DesignSystem from lighter to darker.
    const gradientBlue = [
      '--blue-france-975-75',
      '--blue-france-950-100',
      '--blue-france-925-125',
      '--blue-france-850-200',
      '--blue-france-main-525',
      '--blue-france-sun-113-625-hover',
      '--blue-france-sun-113-625',
      '--grey-50-1000',
    ]
    // Creates an object to access the color name from a scale number.
    const scaleToColor = [utils.zip([scale, gradientBlue])].map(Object.fromEntries)[0]
    const color = scaleToColor[utils.closestInArray(density, scale)]
    return this.styles.getPropertyValue(color)
  }

  #getAgeColor(age) {
    const gradientRed = [
      '--yellow-tournesol-950-100-hover', // Jaune.
      '--warning-425-625-hover', // Orange.
      '--red-marianne-main-472', // Rouge.
    ]
    const color = gradientRed[age - 1]
    return this.styles.getPropertyValue(color)
  }

  flyTo(e) {
    e.preventDefault()
    // Necessary to be able to display communes.
    this.#switchToDepartmentLevel()
    this.map.flyTo(JSON.parse(e.target.dataset.latlon), Number(e.target.dataset.zoom))
  }
}

const utils = (function () {
  // Something utils to move to their dedicated file?

  function generateScale(max, nbItems) {
    // generateScale(477, 7) => [0, 69, 137, 205, 273, 341, 409, 477]
    // See https://stackoverflow.com/a/47968178
    // and https://poopcode.com/divide-a-number-into-x-parts-in-javascript/
    return [0].concat(
      [...Array(nbItems)]
        .map((_, index) => 0 | (max / nbItems + (index < max % nbItems)))
        .map(((acc) => (val) => (acc += val))(0))
    )
  }
  function zip(rows) {
    // Equivalent to zip() in Python.
    // zip([['foo', 'bar'], [1, 2]]) => [['foo', 1], ['bar', 2]]
    // See https://stackoverflow.com/a/10284006
    return rows[0].map((_, index) => rows.map((row) => row[index]))
  }
  function closestInArray(needle, haystack) {
    // closestInArray(10, [1, 4, 9, 12]) => 9
    // See https://stackoverflow.com/a/35000557
    return haystack.reduce((prev, curr) =>
      Math.abs(curr - needle) < Math.abs(prev - needle) ? curr : prev
    )
  }
  return { generateScale, zip, closestInArray }
})()

const mapUtils = (function () {
  // Something map-related utils to move to their dedicated file?

  function boundingBoxAroundPolyCoords(coords) {
    // From https://github.com/maxogden/geojson-js-utils
    let xAll = []
    let yAll = []

    for (let coord of coords[0]) {
      xAll.push(coord[1])
      yAll.push(coord[0])
    }

    xAll = xAll.sort((a, b) => a - b)
    yAll = yAll.sort((a, b) => a - b)

    return [
      [xAll[0], yAll[0]],
      [xAll[xAll.length - 1], yAll[yAll.length - 1]],
    ]
  }

  function pointInBoundingBox(point, bounds) {
    // From https://github.com/maxogden/geojson-js-utils
    return !(
      point.coordinates[1] < bounds[0][0] ||
      point.coordinates[1] > bounds[1][0] ||
      point.coordinates[0] < bounds[0][1] ||
      point.coordinates[0] > bounds[1][1]
    )
  }

  // Point in Polygon
  // http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html

  function pnpoly(x, y, coords) {
    // From https://github.com/maxogden/geojson-js-utils
    let vert = [[0, 0]]

    for (let coord of coords) {
      for (let subcoord of coord) {
        vert.push(subcoord)
      }
      vert.push(coord[0])
      vert.push([0, 0])
    }

    let inside = false
    for (let i = 0, j = vert.length - 1; i < vert.length; j = i++) {
      if (
        vert[i][0] > y != vert[j][0] > y &&
        x <
          ((vert[j][1] - vert[i][1]) * (y - vert[i][0])) / (vert[j][0] - vert[i][0]) +
            vert[i][1]
      )
        inside = !inside
    }

    return inside
  }

  function pointInPolygon(p, poly) {
    // From https://github.com/maxogden/geojson-js-utils
    const coords = poly.type == 'Polygon' ? [poly.coordinates] : poly.coordinates

    let insideBox = false
    for (let coord of coords) {
      if (pointInBoundingBox(p, boundingBoxAroundPolyCoords(coord))) insideBox = true
    }
    if (!insideBox) return false

    let insidePoly = false
    for (let coord of coords) {
      if (pnpoly(p.coordinates[1], p.coordinates[0], coord)) insidePoly = true
    }

    return insidePoly
  }

  function isPoly(l) {
    // From https://github.com/mapbox/leaflet-pip/
    return (
      l.feature &&
      l.feature.geometry &&
      l.feature.geometry.type &&
      ['Polygon', 'MultiPolygon'].indexOf(l.feature.geometry.type) !== -1
    )
  }

  function pointInLayer(p, layer, first) {
    // From https://github.com/mapbox/leaflet-pip/
    p = [p.lng, p.lat]

    const results = []

    layer.eachLayer(function (l) {
      if (first && results.length) return

      if (
        isPoly(l) &&
        pointInPolygon({ type: 'Point', coordinates: p }, l.toGeoJSON().geometry)
      ) {
        results.push(l)
      }
    })
    return results
  }

  return { pointInLayer }
})()
